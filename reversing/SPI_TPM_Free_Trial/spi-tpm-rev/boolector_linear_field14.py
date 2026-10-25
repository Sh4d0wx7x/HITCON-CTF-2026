#!/usr/bin/env python3
"""Solve the linearized field14 system with Boolector (no z=xy constraint).

Equations (from eliminating z via sample 0):
  A_i*x + B_i*y + C_i*r0 - r_i == D_i (mod p),  0 <= r_i < 2^118
Enumerate solutions and check z=x*y against the real leaks.
"""
import sys, os, time, random, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field14_solve import make_samples, P
import pyboolector

B = 1 << 118
W = 256

def bconst(btor, v, w=W):
    return btor.Const(v % (1 << w), w)

def zext(btor, node, w=W):
    return node if node.width == w else btor.Uext(node, w - node.width)

def reduce_mod_p(btor, V):
    p = bconst(btor, P)
    for _ in range(3):
        V = (V & p) + (V >> 127)
    return btor.Cond(btor.Ugte(V, p), V - p, V)

def mul_const(btor, var, c, w=W):
    """var is w-bit; c is an integer constant. Return (var*c) mod 2^w."""
    res = bconst(btor, 0)
    v = var
    while c:
        if c & 1:
            res = res + v
        c >>= 1
        if c:
            v = v << 1
    return res

def build(samples, manual_mul=False):
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
    btor = pyboolector.Boolector()
    btor.Set_opt(0, 1)   # model-gen
    btor.Set_opt(14, 3)  # rewrite-level
    btor.Set_opt(7, 1)   # CaDiCaL
    x = btor.Var(btor.BitVecSort(64), 'x')
    y = btor.Var(btor.BitVecSort(64), 'y')
    r0 = btor.Var(btor.BitVecSort(118), 'r0')
    rx = zext(btor, x)
    ry = zext(btor, y)
    rr0 = zext(btor, r0)
    rvars = []
    for j in range(n-1):
        r = btor.Var(btor.BitVecSort(118), 'r%d' % (j+1))
        rvars.append(r)
        if manual_mul:
            vx = mul_const(btor, rx, A[j])
            vy = mul_const(btor, ry, Bv[j])
            vr = mul_const(btor, rr0, C[j])
        else:
            vx = btor.Mul(bconst(btor, A[j]), rx)
            vy = btor.Mul(bconst(btor, Bv[j]), ry)
            vr = btor.Mul(bconst(btor, C[j]), rr0)
        V = vx + vy + vr + bconst(btor, P - D[j])
        ACC = reduce_mod_p(btor, V)
        btor.Assert(btor.Eq(ACC, zext(btor, r)))
    return btor, x, y, r0, rvars

def enumerate_solutions(samples, limit=10000, timeout_s=300, manual_mul=False):
    btor, x, y, r0, rvars = build(samples, manual_mul)
    sols = []
    t0 = time.time()
    for it in range(limit):
        if time.time() - t0 > timeout_s:
            print('timeout after', it, 'solutions', flush=True)
            break
        res = btor.Sat()
        if res != pyboolector.BTOR_RESULT_SAT:
            print('sat result', res, 'after', it, flush=True)
            break
        xv = int(x.assignment, 2)
        yv = int(y.assignment, 2)
        sols.append((xv, yv))
        if it % 100 == 0:
            print('sol', it, hex(xv), hex(yv), 't', round(time.time()-t0,2), flush=True)
        # block this exact x,y
        btor.Assert(btor.Not(btor.And(btor.Eq(x, btor.Const(xv, 64)), btor.Eq(y, btor.Const(yv, 64)))))
    return sols

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 27
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 42
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10000
    manual = len(sys.argv) > 4 and sys.argv[4] == 'manual'
    rng = random.Random(seed)
    key16 = bytes(rng.getrandbits(8) for _ in range(16))
    samples = make_samples(key16, n, seed=seed)
    kx, ky = struct.unpack('<QQ', key16)
    print('actual key', key16.hex(), hex(kx), hex(ky), 'n', n, flush=True)
    sols = enumerate_solutions(samples, limit, manual_mul=manual)
    print('total sols', len(sols), flush=True)
    for xv, yv in sols:
        z = (xv * yv) % P
        ok = all(((s['a']*yv + s['b']*xv + s['c']*z) % P) >> 118 == s['leak'] for s in samples)
        if ok:
            print('TRUE KEY FOUND', hex(xv), hex(yv), flush=True)
            break
    else:
        print('no true key in enumerated set', flush=True)
