# HITCON CTF 2026 — Writeups

Writeups and solve scripts from HITCON CTF 2026.

## Structure

~~~
HITCON-CTF-2026/
└── Misc/
    └── <challenge>/
        ├── attachments/     # original challenge handout
        ├── src/deploy/      # challenge source as deployed on the server
        ├── Dockerfile
        ├── docker-compose.yml
        ├── README.md        # writeup
        └── solver.py        # solve script
~~~

## Challenges

| Category | Challenge | Summary |
|---|---|---|
| Misc | [mathclipse](Misc/mathclipse/) | JSON-driven attribute swaps on `math`'s object graph, chained into a forced-crash primitive, a `GenericAlias.__args__` unwrap gadget, and a `FileFinder.path_hook` hijack for RCE. |

More write-ups added as challenges get solved.
