#!/usr/bin/env python3
"""
HITCON 2026 "SPI TPM Free Trial" -- live empirical probe.

I can't reach the challenge server from here (no network egress in
this environment), and hand-tracing the custom 64-bit mixer at 0x33d0
bit-exactly carries real risk of another silent transcription error
(see spi_tpm_primitives.py's Part 2 notes for what's confirmed vs.
not). This script is built to get you data that settles the open
questions fast, using a connection/PoW harness copied from the one
that already worked for you (same recv_line/recv_available/solve_pow
shape as your solve.py -- not reinvented).

The key trick: if you encrypt an ALL-ZERO plaintext, the returned
"ciphertext" bytes ARE the raw keystream (plaintext XOR 0 = plaintext,
so ciphertext XOR 0 = keystream). Combined with the now-confirmed
response header (nonce readable at +0x8, cost echoed at +0xc/+0xe),
every call below hands you a clean (nonce, cost, chunk_index) ->
keystream_word sample with no guessing required.

What it does, in order (6 requests total -- genkey costs budget too,
so this stays well under the ~27-query allowance your banner showed):
  1. genkey                                   -> key_id
  2. encrypt key_id COST=1  64 zero bytes     -> sample A (16 words)
  3. encrypt key_id COST=1  64 zero bytes     -> sample B (same cost,
     different nonce -- same-cost/different-nonce comparison)
  4. encrypt key_id COST=2  64 zero bytes     -> sample C
  5. encrypt key_id COST=1000000 (max) 64 zero bytes -> sample D
  6. budget                                   -> sanity check what's left

It prints every raw response plus parsed (nonce, cost, keystream)
triples, so you can eyeball them directly or paste the output back for
more analysis. It does NOT try to decrypt the flag -- that's the next
step once the COST=1 vs COST=max comparison shows whether round count
actually matters the way the static analysis suggests it should.

Usage:
    python3 probe_live.py HOST PORT
    python3 probe_live.py spi-tpm-rev.chal.hitconctf.com 1337
"""
import socket
import sys
import time
import hashlib
import struct
import argparse
import re


class Conn:
    def __init__(self, host, port, timeout=20):
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.sock.settimeout(timeout)
        self.buf = b""

    def recv_line(self, timeout=None):
        if timeout is not None:
            self.sock.settimeout(timeout)
        while b"\n" not in self.buf:
            chunk = self.sock.recv(65536)
            if not chunk:
                if self.buf:
                    line, self.buf = self.buf, b""
                    return line
                raise EOFError("connection closed")
            self.buf += chunk
        line, self.buf = self.buf.split(b"\n", 1)
        return line

    def recv_available(self, idle=0.6):
        self.sock.settimeout(idle)
        data = self.buf
        self.buf = b""
        try:
            while True:
                chunk = self.sock.recv(65536)
                if not chunk:
                    break
                data += chunk
        except socket.timeout:
            pass
        return data

    def send_line(self, s):
        if isinstance(s, str):
            s = s.encode()
        self.sock.sendall(s + b"\n")


def solve_pow(conn, verbose=True):
    params = {}
    while True:
        line = conn.recv_line(timeout=15).decode(errors="replace")
        if verbose:
            print(f"[pow] {line}", file=sys.stderr)
        if line.strip() == "nonce":
            break
        parts = line.strip().split(None, 1)
        if len(parts) == 2:
            params[parts[0]] = parts[1]
        if line.strip() == "proof-of-work accepted":
            return

    prefix = params["prefix"]
    n, r, p, bits = int(params["n"]), int(params.get("r", "8")), \
        int(params.get("p", "1")), int(params["bits"])
    salt = ("spi-tpm-pow-v1:" + prefix).encode()
    full_nibbles, remainder = bits // 4, bits % 4

    t0 = time.time()
    nonce = 0
    while True:
        pw = (prefix + str(nonce)).encode()
        digest = hashlib.scrypt(pw, salt=salt, n=n, r=r, p=p, dklen=32,
                                 maxmem=134217728)
        hexd = digest.hex()
        ok = hexd[:full_nibbles] == "0" * full_nibbles
        if ok and remainder:
            ok = int(hexd[full_nibbles], 16) < (1 << (4 - remainder))
        if ok:
            break
        nonce += 1
    if verbose:
        print(f"[pow] solved nonce={nonce} in {time.time()-t0:.1f}s", file=sys.stderr)

    conn.send_line(str(nonce))
    ack = conn.recv_line(timeout=15).decode(errors="replace")
    if verbose:
        print(f"[pow] {ack}", file=sys.stderr)
    if "accepted" not in ack:
        raise RuntimeError(f"proof-of-work not accepted: {ack!r}")


def wait_for_banner(conn, verbose=True):
    deadline = time.time() + 60
    seen = b""
    while time.time() < deadline:
        chunk = conn.recv_available(idle=1.0)
        if chunk:
            seen += chunk
            if verbose:
                sys.stderr.buffer.write(chunk)
                sys.stderr.flush()
        if b"ready" in seen or b"budget" in seen:
            return seen
        if not chunk and seen:
            return seen
    return seen


def cmd(conn, line, verbose=True, idle=0.8):
    conn.send_line(line)
    out = conn.recv_available(idle=idle)
    if verbose:
        print(f">>> {line}", file=sys.stderr)
        sys.stderr.buffer.write(out)
        if not out.endswith(b"\n"):
            sys.stderr.write("\n")
        sys.stderr.flush()
    return out


HEX_RE = re.compile(rb"[0-9a-fA-F]{32,}")


def extract_hex_blob(raw: bytes):
    """Pull the longest hex run out of a response -- robust to not
    knowing the exact label word (e.g. 'ciphertext', 'flag', etc.)
    without another live sample to confirm it against."""
    matches = HEX_RE.findall(raw)
    if not matches:
        return None
    return max(matches, key=len)


def parse_response_blob(blob: bytes):
    if len(blob) < 0x18:
        return None
    magic, op, hdrlen = struct.unpack_from('<4sHH', blob, 0)
    nonce, = struct.unpack_from('<I', blob, 8)
    cost_lo, = struct.unpack_from('<H', blob, 0xc)
    cost_hi = blob[0xe]
    length, = struct.unpack_from('<H', blob, 0x10)
    ciphertext = blob[hdrlen:] if hdrlen <= len(blob) else b""
    return dict(magic=magic, op=op, hdrlen=hdrlen, nonce=nonce,
                cost_partial=(cost_hi << 16) | cost_lo, length=length,
                ciphertext=ciphertext)


def show_sample(label, raw, plaintext_was_zero=True):
    print(f"\n=== {label} ===")
    blob = extract_hex_blob(raw)
    if not blob:
        print("  (no hex blob found in response -- raw text above)")
        return None
    data = bytes.fromhex(blob.decode())
    parsed = parse_response_blob(data)
    if not parsed:
        print(f"  blob too short to parse ({len(data)} bytes): {blob.decode()}")
        return None
    print(f"  magic={parsed['magic']} op={parsed['op']} hdrlen={parsed['hdrlen']} "
          f"nonce=0x{parsed['nonce']:08x} cost_partial={parsed['cost_partial']} "
          f"length={parsed['length']}")
    ct = parsed['ciphertext']
    print(f"  ciphertext ({len(ct)}B): {ct.hex()}")
    if plaintext_was_zero:
        print(f"  -> keystream == ciphertext (zero plaintext): {ct.hex()}")
        words = [struct.unpack_from('<I', ct, i)[0] for i in range(0, len(ct) - 3, 4)]
        print(f"  -> keystream words (chunk 0..{len(words)-1}): "
              + ", ".join(f"{w:08x}" for w in words))
    parsed['raw_ciphertext'] = ct
    return parsed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("host", nargs="?", default="spi-tpm-rev.chal.hitconctf.com")
    ap.add_argument("port", nargs="?", type=int, default=1337)
    args = ap.parse_args()

    print(f"[*] connecting to {args.host}:{args.port}", file=sys.stderr)
    conn = Conn(args.host, args.port)
    solve_pow(conn)
    wait_for_banner(conn)

    zero64 = "00" * 64

    out = cmd(conn, "genkey")
    m = re.search(rb"\b(\d+)\b", out)
    if not m:
        print("[!] could not parse a key id out of genkey's response -- "
              "raw output above, edit this script's genkey parsing once "
              "you see the real format.", file=sys.stderr)
        sys.exit(1)
    key_id = m.group(1).decode()
    print(f"[*] key id = {key_id}", file=sys.stderr)

    samples = {}
    samples['cost1_a'] = show_sample(
        "COST=1, sample A (64 zero bytes)",
        cmd(conn, f"encrypt {key_id} 1 {zero64}"))
    samples['cost1_b'] = show_sample(
        "COST=1, sample B (same plaintext, different call -> different nonce expected)",
        cmd(conn, f"encrypt {key_id} 1 {zero64}"))
    samples['cost2'] = show_sample(
        "COST=2, 64 zero bytes",
        cmd(conn, f"encrypt {key_id} 2 {zero64}"))
    samples['cost_max'] = show_sample(
        "COST=1000000 (max), 64 zero bytes",
        cmd(conn, f"encrypt {key_id} 1000000 {zero64}", idle=3.0))

    cmd(conn, "budget")

    print("\n=== quick diffs ===")
    a, b = samples.get('cost1_a'), samples.get('cost1_b')
    if a and b:
        xor_ct = bytes(x ^ y for x, y in zip(a['raw_ciphertext'], b['raw_ciphertext']))
        xor_nonce = a['nonce'] ^ b['nonce']
        print(f"cost1_a vs cost1_b: nonce_a=0x{a['nonce']:08x} nonce_b=0x{b['nonce']:08x} "
              f"nonce_xor=0x{xor_nonce:08x}")
        print(f"  ciphertext XOR (first 16B): {xor_ct[:16].hex()}")
    a1, c2 = samples.get('cost1_a'), samples.get('cost2')
    if a1 and c2:
        print(f"cost1 nonce=0x{a1['nonce']:08x} vs cost2 nonce=0x{c2['nonce']:08x} "
              "(different nonces, so a byte-for-byte compare won't isolate COST's "
              "effect by itself -- eyeball whether cost2's keystream words look "
              "qualitatively different/more mixed than cost1's, or paste both "
              "back for a closer look)")

    try:
        cmd(conn, "quit", verbose=False)
    except Exception:
        pass


if __name__ == "__main__":
    main()
