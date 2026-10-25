#!/usr/bin/env python3
from pwn import *
import re, hashlib, time

context.log_level = "info"

def solve_pow(prefix, bits=8):
    salt = b"spi-tpm-pow-v1:" + prefix
    for nonce in range(30_000_000):
        h = hashlib.scrypt(
            prefix + str(nonce).encode(),
            salt=salt, n=32768, r=8, p=1,
            dklen=32, maxmem=256*1024*1024
        )
        if int.from_bytes(h, "big") >> (256 - bits) == 0:
            return nonce
    raise Exception("pow failed")

def try_once():
    r = remote("spi-tpm-rev.chal.hitconctf.com", 1337, timeout=15)
    data = r.recvuntil(b"nonce\n", timeout=10)
    prefix = re.search(rb"prefix ([0-9a-f]+)", data).group(1)
    log.info(f"prefix {prefix.decode()}")
    nonce = solve_pow(prefix)
    log.info(f"nonce {nonce}")
    r.sendline(str(nonce).encode())
    print(r.recvuntil(b"ready", timeout=10).decode())

    def cmd(c):
        r.sendline(c.encode())
        time.sleep(0.8)
        try:
            out = r.recv(timeout=3).decode(errors="replace")
        except:
            out = "<timeout>"
        print(f">>> {c}\n{out}")
        return out

    cmd("budget")
    cmd("genkey")
    cmd("budget")

    # 1. Round-trip under key 1
    ct = cmd("encrypt 1 1 6869")
    m = re.search(r"ciphertext ([0-9a-f]+)", ct)
    if m:
        cmd("decrypt " + m.group(1))
    cmd("budget")

    # 2. Longer known plaintext under key 1 (for cipher analysis)
    cmd("encrypt 1 1 " + "41"*32)          # 32 bytes of 'A'
    cmd("budget")

    # 3. Get flag and try decrypt (will fail, but we keep the blob)
    flag = cmd("get_flag")
    cmd("budget")
    m = re.search(r"flag \d+ ([0-9a-f]+)", flag)
    if m:
        blob = m.group(1)
        print(f"\n[flag blob] {blob}\n")
        cmd("decrypt " + blob)

    cmd("budget")
    r.close()
    return True

for attempt in range(1, 15):
    print(f"\n===== attempt {attempt} =====")
    try:
        if try_once():
            break
    except Exception as e:
        print(f"failed: {e}")
        time.sleep(5)
