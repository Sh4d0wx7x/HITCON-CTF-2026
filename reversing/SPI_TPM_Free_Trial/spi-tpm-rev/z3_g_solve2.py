import z3, json, time, sys, os
C1 = 0xd6e8feb86659fd93
C2 = 0xa5a3564e27f8862f
TAG = 0x62696c696e2d7221
GAMMA = 0x9e3779b97f4a7c15
M1 = 0xbf58476d1ce4e5b9
M2 = 0x94d049bb133111eb
MASK64 = (1 << 64) - 1

def fmix_nf(x):
    x ^= z3.LShR(x, 30); x = x * M1
    x ^= z3.LShR(x, 27); x = x * M2
    return x

def fmix_full(x):
    x = fmix_nf(x)
    x ^= z3.LShR(x, 31)
    return x

def f33_z3(acc, rnd, A, B):
    if isinstance(acc, int):
        x = z3.ZeroExt(48, z3.BitVecVal(acc, 16))
    else:
        x = z3.ZeroExt(48, acc)
    t = A ^ (x * z3.BitVecVal(C1, 64)) ^ (z3.BitVecVal(rnd, 64) * z3.BitVecVal(C2, 64)) ^ z3.BitVecVal(TAG, 64)
    t = t + z3.BitVecVal(GAMMA, 64)
    Y = fmix_nf(t)
    u = B ^ Y ^ z3.LShR(Y, 31)
    v = fmix_full(u + z3.BitVecVal(GAMMA, 64))
    fold = z3.LShR(v, 16) ^ z3.LShR(v, 32) ^ v ^ z3.LShR(v, 48)
    return z3.Extract(15, 0, fold)

def g_z3(a, cost, A, B):
    s = z3.BitVecVal(a, 32)
    for i in range(cost):
        hi = z3.Extract(31, 16, s)
        x = f33_z3(hi, i, A, B)
        x32 = z3.ZeroExt(16, x)
        s = ((x32 ^ s) << 16) | z3.ZeroExt(16, hi)
    return s

def solve(N, timeout_ms, tactic):
    data = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'g_sample.json')))
    cost = data['cost']
    pairs = data['pairs'][:N]
    A = z3.BitVec('A', 64)
    B = z3.BitVec('B', 64)
    if tactic == 'default':
        s = z3.SolverFor('QF_BV')
    else:
        s = z3.Then('simplify', 'bit-blast', tactic).solver()
    s.set('timeout', timeout_ms)
    for a, b in pairs:
        s.add(g_z3(a, cost, A, B) == z3.BitVecVal(b, 32))
    t0 = time.time()
    res = s.check()
    dt = time.time() - t0
    print(f'N={N} tactic={tactic} res={res} time={dt:.2f}s', flush=True)
    if res == z3.sat:
        m = s.model()
        av = m[A].as_long(); bv = m[B].as_long()
        print('  A,B =', hex(av), hex(bv), flush=True)
        k0, k1 = data['k0'], data['k1']
        rol = lambda x, n: ((x << n) | (x >> (64 - n))) & MASK64
        a0 = rol(k1, 17) ^ k0
        b0 = rol(k0, 29) ^ k1
        print('  actual =', hex(a0), hex(b0), 'match', (a0, b0) == (av, bv), flush=True)
        return av, bv
    return None

if __name__ == '__main__':
    tactic = sys.argv[1] if len(sys.argv) > 1 else 'sat'
    ns = [int(x) for x in sys.argv[2:]] or [1, 2, 4]
    for n in ns:
        solve(n, 120000, tactic)
