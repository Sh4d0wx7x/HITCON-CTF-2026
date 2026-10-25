#!/usr/bin/env python3
"""DFS box-constrained enumeration of field14 linear solutions (wrap-aware)."""
import sys, os, time, random, struct, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field14_solve import make_samples, P
from field14_cvp_sample import build, WXY, B, B2
from field14_box_enum import lll_basis, inv_matrix, coeff_ranges
from fpylll import LLL

def box_variants(D):
    base_lo = [0, 0, 0]
    base_hi = [(1<<64)*WXY - 1, (1<<64)*WXY - 1, B-1]
    variants = [(base_lo[:], base_hi[:])]
    for d in D:
        new = []
        if d + B <= P:
            for lo, hi in variants:
                new.append((lo + [d], hi + [d + B - 1]))
        else:
            for lo, hi in variants:
                # high part [d, p-1]
                new.append((lo + [d], hi + [P - 1]))
                # low part [0, d+B-p-1]
                new.append((lo + [0], hi + [d + B - P - 1]))
        variants = new
    return variants

def int_range(a, b):
    ia = a.numerator // a.denominator
    ib = -((-b.numerator) // b.denominator)
    return ia, ib

def prepare(samples, lo, hi, order_mode='default'):
    L, D = lll_basis(samples)
    Inv = inv_matrix(L)
    ranges = coeff_ranges(Inv, lo, hi)
    n = L.nrows
    clo = []; chi = []
    for a, b in ranges:
        ia, ib = int_range(a, b)
        clo.append(ia); chi.append(ib)
    if order_mode == 'norm':
        idx = sorted(range(n), key=lambda i: -sum(int(L[i,j])**2 for j in range(n)))
    elif order_mode == 'span':
        idx = sorted(range(n), key=lambda i: -sum(1 for j in range(n) if abs(int(L[i,j])) > (1<<100)))
    else:
        idx = list(range(n))
    Bm = [[int(L[i,j]) for j in range(n)] for i in idx]
    clo = [clo[i] for i in idx]; chi = [chi[i] for i in idx]
    rem_min = [[0]*n for _ in range(n+1)]
    rem_max = [[0]*n for _ in range(n+1)]
    for i in range(n-1, -1, -1):
        for k in range(n):
            a = clo[i]*Bm[i][k]; b = chi[i]*Bm[i][k]
            rem_min[i][k] = rem_min[i+1][k] + min(a,b)
            rem_max[i][k] = rem_max[i+1][k] + max(a,b)
    return Bm, clo, chi, lo, hi, rem_min, rem_max

def check(x, y, samples):
    z = (x*y) % P
    return all((((s['a']*y + s['b']*x + s['c']*z) % P) >> 118) == s['leak'] for s in samples)

def search(samples, lo, hi, order_mode='default', node_limit=50_000_000, verbose=True):
    Bm, clo, chi, lo, hi, rem_min, rem_max = prepare(samples, lo, hi, order_mode)
    n = len(Bm)
    nodes = 0; leaves = 0; sols = 0
    found = [None]
    t0 = time.time()
    v = [0]*n
    def dfs(i):
        nonlocal nodes, leaves, sols
        nodes += 1
        if nodes > node_limit:
            return True
        if i == n:
            leaves += 1
            if v[0] % WXY == 0 and v[1] % WXY == 0:
                x = v[0] // WXY; y = v[1] // WXY
                if 0 <= x < (1<<64) and 0 <= y < (1<<64):
                    sols += 1
                    if check(x, y, samples):
                        found[0] = (x, y)
                        return True
            return False
        Bi = Bm[i]
        rm = rem_min[i+1]; rx = rem_max[i+1]
        for c in range(clo[i], chi[i]+1):
            for k in range(n):
                v[k] += c*Bi[k]
            ok = True
            for k in range(n):
                if v[k] + rx[k] < lo[k] or v[k] + rm[k] > hi[k]:
                    ok = False; break
            if ok:
                if dfs(i+1):
                    for k in range(n):
                        v[k] -= c*Bi[k]
                    return True
            for k in range(n):
                v[k] -= c*Bi[k]
        return False
    dfs(0)
    dt = time.time()-t0
    if verbose:
        print('nodes', nodes, 'leaves', leaves, 'sols', sols, 'time', round(dt,2), 'found', found[0] is not None, flush=True)
    return found[0], nodes, leaves, sols

def run(n=27, seed=42, mode='default', node_limit=50_000_000):
    rng = random.Random(seed)
    key16 = bytes(rng.getrandbits(8) for _ in range(16))
    kx, ky = struct.unpack('<QQ', key16)
    samples = make_samples(key16, n, seed=seed)
    print('actual', hex(kx), hex(ky), 'n', n, 'mode', mode, flush=True)
    L, D = lll_basis(samples)
    variants = box_variants(D)
    print('variants', len(variants), flush=True)
    total_nodes = 0
    for vi, (lo, hi) in enumerate(variants):
        print('variant', vi, 'lo_hi last', hex(lo[-1]), hex(hi[-1]), flush=True)
        res, nodes, leaves, sols = search(samples, lo, hi, mode, node_limit)
        total_nodes += nodes
        if res is not None:
            print('FOUND', hex(res[0]), hex(res[1]), 'match', res==(kx,ky), flush=True)
            return res
        if nodes > node_limit:
            print('node limit hit', flush=True)
            return None
    print('NOTFOUND total_nodes', total_nodes, flush=True)
    return None

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv)>1 else 27
    seed = int(sys.argv[2]) if len(sys.argv)>2 else 42
    mode = sys.argv[3] if len(sys.argv)>3 else 'default'
    node_limit = int(sys.argv[4]) if len(sys.argv)>4 else 50_000_000
    run(n, seed, mode, node_limit)
