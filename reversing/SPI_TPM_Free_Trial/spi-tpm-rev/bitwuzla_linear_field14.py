#!/usr/bin/env python3
"""Bitwuzla exact linearized field14 system with quotient variables.

A_i*x + B_i*y + C_i*r0 = D_i + r_i + p*k_i   (exact integers)
0 <= r_i < 2^118, 0 <= k_i < 2^120, x,y < 2^64.
Enumerate linear solutions and check z=x*y.
"""
import sys, os, time, random, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field14_solve import make_samples, P
import bitwuzla
from bitwuzla import Kind

W = 256

def bv(tm, w, v):
    return tm.mk_bv_value(tm.mk_bv_sort(w), v % (1 << w))

def op(tm, kind, *args):
    return tm.mk_term(kind, list(args))

def zext(tm, node, w):
    cur = node.sort().bv_size()
    if cur == w:
        return node
    return tm.mk_term(Kind.BV_ZERO_EXTEND, [node], [w - cur])

def build(samples, timeout_ms=300000):
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
    tm = bitwuzla.TermManager()
    opts = bitwuzla.Options()
    opts.set(bitwuzla.Option.PRODUCE_MODELS, 1)
    opts.set(bitwuzla.Option.TIME_LIMIT_PER, timeout_ms)
    btor = bitwuzla.Bitwuzla(tm, opts)
    x = tm.mk_const(tm.mk_bv_sort(64), 'x')
    y = tm.mk_const(tm.mk_bv_sort(64), 'y')
    r0 = tm.mk_const(tm.mk_bv_sort(118), 'r0')
    rx = zext(tm, x, W)
    ry = zext(tm, y, W)
    rr0 = zext(tm, r0, W)
    rvars = []
    for j in range(n-1):
        r = tm.mk_const(tm.mk_bv_sort(118), 'r%d' % (j+1))
        k = tm.mk_const(tm.mk_bv_sort(120), 'k%d' % (j+1))
        rvars.append(r)
        lhs = op(tm, Kind.BV_ADD,
                 op(tm, Kind.BV_ADD,
                    op(tm, Kind.BV_MUL, bv(tm, W, A[j]), rx),
                    op(tm, Kind.BV_MUL, bv(tm, W, Bv[j]), ry)),
                 op(tm, Kind.BV_MUL, bv(tm, W, C[j]), rr0))
        rhs = op(tm, Kind.BV_ADD,
                 op(tm, Kind.BV_ADD, bv(tm, W, D[j]), zext(tm, r, W)),
                 op(tm, Kind.BV_MUL, bv(tm, W, P), zext(tm, k, W)))
        btor.assert_formula(tm.mk_term(Kind.EQUAL, [lhs, rhs]))
    return btor, tm, x, y, r0, rvars

def check_key(x, y, samples):
    if not (0 <= x < (1 << 64) and 0 <= y < (1 << 64)):
        return False
    z = (x * y) % P
    return all((((s['a']*y + s['b']*x + s['c']*z) % P) >> 118) == s['leak'] for s in samples)

def enumerate_solutions(samples, limit=100, timeout_s=300):
    btor, tm, x, y, r0, rvars = build(samples, timeout_s*1000)
    t0 = time.time()
    found = []
    for it in range(limit):
        if time.time() - t0 > timeout_s:
            print('timeout after', it, flush=True)
            break
        res = btor.check_sat()
        if res != bitwuzla.Result.SAT:
            print('result', res, 'after', it, flush=True)
            break
        xv = int(btor.get_value(x).value(2), 2)
        yv = int(btor.get_value(y).value(2), 2)
        found.append((xv, yv))
        print('sol', it, hex(xv), hex(yv), 'check', check_key(xv, yv, samples), 't', round(time.time()-t0,2), flush=True)
        # block exact x,y
        btor.assert_formula(tm.mk_term(Kind.NOT, [tm.mk_term(Kind.AND, [
            tm.mk_term(Kind.EQUAL, [x, bv(tm, 64, xv)]),
            tm.mk_term(Kind.EQUAL, [y, bv(tm, 64, yv)])])]))
        if check_key(xv, yv, samples):
            break
    return found

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 27
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 42
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    timeout_s = int(sys.argv[4]) if len(sys.argv) > 4 else 300
    rng = random.Random(seed)
    key16 = bytes(rng.getrandbits(8) for _ in range(16))
    samples = make_samples(key16, n, seed=seed)
    kx, ky = struct.unpack('<QQ', key16)
    print('actual', hex(kx), hex(ky), 'n', n, flush=True)
    sols = enumerate_solutions(samples, limit, timeout_s)
    print('total', len(sols), flush=True)
