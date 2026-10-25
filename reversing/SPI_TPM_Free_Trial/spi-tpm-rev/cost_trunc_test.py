import subprocess, time, os, select, re, sys

ROOT = '/home/sh4d0w/HitconCTF/reversing/SPI_TPM_Free_Trial/spi-tpm-rev'
p = subprocess.Popen(['./run_local.sh'], cwd=ROOT,
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT, bufsize=0)

def drain(idle=0.6, total=30):
    out = b''
    end = time.time() + total
    last = time.time()
    while time.time() < end:
        r, _, _ = select.select([p.stdout], [], [], 0.1)
        if r:
            d = os.read(p.stdout.fileno(), 65536)
            if not d:
                break
            out += d
            last = time.time()
        elif out and time.time() - last > idle:
            break
    return out

def cmd(c, idle=1.0):
    p.stdin.write((c + '\n').encode())
    p.stdin.flush()
    time.sleep(0.2)
    out = drain(idle=idle)
    print('>>>', c)
    print(out.decode(errors='replace'))
    return out

try:
    print(drain(idle=1.0, total=45).decode(errors='replace'))
    out = cmd('get_flag')
    m = re.search(rb'flag\s+(\d+)\s+([0-9a-fA-F]+)', out)
    if not m:
        print('NO FLAG BLOB')
        sys.exit(1)
    kid, hexblob = m.group(1).decode(), m.group(2).decode()
    blob = bytearray(bytes.fromhex(hexblob))
    print('key id', kid, 'blob len', len(blob), 'cost', hex(int.from_bytes(blob[0xc:0x10], 'little')))
    for newcost in (3, 1):
        b = bytearray(blob)
        b[0xc:0x10] = int(newcost).to_bytes(4, 'little')
        print(f'=== decrypt with cost {newcost} ===')
        cmd('decrypt ' + b.hex())
    cmd('budget')
    cmd('quit')
finally:
    try:
        p.stdin.close()
    except Exception:
        pass
    time.sleep(0.5)
    p.terminate()
    try:
        p.wait(timeout=3)
    except Exception:
        p.kill()
