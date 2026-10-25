#!/usr/bin/env python3
"""SCIP MINLP model of full field14 leaks with z=x*y."""
import sys, os, time, random, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field14_solve import make_samples, P
from pyscipopt import Model

B = 1 << 118
KMAX = 1 << 120

def solve(samples, timeout=300):
    n = len(samples)
    m = Model()
    m.hideOutput()
    m.setRealParam('numerics/infinity', 1e50)
    m.setRealParam('limits/time', timeout)
    x = m.addVar('x', vtype='I', lb=0, ub=(1<<64)-1)
    y = m.addVar('y', vtype='I', lb=0, ub=(1<<64)-1)
    z = m.addVar('z', vtype='I', lb=0, ub=P-1)
    m.addCons(z == x*y)
    for i, s in enumerate(samples):
        r = m.addVar(f'r{i}', vtype='I', lb=0, ub=B-1)
        k = m.addVar(f'k{i}', vtype='I', lb=0, ub=KMAX)
        m.addCons(s['a']*y + s['b']*x + s['c']*z - r - P*k == (s['leak'] << 118))
    t0 = time.time()
    try:
        m.optimize()
    except Exception as e:
        print('EXC', str(e)[:100], 'status', m.getStatus(), 'nsols', m.getNSols(), flush=True)
    dt = time.time()-t0
    if m.getNSols() > 0:
        sol = m.getBestSol()
        xv = int(round(m.getSolVal(sol, x)))
        yv = int(round(m.getSolVal(sol, y)))
        print('SAT', hex(xv), hex(yv), 'time', round(dt,2), flush=True)
        return xv, yv
    else:
        print('NOSOL status', m.getStatus(), 'time', round(dt,2), flush=True)
        return None

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv)>1 else 5
    seed = int(sys.argv[2]) if len(sys.argv)>2 else 42
    timeout = int(sys.argv[3]) if len(sys.argv)>3 else 300
    rng = random.Random(seed)
    key16 = bytes(rng.getrandbits(8) for _ in range(16))
    kx, ky = struct.unpack('<QQ', key16)
    print('actual', hex(kx), hex(ky), 'n', n, flush=True)
    samples = make_samples(key16, n, seed=seed)
    solve(samples, timeout)
