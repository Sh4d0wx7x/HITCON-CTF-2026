#!/usr/bin/env python3
"""
HITCON CTF 2026 - "SPI TPM Free Trial" - libspi_tpm_firmware.so internals
===========================================================================
REVISED. The first version of this file claimed the per-chunk keystream
never touches the matched key slot's secret material. That was wrong --
it came from stopping the trace one function too early. Correcting it
here rather than leaving the mistake in place.

-----------------------------------------------------------------------
PART 1 -- BLAKE2s core (0x1200 compress, 0x1df0 update) -- SOLID
-----------------------------------------------------------------------
Unchanged from before, still verified byte-exact against Python's own
hashlib.blake2s across 11 inputs (0/1/63/64/65/127/128/129/200 bytes).
This is the TPM's internal hash primitive (used by the snapshot-restore
helper at 0x1ea0, not by the main cipher). Two things it resolves from
the earlier sessions' notes: the ".rodata 0x4080 nibble tables" are the
stock BLAKE2 SIGMA table (not a custom S-box), and the "ble..." string
fragment is just the tail of the literal string "failed to reseed
firmware key table", not a second hash construction.

-----------------------------------------------------------------------
PART 2 -- the real cipher (0x17e0, 0x3700, 0x33d0, 0x3850) -- CORRECTED
-----------------------------------------------------------------------
Per 4-byte chunk, the encrypt handler (opcode 2, dispatched from
0x25e0) does three calls in sequence:

  1. r1 = f17e0(plaintext_word, nonce, chunk_index, COST, flag=0)
  2. r2 = f3700(slot_ptr, r1, COST, flag=0)     <-- THE KEY GETS USED HERE
  3. ks = f17e0(r2, nonce, chunk_index, COST, flag=1)   <-- keystream word
     state[0x2440] ^= (COST + r2)               <-- running accumulator

slot_ptr in step 2 is the address of the matched key slot + 0x10 (i.e.
genuine getrandom()-derived secret material, not anything
attacker-visible). f3700 reads 48 bytes of that material into local
buffers, then -- when its flag byte is 0, which is what the encrypt
path uses -- loops **COST times**, each iteration calling f33d0 with
(an evolving 32-bit accumulator, round_index & 3, 8 bytes of key
material, 8 more bytes of key material) and folding the 32-bit result
back into the accumulator via `acc = ((f33d0_result ^ acc) << 16) |
(acc >> 16)`.

So COST is not just an opaque tweak -- **it is literally the round
count for mixing the real key into the keystream**, directly settable
by whoever calls `encrypt KEY COST HEX` (confirmed range-checked to
[1, 1000000], no lower bound beyond >=1). That is the shape of the
"Free Trial" vulnerability this looks like it's pointing at: an
attacker who owns a key slot can ask for COST=1 and look at how little
diffusion of the key survives a single round, and/or compare COST=1
vs larger COST values on the same plaintext under the same key to see
how fast the construction's output stabilizes/avalanches. I have NOT
yet determined whether COST=1 is cryptanalytically weak -- that's a
real question about f33d0's construction, not yet answered.

f33d0 itself (the per-round mix) is built from well-known PUBLIC
64-bit building blocks, not invented from scratch:
  - the 64-bit golden-ratio constant 0x9e3779b97f4a7c15 (same role as
    splitmix64's "gamma")
  - the exact two-multiply finalizer from splitmix64 / MurmurHash3's
    64-bit fmix (constants 0xbf58476d1ce4e5b9, 0x94d049bb133111eb;
    shift amounts 30, 27, 31 match that construction exactly)
  - at least one more multiply-constant (0xd6e8feb86659fd93) and an
    XOR'd literal that spells out b"bilin-r!" when read as bytes
    (0x62696c696e2d7221) -- the author's own name for this construction
    is apparently "bilin"; 0x3850 derives three more sub-values via a
    sibling function (0x32f0) tagged "bilin-a!" / "bilin-b!" / "bilin-c!"
I have NOT done a bit-exact, verified transcription of f33d0/f3850/f32f0
-- it's a real custom composition of those public pieces, not a single
textbook function I can drop in and trust the way BLAKE2s could be.
Getting it bit-perfect by eye, with no way to test it here, risks
another wrong "headline result" like the first version of this file.
The fast way to close that gap is empirical: see probe_live.py, which
is built to use your already-working connection to gather exactly the
comparisons (same plaintext/key at COST=1 vs higher COST, nonce
behaviour, one-bit plaintext deltas) that would make finishing this
transcription fast and checkable instead of another blind trace.

-----------------------------------------------------------------------
PART 3 -- state layout / protocol -- unchanged, still solid
-----------------------------------------------------------------------
Response blob format, confirmed against a real 112-byte get_flag
capture (not just predicted from disassembly):
  +0x00 (8B)  "STP1" + u16 opcode + u16 hdrlen   (hdrlen read as 40/0x28,
              matches the 0x28000231505453 constant in the disassembly
              exactly)
  +0x08 (4B)  per-request nonce (the same 4 bytes obtained from
              getrandom() right before the chunk loop)
  +0x0c (2B)  COST & 0xffff
  +0x0e (1B)  (COST >> 16) & 0xff
  +0x0f (1B)  zero
  +0x10 (2B)  declared plaintext length (pre-padding)
  +0x12 (2B)  zero
  +0x14 (4B)  return value of 0x3850 (the "bilin-a/b/c" slot-derived
              value) for this request -- role not yet determined
  +0x18..+0x27 (16B) NOT YET IDENTIFIED. Real capture shows this is
              non-zero, so something writes it between where my trace
              stopped (0x294c) and the chunk loop (0x2980); next thing
              to pin down if it matters
  +hdrlen..end  ciphertext, length = round_up(declared_length, 4).
              Confirmed arithmetically against the real capture:
              112 - 40 = 72 = round_up(70, 4).
  Opcode 1 = genkey, opcode 2 = encrypt (get_flag is just an internal
  call to this same opcode 2, under a fixed slot -- the real capture's
  blob has op=2). Opcode 3 relates to budget/reset (gated on payload
  length <=0x27 or a magic 32-bit value at +0x10); no separate opcode
  for "decrypt" was found, consistent with decrypt reusing this same
  machinery with KEY/COST/nonce recovered from the ciphertext blob's
  own header rather than being retyped by the user.

restore_snapshot() (0x23c0) still has no cryptographic integrity check
-- bounds/consistency checks on the budget integers only -- but nothing
in connection.sh/run.sh persists a snapshot across a connection, so
this is real but its remote reachability is still unresolved. Lower
priority than Part 2 for now.

-----------------------------------------------------------------------
PART 4 -- decrypt is opcode 3's "magic" branch (0x2c5c) -- NEW
-----------------------------------------------------------------------
Opcode 3 isn't just budget-related -- its branch at 0x2c5c is where
`decrypt` actually lives, and it's a genuinely different shape than
`encrypt`. The request frame wraps a whole encrypt-shaped blob:

  outer frame (opcode 3) header, 0x10 bytes
  +0x10  the user's ciphertext blob, embedded verbatim, starting with
         its own "STP1" header (so outer+0x10 == blob+0x0, outer+0x14
         == blob's op field, outer+0x16 == blob's hdrlen field, etc.)

Checked, in order, before anything else happens: embedded op==2,
embedded hdrlen==0x28, embedded COST in [1,1000000], embedded length
<=4056, and -- the strict one -- **the outer frame's own declared
payload length must exactly equal round_up(embedded length,4)+40**,
i.e. the exact total size of the embedded blob. Any mismatch is
indistinguishable from a validation failure elsewhere, which is
consistent with the generic "error syntax-or-budget" we got back.

Past validation, it does NOT take a key_id from you (decrypt has none
to give). Instead it loops all 8 key slots and, for each, calls the
same tampered-IV hash helper from Part 1/snapshot-restore (0x1ea0) as
f1ea0(state, slot_ptr, embedded_blob_ptr, rounded_length,
local_16B_buf) -- i.e. it hashes (nonce, COST, the field at blob+0x14,
and the ciphertext itself) together with something read from
slot_ptr+0x10 (same offset 0x3700 reads real key material from), then
compares the first 16 bytes of that output against state+0x28 with a
16-byte XOR-reduce-to-one-byte trick. A match means that slot's key
produced this blob; it requires exactly one match ([rsp+0x10]==1) to
proceed. So the field at blob+0x14 -- previously just "0x3850's return
value, role unknown" -- is a per-request authentication tag, computed
at encrypt time from the real key and checked at decrypt time by
brute-forcing all 8 slots against it. Once a unique match is found, it
decrypts using the exact same f17e0/f3700/f17e0 chunk chain as encrypt
(0x2f56-0x2f8b mirror 0x29f3-0x2a28 almost instruction-for-instruction).

What this means practically: decrypt genuinely doesn't care whose key
it is (consistent with the other script's original intuition), but it
is NOT as simple as "replay any blob verbatim" -- the strict outer
length match is the likely reason a naive `decrypt <get_flag's hex>`
failed, and that depends entirely on how spi-tpm-service (the ARM64
guest binary) builds the outer wrapper from the `decrypt HEX` command
text, which I cannot see (no AArch64 disassembly capability in this
environment -- see the conversation for details). If you have
Ghidra/IDA locally, spi-tpm-service's decrypt command handler is now
the single highest-value remaining target: everything it needs to
produce is known precisely from the firmware side above, the only gap
is confirming the service actually builds it that way.
"""

import struct

MASK32 = 0xFFFFFFFF

# --------------------------------------------------------------------
# PART 1 -- BLAKE2s (verified byte-exact, see module docstring)
# --------------------------------------------------------------------

IV = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]

SIGMA = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3],
    [11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4],
    [7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8],
    [9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13],
    [2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9],
    [12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11],
    [13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10],
    [6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5],
    [10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0],
]

TAMPERED_IV0 = 0x6B08C677  # .rodata 0x4140, used only by the snapshot helper


def _rotr32(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK32


def _g(v, a, b, c, d, x, y):
    v[a] = (v[a] + v[b] + x) & MASK32
    v[d] = _rotr32(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d]) & MASK32
    v[b] = _rotr32(v[b] ^ v[c], 12)
    v[a] = (v[a] + v[b] + y) & MASK32
    v[d] = _rotr32(v[d] ^ v[a], 8)
    v[c] = (v[c] + v[d]) & MASK32
    v[b] = _rotr32(v[b] ^ v[c], 7)


def blake2s_compress(h, t0, t1, m, is_final):
    v = h[:8] + IV[:8]
    v[12] ^= t0
    v[13] ^= t1
    if is_final:
        v[14] ^= MASK32
    for r in range(10):
        s = SIGMA[r]
        _g(v, 0, 4, 8, 12, m[s[0]], m[s[1]])
        _g(v, 1, 5, 9, 13, m[s[2]], m[s[3]])
        _g(v, 2, 6, 10, 14, m[s[4]], m[s[5]])
        _g(v, 3, 7, 11, 15, m[s[6]], m[s[7]])
        _g(v, 0, 5, 10, 15, m[s[8]], m[s[9]])
        _g(v, 1, 6, 11, 12, m[s[10]], m[s[11]])
        _g(v, 2, 7, 8, 13, m[s[12]], m[s[13]])
        _g(v, 3, 4, 9, 14, m[s[14]], m[s[15]])
    for i in range(8):
        h[i] ^= v[i] ^ v[i + 8]
    return h


def blake2s(data: bytes, digest_size: int = 32, iv0: int = IV[0]) -> bytes:
    h = [iv0] + IV[1:8]
    h[0] ^= 0x01010000 ^ digest_size
    t0 = t1 = 0
    n = len(data)
    i = 0
    if n == 0:
        return b''.join(struct.pack('<I', w) for w in
                         blake2s_compress(h, 0, 0, [0] * 16, True))[:digest_size]
    while n - i > 64:
        block = list(struct.unpack('<16I', data[i:i + 64]))
        t0 = (t0 + 64) & MASK32
        if t0 == 0:
            t1 = (t1 + 1) & MASK32
        blake2s_compress(h, t0, t1, block, False)
        i += 64
    last = data[i:n] + b'\x00' * (64 - (n - i))
    block = list(struct.unpack('<16I', last))
    t0 = (t0 + (n - i)) & MASK32
    if t0 < (n - i):
        t1 = (t1 + 1) & MASK32
    blake2s_compress(h, t0, t1, block, True)
    return b''.join(struct.pack('<I', w) for w in h)[:digest_size]


# --------------------------------------------------------------------
# PART 3 -- response blob parsing (confirmed against a real capture)
# --------------------------------------------------------------------

def parse_response_blob(blob: bytes) -> dict:
    """Parse an encrypt/get_flag response blob. See Part 3 docstring
    for field provenance. Ciphertext slice uses the self-reported
    hdrlen rather than a hardcoded offset."""
    magic, op, hdrlen = struct.unpack_from('<4sHH', blob, 0)
    nonce, = struct.unpack_from('<I', blob, 8)
    cost_lo, = struct.unpack_from('<H', blob, 0xc)
    cost_hi = blob[0xe]
    length, = struct.unpack_from('<H', blob, 0x10)
    field14, = struct.unpack_from('<I', blob, 0x14)
    unknown_18_27 = blob[0x18:hdrlen] if hdrlen > 0x18 else b''
    ciphertext = blob[hdrlen:]
    return dict(magic=magic, op=op, hdrlen=hdrlen, nonce=nonce,
                cost_lo16=cost_lo, cost_hi8=cost_hi,
                cost_partial=(cost_hi << 16) | cost_lo,
                length=length, field14=field14,
                unknown_18_27=unknown_18_27, ciphertext=ciphertext)


if __name__ == "__main__":
    h = blake2s(b"hello spi-tpm")
    print("blake2s(b'hello spi-tpm') =", h.hex())
    real_flag_blob = bytes.fromhex(
        "5354503102002800b69d7c02b35f0800460000009dc2695ebed15f4587ac65"
        "a1c0fa611a19082d26e68fe9239ddee18d719af73460708d799e503ab0e671"
        "d216de837b96282614ae0b01d1c11c549f1e68c8959892b3b828c06e3b1acf"
        "901b41efeaa03c00acce620c79f611411602a9")
    print(parse_response_blob(real_flag_blob))
