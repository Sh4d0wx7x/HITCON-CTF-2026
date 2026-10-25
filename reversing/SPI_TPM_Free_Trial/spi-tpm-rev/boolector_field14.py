#!/usr/bin/env python3
import sys, os, time, random, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field14_solve import make_samples, P, coeffs
import pyboolector

W = 512  # working width (power of 2 for Boolector shifts)

def bv_const(btor, v, w=W):
    return btor.Const(v, w)

def zext(btor, node, w=W):
    cur = node.width
    if cur == w:
        return node
    return btor.Uext(node, w - cur)

def reduce_mod_p(btor, V):
    # V width W, reduce mod 2^127-1
    p = bv_const(btor, P)
    # fold 3 times; W=384 -> after 3 folds small
    for _ in range(3):
        V = (V & p) + (V >> 127)
    # V < p + 2^3; conditionally subtract p
    return btor.Cond(btor.Ugte(V, p), V - p, V)

def solve(samples, timeout_s=300, engine=1):
    btor = pyboolector.Boolector()
    btor.Set_opt(0, 1)   # model-gen
    btor.Set_opt(14, 3)  # rewrite-level
    btor.Set_opt(7, engine)  # sat-engine: 0=CMS, 1=CaDiCaL, 2=Lingeling, 3=PicoSAT, 4=MiniSAT
    x = btor.Var(btor.BitVecSort(64), 'x')
    y = btor.Var(btor.BitVecSort(64), 'y')
    xy = btor.Mul(zext(btor, x), zext(btor, y))  # 384-bit exact product
    for smp in samples:
        a, b, c, leak = smp['a'], smp['b'], smp['c'], smp['leak']
        ay = btor.Mul(bv_const(btor, a), zext(btor, y))
        bx = btor.Mul(bv_const(btor, b), zext(btor, x))
        cz = btor.Mul(bv_const(btor, c), xy)
        V = ay + bx + cz
        ACC = reduce_mod_p(btor, V)
        btor.Assert(btor.Eq(ACC >> 118, bv_const(btor, leak)))
    t0 = time.time()
    res = btor.Sat()
    dt = time.time() - t0
    print(f'boolector: res={res} time={dt:.2f}s', flush=True)
    if res == pyboolector.BTOR_RESULT_SAT:
        xv = int(x.assignment, 2)
        yv = int(y.assignment, 2)
        print('  found x,y =', hex(xv), hex(yv))
        return xv, yv
    return None

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    rng = random.Random(42)
    key16 = bytes(rng.getrandbits(8) for _ in range(16))
    samples = make_samples(key16, n)
    kx, ky = struct.unpack('<QQ', key16)
    print('key', key16.hex(), 'n', n, 'actual', hex(kx), hex(ky), flush=True)
    res = solve(samples, timeout)
    if res:
        print('match', res == (kx, ky))
