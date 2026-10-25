#!/usr/bin/env python3
"""SCIP model of the linearized field14 system, enumerate candidates."""
import sys, os, time, random, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field14_solve import make_samples, P
from pyscipopt import Model

B = 1 << 118
KMAX = 1 << 120

def build(samples):
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
    m = Model()
    m.hideOutput()
    m.setRealParam('numerics/infinity', 1e50)
    x = m.addVar('x', vtype='I', lb=0, ub=(1<<64)-1)
    y = m.addVar('y', vtype='I', lb=0, ub=(1<<64)-1)
    r0 = m.addVar('r0', vtype='I', lb=0, ub=B-1)
    rvars = []; kvars = []
    for j in range(n-1):
        r = m.addVar(f'r{j+1}', vtype='I', lb=0, ub=B-1)
        k = m.addVar(f'k{j+1}', vtype='I', lb=0, ub=KMAX)
        rvars.append(r); kvars.append(k)
        m.addCons(A[j]*x + Bv[j]*y + C[j]*r0 - r - P*k == D[j])
    return m, x, y, r0, rvars

def check_key(x, y, samples):
    z = (x * y) % P
    return all((((s['a']*y + s['b']*x + s['c']*z) % P) >> 118) == s['leak'] for s in samples)

def run(n, seed, limit, timeout):
    rng = random.Random(seed)
    key16 = bytes(rng.getrandbits(8) for _ in range(16))
    kx, ky = struct.unpack('<QQ', key16)
    samples = make_samples(key16, n, seed=seed)
    print('actual', hex(kx), hex(ky), 'n', n, flush=True)
    m, x, y, r0, rvars = build(samples)
    m.setRealParam('limits/time', timeout)
    t0 = time.time()
    for it in range(limit):
        m.optimize()
        if m.getNSols() == 0:
            print('nosol', it, m.getStatus(), flush=True)
            break
        sol = m.getBestSol()
        xv = int(round(m.getSolVal(sol, x)))
        yv = int(round(m.getSolVal(sol, y)))
        ok = check_key(xv, yv, samples)
        print('sol', it, hex(xv), hex(yv), 'TRUE' if ok else '', 't', round(time.time()-t0,2), flush=True)
        if ok:
            return xv, yv
        return xv, yv
    return None

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv)>1 else 27
    seed = int(sys.argv[2]) if len(sys.argv)>2 else 42
    limit = int(sys.argv[3]) if len(sys.argv)>3 else 20
    timeout = int(sys.argv[4]) if len(sys.argv)>4 else 300
    run(n, seed, limit, timeout)
