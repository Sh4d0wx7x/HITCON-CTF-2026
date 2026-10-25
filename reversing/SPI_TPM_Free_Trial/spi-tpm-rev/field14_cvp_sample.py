#!/usr/bin/env python3
"""Randomized CVP sampling of the field14 linear solution set."""
import sys, os, time, random, struct, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field14_solve import make_samples, P
from fpylll import IntegerMatrix, LLL, CVP

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
    return L, D, A, Bv, C

def extract(v, D, wx=WXY):
    if v[0] % wx or v[1] % wx:
        return None
    x = v[0] // wx
    y = v[1] // wx
    if not (0 <= x < (1<<64) and 0 <= y < (1<<64)):
        return None
    r0 = v[2]
    if not (0 <= r0 < B):
        return None
    rs = []
    for j, d in enumerate(D):
        u = v[3+j]
        r = (u - d) % P
        if not (0 <= r < B):
            return None
        rs.append(r)
    return x, y, r0, rs

def check(x, y, samples):
    z = (x * y) % P
    return all((((s['a']*y + s['b']*x + s['c']*z) % P) >> 118) == s['leak'] for s in samples)

def run(n=27, seed=42, trials=1000, method='fast'):
    rng = random.Random(seed)
    key16 = bytes(rng.getrandbits(8) for _ in range(16))
    samples = make_samples(key16, n, seed=seed)
    kx, ky = struct.unpack('<QQ', key16)
    print('actual', hex(kx), hex(ky), flush=True)
    L, D, A, Bv, C = build(samples)
    LLL.reduction(L, delta=0.99)
    seen = {}
    true_found = False
    t0 = time.time()
    for it in range(trials):
        # random target: x,y,r0 centered; r_i random in [0,B)
        target = [ (1<<63)*WXY, (1<<63)*WXY, B2 ]
        target += [ (D[j] + rng.randrange(B)) for j in range(len(D)) ]
        v = CVP.closest_vector(L, target, method=method)
        res = extract(v, D)
        if res:
            x, y, r0, rs = res
            key = (x, y)
            if key not in seen:
                seen[key] = 1
                ok = check(x, y, samples)
                if ok:
                    print('TRUE FOUND at trial', it, hex(x), hex(y), flush=True)
                    true_found = True
                    break
        if (it+1) % 100 == 0:
            print('trial', it+1, 'distinct', len(seen), 'time', round(time.time()-t0,2), flush=True)
    print('done distinct', len(seen), 'true', true_found, 'time', round(time.time()-t0,2), flush=True)
    return seen, true_found

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 27
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 42
    trials = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    method = sys.argv[4] if len(sys.argv) > 4 else 'fast'
    run(n, seed, trials, method)
