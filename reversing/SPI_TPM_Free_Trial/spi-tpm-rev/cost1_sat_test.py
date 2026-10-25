#!/usr/bin/env python3
import z3, time, random, struct, sys

C1 = 0xd6e8feb86659fd93
C2 = 0xa5a3564e27f8862f
TAG = 0x62696c696e2d7221
GAMMA = 0x9e3779b97f4a7c15
M1 = 0xbf58476d1ce4e5b9
M2 = 0x94d049bb133111eb

def fmix_nf(x):
    x = x ^ z3.LShR(x, 30)
    x = x * z3.BitVecVal(M1, 64)
    x = x ^ z3.LShR(x, 27)
    x = x * z3.BitVecVal(M2, 64)
    return x

def fmix_full(x):
    y = fmix_nf(x)
    return y ^ z3.LShR(y, 31)

def f33_z3(p, rnd, A, B):
    # p is 16-bit BitVec or int
    if isinstance(p, int):
        pv = z3.BitVecVal(p, 16)
    else:
        pv = p
    x = z3.ZeroExt(48, pv)
    t = A ^ (x * z3.BitVecVal(C1, 64)) ^ z3.BitVecVal(rnd*C2 & ((1<<64)-1), 64) ^ z3.BitVecVal(TAG, 64)
    t = t + z3.BitVecVal(GAMMA, 64)
    Y = fmix_nf(t)
    u = B ^ Y ^ z3.LShR(Y, 31)
    v = fmix_full(u + z3.BitVecVal(GAMMA, 64))
    fold = z3.LShR(v, 16) ^ z3.LShR(v, 32) ^ v ^ z3.LShR(v, 48)
    return z3.Extract(15, 0, fold)

def g_cost1_z3(a, A, B):
    # a 32-bit; returns b 32-bit bitvec
    s = z3.BitVecVal(a, 32) if isinstance(a, int) else a
    hi = z3.Extract(31, 16, s)
    x = f33_z3(hi, 0, A, B)  # 16-bit output; only low 16 bits of f33d0 matter
    # b = ((x ^ s) << 16) | hi; only low 16 bits of x^s survive the shift
    lo = x ^ z3.Extract(15, 0, s)
    return z3.Concat(lo, hi)

def solve_cost1(pairs, timeout=300000):
    A = z3.BitVec('A', 64)
    B = z3.BitVec('B', 64)
    s = z3.Solver()
    s.set('timeout', timeout)
    for a, b in pairs:
        s.add(g_cost1_z3(a, A, B) == z3.BitVecVal(b, 32))
    t0 = time.time()
    r = s.check()
    print('res', r, 'time', time.time()-t0)
    if r == z3.sat:
        m = s.model()
        return m[A].as_long(), m[B].as_long()
    return None

if __name__ == '__main__':
    # test with random A,B and generated pairs
    rng = random.Random(1)
    A0 = rng.getrandbits(64); B0 = rng.getrandbits(64)
    def fmix(x):
        x &= (1<<64)-1
        x ^= x >> 30; x = (x*M1) & ((1<<64)-1)
        x ^= x >> 27; x = (x*M2) & ((1<<64)-1)
        x ^= x >> 31
        return x & ((1<<64)-1)
    def f33(p, rnd, A, B):
        t = A ^ ((p*C1) & ((1<<64)-1)) ^ ((rnd*C2) & ((1<<64)-1)) ^ TAG
        t = (t + GAMMA) & ((1<<64)-1)
        y = fmix(t)
        u = B ^ y ^ (y>>31)
        v = fmix((u + GAMMA) & ((1<<64)-1))
        fold = ((v>>16) ^ (v>>32) ^ v ^ (v>>48)) & 0xffff
        return fold
    def g(a):
        hi = (a>>16)&0xffff
        x = f33(hi, 0, A0, B0)
        return (((x ^ a) << 16) & 0xffffffff) | hi
    pairs = [(rng.getrandbits(32), 0) for _ in range(10)]
    pairs = [(a, g(a)) for a, _ in pairs]
    print('true', hex(A0), hex(B0))
    for n in [1,2,3,4,5,6,8,10]:
        print('--- n', n)
        res = solve_cost1(pairs[:n], timeout=120000)
        if res:
            print('got', hex(res[0]), hex(res[1]), 'match', res == (A0,B0))
            break
