#!/usr/bin/env python3
"""Independent exact polynomial checks; standard library only; no assert statements."""
from fractions import Fraction as F
from itertools import permutations, combinations
from math import comb, factorial
import json
from pathlib import Path

def fail_if(b, msg):
    if b: raise RuntimeError(msg)
def add(dst, src, c=1, dz=0):
    for (l,z),v in src.items():
        key=(l,z+dz); dst[key]=dst.get(key,F(0))+c*v
        if not dst[key]: del dst[key]
def mul(p,q):
    out={}
    for (a,b),v in p.items():
        for (c,d),w in q.items():
            key=(a+c,b+d); out[key]=out.get(key,F(0))+v*w
    return {k:v for k,v in out.items() if v}
def entry(a,e,red):
    return {(h,int(red)):F(comb(e,h))*a**(e-h) for h in range(e+1) if a or e==h}
def matrix(a,e,I,J):
    return [[entry(x,y,i in I and j in J) for j,y in enumerate(e)] for i,x in enumerate(a)]
def direct(A):
    n=len(A); out={}
    for p in permutations(range(n)):
        sign=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)); v={(0,0):F(1)}
        for i,j in enumerate(p): v=mul(v,A[i][j])
        add(out,v,sign)
    return out
def laplace(A):
    n=len(A); states={0:{(0,0):F(1)}}
    for mask in range(1,1<<n):
        i=mask.bit_count()-1; out={}
        cols=[j for j in range(n) if mask>>j&1]
        for pos,j in enumerate(cols): add(out,mul(states[mask^(1<<j)],A[i][j]),(-1)**(i+pos))
        states[mask]=out
    return states[(1<<n)-1]
def vd(x,ids):
    ids=sorted(ids); v=F(1)
    for p,q in combinations(ids,2): v*=x[q]-x[p]
    return v
def H(k):
    v=1
    for q in range(k):v*=factorial(q)
    return v
def string(q): return str(q.numerator) if q.denominator==1 else str(q)
def polyjson(p): return {f'{l},{z}':string(v) for (l,z),v in sorted(p.items())}
def check_square(name,a,e,I,J):
    n=len(a); a=list(map(F,a)); I=set(I);J=set(J); k=len(I); m=n-k
    p=direct(matrix(a,e,I,J)); q=laplace(matrix(a,e,I,J)); fail_if(p!=q,name+' determinant mismatch')
    ic=set(range(n))-I; jc=set(range(n))-J
    other=laplace(matrix(a,e,ic,jc)); shifted={}
    shift=2*k-n
    if shift>=0:
        add(shifted,other,dz=shift);fail_if(p!=shifted,name+' complement mismatch')
    else:
        add(shifted,p,dz=-shift);fail_if(other!=shifted,name+' complement mismatch')
    C=F((-1)**(sum(I)+sum(J)),H(k)*H(m))*vd(a,I)*vd(a,ic)*vd(e,J)*vd(e,jc)
    D=sum(e)-k*(k-1)//2-m*(m-1)//2
    lo=max(0,2*k-n); width=min(k,m)
    stats={}
    for t in range(n+1):
        pt={l:v for (l,z),v in p.items() if z==t}
        if t<lo or t>k:fail_if(bool(pt),name+' impossible target nonzero');continue
        expected=C*(-1)**(k-t)*comb(width,t-lo)
        fail_if(max(pt,default=-1)!=D or pt.get(D)!=expected,name+f' target {t} degree/LC mismatch')
        stats[str(t)]={'degree':D,'leading_coefficient':string(expected)}
    if n==2*k-1:
        for x,S in [(a,I),(e,J)]:
            comp=set(range(n))-S
            lhs=sum((-1)**(sum(S)-p)*vd(x,S-{p})*vd(x,comp|{p}) for p in S)
            rhs=(-1)**sum(S)*vd(x,S)*vd(x,comp)
            fail_if(lhs!=rhs,name+' interpolation identity mismatch')
    return {'name':name,'a':list(map(str,a)),'e':e,'I':sorted(I),'J':sorted(J),'D':D,'C':string(C),'targets':stats,'polynomial':polyjson(p)}
def check_rectangle(name,a,e,I,J):
    n=len(a);a=list(map(F,a));I=set(I);J=set(J);r=len(I);s=len(J)
    fail_if(not (r<s and r+s<=n), 'bad rectangle')
    p=direct(matrix(a,e,I,J));q=laplace(matrix(a,e,I,J));fail_if(p!=q,name+' determinant mismatch')
    D=sum(e)-r*(r-1)//2-(n-r)*(n-r-1)//2
    S=sum((-1)**sum(B)*vd(e,B)*vd(e,set(range(n))-set(B)) for B in combinations(sorted(J),r))
    C=F((-1)**sum(I),H(r)*H(n-r))*vd(a,I)*vd(a,set(range(n))-I)*S
    top={z:v for (l,z),v in p.items() if l==D}
    expected={t:C*(-1)**(r-t)*comb(r,t) for t in range(r+1) if C}
    fail_if(top!=expected,name+' rectangle top mismatch')
    stats={}
    for t in range(r+1):
        pt={l:v for (l,z),v in p.items() if z==t}
        deg=max(pt,default=-1); stats[str(t)]={'degree':deg,'leading_coefficient':string(pt[deg]) if deg>=0 else '0'}
    return {'name':name,'a':list(map(str,a)),'e':e,'I':sorted(I),'J':sorted(J),'candidate_degree':D,'column_sum':string(S),'candidate_leading_coefficient':string(C),'actual_targets':stats,'polynomial':polyjson(p)}

def main():
    out={'square_cases':[
        check_square('n5_standard',list(range(5)),list(range(5)),range(3),range(3)),
        check_square('n5_nonprincipal_gapped',[F(3,2),-2,4,F(1,3),7],[6,0,4,1,9],{0,2,4},{1,2,4}),
        check_square('n7_standard',list(range(7)),list(range(7)),range(4),range(4)),
        check_square('n5_majority_k4',[2,-1,4,0,7],[0,2,5,1,7],{0,1,3,4},{0,1,2,4}),
        check_square('n3_full',[-2,0,3],[0,1,4],range(3),range(3))
    ],'rectangle_cases':[
        check_rectangle('n4_standard_top_zero',list(range(4)),list(range(4)),{0},{0,3}),
        check_rectangle('n5_integer_top_zero',list(range(5)),[0,1,2,4,6],{0},{0,3}),
        check_rectangle('n8_standard_3x4_top_zero',list(range(8)),list(range(8)),{0,1,2},{0,1,6,7}),
        check_rectangle('n6_genuine_2x3_top_zero',list(range(6)),[0,1,2,3,4,6],{0,1},{0,2,5}),
        check_rectangle('n5_saturated_2x3',list(range(5)),[0,1,2,4,6],{0,2},{0,2,4})
    ]}
    path=Path(__file__).with_name('results.json'); path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({g:[{k:v for k,v in case.items() if k!='polynomial'} for case in cases] for g,cases in out.items()},indent=2))
if __name__=='__main__':main()
