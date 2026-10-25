import json, os, sys, time
import pyboolector as p

C1 = 0xd6e8feb86659fd93
C2 = 0xa5a3564e27f8862f
TAG = 0x62696c696e2d7221
GAMMA = 0x9e3779b97f4a7c15
M1 = 0xbf58476d1ce4e5b9
M2 = 0x94d049bb133111eb

btor = p.Boolector()
btor.Set_opt(p.BtorOption.BTOR_OPT_MODEL_GEN, 1)
# btor.Set_opt(p.BtorOption.BTOR_OPT_SAT_ENGINE, p.BtorOptSatEngine.BTOR_OPT_SAT_ENGINE_CADICAL)
# btor.Set_opt(p.BtorOption.BTOR_OPT_ENGINE, p.BtorOptEngine.BTOR_OPT_ENGINE_SMT)


def C(v, w):
    return btor.Const(v, w)


def fmix_nf(x):
    x = btor.Xor(x, btor.Srl(x, C(30, 64)))
    x = btor.Mul(x, C(M1, 64))
    x = btor.Xor(x, btor.Srl(x, C(27, 64)))
    x = btor.Mul(x, C(M2, 64))
    return x


def fmix_full(x):
    x = fmix_nf(x)
    x = btor.Xor(x, btor.Srl(x, C(31, 64)))
    return x


def f33(acc, rnd, A, B):
    x = btor.Uext(acc, 48)
    t = btor.Xor(A, btor.Mul(x, C(C1, 64)))
    t = btor.Xor(t, C((rnd * C2) & ((1 << 64) - 1), 64))
    t = btor.Xor(t, C(TAG, 64))
    t = btor.Add(t, C(GAMMA, 64))
    Y = fmix_nf(t)
    u = btor.Xor(B, btor.Xor(Y, btor.Srl(Y, C(31, 64))))
    v = fmix_full(btor.Add(u, C(GAMMA, 64)))
    fold = btor.Xor(btor.Srl(v, C(16, 64)), btor.Xor(btor.Srl(v, C(32, 64)), btor.Xor(v, btor.Srl(v, C(48, 64)))))
    return btor.Slice(fold, 15, 0)


def g(a, cost, A, B):
    s = C(a, 32)
    for i in range(cost):
        hi = btor.Slice(s, 31, 16)
        x = f33(hi, i, A, B)
        x32 = btor.Uext(x, 16)
        s = btor.Xor(btor.Sll(btor.Xor(x32, s), C(16, 32)), btor.Uext(hi, 16))
    return s


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    here = os.path.dirname(os.path.abspath(__file__))
    data = json.load(open(os.path.join(here, 'g_sample.json')))
    cost = data['cost']
    pairs = data['pairs'][:N]
    s64 = btor.BitVecSort(64)
    A = btor.Var(s64, 'A')
    B = btor.Var(s64, 'B')
    for a, b in pairs:
        btor.Assert(btor.Eq(g(a, cost, A, B), C(b, 32)))
    t0 = time.time()
    res = btor.Sat()
    dt = time.time() - t0
    sat = p.BtorSolverResult.BTOR_RESULT_SAT
    print(f'N={N} res={res} sat={res == sat} time={dt:.2f}s', flush=True)
    if res == sat:
        av = int(A.assignment, 2)
        bv = int(B.assignment, 2)
        print('A,B =', hex(av), hex(bv), flush=True)
        k0, k1 = data['k0'], data['k1']
        MASK64 = (1 << 64) - 1
        rol = lambda x, n: ((x << n) | (x >> (64 - n))) & MASK64
        a0 = rol(k1, 17) ^ k0
        b0 = rol(k0, 29) ^ k1
        print('actual =', hex(a0), hex(b0), 'match', (a0, b0) == (av, bv), flush=True)


if __name__ == '__main__':
    main()
