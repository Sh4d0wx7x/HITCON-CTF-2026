#!/usr/bin/env python3
"""Bitwuzla model of cost-1 G(a) key recovery."""
import sys, os, time, random, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boolector_cost1 import gen_pairs, C1, C2, TAG, GAMMA, M1, M2
from cipher_model import MASK64
import bitwuzla
from bitwuzla import Kind

def bv(tm, sort, v):
    return tm.mk_bv_value(sort, v)

def op(tm, kind, *args):
    return tm.mk_term(kind, list(args))

def fmix_nf(tm, sort, x):
    x = op(tm, Kind.BV_XOR, x, op(tm, Kind.BV_SHR, x, bv(tm, sort, 30)))
    x = op(tm, Kind.BV_MUL, x, bv(tm, sort, M1))
    x = op(tm, Kind.BV_XOR, x, op(tm, Kind.BV_SHR, x, bv(tm, sort, 27)))
    x = op(tm, Kind.BV_MUL, x, bv(tm, sort, M2))
    return x

def fmix_full(tm, sort, x):
    y = fmix_nf(tm, sort, x)
    return op(tm, Kind.BV_XOR, y, op(tm, Kind.BV_SHR, y, bv(tm, sort, 31)))

def f33_low16(tm, sort, p16, k0, k1, rnd):
    # p16: 16-bit term; k0,k1: 64-bit
    p64 = op(tm, Kind.BV_ZERO_EXTEND, p16, bv(tm, sort, 48)) if False else tm.mk_term(Kind.BV_ZERO_EXTEND, [p16], [48])
    rax = k1
    rdi = op(tm, Kind.BV_MUL, p64, bv(tm, sort, C1))
    rax = op(tm, Kind.BV_ROL, rax, bv(tm, sort, 17))
    rax = op(tm, Kind.BV_XOR, rax, k0)
    rsi = op(tm, Kind.BV_ROL, k0, bv(tm, sort, 29))
    rsi = op(tm, Kind.BV_XOR, rsi, k1)
    rax = op(tm, Kind.BV_XOR, rax, rdi)
    rax = op(tm, Kind.BV_XOR, rax, bv(tm, sort, (rnd * C2) & MASK64))
    rax = op(tm, Kind.BV_XOR, rax, bv(tm, sort, TAG))
    rax = op(tm, Kind.BV_ADD, rax, bv(tm, sort, GAMMA))
    y = fmix_nf(tm, sort, rax)
    rsi = op(tm, Kind.BV_XOR, rsi, y)
    rsi = op(tm, Kind.BV_XOR, rsi, op(tm, Kind.BV_SHR, y, bv(tm, sort, 31)))
    rax = fmix_full(tm, sort, op(tm, Kind.BV_ADD, rsi, bv(tm, sort, GAMMA)))
    fold = op(tm, Kind.BV_XOR,
              op(tm, Kind.BV_XOR,
                 op(tm, Kind.BV_SHR, rax, bv(tm, sort, 16)),
                 op(tm, Kind.BV_SHR, rax, bv(tm, sort, 32))),
              op(tm, Kind.BV_XOR, rax, op(tm, Kind.BV_SHR, rax, bv(tm, sort, 48))))
    return tm.mk_term(Kind.BV_EXTRACT, [fold], [15, 0])

def solve(kx, ky, pairs, timeout_ms=300000):
    tm = bitwuzla.TermManager()
    opts = bitwuzla.Options()
    opts.set(bitwuzla.Option.PRODUCE_MODELS, 1)
    opts.set(bitwuzla.Option.TIME_LIMIT_PER, timeout_ms)
    b = bitwuzla.Bitwuzla(tm, opts)
    sort = tm.mk_bv_sort(64)
    x = tm.mk_const(sort, 'x')
    y = tm.mk_const(sort, 'y')
    for a, bb in pairs:
        ahi = tm.mk_bv_value(tm.mk_bv_sort(16), (a >> 16) & 0xffff)
        alo = tm.mk_bv_value(tm.mk_bv_sort(16), a & 0xffff)
        f = f33_low16(tm, sort, ahi, x, y, 0)
        blo = op(tm, Kind.BV_XOR, f, alo)
        bnode = tm.mk_term(Kind.BV_CONCAT, [blo, ahi])
        b.assert_formula(tm.mk_term(Kind.EQUAL, [bnode, tm.mk_bv_value(tm.mk_bv_sort(32), bb)]))
    t0 = time.time()
    res = b.check_sat()
    dt = time.time() - t0
    print('res', res, 'time', round(dt,2), flush=True)
    if res == bitwuzla.Result.SAT:
        xv = int(b.get_value(x).value(2), 2)
        yv = int(b.get_value(y).value(2), 2)
        print('found', hex(xv), hex(yv), 'match', (xv,yv)==(kx,ky), flush=True)
        return xv, yv
    return None

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    timeout_ms = int(sys.argv[3]) if len(sys.argv) > 3 else 300000
    rng = random.Random(seed)
    kx = rng.getrandbits(64); ky = rng.getrandbits(64)
    pairs = gen_pairs(kx, ky, n, seed)
    print('actual', hex(kx), hex(ky), 'n', n, flush=True)
    solve(kx, ky, pairs, timeout_ms)
