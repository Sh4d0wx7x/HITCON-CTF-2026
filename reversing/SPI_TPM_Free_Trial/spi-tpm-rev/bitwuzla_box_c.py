#!/usr/bin/env python3
"""Bitwuzla model over LLL coefficient variables with box + z=xy + sample0."""
import sys, os, time, random, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field14_solve import make_samples, P
from field14_cvp_sample import WXY, B
from field14_box_search import prepare, box_variants
from field14_box_enum import lll_basis, inv_matrix
import bitwuzla
from bitwuzla import Kind

def bv(tm, w, v):
    return tm.mk_bv_value(tm.mk_bv_sort(w), v % (1 << w))

def op(tm, kind, *args):
    return tm.mk_term(kind, list(args))

def zext(tm, node, w):
    cur = node.sort().bv_size()
    if cur == w:
        return node
    return tm.mk_term(Kind.BV_ZERO_EXTEND, [node], [w-cur])

def build_model(samples, lo, hi, timeout_ms=300000):
    Bm, clo, chi, lo, hi, _, _ = prepare(samples, lo, hi, 'default')
    n = len(Bm)
    sizes = [chi[i]-clo[i]+1 for i in range(n)]
    maxsize = max(sizes)
    cw = max(1, (maxsize-1).bit_length())
    W = 256
    OFF = 1 << 200
    tm = bitwuzla.TermManager()
    opts = bitwuzla.Options()
    opts.set(bitwuzla.Option.PRODUCE_MODELS, 1)
    opts.set(bitwuzla.Option.TIME_LIMIT_PER, timeout_ms)
    btor = bitwuzla.Bitwuzla(tm, opts)
    d = [tm.mk_const(tm.mk_bv_sort(cw), f'd{i}') for i in range(n)]
    for i in range(n):
        btor.assert_formula(tm.mk_term(Kind.BV_ULE, [d[i], bv(tm, cw, sizes[i]-1)]))
    base = [sum(clo[i]*Bm[i][k] for i in range(n)) for k in range(n)]
    S = []
    for k in range(n):
        s = bv(tm, W, OFF + base[k])
        for i in range(n):
            s = op(tm, Kind.BV_ADD, s, op(tm, Kind.BV_MUL, zext(tm, d[i], W), bv(tm, W, Bm[i][k])))
        S.append(s)
        btor.assert_formula(tm.mk_term(Kind.BV_UGE, [s, bv(tm, W, lo[k]+OFF)]))
        btor.assert_formula(tm.mk_term(Kind.BV_ULE, [s, bv(tm, W, hi[k]+OFF)]))
    v0 = op(tm, Kind.BV_SUB, S[0], bv(tm, W, OFF))
    v1 = op(tm, Kind.BV_SUB, S[1], bv(tm, W, OFF))
    v2 = op(tm, Kind.BV_SUB, S[2], bv(tm, W, OFF))
    x64 = tm.mk_term(Kind.BV_EXTRACT, [op(tm, Kind.BV_SHR, v0, bv(tm, W, 54))], [63, 0])
    y64 = tm.mk_term(Kind.BV_EXTRACT, [op(tm, Kind.BV_SHR, v1, bv(tm, W, 54))], [63, 0])
    x128 = zext(tm, x64, 128); y128 = zext(tm, y64, 128)
    z128 = op(tm, Kind.BV_MUL, x128, y128)
    # sample 0 equation
    s0 = samples[0]
    a0 = s0['a']; b0 = s0['b']; c0 = s0['c']; T0 = s0['leak'] << 118
    k0 = tm.mk_const(tm.mk_bv_sort(130), 'k0')
    lhs = op(tm, Kind.BV_ADD,
             op(tm, Kind.BV_ADD,
                op(tm, Kind.BV_MUL, zext(tm, x64, W), bv(tm, W, b0)),
                op(tm, Kind.BV_MUL, zext(tm, y64, W), bv(tm, W, a0))),
             op(tm, Kind.BV_MUL, zext(tm, z128, W), bv(tm, W, c0)))
    rhs = op(tm, Kind.BV_ADD,
             op(tm, Kind.BV_ADD, bv(tm, W, T0), v2),
             op(tm, Kind.BV_MUL, bv(tm, W, P), zext(tm, k0, W)))
    btor.assert_formula(tm.mk_term(Kind.EQUAL, [lhs, rhs]))
    return btor, tm, d, x64, y64, z128, cw

def solve(samples, lo, hi, timeout_ms=300000):
    t0 = time.time()
    btor, tm, d, x64, y64, z128, cw = build_model(samples, lo, hi, timeout_ms)
    res = btor.check_sat()
    dt = time.time()-t0
    if res == bitwuzla.Result.SAT:
        xv = int(btor.get_value(x64).value(2), 2)
        yv = int(btor.get_value(y64).value(2), 2)
        print('SAT', hex(xv), hex(yv), 'time', round(dt,2), flush=True)
        return xv, yv
    else:
        print('UNKNOWN/UNSAT', res, 'time', round(dt,2), flush=True)
        return None

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv)>1 else 27
    seed = int(sys.argv[2]) if len(sys.argv)>2 else 42
    timeout_s = int(sys.argv[3]) if len(sys.argv)>3 else 300
    rng = random.Random(seed)
    key16 = bytes(rng.getrandbits(8) for _ in range(16))
    kx, ky = struct.unpack('<QQ', key16)
    samples = make_samples(key16, n, seed=seed)
    print('actual', hex(kx), hex(ky), flush=True)
    L, D = lll_basis(samples)
    variants = box_variants(D)
    for vi, (lo, hi) in enumerate(variants):
        print('variant', vi, flush=True)
        res = solve(samples, lo, hi, timeout_s*1000)
        if res is not None:
            print('match', res==(kx,ky), flush=True)
            break
