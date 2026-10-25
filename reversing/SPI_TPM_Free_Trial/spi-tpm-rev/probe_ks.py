#!/usr/bin/env python3
from pwn import *
import re, hashlib, time, struct, binascii

context.log_level = "info"

def solve_pow(prefix, bits=8):
    salt = b"spi-tpm-pow-v1:" + prefix
    for nonce in range(40_000_000):
        h = hashlib.scrypt(prefix + str(nonce).encode(),
                           salt=salt, n=32768, r=8, p=1,
                           dklen=32, maxmem=256<<20)
        if int.from_bytes(h, "big") >> (256 - bits) == 0:
            return nonce
    raise Exception("pow failed")

def parse_stp1(hexstr):
    b = bytes.fromhex(hexstr)
    return {
        "raw": b,
        "nonce": struct.unpack_from("<I", b, 8)[0],
        "cost":  struct.unpack_from("<I", b, 12)[0],
        "length":struct.unpack_from("<I", b, 16)[0],
        "tag":   struct.unpack_from("<I", b, 20)[0],
        "hdr_rest": b[24:40],
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
        return out

    print(cmd("budget"))
    print(cmd("genkey"))          # fills slots; key 1 may already exist from boot
    print(cmd("budget"))

    samples = []

    # --- 1. Zero plaintext of several lengths (raw keystream) ---
    for n in [4, 8, 16, 32, 64]:
        pt = "00" * n
        before = cmd("budget")
        resp = cmd(f"encrypt 1 1 {pt}")
        after = cmd("budget")
        m = re.search(r"ciphertext ([0-9a-f]+)", resp)
        if not m:
            print(f"[!] encrypt {n} bytes failed:\n{resp}")
            continue
        info = parse_stp1(m.group(1))
        ks = info["payload"]
        samples.append(info)
        print(f"\n[ZERO len={n}] nonce={info['nonce']:08x} cost={info['cost']} "
              f"tag={info['tag']:08x}")
        print(f"  keystream = {ks.hex()}")
        print(f"  budget: {before.strip()} -> {after.strip()}")

    # --- 2. Known plaintext (all 'A') to confirm XOR ---
    pt_hex = "41" * 16
    resp = cmd(f"encrypt 1 1 {pt_hex}")
    m = re.search(r"ciphertext ([0-9a-f]+)", resp)
    if m:
        info = parse_stp1(m.group(1))
        ct = info["payload"]
        pt = bytes.fromhex(pt_hex)
        # If we had the matching zero-keystream for same nonce we could verify,
        # but nonces differ. Still record it.
        print(f"\n[AAAA len=16] nonce={info['nonce']:08x} tag={info['tag']:08x}")
        print(f"  ciphertext = {ct.hex()}")

    # --- 3. Grab the flag blob for later offline work ---
    flag_resp = cmd("get_flag")
    m = re.search(r"flag \d+ ([0-9a-f]+)", flag_resp)
    if m:
        fb = parse_stp1(m.group(1))
        print(f"\n[FLAG] nonce={fb['nonce']:08x} cost={fb['cost']} "
              f"len={fb['length']} tag={fb['tag']:08x}")
        print(f"  payload = {fb['payload'].hex()}")
        print(f"  full    = {m.group(1)}")

    print(cmd("budget"))
    r.close()

    # Quick structural summary
    print("\n=== keystream word summary (first sample) ===")
    if samples:
        s0 = samples[0]["payload"]
        words = [struct.unpack_from("<I", s0, i)[0] for i in range(0, len(s0), 4)]
        print(" ".join(f"{w:08x}" for w in words))

    return True

for attempt in range(1, 12):
    print(f"\n===== attempt {attempt} =====")
    try:
        if try_once():
            break
    except Exception as e:
        print(f"failed: {e}")
        time.sleep(4)
