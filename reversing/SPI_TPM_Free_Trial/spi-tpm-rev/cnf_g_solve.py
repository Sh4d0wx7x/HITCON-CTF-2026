import z3, json, time, sys, os
from pysat.solvers import Solver

C1 = 0xd6e8feb86659fd93
C2 = 0xa5a3564e27f8862f
TAG = 0x62696c696e2d7221
GAMMA = 0x9e3779b97f4a7c15
M1 = 0xbf58476d1ce4e5b9
M2 = 0x94d049bb133111eb


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


def lit_key(lit):
    if z3.is_not(lit):
        return lit.arg(0), True
    return lit, False


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    timeout_ms = int(sys.argv[2]) if len(sys.argv) > 2 else 300000
    here = os.path.dirname(os.path.abspath(__file__))
    data = json.load(open(os.path.join(here, 'g_sample.json')))
    cost = data['cost']
    pairs = data['pairs'][:N]
    A = z3.BitVec('A', 64)
    B = z3.BitVec('B', 64)
    a_bits = [z3.Bool(f'a{i}') for i in range(64)]
    b_bits = [z3.Bool(f'b{i}') for i in range(64)]
    g = z3.Goal()
    for a, b in pairs:
        g.add(g_z3(a, cost, A, B) == z3.BitVecVal(b, 32))
    for i in range(64):
        g.add(a_bits[i] == (z3.Extract(i, i, A) == z3.BitVecVal(1, 1)))
        g.add(b_bits[i] == (z3.Extract(i, i, B) == z3.BitVecVal(1, 1)))
    t0 = time.time()
    cnf = z3.Then('simplify', 'bit-blast', 'tseitin-cnf')(g)
    print(f'N={N} bitblast+cnf time={time.time()-t0:.1f}s goals={len(cnf)}', flush=True)
    sub = cnf[0]
    print('num clauses', len(sub), flush=True)
    var_ids = {}
    clauses = []
    next_id = 1
    def vid(ast):
        nonlocal next_id
        k = ast.get_id()
        if k not in var_ids:
            var_ids[k] = next_id
            next_id += 1
        return var_ids[k]
    def add_lit(lit):
        if z3.is_true(lit):
            return None
        if z3.is_false(lit):
            return 0
        var, neg = lit_key(lit)
        x = vid(var)
        return -x if neg else x
    nskip = 0
    for f in sub:
        if z3.is_or(f):
            lits = []
            sat = False
            for lit in f.children():
                x = add_lit(lit)
                if x is None:
                    sat = True; break
                if x != 0:
                    lits.append(x)
            if sat:
                nskip += 1
            elif lits:
                clauses.append(lits)
        elif z3.is_true(f):
            nskip += 1
        elif z3.is_false(f):
            clauses.append([])
        else:
            x = add_lit(f)
            if x is not None and x != 0:
                clauses.append([x])
    print(f'vars={next_id-1} clauses={len(clauses)} skipped={nskip}', flush=True)
    # markers
    amark = [vid(a_bits[i]) for i in range(64)]
    bmark = [vid(b_bits[i]) for i in range(64)]
    t1 = time.time()
    sol = Solver(name='cadical153', bootstrap_with=clauses)
    res = sol.solve()
    print(f'solve res={res} time={time.time()-t1:.1f}s', flush=True)
    if res:
        m = sol.get_model()
        mv = set(x for x in m if x > 0)
        av = sum((1 << i) for i in range(64) if amark[i] in mv)
        bv = sum((1 << i) for i in range(64) if bmark[i] in mv)
        print('A,B =', hex(av), hex(bv), flush=True)
        k0, k1 = data['k0'], data['k1']
        MASK64 = (1 << 64) - 1
        rol = lambda x, n: ((x << n) | (x >> (64 - n))) & MASK64
        a0 = rol(k1, 17) ^ k0
        b0 = rol(k0, 29) ^ k1
        print('actual =', hex(a0), hex(b0), 'match', (a0, b0) == (av, bv), flush=True)
    sol.delete()


if __name__ == '__main__':
    main()
