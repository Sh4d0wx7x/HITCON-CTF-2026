#!/usr/bin/env python3
from pwn import *
import re, hashlib, time, sys

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
    log.info("solving pow...")
    nonce = solve_pow(prefix)
    log.info(f"nonce {nonce}")
    r.sendline(str(nonce).encode())
    banner = r.recvuntil(b"ready", timeout=10)
    print(banner.decode())

    def cmd(c):
        r.sendline(c.encode())
        time.sleep(0.7)
        try:
            return r.recv(timeout=3).decode(errors="replace")
        except:
            return "<timeout>"

    for c in ["budget", "genkey", "budget",
              "encrypt 1 1 6869", "budget",
              "get_flag", "budget"]:
        print(f"\n>>> {c}")
        print(cmd(c))
    r.close()
    return True

for attempt in range(1, 20):
    print(f"\n===== attempt {attempt} =====")
    try:
        if try_once():
            break
    except Exception as e:
        print(f"failed: {e}")
        time.sleep(4)
else:
    print("all attempts failed")
