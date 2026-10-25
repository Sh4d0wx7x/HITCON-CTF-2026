import ctypes, struct, random, sys
MASK32=0xffffffff; MASK64=0xffffffffffffffff
def rol64(x,n): return ((x<<n)|(x>>(64-n)))&MASK64
def ror64(x,n): return ((x>>n)|(x<<(64-n)))&MASK64
def fmix64(x):
    x&=MASK64
    x^=x>>30; x=(x*0xbf58476d1ce4e5b9)&MASK64
    x^=x>>27; x=(x*0x94d049bb133111eb)&MASK64
    x^=x>>31
    return x&MASK64
def f33d0(acc16, key0, key1, rnd):
    acc16 &= 0xffff; rnd &= MASK32
    r8=0xd6e8feb86659fd93
    rax=key1&MASK64
    rdi=(acc16*r8)&MASK64
    rax=rol64(rax,0x11)
    gamma=0x9e3779b97f4a7c15
    rax^=key0&MASK64
    rsi=rol64(key0&MASK64,0x1d)
    rsi^=key1&MASK64
    rax^=rdi
    rcx=(rnd*0xa5a3564e27f8862f)&MASK64
    rax^=rcx
    rax^=0x62696c696e2d7221
    rax=(rax+gamma)&MASK64
    # first fmix WITHOUT the final xor; the assembly xors y and y>>31 into rsi
    y=rax
    y^=y>>30; y=(y*0xbf58476d1ce4e5b9)&MASK64
    y^=y>>27; y=(y*0x94d049bb133111eb)&MASK64
    rsi^=y
    rsi^=(y>>31)&MASK64
    rax=(rsi+gamma)&MASK64
    rax=fmix64(rax)
    # fold64->32: eax ^= edx>>32; eax ^= edx; eax ^= edx>>16; eax ^= edx>>48
    eax=((rax>>16)&MASK32) ^ ((rax>>32)&MASK32) ^ (rax&MASK32) ^ ((rax>>48)&MASK32)
    return eax&MASK32
def f3700_round(state,key0,key1,rnd):
    hi=(state>>16)&0xffff
    x=f33d0(hi,key0,key1,rnd)
    return (((x^state)<<16)&MASK32) | hi
def f3700(key_bytes, value, cost, flag):
    key0=struct.unpack_from('<Q',key_bytes,0)[0]
    key1=struct.unpack_from('<Q',key_bytes,8)[0]
    state=value&MASK32
    if flag==0:
        for i in range(cost):
            state=f3700_round(state,key0,key1,i&3)
        return state
    else:
        # inverse loop 0x3760: rnd = (cost-1-j)&3; new = (state<<16) | ((f33d0(hi) xor hi)&0xffff)
        for j in range(cost):
            rnd=(cost-1-j)&3
            lo=state&0xffff
            hi=(state>>16)&0xffff
            x=f33d0(lo,key0,key1,rnd)
            state=((lo<<16)&MASK32) | ((x^hi)&0xffff)
        return state
def triple32(x):
    x&=MASK32
    x^=x>>16; x=(x*0x21f0aaad)&MASK32
    x^=x>>15; x=(x*0x735a2d97)&MASK32
    x^=x>>15
    return x&MASK32
OFF=[0x9e3779b9,0x3c6ef372,0xdaa66d2b,0x78dde6e4,0x1715609d,0xb54cda56]
def f17e0(value,nonce,chunk,cost,r8,r9):
    # mask
    mask=0xffffffff if r8==0 else 0
    mask=(mask & 0xbb03e172)&MASK32
    mask=(mask - 0x2e4ab5cb)&MASK32
    seed=((chunk*0x9e3779b9)&MASK32) ^ (nonce&MASK32) ^ ((cost*0x735a2d97)&MASK32) ^ mask
    seed&=MASK32
    words=[triple32((seed+o)&MASK32) for o in OFF]
    if r9==0:
        r10=value&MASK32
        eax=(value>>16)&MASK32
        edi=3; r8d=7
        for i in range(6):
            esi=words[i]
            edx=eax
            ecx=r8d&0xff
            # rol ax,cl (16-bit)
            ax=eax&0xffff
            ax=((ax<<ecx)|(ax>>(16-ecx)))&0xffff if ecx else ax
            eax=(eax&0xffff0000)|ax
            ecx=edi&0xff
            edi+=2; r8d+=1
            r11=(esi>>16)&0xffff
            esi=(esi+edx)&MASK32
            si=esi&0xffff
            si=((si<<ecx)|(si>>(16-ecx)))&0xffff if ecx else si
            esi=(esi&0xffff0000)|si
            eax=(eax+r11)&MASK32
            eax^=esi
            eax^=r10
            r10=edx
        return (((eax<<16)&MASK32) | (edx&0xffff))&MASK32
    else:
        eax=value&MASK32
        r9d=(value>>16)&MASK32
        edi=0xc; r8d=0xd
        for i in range(6):
            esi=words[5-i]
            ecx=edi&0xff
            old_eax=eax
            edx=eax
            edi-=1
            dx=edx&0xffff
            dx=((dx<<ecx)|(dx>>(16-ecx)))&0xffff if ecx else dx
            edx=(edx&0xffff0000)|dx
            ecx=r8d&0xff
            r8d-=2
            r11=(esi>>16)&0xffff
            esi=(esi+eax)&MASK32
            si=esi&0xffff
            si=((si<<ecx)|(si>>(16-ecx)))&0xffff if ecx else si
            esi=(esi&0xffff0000)|si
            edx=(edx+r11)&MASK32
            edx^=esi
            edx^=r9d
            r9d=old_eax
            if i != 5:
                eax=edx
        return (((eax<<16)&MASK32) | (edx&0xffff))&MASK32

if __name__=='__main__':
    # self-test f33d0 against known? just print
    for args in [(0,0,0,0),(0x1234,0x1122334455667788,0x99aabbccddeeff00,2)]:
        print(args, hex(f33d0(*args)))
    print('f17e0', hex(f17e0(0x12345678,0xdeadbeef,3,5,0,0)), hex(f17e0(0x12345678,0xdeadbeef,3,5,1,0)))
