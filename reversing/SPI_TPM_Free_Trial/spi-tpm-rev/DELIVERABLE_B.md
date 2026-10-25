# Deliverable (b): the `get_flag` budget bypass

## Short answer

`get_flag` is free because the flag is encrypted **once at startup**, before
the userland budget variable exists, by calling the encryption wrapper
directly. `get_flag` itself only prints the cached ciphertext blob. It does
not call the firmware, the ioctl wrappers, or any budget check.

The decrypt budget is a **separate** obstacle: replaying the cached blob
through the normal `decrypt` command charges

```
0x85fb3 * (ceil(70/4) + 0x100) = 548787 * 274 = 150,367,638
```

against a budget of 1024, so the service rejects it before the ioctl. No
remote bypass of that decrypt-budget comparison has been found.

## Exact startup flow

`spi-tpm-service` (AArch64, static PIE) does this at boot:

```
0x93d0-0x9450   read /flag into sp+0x118; length in x21
0x945c          genkey wrapper 0x9dc0 -> key id 1
0x9468-0x9490   encrypt wrapper 0x9e80:
                  x0 = fd
                  w1 = key id 1
                  x2 = /flag plaintext at sp+0x118
                  w3 = flag length
                  w4 = 0x85fb3
                  x5 = cached blob at sp+0x64
                  x6 = cached length at sp+0x110 (capacity 0xa8)
0x94a0-0x94b0   wipe the 128-byte plaintext buffer
0x94b4-0x94c0   initialize budget = 1024, queries = 27
```

The cost constant is built at `0x9474` / `0x948c`:

```
mov w4, #0x5fb3
movk w4, #0x8, lsl #16      ; w4 = 0x00085fb3
```

The encryption wrapper `0x9e80`, the kernel module, and the host firmware
have **no budget accounting**. The budget checks exist only in the text
command handlers:

- encrypt handler: `0x9b24-0x9b54`
- decrypt handler: `0x9a0c-0x9a20`

Because the startup call goes directly to `0x9e80`, the hard-coded cost
`0x85fb3` is never compared with 1024. The flag is encrypted for free.

`get_flag` at `0x9914` is read-only: it prints the cached opcode-2 blob from
`sp+0x64` (and its key id). That is the bypass: the ciphertext is obtained
without spending budget or a query on encryption.

## Why replaying the blob still fails

The cached blob is a normal opcode-2 blob under the startup key. The
firmware would accept it, but the `decrypt` handler computes the charge from
the blob's inner cost and length **before** calling the ioctl. For the remote
flag blob:

```
inner cost   = 0x85fb3 = 548787
inner length = 70
charge       = 548787 * (ceil(70/4) + 0x100)
             = 548787 * 274
             = 150,367,638
budget       = 1024
```

The branch at `0x9a20` (`b.hi 0x98f4`) rejects the request with
`error syntax-or-budget`.

## Local proof that only the budget gate blocks replay

Patch **only** the decrypt budget branch at file offset `0x9a20` in the
extracted initramfs `/init`:

```
before: a8 f6 ff 54   ; b.hi 0x98f4
after:  1f 20 03 d5   ; nop
```

Boot the patched initramfs with the local flag `hitcon{test}\n`, run
`get_flag`, and send the returned blob unmodified to `decrypt`:

```
plaintext 686974636f6e7b746573747d0a = hitcon{test}\n
```

No crypto, key, nonce, or startup cost was changed. This proves:

- the cached blob's key and MAC are valid for replay;
- the service-side budget comparison at `0x9a20` is the sole blocker;
- the firmware outer-frame, length, and MAC checks pass for the normal
  decrypt wrapper.

## Why the obvious shortcuts fail

### Patch the blob's cost field

The full 32-bit cost is authenticated. `f1ea0` absorbs `blob[0:0x18]`
(including the cost) and `f33d0` multiplies the full 32-bit cost by
`0xa5a3564e27f8862f`. Patching the remote blob's cost to 1 returns
`error hardware`.

A local test with cost `3` (the same low 4 bits as `0x85fb3`) passes the
service budget gate with a charge of `3 * 260 = 780`, but the firmware also
returns `error hardware`. The tag is not a low-bit function; there is no
truncation shortcut.

### Replay a self-made low-cost blob

Its tag is valid only for its own ciphertext, nonce, and cost. It does not
decrypt the flag blob.

### Overflow into the budget

The budget is at `sp+0x58`, below all large service buffers:

```
sp+0x058  budget (64-bit)
sp+0x060  queries
sp+0x064  cached get_flag blob (0xa8)
sp+0x110  cached blob length
sp+0x118  flag plaintext (0x80, wiped after startup)
sp+0x198  decrypt output (0x400)
sp+0x598  encrypt output / decrypt input (0x1000)
sp+0x1598 line buffer (0x2080)
```

All service hex-decode and response writes go upward, away from the budget.
Firmware request/response buffers are exactly sized:

- firmware request buffer: `0x1010` bytes (16-byte header + up to `0x1000`
  payload); payload `>0x1000` is rejected;
- response buffer: `0x1008` bytes at `+0x1010..+0x2017`; the response blob
  starts at `+0x1018`;
- kernel encrypt `inlen <= 0xfd8`, so `blob_len = 0x28 + round4(inlen) <=
  0x1000`;
- kernel decrypt inner length `<= 0xfd8`, `outcap >= inner length`;
- service caps plaintext and inner length at `0x400`.

No firmware or kernel overflow into the key slots or service budget was
found.

### SRAM/DMA leak

The QEMU `spi-tpm-dma` device only parses descriptors and checks lengths; it
does not copy data. The `spi-tpm-sram` device is a `0x2000`-byte RAM region
at guest physical `0xc002000`. The kernel's `spi_stm32` driver allocates the
whole SRAM pool but uses kmalloc buffers because the SPI transfer is
`0x2004 > 0x2000`; the boot log says "cryptographic accelerator ready
(kmalloc buffers)". A local SRAM dump after the startup encrypt is all zero,
even with `spi_stm32.polling_limit_us=0`. This route is dead.

### Cost/length mismatch between service and firmware

Both read the same inner blob fields. The service's charge and the
firmware's MAC/cipher use the same cost and length. There is no mismatch to
exploit.

## Status

- Deliverable (b): **complete**.
- Remote flag: **not recovered**. The service-side decrypt budget gate is
  still the barrier.
- Remaining possible routes: a genuine kernel/service logic bug, a
  host-side migration/snapshot path, or recovering the 128-bit flag key from
  low-cost encrypt-oracle samples. None is currently validated.

Full analysis and corrections are in
`../resources.txt`, especially sections 0, 4.5-4.7, 6.2-6.7, 9-11, and 13.
