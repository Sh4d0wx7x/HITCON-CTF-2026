import ctypes, struct, sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cipher_model import f17e0, f3700

LIB = '/home/sh4d0w/HitconCTF/reversing/SPI_TPM_Free_Trial/spi-tpm-rev/src/libspi_tpm_firmware.so'
lib = ctypes.CDLL(LIB)
getapi = lib.spi_tpm_fw_get_api_v1
getapi.argtypes = [ctypes.c_uint32]
getapi.restype = ctypes.POINTER(ctypes.c_uint64)
api = getapi(1)
create = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p))(api[3])
feed = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_uint8)(api[6])

st = ctypes.c_void_p()
assert create(None, ctypes.byref(st)) == 0

def put(off, data):
    ctypes.memmove(st.value + off, data, len(data))

def get(off, n):
    return ctypes.string_at(st.value + off, n)

def frame(op, payload=b'', key=0, cost=0, transfer_len=0x2004):
    ln = len(payload)
    hdr = struct.pack('<BBHIII', 0xa5, op, ln, key, cost, transfer_len)
    raw = hdr + payload
    raw = raw + b'\x00' * (transfer_len - len(raw))
    put(0x2420, struct.pack('<I', 0))
    put(0x2424, struct.pack('<I', 0x10))
    put(0x2428, struct.pack('<I', 0x10))
    put(0x242c, struct.pack('<I', 0x10))
    put(0x2430, struct.pack('<I', 0))
    put(0x2434, struct.pack('<I', 0))
    for b in raw:
        feed(st, b)

def response():
    hdr = get(0x1010, 8)
    a5, op, ln, status = struct.unpack_from('<BBHI', hdr, 0)
    return dict(a5=a5, op=op, ln=ln, status=status, payload=get(0x1018, ln))

# genkey
frame(1, b'')
r = response()
assert r['a5'] == 0xa5 and r['status'] == 0, r
kid = struct.unpack_from('<I', r['payload'], 0)[0]
s = ctypes.string_at(st.value, 0x24b0)
slot = None
for i in range(8):
    off = 0x2020 + i * 0x80
    sl = s[off:off+0x80]
    if sl[0x70] and struct.unpack_from('<I', sl, 0)[0] == kid:
        slot = sl
        break
assert slot is not None
key48 = slot[0x10:0x50]
k0, k1 = struct.unpack_from('<QQ', key48, 0)
print('key id', kid, 'k0', hex(k0), 'k1', hex(k1))

# encrypt 1024 zero bytes at cost 3
pt = b'\x00' * 1024
cost = 3
frame(2, pt, key=kid, cost=cost)
r = response()
assert r['a5'] == 0xa5 and r['status'] == 0, r
blob = r['payload']
assert blob[:4] == b'STP1' and blob[4:6] == b'\x02\x00' and blob[6:8] == b'\x28\x00'
nonce, = struct.unpack_from('<I', blob, 8)
bcost, = struct.unpack_from('<I', blob, 12)
ln, = struct.unpack_from('<I', blob, 16)
ct = blob[0x28:0x28 + ((ln + 3) & ~3)]
print('nonce', hex(nonce), 'cost', bcost, 'len', ln, 'ctlen', len(ct))

pairs = []
for i in range(0, (ln + 3) & ~3, 4):
    cw, = struct.unpack_from('<I', ct, i)
    a = f17e0(0, nonce, i // 4, cost, 0, 0)
    b = f17e0(cw, nonce, i // 4, cost, 1, 1)
    # verify with the known key
    b2 = f3700(key48, a, cost, 0)
    if b != b2:
        print('MISMATCH', i // 4, hex(a), hex(b), hex(b2))
        break
    pairs.append((a, b))
else:
    print('all pairs verified; count', len(pairs))
    out = dict(key48=key48.hex(), k0=k0, k1=k1, nonce=nonce, cost=cost, pairs=pairs)
    outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'g_sample.json')
    with open(outpath, 'w') as f:
        json.dump(out, f)
    print('saved', outpath)
    for i, (a, b) in enumerate(pairs[:4]):
        print(i, hex(a), '->', hex(b))
