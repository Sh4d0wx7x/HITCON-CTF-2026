#!/usr/bin/env python3
"""
Follow-up to probe_live.py: isolate how COST maps to budget charge.

Your last run showed budget 1024 -> 832 over 3 successful encrypts
(COST 1, 1, 2; all length=64), then COST=1,000,000 failed with
"error syntax-or-budget". That smells like COST is charged against
the budget pool directly, not just range-checked -- this script tries
to measure that charge precisely.

Plaintext length is held FIXED and tiny (4 bytes -> 1 chunk) across
every call, so the length-based part of the charge stays constant and
whatever budget delta shows up between steps should be attributable
to COST alone. Reports budget after every step so you can see the
deltas directly without doing arithmetic by hand.

11 requests total (genkey + 5x[encrypt, budget]) -- safely under the
~27-query allowance, and COST tops out at 100 (vs. the 1,000,000 that
failed last time) to avoid spending the whole budget on one failed
call before getting any data.

Usage: python3 probe_cost_budget.py HOST PORT
"""
import socket
import sys
import time
import hashlib
import argparse
import re

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)


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
        self.sock.sendall((s if isinstance(s, bytes) else s.encode()) + b"\n")


def solve_pow(conn):
    params = {}
    while True:
        line = conn.recv_line(timeout=15).decode(errors="replace")
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
    t0, nonce = time.time(), 0
    while True:
        digest = hashlib.scrypt((prefix + str(nonce)).encode(), salt=salt,
                                 n=n, r=r, p=p, dklen=32, maxmem=134217728)
        hexd = digest.hex()
        ok = hexd[:full_nibbles] == "0" * full_nibbles
        if ok and remainder:
            ok = int(hexd[full_nibbles], 16) < (1 << (4 - remainder))
        if ok:
            break
        nonce += 1
    print(f"[pow] solved nonce={nonce} in {time.time()-t0:.1f}s", file=sys.stderr)
    conn.send_line(str(nonce))
    ack = conn.recv_line(timeout=15).decode(errors="replace")
    print(f"[pow] {ack}", file=sys.stderr)
    if "accepted" not in ack:
        raise RuntimeError(f"proof-of-work not accepted: {ack!r}")


def wait_for_banner(conn):
    deadline = time.time() + 60
    seen = b""
    while time.time() < deadline:
        chunk = conn.recv_available(idle=1.0)
        if chunk:
            seen += chunk
            sys.stderr.buffer.write(chunk)
            sys.stderr.flush()
        if b"ready" in seen or (not chunk and seen):
            return seen
    return seen


def cmd(conn, line, idle=0.8):
    conn.send_line(line)
    out = conn.recv_available(idle=idle)
    print(f">>> {line}", file=sys.stderr)
    sys.stderr.buffer.write(out)
    if not out.endswith(b"\n"):
        sys.stderr.write("\n")
    sys.stderr.flush()
    return out.decode(errors="replace")


def parse_budget(text):
    m = re.search(r"budget\s+(\d+)\s+queries\s+(\d+)", text)
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("host", nargs="?", default="spi-tpm-rev.chal.hitconctf.com")
    ap.add_argument("port", nargs="?", type=int, default=1337)
    args = ap.parse_args()

    conn = Conn(args.host, args.port)
    solve_pow(conn)
    wait_for_banner(conn)

    m = re.search(r"\b(\d+)\b", cmd(conn, "genkey"))
    if not m:
        print("[!] couldn't parse genkey response", file=sys.stderr)
        sys.exit(1)
    key_id = m.group(1)

    b0, q0 = parse_budget(cmd(conn, "budget"))
    print(f"\n[*] starting budget={b0} queries={q0}")

    results = [(None, b0, q0)]
    for cost in (1, 5, 10, 50, 100):
        out = cmd(conn, f"encrypt {key_id} {cost} 00000000")
        if "error" in out:
            print(f"[!] COST={cost} failed: {out.strip()}")
            results.append((cost, None, None))
            continue
        b, q = parse_budget(cmd(conn, "budget"))
        results.append((cost, b, q))

    print("\n=== budget deltas by COST (fixed 4-byte plaintext each call) ===")
    print(f"{'COST':>10} {'budget_after':>13} {'delta':>8} {'queries_after':>14}")
    prev_b = b0
    for cost, b, q in results[1:]:
        if b is None:
            print(f"{cost:>10} {'FAILED':>13}")
            continue
        delta = (prev_b - b) if prev_b is not None else None
        print(f"{cost:>10} {b:>13} {delta if delta is not None else '?':>8} {q:>14}")
        prev_b = b

    try:
        cmd(conn, "quit")
    except Exception:
        pass


if __name__ == "__main__":
    main()
