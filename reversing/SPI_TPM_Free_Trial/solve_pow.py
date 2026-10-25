import hashlib
import sys

prefix = bytes.fromhex(sys.argv[1])
bits = 8
salt = b"spi-tpm-pow-v1:" + sys.argv[1].encode()

nonce = 0
while True:
    password = prefix.hex().encode() + str(nonce).encode()
    digest = hashlib.scrypt(
        password,
        salt=salt,
        n=32768,
        r=8,
        p=1,
        dklen=32,
        maxmem=128 * 1024 * 1024,
    )

    if digest[0] == 0:
        print(f"nonce = {nonce}")
        print(f"digest = {digest.hex()}")
        break

    nonce += 1
