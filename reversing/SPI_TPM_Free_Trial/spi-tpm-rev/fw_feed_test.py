import ctypes, struct, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cipher_model import f17e0, f3700

LIB = '/home/sh4d0w/HitconCTF/reversing/SPI_TPM_Free_Trial/spi-tpm-rev/src/libspi_tpm_firmware.so'
lib = ctypes.CDLL(LIB)
getapi = lib.spi_tpm_fw_get_api_v1
getapi.argtypes = [ctypes.c_uint32]
getapi.restype = ctypes.POINTER(ctypes.c_uint64)
api = getapi(1)
base = ctypes.cast(api, ctypes.c_void_p).value - 0x5d20
create = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p))(api[3])
destroy = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(api[4])
feed = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_uint8)(api[6])
geterr = ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.c_void_p)(api[10])

st = ctypes.c_void_p()
print('create', create(None, ctypes.byref(st)), hex(st.value))

def state_bytes():
    return ctypes.string_at(st.value, 0x24b0)

def put(off, data):
    ctypes.memmove(st.value + off, data, len(data))

def get(off, n):
    return ctypes.string_at(st.value + off, n)

def frame(op, payload=b'', key=0, cost=0, transfer_len=0x2004):
    ln = len(payload)
    hdr = struct.pack('<BBHIII', 0xa5, op, ln, key, cost, transfer_len)
    assert len(hdr) == 16
    raw = hdr + payload
    raw = raw + b'\x00' * (transfer_len - len(raw))
    # reset the SPI state fields to the create defaults
    put(0x2420, struct.pack('<I', 0))       # cursor
    put(0x2424, struct.pack('<I', 0x10))    # limit
    put(0x2428, struct.pack('<I', 0x10))    # request total
    put(0x242c, struct.pack('<I', 0x10))    # response start
    put(0x2430, struct.pack('<I', 0))       # response length
    put(0x2434, struct.pack('<I', 0))       # transfer limit
    rets = bytearray()
    for b in raw:
        r = feed(st, b)
        rets.append(r & 0xff)
    return bytes(rets)

def response():
    hdr = get(0x1010, 8)
    a5, op, ln, status = struct.unpack_from('<BBHI', hdr, 0)
    payload = get(0x1018, ln)
    return dict(a5=a5, op=op, ln=ln, status=status, payload=payload,
                cursor=struct.unpack_from('<I', get(0x2420, 4))[0],
                limit=struct.unpack_from('<I', get(0x2424, 4))[0],
                resp_len=struct.unpack_from('<I', get(0x2430, 4))[0])

# genkey
rets = frame(1, b'')
r = response()
print('genkey response', {k: (v.hex() if isinstance(v, bytes) else v) for k, v in r.items()})
s = state_bytes()
slots = []
for i in range(8):
    off = 0x2020 + i * 0x80
    slot = s[off:off+0x80]
    valid = slot[0x70]
    kid = struct.unpack_from('<I', slot, 0)[0]
    print(f'slot{i}: valid={valid:02x} kid={kid} key16={slot[0x10:0x20].hex()}')
    if valid:
        slots.append((i, kid, slot[0x10:0x50]))
if not slots:
    print('no valid slot'); sys.exit(1)
idx, kid, key48 = slots[0]
print('using slot', idx, 'kid', kid, 'key48', key48.hex())

# encrypt 16 zero bytes, cost 3
pt = b'\x00' * 16
rets = frame(2, pt, key=kid, cost=3)
r = response()
print('encrypt response', {k: (v.hex() if isinstance(v, bytes) else v) for k, v in r.items()})
blob = r['payload']
print('blob len', len(blob), 'magic', blob[:4], 'op/hdr', blob[4:8].hex())
if len(blob) >= 0x28:
    nonce, = struct.unpack_from('<I', blob, 8)
    cost, = struct.unpack_from('<I', blob, 12)
    ln, = struct.unpack_from('<I', blob, 16)
    field14, = struct.unpack_from('<I', blob, 20)
    tag = blob[0x18:0x28]
    ct = blob[0x28:0x28 + ((ln + 3) & ~3)]
    print(f'nonce={nonce:08x} cost={cost} len={ln} field14={field14:08x} tag={tag.hex()} ct={ct.hex()}')
    # verify cipher model
    k0, k1 = struct.unpack_from('<QQ', key48, 0)
    ok = True
    for i in range(0, (ln + 3) & ~3, 4):
        p = pt[i:i+4].ljust(4, b'\x00')
        pw, = struct.unpack('<I', p)
        a = f17e0(pw, nonce, i // 4, cost, 0, 0)
        b = f3700(key48, a, cost, 0)
        cw = f17e0(b, nonce, i // 4, cost, 1, 0)
        got, = struct.unpack_from('<I', ct, i)
        print(f'block{i//4}: p={pw:08x} a={a:08x} b={b:08x} cw={cw:08x} got={got:08x} ok={cw==got}')
        ok &= (cw == got)
    print('model ok', ok)

# also verify f33d0-based G chain from a known a/b pair
print('done')
