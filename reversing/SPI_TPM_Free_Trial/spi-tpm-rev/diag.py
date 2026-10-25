#!/usr/bin/env python3
"""
diag.py -- targeted diagnostics for spi-tpm-rev, run after solve.py's first
attempt showed `decrypt` on get_flag's own blob failing with
'error syntax-or-budget'.

Tests, in order, reporting budget/queries after each:
  1. baseline budget
  2. encrypt 1 0 <16 zero bytes>   -- can we address the flag's own key
     slot (id=1) directly, as plaintext we control? All-zero plaintext
     means a returned ciphertext IS the raw keystream for an XOR cipher.
  3. encrypt 1 5 <16 zero bytes>   -- same, higher COST, to see how
     output/budget scales with COST (only run if step 2 looked cheap)
  4. get_flag again (fresh blob) -> budget check immediately after, to
     see exactly how much budget get_flag itself consumes
  5. decrypt on that fresh blob, immediately, budget check after

Then drops to interactive mode so you can keep going by hand with
whatever budget/queries remain. Doesn't assume which branch will work --
prints everything clearly so we can read the real behaviour off it.

Usage: python3 diag.py HOST PORT
"""
import socket, sys, time, hashlib, re, select, os

class Conn:
    def __init__(self, host, port, timeout=20):
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.sock.settimeout(timeout)
        self.buf = b""
    def recv_line(self, timeout=15):
        self.sock.settimeout(timeout)
        while b"\n" not in self.buf:
            chunk = self.sock.recv(65536)
            if not chunk:
                line, self.buf = self.buf, b""
                return line
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

def solve_pow(conn):
    params = {}
    while True:
        line = conn.recv_line().decode(errors="replace")
        print(f"[pow] {line}", file=sys.stderr)
        if line.strip() == "nonce":
            break
        if "accepted" in line:
            return
        parts = line.strip().split(None, 1)
        if len(parts) == 2:
            params[parts[0]] = parts[1]
    prefix, n, r, p, bits = params["prefix"], int(params["n"]), int(params.get("r", 8)), \
        int(params.get("p", 1)), int(params["bits"])
    salt = ("spi-tpm-pow-v1:" + prefix).encode()
    full, rem = bits // 4, bits % 4
    t0, nonce = time.time(), 0
    while True:
        d = hashlib.scrypt((prefix + str(nonce)).encode(), salt=salt, n=n, r=r, p=p,
                            dklen=32, maxmem=134217728).hex()
        ok = d[:full] == "0" * full
        if ok and rem:
            ok = int(d[full], 16) < (1 << (4 - rem))
        if ok:
            break
        nonce += 1
    print(f"[pow] solved nonce={nonce} in {time.time()-t0:.1f}s", file=sys.stderr)
    conn.send_line(str(nonce))
    print(f"[pow] {conn.recv_line().decode(errors='replace')}", file=sys.stderr)

def cmd(conn, line):
    conn.send_line(line)
    out = conn.recv_available(idle=0.7)
    txt = out.decode(errors="replace")
    print(f">>> {line}\n{txt}" + ("" if txt.endswith(chr(10)) else "\n"), file=sys.stderr)
    return txt

def parse_budget(txt):
    m = re.search(r"budget\s+(\d+)\s+queries\s+(\d+)", txt)
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)

def bridge(sock):
    sock.setblocking(False)
    stdin_fd = sys.stdin.fileno()
    while True:
        r, _, _ = select.select([sock, stdin_fd], [], [])
        if sock in r:
            try:
                data = sock.recv(65536)
            except BlockingIOError:
                data = b""
            if not data:
                print("[*] connection closed", file=sys.stderr)
                return
            sys.stdout.buffer.write(data); sys.stdout.buffer.flush()
        if stdin_fd in r:
            line = os.read(stdin_fd, 65536)
            if not line:
                return
            sock.sendall(line)

def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} HOST PORT", file=sys.stderr); sys.exit(1)
    host, port = sys.argv[1], int(sys.argv[2])
    conn = Conn(host, port)
    solve_pow(conn)

    banner = conn.recv_available(idle=1.0).decode(errors="replace")
    print(banner, file=sys.stderr)

    b0, q0 = parse_budget(banner)
    print(f"\n[*] baseline from banner: budget={b0} queries={q0}\n", file=sys.stderr)

    print("="*70, file=sys.stderr)
    print("TEST 1: can we address the flag's key slot (id=1) directly?", file=sys.stderr)
    print("="*70, file=sys.stderr)
    r1 = cmd(conn, "encrypt 1 0 00000000000000000000000000000000")
    bt = cmd(conn, "budget")
    b1, q1 = parse_budget(bt)
    slot1_open = r1.strip().startswith("ciphertext")
    print(f"[*] slot-1 direct addressing: {'OPEN -- big deal!' if slot1_open else 'blocked / errored'}", file=sys.stderr)
    if b0 is not None and b1 is not None:
        print(f"[*] budget delta from that one call: {b0-b1} (queries used: {q0-q1})", file=sys.stderr)

    if slot1_open:
        print("\n[*] slot 1 is addressable -- gathering a few more chosen-plaintext", file=sys.stderr)
        print("[*] samples at low cost before we decide how to spend more budget.\n", file=sys.stderr)
        cmd(conn, "encrypt 1 0 00000000000000000000000000000001")  # 1-bit diff, for differential analysis
        cmd(conn, "encrypt 1 0 ffffffffffffffffffffffffffffffff")
        cmd(conn, "encrypt 1 5 00000000000000000000000000000000")  # same zero PT, higher cost -- compare
        bt2 = cmd(conn, "budget")
        print(f"[*] budget/queries now: {bt2.strip()}", file=sys.stderr)
        print("\n[*] STOPPING here deliberately to preserve remaining budget.", file=sys.stderr)
        print("[*] Copy the 'ciphertext ...' lines above back for analysis before doing anything else.\n", file=sys.stderr)
    else:
        print("\n" + "="*70, file=sys.stderr)
        print("TEST 2: does get_flag drain the budget? (fallback path)", file=sys.stderr)
        print("="*70, file=sys.stderr)
        gf = cmd(conn, "get_flag")
        bt3 = cmd(conn, "budget")
        b2, q2 = parse_budget(bt3)
        if b1 is not None and b2 is not None:
            print(f"[*] budget delta from get_flag alone: {b1-b2} (queries used: {q1-q2})", file=sys.stderr)
        m = re.search(r"flag\s+(\d+)\s+([0-9a-fA-F]+)", gf)
        if m:
            print(f"\n[*] immediately attempting decrypt on the fresh blob (budget={b2})...", file=sys.stderr)
            cmd(conn, "decrypt " + m.group(2))
            cmd(conn, "budget")

    print("\n[*] entering interactive mode (Ctrl-D to quit)\n", file=sys.stderr)
    bridge(conn.sock)

if __name__ == "__main__":
    main()
