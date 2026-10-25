#!/usr/bin/env python3
from pwn import *
import re, hashlib, time, struct

context.log_level = "info"

def solve_pow(prefix, bits=8):
    salt = b"spi-tpm-pow-v1:" + prefix
    for n in range(40_000_000):
        h = hashlib.scrypt(prefix+str(n).encode(), salt=salt,
                           n=32768, r=8, p=1, dklen=32, maxmem=256<<20)
        if int.from_bytes(h,"big")>>(256-bits)==0: return n
    raise Exception("pow fail")

def parse(hexstr):
    b = bytes.fromhex(hexstr)
    return {
        "nonce": struct.unpack_from("<I",b,8)[0],
        "cost":  struct.unpack_from("<I",b,12)[0],
        "tag":   struct.unpack_from("<I",b,20)[0],
        "payload": b[40:],
    }

r = remote("spi-tpm-rev.chal.hitconctf.com", 1337, timeout=15)
data = r.recvuntil(b"nonce\n")
prefix = re.search(rb"prefix ([0-9a-f]+)", data).group(1)
log.info(f"prefix {prefix.decode()}")
r.sendline(str(solve_pow(prefix)).encode())
print(r.recvuntil(b"ready").decode())

def cmd(c):
    r.sendline(c.encode()); time.sleep(0.7)
    try: return r.recv(timeout=2).decode(errors="replace")
    except: return "<timeout>"

print(cmd("budget"))
print(cmd("genkey"))

# Same plaintext length, different COSTs → different nonces, but we can still
# see if the *structure* of the keystream changes dramatically with COST.
for cost in [1, 2, 5, 10]:
    resp = cmd(f"encrypt 1 {cost} " + "00"*16)
    m = re.search(r"ciphertext ([0-9a-f]+)", resp)
    if m:
        info = parse(m.group(1))
        print(f"COST={cost:2d} nonce={info['nonce']:08x} tag={info['tag']:08x} "
              f"ks={info['payload'].hex()}")
    else:
        print(f"COST={cost} failed: {resp.strip()}")
    print(cmd("budget").strip())

# Also grab flag once more
print(cmd("get_flag"))
r.close()
