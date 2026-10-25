#!/usr/bin/env python3
"""Recover the 16-byte cipher key from field14 leak samples.

Model (verified against libspi_tpm_firmware.so 0x3850):
  ACC_i = a_i*x + b_i*y + c_i*x*y  (mod p), p = 2^127-1
  field14_i = splitmix64(nonce_i ^ TAG_RT) ^ (ACC_i >> 118)
where x = key[0:8], y = key[8:16] little-endian, and
  a_i = h_b(nonce_i), b_i = h_a(nonce_i), c_i = h_c(nonce_i)
are 128-bit values from 0x32f0(nonce, "!?-nilib").
"""
import ctypes, struct, random, sys, os, time

LIB = '/home/sh4d0w/HitconCTF/reversing/SPI_TPM_Free_Trial/spi-tpm-rev/src/libspi_tpm_firmware.so'
lib = ctypes.CDLL(LIB)
getapi = lib.spi_tpm_fw_get_api_v1
getapi.argtypes = [ctypes.c_uint32]
getapi.restype = ctypes.POINTER(ctypes.c_uint64)
api = getapi(1)
base = ctypes.cast(api, ctypes.c_void_p).value - 0x5d20
shim = ctypes.CDLL('/tmp/opencode/shim.so')

class U128(ctypes.Structure):
    _fields_ = [('lo', ctypes.c_uint64), ('hi', ctypes.c_uint64)]

shim.call32f0.argtypes = [ctypes.c_uint64, ctypes.c_uint32, ctypes.c_uint64]
shim.call32f0.restype = U128
f3850 = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint64)(base + 0x3850)

P = (1 << 127) - 1
M64 = (1 << 64) - 1
TAG_A = 0x62696c696e2d6121
TAG_B = 0x62696c696e2d6221
TAG_C = 0x62696c696e2d6321
TAG_RT = 0x62696c696e2d7274

def h(nonce, tag):
    r = shim.call32f0(base + 0x32f0, nonce, tag)
    return r.lo, r.hi

def h128(nonce, tag):
    lo, hi = h(nonce, tag)
    return lo | (hi << 64)

def splitmix(x):
    x = (x + 0x9e3779b97f4a7c15) & M64
    x = ((x ^ (x >> 30)) * 0xbf58476d1ce4e5b9) & M64
    x = ((x ^ (x >> 27)) * 0x94d049bb133111eb) & M64
    return x ^ (x >> 31)

def coeffs(nonce):
    return h128(nonce, TAG_B) % P, h128(nonce, TAG_A) % P, h128(nonce, TAG_C) % P

def field14_model(key16, nonce):
    x, y = struct.unpack('<QQ', key16)
    a, b, c = coeffs(nonce)
    # a = h_b multiplies y; b = h_a multiplies x; c = h_c multiplies x*y
    acc = (a * y + b * x + c * x * y) % P
    leak = acc >> 118
    return (splitmix(nonce ^ TAG_RT) & 0xffffffff) ^ leak, leak

def field14_real(key16, nonce):
    buf = ctypes.create_string_buffer(key16, 16)
    return f3850(buf, nonce, 0)

def make_samples(key16, n, seed=1234):
    rng = random.Random(seed)
    samples = []
    for _ in range(n):
        nonce = rng.getrandbits(32)
        f, leak = field14_model(key16, nonce)
        assert field14_real(key16, nonce) == f
        a, b, c = coeffs(nonce)
        samples.append(dict(nonce=nonce, a=a, b=b, c=c, leak=leak, field14=f))
    return samples

# ---------------- Z3 model ----------------

def z3_solve(key16, samples, timeout_ms=300000, width=320):
    import z3
    x = z3.BitVec('x', 64)
    y = z3.BitVec('y', 64)
    z = z3.ZeroExt(64, x) * z3.ZeroExt(64, y)  # 128-bit exact product
    s = z3.Solver()
    s.set('timeout', timeout_ms)
    pw = z3.BitVecVal(P, width)
    mask = z3.BitVecVal(P, width)
    for smp in samples:
        a, b, c, leak = smp['a'], smp['b'], smp['c'], smp['leak']
        ay = z3.ZeroExt(width - 64, y) * z3.BitVecVal(a, width)
        bx = z3.ZeroExt(width - 64, x) * z3.BitVecVal(b, width)
        cz = z3.ZeroExt(width - 128, z) * z3.BitVecVal(c, width)
        V = ay + bx + cz
        # fold mod 2^127-1
        V = (V & mask) + z3.LShR(V, 127)
        V = (V & mask) + z3.LShR(V, 127)
        V = (V & mask) + z3.LShR(V, 127)
        V = z3.If(z3.UGE(V, pw), V - pw, V)
        s.add(z3.LShR(V, 118) == z3.BitVecVal(leak, width))
    t0 = time.time()
    res = s.check()
    dt = time.time() - t0
    print(f'z3: res={res} time={dt:.2f}s', flush=True)
    if res == z3.sat:
        m = s.model()
        xv = m[x].as_long()
        yv = m[y].as_long()
        print('  found x,y =', hex(xv), hex(yv))
        kx, ky = struct.unpack('<QQ', key16)
        print('  actual   =', hex(kx), hex(ky), 'match', (xv, yv) == (kx, ky))
        return xv, yv
    return None

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'test'
    if mode == 'test':
        rng = random.Random(42)
        key16 = bytes(rng.getrandbits(8) for _ in range(16))
        # use a plausible key: random 16 bytes
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 300000
        samples = make_samples(key16, n)
        print('key', key16.hex(), 'samples', n)
        for smp in samples[:3]:
            print(' nonce', hex(smp['nonce']), 'leak', hex(smp['leak']), 'field14', hex(smp['field14']))
        z3_solve(key16, samples, timeout)
