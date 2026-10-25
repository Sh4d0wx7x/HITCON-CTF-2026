
#!/usr/bin/env python3

FLAG_BLOB = bytes.fromhex(
    "5354503102002800da999ea8b35f080046000000"
    "f3f6872d2d5627b20dc7768cacc8440a3bf8087e"
    "1dbee8ff9e816038f62039b217aa4eede8bc992d7"
    "ba666422b07ccec5686643dd5d3c88103b8f33032"
    "bce03d80c69ee78d445f4c72e071e7b26d8891c4"
    "ceb35d8f089ab59d835bc7"
)

CONSTRAINTS = [
    (0x5B4B, 0x6A4D),
    (0x3192, 0xD605),
    (0x4F04, 0x7CE8),
    (0xB834, 0x89A3),
]

def main():
    print(f"[+] Flag packet: {len(FLAG_BLOB)} bytes")
    print(f"[+] Magic: {FLAG_BLOB[:4]!r}")
    print(f"[+] Version: {int.from_bytes(FLAG_BLOB[4:6], 'little')}")
    print(f"[+] Header length: {int.from_bytes(FLAG_BLOB[6:8], 'little')}")
    print(f"[+] Cost: {int.from_bytes(FLAG_BLOB[12:16], 'little')}")
    print(f"[+] Payload length: {int.from_bytes(FLAG_BLOB[16:20], 'little')}")
    print("[+] Constraints:")
    for x, target in CONSTRAINTS:
        print(f"    f33d0({x:#06x}) & 0xffff == {target:#06x}")

    print("\n[!] Packet captured; key recovery and decryption are not implemented.")
    print("[!] The equations/constants from solve.py are required for that stage.")

if __name__ == "__main__":
    main()
