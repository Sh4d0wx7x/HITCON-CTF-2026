#!/usr/bin/env python3
"""Boolector model of cost-1 G(a) key recovery from known (a,b) pairs."""
import sys, os, time, random, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cipher_model import f33d0, f3700, MASK64
import pyboolector

C1 = 0xd6e8feb86659fd93
C2 = 0xa5a3564e27f8862f
TAG = 0x62696c696e2d7221
GAMMA = 0x9e3779b97f4a7c15
M1 = 0xbf58476d1ce4e5b9
M2 = 0x94d049bb133111eb

def rol64(btor, x, n):
    return btor.Rol(x, n)

def fmix_nf(btor, x):
    x = x ^ (x >> 30)
    x = x * btor.Const(M1, 64)
    x = x ^ (x >> 27)
    x = x * btor.Const(M2, 64)
    return x

def fmix_full(btor, x):
    y = fmix_nf(btor, x)
    return y ^ (y >> 31)

def f33_low16(btor, p16, k0, k1, rnd):
    # p16: 16-bit node; k0,k1: 64-bit nodes
    p64 = btor.Uext(p16, 48)
    rax = k1
    rdi = p64 * btor.Const(C1, 64)
    rax = rol64(btor, rax, 17)
    rax = rax ^ k0
    rsi = rol64(btor, k0, 29)
    rsi = rsi ^ k1
    rax = rax ^ rdi
    rax = rax ^ btor.Const((rnd * C2) & MASK64, 64)
    rax = rax ^ btor.Const(TAG, 64)
    rax = rax + btor.Const(GAMMA, 64)
    y = fmix_nf(btor, rax)
    rsi = rsi ^ y
    rsi = rsi ^ (y >> 31)
    rax = fmix_full(btor, rsi + btor.Const(GAMMA, 64))
    fold = (rax >> 16) ^ (rax >> 32) ^ rax ^ (rax >> 48)
    return btor.Slice(fold, 15, 0)

def gen_pairs(kx, ky, n, seed=1):
    rng = random.Random(seed)
    key = struct.pack('<QQ', kx, ky) + b'\x00'*32
    pairs = []
    for _ in range(n):
        a = rng.getrandbits(32)
        b = f3700(key, a, 1, 0)
        pairs.append((a, b))
    return pairs

def solve(kx, ky, pairs, engine=1):
    btor = pyboolector.Boolector()
    btor.Set_opt(0, 1)   # model-gen
    btor.Set_opt(14, 3)  # rewrite-level
    btor.Set_opt(7, engine)
    x = btor.Var(btor.BitVecSort(64), 'x')
    y = btor.Var(btor.BitVecSort(64), 'y')
    for a, b in pairs:
        ahi = btor.Const((a >> 16) & 0xffff, 16)
        alo = btor.Const(a & 0xffff, 16)
        f = f33_low16(btor, ahi, x, y, 0)
        blo = f ^ alo
        bnode = btor.Concat(blo, ahi)
        btor.Assert(btor.Eq(bnode, btor.Const(b, 32)))
    t0 = time.time()
    res = btor.Sat()
    dt = time.time() - t0
    print('res', res, 'time', round(dt,2), flush=True)
    if res == pyboolector.BTOR_RESULT_SAT:
        xv = int(x.assignment, 2); yv = int(y.assignment, 2)
        print('found', hex(xv), hex(yv), 'match', (xv,yv)==(kx,ky), flush=True)
        return xv, yv
    return None

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    engine = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    rng = random.Random(seed)
    kx = rng.getrandbits(64); ky = rng.getrandbits(64)
    pairs = gen_pairs(kx, ky, n, seed)
    print('actual', hex(kx), hex(ky), 'n', n, flush=True)
    solve(kx, ky, pairs, engine)
