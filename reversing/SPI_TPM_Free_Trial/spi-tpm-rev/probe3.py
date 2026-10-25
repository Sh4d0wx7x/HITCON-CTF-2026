#!/usr/bin/env python3
from pwn import *
import re, hashlib, time, binascii

context.log_level = "info"

def solve_pow(prefix, bits=8):
    salt = b"spi-tpm-pow-v1:" + prefix
    for nonce in range(30_000_000):
        h = hashlib.scrypt(prefix + str(nonce).encode(),
                           salt=salt, n=32768, r=8, p=1,
                           dklen=32, maxmem=256*1024*1024)
        if int.from_bytes(h, "big") >> (256-bits) == 0:
            return nonce
    raise Exception("pow fail")

def parse_stp1(hexstr):
    b = bytes.fromhex(hexstr)
    return {
        "raw": b,
        "cost": int.from_bytes(b[12:16], "little"),
        "length": int.from_bytes(b[16:20], "little"),
        "tag": int.from_bytes(b[20:24], "little"),
        "hdr_rest": b[24:40].hex(),
        "payload": b[40:],
    }

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

    # --- controlled budget + cipher tests under key 1, cost 1 ---
    tests = [
        "00",
        "0000",
        "41",
        "4141",
        "41414141",
        "00"*16,
        "41"*16,
        "00"*32,
        "41"*32,
    ]

    cts = {}
    for pt in tests:
        before = cmd("budget")
        ct = cmd(f"encrypt 1 1 {pt}")
        after = cmd("budget")
        m = re.search(r"ciphertext ([0-9a-f]+)", ct)
        if m:
            info = parse_stp1(m.group(1))
            cts[pt] = info
            print(f"[pt len={len(pt)//2}] cost={info['cost']} len={info['length']} "
                  f"tag={info['tag']:08x} payload={info['payload'].hex()}")
        print()

    # get flag
    flag = cmd("get_flag")
    m = re.search(r"flag \d+ ([0-9a-f]+)", flag)
    if m:
        fb = parse_stp1(m.group(1))
        print("\n=== FLAG PACKET ===")
        print(f"cost   = {fb['cost']}")
        print(f"length = {fb['length']}")
        print(f"tag    = {fb['tag']:08x}")
        print(f"hdr+20 = {fb['hdr_rest']}")
        print(f"payload= {fb['payload'].hex()}")
        print(f"full   = {m.group(1)}")

    cmd("budget")
    r.close()
    return True

for attempt in range(1, 12):
    print(f"\n===== attempt {attempt} =====")
    try:
        if try_once():
            break
    except Exception as e:
        print(f"failed: {e}")
        time.sleep(4)
