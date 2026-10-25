#!/usr/bin/env python3
"""Try fpylll CVP on the linearized field14 lattice."""
import sys, os, time, random, struct, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field14_solve import make_samples, P
from fpylll import IntegerMatrix, LLL, BKZ, CVP

B = 1 << 118
B2 = 1 << 117
WXY = 1 << 54

def build(samples, wx=WXY):
    n = len(samples)
    a = [s['a'] for s in samples]
    b = [s['b'] for s in samples]
    c = [s['c'] for s in samples]
    T = [s['leak'] << 118 for s in samples]
    c0inv = pow(c[0], -1, P)
    A = []; Bv = []; C = []; D = []
    for i in range(1, n):
        ci_c0 = (c[i] * c0inv) % P
        A.append((b[i] - ci_c0 * b[0]) % P)
        Bv.append((a[i] - ci_c0 * a[0]) % P)
        C.append(ci_c0)
        D.append((T[i] - ci_c0 * T[0]) % P)
    m = n - 1
    dim = 3 + m
    L = IntegerMatrix(dim, dim)
    L[0, 0] = 1
    for j in range(m):
        L[0, 3+j] = A[j]
    L[1, 1] = 1
    for j in range(m):
        L[1, 3+j] = Bv[j]
    L[2, 2] = 1
    for j in range(m):
        L[2, 3+j] = C[j]
    for j in range(m):
        L[3+j, 3+j] = P
    for r in range(dim):
        L[r, 0] *= wx
        L[r, 1] *= wx
    target = [ (1<<63)*wx, (1<<63)*wx, B2 ] + [ (D[j] + B2) for j in range(m) ]
    return L, target, A, Bv, C, D

def check(x, y, samples):
    if not (0 <= x < (1<<64) and 0 <= y < (1<<64)):
        return False
    z = (x * y) % P
    return all((((s['a']*y + s['b']*x + s['c']*z) % P) >> 118) == s['leak'] for s in samples)

def run(n=27, seed=42, method='fast'):
    rng = random.Random(seed)
    key16 = bytes(rng.getrandbits(8) for _ in range(16))
    samples = make_samples(key16, n, seed=seed)
    kx, ky = struct.unpack('<QQ', key16)
    print('actual', hex(kx), hex(ky), flush=True)
    L, target, A, Bv, C, D = build(samples)
    print('dim', L.nrows, flush=True)
    t0 = time.time()
    LLL.reduction(L, delta=0.99)
    print('LLL', time.time()-t0, flush=True)
    t0 = time.time()
    v = CVP.closest_vector(L, target, method=method)
    print('CVP', time.time()-t0, flush=True)
    x = v[0] // WXY
    y = v[1] // WXY
    print('candidate x,y', hex(x), hex(y), 'check', check(x,y,samples), flush=True)
    print('diffs bits', [abs(v[i]-target[i]).bit_length() for i in range(len(v))][:5], flush=True)
    return v, target, samples

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 27
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 42
    method = sys.argv[3] if len(sys.argv) > 3 else 'fast'
    run(n, seed, method)
