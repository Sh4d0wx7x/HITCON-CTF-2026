#!/usr/bin/env python3
"""Lattice attack on field14 leak: 27 samples, 2D HNP with bilinear z=xy."""
import sys, os, time, random, struct, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field14_solve import make_samples, P, coeffs
from fpylll import IntegerMatrix, LLL, BKZ

B = 1 << 118
B2 = 1 << 117

def build_lattice(samples, wx=1<<56, wr=8, M=1<<120):
    n = len(samples)
    assert n >= 4
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
    m = n - 1  # number of equations
    dim = 3 + m + 1  # x,y,r0, r1..rm, last
    L = IntegerMatrix(dim, dim)
    # rows 0..2: x,y,r0
    L[0, 0] = 1
    for j in range(m):
        L[0, 3+j] = A[j]
    L[1, 1] = 1
    for j in range(m):
        L[1, 3+j] = Bv[j]
    L[2, 2] = 1
    for j in range(m):
        L[2, 3+j] = C[j]
    # rows 3..3+m-1: p in r_i coordinate
    for j in range(m):
        L[3+j, 3+j] = P
    # target row
    L[3+m, 2] = -B2
    for j in range(m):
        L[3+m, 3+j] = -(D[j] + B2)
    L[3+m, dim-1] = M
    # scale columns
    for r in range(dim):
        L[r, 0] *= wx
        L[r, 1] *= wx
        for j in range(2, 3+m):
            L[r, j] *= wr
    return L, A, Bv, C, D

def check_vec(vec, samples, wx=1<<56, wr=8, M=1<<120, verbose=False):
    dim = len(vec)
    # last coordinate should be +-M (or multiple)
    last = vec[-1]
    if last == 0:
        return None
    if last % M != 0:
        return None
    k = last // M
    if k != 1 and k != -1:
        return None
    # undo scaling and target shift
    x = vec[0] // wx
    y = vec[1] // wx
    r0 = vec[2] // wr + B2
    if vec[0] % wx or vec[1] % wx or vec[2] % wr:
        return None
    if not (0 <= x < (1<<64) and 0 <= y < (1<<64)):
        return None
    r = [r0]
    for j in range(3, dim-1):
        if vec[j] % wr:
            return None
        r.append(vec[j] // wr + B2)
    for v in r:
        if not (0 <= v < B):
            return None
    # verify leaks directly
    for i, smp in enumerate(samples):
        a, b, c = smp['a'], smp['b'], smp['c']
        z = (x * y) % P
        acc = (a * y + b * x + c * z) % P
        if (acc >> 118) != smp['leak']:
            return None
    if verbose:
        print('FOUND x,y', hex(x), hex(y), 'k', k, 'r0', r[0])
    return x, y, r

def run(n=27, seed=42, block=20):
    rng = random.Random(seed)
    key16 = bytes(rng.getrandbits(8) for _ in range(16))
    samples = make_samples(key16, n, seed=seed)
    kx, ky = struct.unpack('<QQ', key16)
    print('actual key', key16.hex(), hex(kx), hex(ky), flush=True)
    L, A, Bv, C, D = build_lattice(samples)
    print('lattice built', L.nrows, L.ncols, flush=True)
    # compute true vector coordinates (for diagnostics)
    wx, wr, M = 1<<56, 8, 1<<120
    true_vec = [kx*wx, ky*wx, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # fill r_i and target shift
    rlist = []
    for smp in samples:
        acc = (smp['a']*ky + smp['b']*kx + smp['c']*((kx*ky)%P)) % P
        rlist.append(acc & (B-1))
    true_vec[2] = (rlist[0] - B2) * wr
    for j in range(n-1):
        true_vec[3+j] = (rlist[j+1] - B2) * wr
    true_vec[-1] = M
    tn = math.isqrt(sum(v*v for v in true_vec))
    print('true vec norm bits', tn.bit_length(), flush=True)
    t0 = time.time()
    LLL.reduction(L, delta=0.99)
    print('LLL done', time.time()-t0, flush=True)
    for i in range(min(5, L.nrows)):
        vec = [int(L[i, j]) for j in range(L.ncols)]
        nrm = math.isqrt(sum(v*v for v in vec))
        print('  LLL row', i, 'norm bits', nrm.bit_length(), 'last bits', abs(vec[-1]).bit_length(), flush=True)
    found = []
    for i in range(L.nrows):
        vec = [int(L[i, j]) for j in range(L.ncols)]
        res = check_vec(vec, samples)
        if res:
            found.append(res)
            print('LLL vector', i, 'FOUND', hex(res[0]), hex(res[1]), flush=True)
    print('LLL found', len(found), flush=True)
    if found:
        return found
    t0 = time.time()
    BKZ.reduction(L, BKZ.Param(block_size=block, max_loops=4))
    print('BKZ done', time.time()-t0, flush=True)
    for i in range(min(5, L.nrows)):
        vec = [int(L[i, j]) for j in range(L.ncols)]
        nrm = math.isqrt(sum(v*v for v in vec))
        print('  BKZ row', i, 'norm bits', nrm.bit_length(), 'last bits', abs(vec[-1]).bit_length(), flush=True)
    for i in range(L.nrows):
        vec = [int(L[i, j]) for j in range(L.ncols)]
        res = check_vec(vec, samples)
        if res:
            found.append(res)
            print('BKZ vector', i, 'FOUND', hex(res[0]), hex(res[1]), flush=True)
    print('total found', len(found), flush=True)
    return found

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 27
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 42
    block = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    run(n, seed, block)
