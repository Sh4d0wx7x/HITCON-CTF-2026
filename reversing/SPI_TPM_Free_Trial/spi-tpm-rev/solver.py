#!/usr/bin/env python3
"""
SPI TPM Free Trial – complete solver skeleton
HITCON CTF 2026

Validated components:
  - Ownership bypass (encrypt under key id 1)
  - Bit-exact f17e0 / f3700 / f33d0
  - F1 inverter
  - Feistel consistency
  - 12 clean constraints from live harvest
  - Offline decrypt path

The only remaining research step is the structured algebraic
recovery of (k0, k1) from the constraints.
"""

import os, sys, subprocess
from pathlib import Path

M64 = 0xFFFFFFFFFFFFFFFF
M32 = 0xFFFFFFFF
M16 = 0xFFFF

C1 = 0xd6e8feb86659fd93
C2 = 0x9e3779b97f4a7c15
C4 = 0xbf58476d1ce4e5b9
C5 = 0x62696c696e2d7221
C6 = 0x94d049bb133111eb
INV_C4 = 0x96de1b173f119089
INV_C6 = 0x319642b2d24d8ec3

def rotl64(x, n):
    x &= M64
    n &= 63
    return ((x << n) | (x >> (64 - n))) & M64

def rotl16(x, n):
    x &= M16
    n &= 15
    return ((x << n) | (x >> (16 - n))) & M16

def triple32(x):
    x &= M32
    x ^= x >> 16
    x = (x * 0x21f0aaad) & M32
    x ^= x >> 15
    x = (x * 0x735a2d97) & M32
    x ^= x >> 15
    return x

OFFSETS = [0x9e3779b9, 0x3c6ef372, 0xdaa66d2b, 0x78dde6e4, 0x1715609d, 0xb54cda56]

def f17e0(value, nonce, chunk, cost, flag_r8):
    mask = M32 if flag_r8 == 0 else 0
    mask &= 0xbb03e172
    mask = (mask - 0x2e4ab5cb) & M32
    seed = ((chunk * 0x9e3779b9) ^ nonce ^ (cost * 0x735a2d97) ^ mask) & M32
    W = [triple32((seed + off) & M32) for off in OFFSETS]
    A = value >> 16
    R = value
    for i in range(6):
        rot1, rot2 = 7 + i, 3 + 2 * i
        Wi = W[i]
        edx = A
        A = (A & 0xFFFF0000) | rotl16(A, rot1)
        r11 = Wi >> 16
        esi = (Wi + edx) & M32
        esi = (esi & 0xFFFF0000) | rotl16(esi, rot2)
        A = (A + r11) ^ esi ^ R
        R = edx
    return ((A & M16) << 16) | (R & M16)

def f33d0(hi16, k0, k1, ridx=0):
    t_acc = (hi16 * C1) & M64
    t2 = rotl64(k1, 17) ^ k0 ^ t_acc
    t3 = rotl64(k0, 29) ^ k1
    t2 ^= C5
    t2 = (t2 + C2) & M64
    x = t2
    x ^= x >> 30
    x = (x * C4) & M64
    x ^= x >> 27
    A = (x * C6) & M64
    rsi = t3 ^ A ^ (A >> 31)
    Cin = (rsi + C2) & M64
    y = Cin
    y ^= y >> 30
    y = (y * C4) & M64
    y ^= y >> 27
    y = (y * C6) & M64
    D = y ^ (y >> 31)
    return (D ^ (D >> 16) ^ (D >> 32) ^ (D >> 48)) & 0xFFFF

def f3700(k0, k1, S0, cost, flag):
    S = S0 & M32
    if flag == 0:
        for i in range(cost):
            H, L = (S >> 16) & 0xFFFF, S & 0xFFFF
            out = f33d0(H, k0, k1, i & 3)
            S = (((out ^ L) & 0xFFFF) << 16) | H
    else:
        for step in range(cost):
            L, H = S & 0xFFFF, (S >> 16) & 0xFFFF
            out = f33d0(L, k0, k1, (cost - 1 - step) & 3)
            S = (L << 16) | ((out ^ H) & 0xFFFF)
    return S & M32

# ---------- F1 inverter ----------
INV_SRC = r'''
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#define M32 0xFFFFFFFFu
#define M16 0xFFFFu
static uint32_t rotl16(uint32_t x, int n) {
    n &= 15;
    uint32_t lo = x & M16;
    return (x & 0xFFFF0000u) | (((lo << n) | (lo >> (16-n))) & M16);
}
static uint32_t triple32(uint32_t x) {
    x ^= x >> 16; x *= 0x21f0aaad; x ^= x >> 15;
    x *= 0x735a2d97; x ^= x >> 15; return x;
}
static const uint32_t OFF[6] = {0x9e3779b9,0x3c6ef372,0xdaa66d2b,0x78dde6e4,0x1715609d,0xb54cda56};
uint32_t f17e0(uint32_t v, uint32_t n, uint32_t c, uint32_t cost, int fl) {
    uint32_t mask = fl ? 0 : M32;
    mask &= 0xbb03e172; mask -= 0x2e4ab5cb;
    uint32_t seed = (c*0x9e3779b9)^n^(cost*0x735a2d97)^mask;
    uint32_t W[6]; for(int i=0;i<6;i++) W[i]=triple32(seed+OFF[i]);
    uint32_t A=v>>16, R=v;
    for(int i=0;i<6;i++){
        uint32_t edx=A; A=rotl16(A,7+i);
        uint32_t esi=W[i]+edx; esi=rotl16(esi,3+2*i);
        A=(A+(W[i]>>16))^esi^R; R=edx;
    }
    return ((A&M16)<<16)|(R&M16);
}
int main(int argc,char**argv){
    uint32_t target=strtoul(argv[1],0,0);
    uint32_t nonce=strtoul(argv[2],0,0);
    uint32_t chunk=strtoul(argv[3],0,0);
    uint32_t cost=strtoul(argv[4],0,0);
    for(uint64_t v=0;v<=0xffffffffull;v++)
        if(f17e0((uint32_t)v,nonce,chunk,cost,1)==target){printf("%08x\n",(uint32_t)v);return 0;}
    return 1;
}
'''

def build_inverter():
    src = Path("/tmp/inv_f17e0.c")
    bin = Path("/tmp/inv_f17e0")
    if not bin.exists() or (src.exists() and src.stat().st_mtime > bin.stat().st_mtime):
        src.write_text(INV_SRC)
        os.system(f"gcc -O3 -march=native -o {bin} {src}")
        os.chmod(bin, 0o755)
    return str(bin)

def invert_f1(ct, nonce, chunk=0, cost=1):
    inv = build_inverter()
    out = subprocess.check_output([inv, hex(ct), hex(nonce), str(chunk), str(cost)], timeout=180).decode().strip()
    return int(out, 16)

# ---------- Best data we collected ----------
CONSTRAINTS = [
    (0xed32, 0x8551),
    (0x1c6f, 0x50ec),
    (0xfc17, 0x89a7),
    (0x914c, 0x94bb),
    (0xf944, 0xede0),
    (0xc238, 0xa93c),
    (0xae93, 0x85ca),
    (0x5ee6, 0x5804),
    (0x1b99, 0x9484),
    (0x73dd, 0xb6bf),
    (0x20be, 0x27a2),
    (0xcec2, 0xdc6f),
]

FLAG_BLOB = (
    "53545031020028003a05a08bb35f080046000000cbf5b75dd70e32e4094adeab9182efca"
    "1c1897468bc86f3ee29282a76869e577d9fa50170dd2eb52acf253aaacb03058f254f91d"
    "52f48acb449b3c601b715fc72392b80ba7c9a433be509cba41bbd19fdac7b0a814442baa"
    "cfadb16c"
)

def verify_key(k0, k1):
    return all(f33d0(hi, k0, k1) == tgt for hi, tgt in CONSTRAINTS)

def decrypt_flag(k0, k1):
    blob = bytes.fromhex(FLAG_BLOB)
    nonce = int.from_bytes(blob[8:12], "little")
    cost  = int.from_bytes(blob[0xc:0xe], "little") | (blob[0xe] << 16)
    length = int.from_bytes(blob[0x10:0x12], "little")
    ct = blob[0x28:]
    pt = bytearray()
    for c in range((length + 3) // 4):
        ctw = int.from_bytes(ct[c*4:c*4+4].ljust(4, b"\x00"), "little")
        b = invert_f1(ctw, nonce, c, cost)
        a = f3700(k0, k1, b, cost, flag=1)
        ptw = f17e0(a, nonce, c, cost, 0)
        pt += ptw.to_bytes(4, "little")
    return bytes(pt[:length])

if __name__ == "__main__":
    print("[*] 12 constraints loaded")
    for hi, t in CONSTRAINTS:
        print(f"    f33d0({hi:#06x}) == {t:#06x}")

    print("""
[*] All validated pieces are present.

    Remaining work:
      1. Lift the 16-bit fold
      2. Invert the two splitmix stages
      3. Form linear relations on (k0, k1)
      4. Solve the rank-62 map (4 candidates)
      5. verify_key() → True
      6. pt = decrypt_flag(k0, k1)
""")

    # Once you have a real key:
    # k0 = 0x................................
    # k1 = 0x................................
    # if verify_key(k0, k1):
    #     print(decrypt_flag(k0, k1))
