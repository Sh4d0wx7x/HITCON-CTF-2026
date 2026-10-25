#!/usr/bin/env python3
"""
diag2.py -- same goal as diag.py, but with a much more generous read
timeout (the server/connection has enough latency that 0.6-0.7s windows
were causing responses to bleed into the NEXT command's capture, which
badly confused the first diagnostic run).

Order of operations (ground truth first, edge cases second):
  1. genkey                                  -> our own key id K
  2. encrypt K 0 <16 zero bytes>              -> expect success; this is
     our first-ever confirmed-good ciphertext to compare everything else against
  3. budget
  4. decrypt <that ciphertext>                -> expect success; confirms
     round-trip and shows the exact 'plaintext ...' response format
  5. budget
  6. encrypt K 100 <16 zero bytes>            -> same plaintext, higher
     COST, to see how structure/budget change with COST
  7. budget                                   -> does it drop by ~100?
  8. encrypt K 999999 <16 zero bytes>         -> deliberately too expensive,
     to see the EXACT text of a genuine budget-exceeded error (compare
     against 'error syntax-or-budget')
  9. budget
  10. encrypt 1 0 <16 zero bytes>             -> retest flag-slot access,
      cleanly this time
  11. budget
  12. decrypt <a flag ciphertext we already captured earlier -- reused here
      so we don't need another get_flag call>
  13. budget

Then interactive mode.

Usage: python3 diag2.py HOST PORT
"""
import socket, sys, time, hashlib, re, select, os

# one of the flag blobs already captured in this conversation -- reused so
# this run doesn't need to call get_flag again
KNOWN_FLAG_HEX = ("5354503102002800fe9a3960b35f080046000000e62a919d292898c7ba2db6"
                   "23ea23bc6bce36cf552f6e1bfe9d2285bfb42b177763b613fa7e5825241605980"
                   "a9dec7444eb1f4c8368b29a82ae8a6d449f2944339f7bc4aa6dc12f761ec7083ce"
                   "ffc5830023cbd2cfb86d139323a435e")

IDLE = 2.5   # seconds of quiet before we consider a response "done"
MAXWAIT = 20.0

class Conn:
    def __init__(self, host, port, timeout=25):
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
    def recv_available(self, idle=IDLE, maxwait=MAXWAIT):
        buf = self.buf
        self.buf = b""
        self.sock.setblocking(False)
        last = time.time()
        deadline = time.time() + maxwait
        while True:
            r, _, _ = select.select([self.sock], [], [], 0.2)
            if r:
                try:
                    chunk = self.sock.recv(65536)
                except BlockingIOError:
                    chunk = b""
                if chunk:
                    buf += chunk
                    last = time.time()
                elif chunk == b"":
                    break  # connection closed
            if time.time() - last > idle or time.time() > deadline:
                break
        return buf
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
    out = conn.recv_available()
    txt = out.decode(errors="replace")
    print(f"\n>>> {line}\n{'-'*60}\n{txt}{'' if txt.endswith(chr(10)) else chr(10)}{'-'*60}", file=sys.stderr)
    return txt

def last_budget(txt):
    ms = list(re.finditer(r"budget\s+(\d+)\s+queries\s+(\d+)", txt))
    if not ms:
        return None, None
    m = ms[-1]  # take the LAST match in case of any residual bleed-through
    return int(m.group(1)), int(m.group(2))

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

    banner = conn.recv_available().decode(errors="replace")
    print(f"\n[banner]\n{banner}", file=sys.stderr)

    print("\n" + "#"*70, file=sys.stderr)
    print("# STEP 1-5: establish a clean own-key encrypt/decrypt round trip", file=sys.stderr)
    print("#"*70, file=sys.stderr)

    gk = cmd(conn, "genkey")
    mk = re.search(r"key\s+(\d+)", gk)
    if not mk:
        print("[!] could not parse key id from genkey -- stopping scripted phase", file=sys.stderr)
        bridge(conn.sock); return
    K = mk.group(1)
    print(f"[*] our key id: {K}", file=sys.stderr)

    e1 = cmd(conn, f"encrypt {K} 0 00000000000000000000000000000000")
    mc = re.search(r"ciphertext\s+([0-9a-fA-F]+)", e1)
    b_txt = cmd(conn, "budget")
    b1, q1 = last_budget(b_txt)
    print(f"[*] after COST=0 own-key encrypt: budget={b1} queries={q1}", file=sys.stderr)

    if mc:
        C0 = mc.group(1)
        d1 = cmd(conn, f"decrypt {C0}")
        b_txt = cmd(conn, "budget")
        b2, q2 = last_budget(b_txt)
        print(f"[*] after decrypt of our own ciphertext: budget={b2} queries={q2}", file=sys.stderr)
    else:
        print("[!] encrypt with our own freshly-created key did NOT return a "
              "'ciphertext' line -- see raw output above, something more basic "
              "than key ownership is going on", file=sys.stderr)

    print("\n" + "#"*70, file=sys.stderr)
    print("# STEP 6-9: COST vs budget relationship", file=sys.stderr)
    print("#"*70, file=sys.stderr)
    cmd(conn, f"encrypt {K} 100 00000000000000000000000000000000")
    b_txt = cmd(conn, "budget")
    b3, q3 = last_budget(b_txt)
    print(f"[*] after COST=100 own-key encrypt: budget={b3} queries={q3}", file=sys.stderr)

    cmd(conn, f"encrypt {K} 999999 00000000000000000000000000000000")
    b_txt = cmd(conn, "budget")
    b4, q4 = last_budget(b_txt)
    print(f"[*] after COST=999999 (deliberately too big): budget={b4} queries={q4}", file=sys.stderr)

    print("\n" + "#"*70, file=sys.stderr)
    print("# STEP 10-13: retest flag-slot access and flag blob decrypt, cleanly", file=sys.stderr)
    print("#"*70, file=sys.stderr)
    cmd(conn, "encrypt 1 0 00000000000000000000000000000000")
    b_txt = cmd(conn, "budget")
    b5, q5 = last_budget(b_txt)
    print(f"[*] after encrypt-on-slot-1 attempt: budget={b5} queries={q5}", file=sys.stderr)

    cmd(conn, f"decrypt {KNOWN_FLAG_HEX}")
    b_txt = cmd(conn, "budget")
    b6, q6 = last_budget(b_txt)
    print(f"[*] after decrypt-flag-blob attempt: budget={b6} queries={q6}", file=sys.stderr)

    print("\n[*] scripted phase done -- entering interactive mode (Ctrl-D to quit)\n", file=sys.stderr)
    bridge(conn.sock)

if __name__ == "__main__":
    main()
