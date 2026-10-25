#!/usr/bin/env python3
"""
diag4.py -- now that we know cost must be >=1 (and budget = 15 + cost*rounded_len),
retest whether slot 1 (the flag's key) is directly addressable via encrypt.
If so, gather a cheap power-of-2 cost ladder against it (minimum-size 4-byte
all-zero plaintext each time, so ciphertext == raw keystream) for offline
differential/chaining analysis. Budget-adaptive: checks real remaining
budget before each step and stops the ladder early rather than overspending.

Usage: python3 diag4.py HOST PORT
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
    print(f"\n>>> {line}\n{'-'*60}\n{txt}{'' if txt.endswith(chr(10)) else chr(10)}{'-'*60}", file=sys.stderr)
    return txt

def parse_budget(txt):
    ms = list(re.finditer(r"budget\s+(\d+)\s+queries\s+(\d+)", txt))
    if not ms:
        return None, None
    m = ms[-1]
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
    budget, queries = parse_budget(banner)
    print(f"[*] starting budget={budget} queries={queries}", file=sys.stderr)

    print("\n" + "#"*70, file=sys.stderr)
    print("# Ground truth: own key round trip (cost=1, minimum-size plaintext)", file=sys.stderr)
    print("#"*70, file=sys.stderr)
    gk = cmd(conn, "genkey")
    mk = re.search(r"key\s+(\d+)", gk)
    K = mk.group(1) if mk else "0"
    print(f"[*] our key id: {K}", file=sys.stderr)

    e_own = cmd(conn, f"encrypt {K} 1 00000000")
    mc = re.search(r"ciphertext\s+([0-9a-fA-F]+)", e_own)
    if mc:
        cmd(conn, f"decrypt {mc.group(1)}")
    bt = cmd(conn, "budget")
    budget, queries = parse_budget(bt)
    print(f"[*] after own-key encrypt+decrypt: budget={budget} queries={queries}", file=sys.stderr)

    print("\n" + "#"*70, file=sys.stderr)
    print("# CRITICAL TEST: encrypt against slot 1 (the flag's key) at valid cost", file=sys.stderr)
    print("#"*70, file=sys.stderr)
    r1 = cmd(conn, "encrypt 1 1 00000000")
    bt = cmd(conn, "budget")
    budget, queries = parse_budget(bt)
    slot1_open = r1.strip().startswith("ciphertext")
    print(f"\n[*] slot-1 direct access: {'OPEN' if slot1_open else 'BLOCKED'}", file=sys.stderr)
    print(f"[*] budget={budget} queries={queries}", file=sys.stderr)

    if slot1_open:
        print("\n" + "#"*70, file=sys.stderr)
        print("# Gathering a cost ladder against slot 1 (all-zero 4-byte plaintext each time)", file=sys.stderr)
        print("#"*70, file=sys.stderr)
        # repeat cost=1 once more first -- check nonce determinism
        cmd(conn, "encrypt 1 1 00000000")
        bt = cmd(conn, "budget")
        budget, queries = parse_budget(bt)
        print(f"[*] budget={budget} queries={queries}", file=sys.stderr)

        for cost in [2, 4, 8, 16, 32, 64, 128, 256, 512]:
            required = 15 + cost * 4
            if budget is not None and required > budget:
                print(f"[*] stopping ladder: cost={cost} needs ~{required} budget, only {budget} left", file=sys.stderr)
                break
            cmd(conn, f"encrypt 1 {cost} 00000000")
            bt = cmd(conn, "budget")
            new_budget, queries = parse_budget(bt)
            print(f"[*] cost={cost}: budget={new_budget} queries={queries}", file=sys.stderr)
            budget = new_budget
    else:
        print("[*] trying to read the exact error -- if it differs from "
              "'error syntax-or-budget' that tells us something new", file=sys.stderr)

    print("\n[*] scripted phase done -- entering interactive mode (Ctrl-D to quit)\n", file=sys.stderr)
    bridge(conn.sock)

if __name__ == "__main__":
    main()
