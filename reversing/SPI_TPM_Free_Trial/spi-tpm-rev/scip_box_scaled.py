#!/usr/bin/env python3
"""SCIP model over LLL coefficient variables, scaled box constraints."""
import sys, os, time, random, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field14_solve import make_samples, P
from field14_cvp_sample import WXY, B
from field14_box_search import prepare, box_variants
from field14_box_enum import lll_basis
from pyscipopt import Model, quicksum

def solve(samples, lo, hi, timeout=120):
    Bm, clo, chi, lo, hi, _, _ = prepare(samples, lo, hi, 'default')
    n = len(Bm)
    m = Model()
    m.hideOutput()
    m.setRealParam('numerics/infinity', 1e50)
    m.setRealParam('limits/time', timeout)
    c = [m.addVar(f'c{i}', vtype='I', lb=clo[i], ub=chi[i]) for i in range(n)]
    for k in range(n):
        s = max(abs(Bm[i][k]) for i in range(n))
        if s == 0:
            continue
        expr = quicksum(c[i] * (Bm[i][k]/s) for i in range(n))
        m.addCons(expr >= lo[k]/s)
        m.addCons(expr <= hi[k]/s)
    t0 = time.time()
    try:
        m.optimize()
    except Exception as e:
        print('EXC', str(e)[:80], 'status', m.getStatus(), flush=True)
    dt = time.time()-t0
    if m.getNSols() > 0:
        sol = m.getBestSol()
        cv = [int(round(m.getSolVal(sol, c[i]))) for i in range(n)]
        v = [sum(cv[i]*Bm[i][k] for i in range(n)) for k in range(n)]
        x = v[0]//WXY; y = v[1]//WXY
        ok = all(lo[k] <= v[k] <= hi[k] for k in range(n))
        print('SAT', hex(x), hex(y), 'boxok', ok, 'time', round(dt,2), flush=True)
        return x, y, cv, Bm, clo
    else:
        print('NOSOL', m.getStatus(), 'time', round(dt,2), flush=True)
        return None

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv)>1 else 27
    seed = int(sys.argv[2]) if len(sys.argv)>2 else 42
    timeout = int(sys.argv[3]) if len(sys.argv)>3 else 120
    rng = random.Random(seed)
    key16 = bytes(rng.getrandbits(8) for _ in range(16))
    kx, ky = struct.unpack('<QQ', key16)
    samples = make_samples(key16, n, seed=seed)
    print('actual', hex(kx), hex(ky), flush=True)
    L, D = lll_basis(samples)
    variants = box_variants(D)
    for vi, (lo, hi) in enumerate(variants):
        print('variant', vi, flush=True)
        res = solve(samples, lo, hi, timeout)
        if res is not None:
            x, y, cv, Bm, clo = res
            print('match', (x,y)==(kx,ky), flush=True)
            break
