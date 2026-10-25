#!/usr/bin/env python3
"""Bitwuzla box-only model over LLL coefficients; enumerate solutions."""
import sys, os, time, random, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field14_solve import make_samples, P
from field14_cvp_sample import WXY, B
from field14_box_search import prepare, box_variants
from field14_box_enum import lll_basis
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

def build(samples, lo, hi, timeout_ms=300000):
    Bm, clo, chi, lo, hi, _, _ = prepare(samples, lo, hi, 'default')
    n = len(Bm)
    sizes = [chi[i]-clo[i]+1 for i in range(n)]
    cw = max(1, (max(sizes)-1).bit_length())
    W = 160
    OFF = 1 << 145
    tm = bitwuzla.TermManager()
    opts = bitwuzla.Options()
    opts.set(bitwuzla.Option.PRODUCE_MODELS, 1)
    opts.set(bitwuzla.Option.TIME_LIMIT_PER, timeout_ms)
    btor = bitwuzla.Bitwuzla(tm, opts)
    d = [tm.mk_const(tm.mk_bv_sort(cw), f'd{i}') for i in range(n)]
    for i in range(n):
        btor.assert_formula(tm.mk_term(Kind.BV_ULE, [d[i], bv(tm, cw, sizes[i]-1)]))
    base = [sum(clo[i]*Bm[i][k] for i in range(n)) for k in range(n)]
    for k in range(n):
        s = bv(tm, W, OFF + base[k])
        for i in range(n):
            s = op(tm, Kind.BV_ADD, s, op(tm, Kind.BV_MUL, zext(tm, d[i], W), bv(tm, W, Bm[i][k])))
        btor.assert_formula(tm.mk_term(Kind.BV_UGE, [s, bv(tm, W, lo[k]+OFF)]))
        btor.assert_formula(tm.mk_term(Kind.BV_ULE, [s, bv(tm, W, hi[k]+OFF)]))
    return btor, tm, d, Bm, clo, cw

def get_sol(btor, tm, d, Bm, clo, cw):
    dvals = [int(btor.get_value(x).value(2), 2) for x in d]
    v = [sum((clo[i]+dvals[i])*Bm[i][k] for i in range(len(Bm))) for k in range(len(Bm))]
    return dvals, v

def check(x, y, samples):
    z = (x*y) % P
    return all((((s['a']*y + s['b']*x + s['c']*z) % P) >> 118) == s['leak'] for s in samples)

def run(n=27, seed=42, timeout_s=300, maxsol=5000):
    rng = random.Random(seed)
    key16 = bytes(rng.getrandbits(8) for _ in range(16))
    kx, ky = struct.unpack('<QQ', key16)
    samples = make_samples(key16, n, seed=seed)
    print('actual', hex(kx), hex(ky), flush=True)
    L, D = lll_basis(samples)
    variants = box_variants(D)
    for vi, (lo, hi) in enumerate(variants):
        print('variant', vi, flush=True)
        btor, tm, d, Bm, clo, cw = build(samples, lo, hi, timeout_s*1000)
        t0 = time.time()
        for it in range(maxsol):
            res = btor.check_sat()
            if res != bitwuzla.Result.SAT:
                print('end', res, 'it', it, 'time', round(time.time()-t0,2), flush=True)
                break
            dvals, v = get_sol(btor, tm, d, Bm, clo, cw)
            x = v[0]//WXY; y = v[1]//WXY
            ok = check(x, y, samples)
            print('sol', it, hex(x), hex(y), 'TRUE' if ok else '', 't', round(time.time()-t0,2), flush=True)
            if ok:
                print('FOUND', hex(x), hex(y), 'match', (x,y)==(kx,ky), flush=True)
                return x, y
            # block
            eqs = [tm.mk_term(Kind.EQUAL, [d[i], bv(tm, cw, dvals[i])]) for i in range(len(d))]
            btor.assert_formula(tm.mk_term(Kind.NOT, [tm.mk_term(Kind.AND, eqs)]))
        print('variant done', vi, flush=True)
    return None

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv)>1 else 27
    seed = int(sys.argv[2]) if len(sys.argv)>2 else 42
    timeout_s = int(sys.argv[3]) if len(sys.argv)>3 else 300
    maxsol = int(sys.argv[4]) if len(sys.argv)>4 else 5000
    run(n, seed, timeout_s, maxsol)
