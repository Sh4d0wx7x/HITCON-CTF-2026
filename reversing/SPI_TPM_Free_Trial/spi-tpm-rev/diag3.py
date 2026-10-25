#!/usr/bin/env python3
"""
diag3.py -- every encrypt/decrypt attempt so far has failed with the exact
same 'error syntax-or-budget', regardless of key id, cost (0/100/999999),
or target slot. That points at something about the HEX argument itself, or
the exact syntax expected, rather than budget/ownership. This probes
systematically: bare commands (to surface a possibly-different arg-count
error), varying hex length, non-zero content, and an unknown command (to
see if the live server echoes its own usage/help text, which we've only
ever seen via static strings so far).

Usage: python3 diag3.py HOST PORT
"""
import socket, sys, time, hashlib, re, select, os

IDLE = 2.5
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
                    break
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
    print(f"\n>>> {line!r}\n{'-'*60}\n{txt}{'' if txt.endswith(chr(10)) else chr(10)}{'-'*60}", file=sys.stderr)
    return txt

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
    print(f"\n[banner]\n{conn.recv_available().decode(errors='replace')}", file=sys.stderr)

    gk = cmd(conn, "genkey")
    mk = re.search(r"key\s+(\d+)", gk)
    K = mk.group(1) if mk else "0"
    print(f"[*] using key id: {K}", file=sys.stderr)

    # --- arg-count probes (looking for a DIFFERENT error message than
    #     'error syntax-or-budget', which would tell us arg parsing itself
    #     is the issue vs. something deeper) ---
    cmd(conn, "encrypt")
    cmd(conn, f"encrypt {K}")
    cmd(conn, f"encrypt {K} 1")

    # --- unknown command: does the live server echo its own usage/help text? ---
    cmd(conn, "help")
    cmd(conn, "???")

    # --- hex length/content probes, all with cost=1 (avoid cost=0 in case
    #     zero is specially rejected) ---
    cmd(conn, f"encrypt {K} 1 41")                      # 1 byte, non-zero
    cmd(conn, f"encrypt {K} 1 4141")                     # 2 bytes
    cmd(conn, f"encrypt {K} 1 " + "41"*16)                # 16 bytes, non-zero (vs our earlier all-zero test)
    cmd(conn, f"encrypt {K} 1 " + "00"*16)                # 16 bytes, zero (repeat of earlier test, cost=1 this time not 0)
    cmd(conn, f"encrypt {K} 1 " + "41"*64)                # 64 bytes, non-zero -- in case of a MINIMUM length
    cmd(conn, f"encrypt {K} 1 " + "0123456789abcdef"*4)   # 32 bytes, structured non-repeating pattern

    cmd(conn, "budget")

    print("\n[*] scripted phase done -- entering interactive mode (Ctrl-D to quit)\n", file=sys.stderr)
    bridge(conn.sock)

if __name__ == "__main__":
    main()
