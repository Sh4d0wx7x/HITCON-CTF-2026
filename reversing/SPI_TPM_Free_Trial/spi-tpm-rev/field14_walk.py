#!/usr/bin/env python3
"""Connected-component walk over field14 linear solutions."""
import sys, os, time, random, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field14_solve import make_samples, P
from field14_cvp_sample import build, WXY, B
from field14_box_search import prepare, box_variants
from field14_box_enum import lll_basis

def check(x, y, samples):
    z = (x*y) % P
    return all((((s['a']*y + s['b']*x + s['c']*z) % P) >> 118) == s['leak'] for s in samples)

def in_box(v, lo, hi, n):
    return all(lo[k] <= v[k] <= hi[k] for k in range(n))

def xy_of(v):
    if v[0] % WXY or v[1] % WXY:
        return None
    x = v[0]//WXY; y = v[1]//WXY
    if 0 <= x < (1<<64) and 0 <= y < (1<<64):
        return x, y
    return None

def walk(samples, D, variant_idx, start, max_pop=200000):
    lo, hi = box_variants(D)[variant_idx]
    Bm, clo, chi, lo, hi, _, _ = prepare(samples, lo, hi, 'default')
    n = len(Bm)
    steps = []
    for i in range(n):
        for s in (1, -1):
            steps.append(tuple(s*Bm[i][k] for k in range(n)))
    start = tuple(start)
    seen = {start}
    pop = [start]
    truelist = []
    t0 = time.time()
    while pop:
        v = pop.pop()
        xy = xy_of(v)
        if xy and check(*xy, samples):
            truelist.append(xy)
            print('TRUE', hex(xy[0]), hex(xy[1]), 'queue', len(pop), 'seen', len(seen), 't', round(time.time()-t0,2), flush=True)
        for st in steps:
            w = tuple(v[k]+st[k] for k in range(n))
            if w not in seen and in_box(w, lo, hi, n):
                seen.add(w)
                pop.append(w)
                if len(seen) > max_pop:
                    print('maxpop', len(seen), flush=True)
                    return seen, truelist
    return seen, truelist

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv)>1 else 27
    seed = int(sys.argv[2]) if len(sys.argv)>2 else 42
    rng = random.Random(seed)
    key16 = bytes(rng.getrandbits(8) for _ in range(16))
    kx, ky = struct.unpack('<QQ', key16)
    samples = make_samples(key16, n, seed=seed)
    print('actual', hex(kx), hex(ky), flush=True)
    L, D = lll_basis(samples)
    # true-key lattice vector as start (sanity check of connectivity)
    a=[s['a'] for s in samples]; b=[s['b'] for s in samples]; c=[s['c'] for s in samples]
    T=[s['leak']<<118 for s in samples]
    c0inv=pow(c[0],-1,P); A=[];Bv=[];C=[];D2=[]
    for i in range(1,n):
        ci_c0=(c[i]*c0inv)%P
        A.append((b[i]-ci_c0*b[0])%P); Bv.append((a[i]-ci_c0*a[0])%P); C.append(ci_c0); D2.append((T[i]-ci_c0*T[0])%P)
    def acc(i): return (a[i]*ky+b[i]*kx+c[i]*kx*ky)%P
    r0=acc(0)&(B-1)
    u=[(A[i]*kx+Bv[i]*ky+C[i]*r0)%P for i in range(len(A))]
    vtrue=[kx*WXY,ky*WXY,r0]+u
    vs=box_variants(D2)
    vi_true=None
    for i,(lo,hi) in enumerate(vs):
        if all(lo[k]<=vtrue[k]<=hi[k] for k in range(len(vtrue))):
            vi_true=i
    print('true variant', vi_true, flush=True)
    from fpylll import CVP
    target=list(vtrue)
    for i in range(len(target)):
        pass
    # CVP start from true target: returns vtrue (still valid)
    start=vtrue
    seen, truelist = walk(samples, D2, vi_true, start, max_pop=4000)
    print('component size', len(seen), 'true found', len(truelist), flush=True)
