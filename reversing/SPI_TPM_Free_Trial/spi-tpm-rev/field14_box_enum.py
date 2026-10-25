#!/usr/bin/env python3
"""Enumerate field14 linear solutions by box-constrained lattice enumeration."""
import sys, os, time, random, struct, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field14_solve import make_samples, P
from field14_cvp_sample import build, check, extract, WXY, B, B2
from fpylll import IntegerMatrix, LLL
from fractions import Fraction

def lll_basis(samples):
    L, D, A, Bv, C = build(samples)
    LLL.reduction(L, delta=0.99)
    return L, D

def inv_matrix(L):
    n = L.nrows
    # exact inverse via sympy
    import sympy
    M = sympy.Matrix([[int(L[i,j]) for j in range(n)] for i in range(n)])
    t0 = time.time()
    Inv = M.inv()
    print('inverse time', round(time.time()-t0,2), flush=True)
    return Inv

def coeff_ranges(Inv, box_lo, box_hi):
    n = Inv.rows
    ranges = []
    for i in range(n):
        lo = Fraction(0); hi = Fraction(0)
        for j in range(n):
            a = Fraction(Inv[j,i])
            if a >= 0:
                lo += a * box_lo[j]; hi += a * box_hi[j]
            else:
                lo += a * box_hi[j]; hi += a * box_lo[j]
        ranges.append((lo, hi))
    return ranges

def box_bounds(D):
    # scaled box for x,y,r0 and residues
    lo = [0, 0, 0]
    hi = [(1<<64)*WXY - 1, (1<<64)*WXY - 1, B-1]
    for d in D:
        lo.append(d)
        hi.append(d + B - 1)
    return lo, hi

def main(n=27, seed=42):
    rng = random.Random(seed)
    key16 = bytes(rng.getrandbits(8) for _ in range(16))
    kx, ky = struct.unpack('<QQ', key16)
    samples = make_samples(key16, n, seed=seed)
    print('actual', hex(kx), hex(ky), flush=True)
    L, D = lll_basis(samples)
    Inv = inv_matrix(L)
    lo, hi = box_bounds(D)
    ranges = coeff_ranges(Inv, lo, hi)
    sizes = []
    for i, (a, b) in enumerate(ranges):
        ia = a.numerator // a.denominator
        ib = -((-b.numerator) // b.denominator)
        sizes.append(ib - ia + 1)
        print(i, 'range', ia, ib, 'size', sizes[-1], flush=True)
    prod = 1
    for s in sizes:
        prod *= max(0, s)
    print('product', prod, 'bits', prod.bit_length(), flush=True)

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv)>1 else 27
    seed = int(sys.argv[2]) if len(sys.argv)>2 else 42
    main(n, seed)
