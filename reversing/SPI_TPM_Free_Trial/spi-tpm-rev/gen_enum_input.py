#!/usr/bin/env python3
"""Generate enum_input.txt for the C++ box enumerator."""
import sys, os, random, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field14_solve import make_samples, P
from field14_cvp_sample import WXY, B
from field14_box_search import prepare, box_variants
from field14_box_enum import lll_basis

def s256_bytes(v):
    # return 4 big-endian 64-bit limbs (limb3..limb0), signed two's complement
    v &= (1<<256)-1
    return [ (v >> (192-64*i)) & ((1<<64)-1) for i in range(4) ]

def main(n=27, seed=42, variant=0, out='enum_input.txt'):
    rng = random.Random(seed)
    key16 = bytes(rng.getrandbits(8) for _ in range(16))
    kx, ky = struct.unpack('<QQ', key16)
    samples = make_samples(key16, n, seed=seed)
    L, D = lll_basis(samples)
    lo, hi = box_variants(D)[variant]
    Bm, clo, chi, lo, hi, _, _ = prepare(samples, lo, hi, 'default')
    N = len(Bm)
    with open(out, 'w') as f:
        f.write(f'{N}\n')
        for i in range(N):
            f.write(' '.join(str(x) for x in s256_bytes(Bm[i][j]) for j in [] ) if False else '')
        # proper emission
        f.truncate(0)
        f.write(f'{N}\n')
        for i in range(N):
            parts=[]
            for j in range(N):
                parts += [str(x) for x in s256_bytes(Bm[i][j])]
            f.write(' '.join(parts)+'\n')
        for k in range(N):
            f.write(' '.join(str(x) for x in s256_bytes(lo[k]))+'\n')
        for k in range(N):
            f.write(' '.join(str(x) for x in s256_bytes(hi[k]))+'\n')
        for i in range(N):
            f.write(f'{clo[i]} {chi[i]}\n')
    print('wrote', out, 'n', N, 'variant', variant, flush=True)

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv)>1 else 27
    seed = int(sys.argv[2]) if len(sys.argv)>2 else 42
    variant = int(sys.argv[3]) if len(sys.argv)>3 else 0
    main(n, seed, variant)
