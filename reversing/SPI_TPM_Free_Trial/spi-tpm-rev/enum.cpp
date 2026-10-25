// Box-constrained lattice solution enumerator for field14 linearized system.
// DFS with interval (bounds-consistency) pruning over LLL-reduced basis coefficients.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <string>
using namespace std;

typedef unsigned long long u64;
// minimal signed 256-bit (4 x u64 limbs, two's complement)
struct S256 {
    u64 l[4];
};
static inline S256 from_i64(long long v){ S256 r; unsigned long long uv=(u64)v; bool neg=v<0; r.l[0]=uv; u64 fill = neg?~0ULL:0ULL; r.l[1]=fill;r.l[2]=fill;r.l[3]=fill; // note: two's complement of small negative works since l[0] holds low bits of v
    if(neg){ /* v negative: two's complement 256-bit of v = 2^256+v */
        unsigned long long acc=(u64)v; // already two's complement of low 64 bits
        r.l[0]=acc; r.l[1]=~0ULL; r.l[2]=~0ULL; r.l[3]=~0ULL;
        // subtract nothing else: 2^256 + v with v negative -> high limbs all ones, low = v mod 2^64
        // but v e.g. -3: low = 0xFFFF...FD, limbs = all 1 except low -> correct
        if(acc!=~0ULL){/* fine */}
    }
    return r;
}
static inline S256 add(const S256&a,const S256&b){S256 r; unsigned __int128 c=0; for(int i=0;i<4;i++){unsigned __int128 s=(unsigned __int128)a.l[i]+b.l[i]+c; r.l[i]=(u64)s; c=s>>64;} return r;}
static inline S256 sub(const S256&a,const S256&b){S256 r; unsigned __int128 br=0; for(int i=0;i<4;i++){unsigned __int128 d=(unsigned __int128)a.l[i]-(b.l[i]+ (i==0?(u64)0:0)) - (i==0?0:0); // do proper
        }
    // simpler: negate b then add
    S256 n; bool allones=true; for(int i=0;i<4;i++){ if(b.l[i]!=~0ULL) allones=false; }
    // compute -b = ~b + 1
    u64 carry=1; for(int i=0;i<4;i++){ u64 nb=~b.l[i]; unsigned __int128 s=(unsigned __int128)nb+carry; n.l[i]=(u64)s; carry=(u64)(s>>64);} 
    return add(a,n);
}
static inline int cmp(const S256&a,const S256&b){ for(int i=3;i>=0;i--){ if(a.l[i]!=b.l[i]) return a.l[i]<b.l[i]?-1:1; } return 0; }
static inline bool is_neg(const S256&a){ return (long long)a.l[3]<0; }

static S256 mul_small(const S256&a, long long c){
    // multiply 256-bit signed by small |c|<=2^63
    S256 r; bool cneg=c<0; unsigned long long m = cneg? (u64)(-c) : (u64)c;
    // unsigned multiply
    u64 t[4]={0,0,0,0}; unsigned __int128 carry=0;
    for(int i=0;i<4;i++){ unsigned __int128 cur=(unsigned __int128)a.l[i]*m + carry; t[i]=(u64)cur; carry=cur>>64; }
    // carry overflow beyond 4 limbs ignored (mod 2^256)
    S256 rr; for(int i=0;i<4;i++) rr.l[i]=t[i];
    if(cneg){ // negate
        u64 carry2=1; for(int i=0;i<4;i++){ u64 nb=~rr.l[i]; unsigned __int128 s=(unsigned __int128)nb+carry2; rr.l[i]=(u64)s; carry2=(u64)(s>>64);} }
    return rr;
}

struct Input {
    int n;
    vector<array<S256,4>> basis; // n x n
    vector<S256> lo, hi;
};

int main(int argc, char** argv){
    FILE* f = fopen(argv[1], "r");
    int n; fscanf(f, "%d", &n);
    vector<vector<S256>> B(n, vector<S256>(n));
    auto readS=[&](S256 &x){ long long a,b,c,d; // read as 4 decimal u64 limbs? read as two 64-bit halves via unsigned decimal
        unsigned long long w0,w1,w2,w3; fscanf(f,"%llu %llu %llu %llu",&w3,&w2,&w1,&w0); // big-endian limbs, signed two's complement
        x.l[0]=w0;x.l[1]=w1;x.l[2]=w2;x.l[3]=w3; };
    for(int i=0;i<n;i++) for(int j=0;j<n;j++) readS(B[i][j]);
    vector<S256> lo(n), hi(n);
    for(int i=0;i<n;i++) readS(lo[i]);
    for(int i=0;i<n;i++) readS(hi[i]);
    long long clo[n]; long long chi[n];
    for(int i=0;i<n;i++) fscanf(f,"%lld %lld",&clo[i],&chi[i]);
    fclose(f);
    // suffix min/max per level
    vector<vector<S256>> smin(n+1, vector<S256>(n)), smax(n+1, vector<S256>(n));
    for(int k=0;k<n;k++){ smin[n][k]=from_i64(0); smax[n][k]=from_i64(0); }
    for(int i=n-1;i>=0;i--){
        for(int k=0;k<n;k++){
            S256 a=mul_small(B[i][k], clo[i]);
            S256 b=mul_small(B[i][k], chi[i]);
            S256 mn = is_neg(a)? (cmp(a,b)<0?a:b) : (cmp(a,b)<0?a:b);
            // generic min/max
            int c=cmp(a,b); S256 mna = c<0?a:b; S256 mxb = c<0?b:a;
            smin[i][k]=add(smin[i+1][k], mna);
            smax[i][k]=add(smax[i+1][k], mxb);
        }
    }
    vector<S256> v(n, from_i64(0));
    long long nodes=0, leaves=0, sols=0, trueh=0;
    // DFS
    // iterative or recursive; recursive with depth 29 fine
    bool limit_hit=false;
    long long node_limit = (argc>2)? atoll(argv[2]) : 2000000000LL;
    // We'll do recursion; function using captured vars
    // For speed, use plain arrays.
    static S256 vv[64]; static S256 BB[64][64]; static S256 smn[65][64], smx[65][64]; static S256 LO[64], HI[64];
    for(int k=0;k<n;k++){ LO[k]=lo[k]; HI[k]=hi[k]; for(int j=0;j<n;j++) BB[j][k]=B[j][k]; }
    for(int i=0;i<=n;i++) for(int k=0;k<n;k++){ smn[i][k]=smin[i][k]; smx[i][k]=smax[i][k]; }
    long long CL[64], CH[64];
    for(int i=0;i<n;i++){CL[i]=clo[i];CH[i]=chi[i];}
    // Output buffering
    vector<string> out;
    char buf[256];

    // iterative DFS with explicit stack (c index per level)
    int lvl=0; long long cur[64]; for(int i=0;i<n;i++) cur[i]=CL[i]-1; // will increment first
    bool entered=false;
    while(true){
        if(lvl==n){
            // leaf: check box exactly
            nodes++;
            bool ok=true;
            for(int k=0;k<n;k++){ if(cmp(vv[k],LO[k])<0||cmp(vv[k],HI[k])>0){ok=false;break;} }
            leaves++;
            if(ok){
                sols++;
                // output v limbs for python-side check
                snprintf(buf,sizeof(buf),"SOL");
                string s=buf;
                for(int k=0;k<n;k++){ char t[128]; snprintf(t,sizeof(t)," %016llx%016llx%016llx%016llx", (unsigned long long)vv[k].l[3],(unsigned long long)vv[k].l[2],(unsigned long long)vv[k].l[1],(unsigned long long)vv[k].l[0]); s+=t; }
                out.push_back(s);
            }
            // backtrack
            lvl--;
            if(lvl>=0){ // undo current coeff at lvl
                long long c=cur[lvl];
                for(int k=0;k<n;k++){ vv[k]=sub(vv[k], mul_small(BB[lvl][k], c)); }
            }
            continue;
        }
        if(lvl==-1) break;
        if(entered && cur[lvl]>=CH[lvl]){
            // backtrack
            lvl--;
            if(lvl>=0){ long long c=cur[lvl]; for(int k=0;k<n;k++){ vv[k]=sub(vv[k], mul_small(BB[lvl][k], c)); } }
            continue;
        }
        entered=true;
        cur[lvl]++;
        long long c=cur[lvl];
        nodes++;
        if(nodes>node_limit){ limit_hit=true; break; }
        // apply
        bool ok=true;
        for(int k=0;k<n;k++){ vv[k]=add(vv[k], mul_small(BB[lvl][k], c)); }
        // check interval feasibility with suffix
        const S256* mn=&smn[lvl+1][0]; const S256* mx=&smx[lvl+1][0];
        for(int k=0;k<n;k++){
            S256 t=add(vv[k], mx[k]);
            if(cmp(t, LO[k])<0){ ok=false; break; }
            t=add(vv[k], mn[k]);
            if(cmp(t, HI[k])>0){ ok=false; break; }
        }
        if(ok){ lvl++; entered=false; cur[lvl]=CL[lvl]-1; }
        else {
            // undo this coeff, try next
            for(int k=0;k<n;k++) vv[k]=sub(vv[k], mul_small(BB[lvl][k], c));
        }
    }
    fprintf(stderr,"nodes %lld leaves %lld sols %lld limit_hit %d\n", nodes, leaves, sols, (int)limit_hit);
    for(auto&s:out) printf("%s\n", s.c_str());
    return 0;
}
