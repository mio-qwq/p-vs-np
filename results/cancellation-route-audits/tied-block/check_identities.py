#!/usr/bin/env python3
"""Bounded exact checks of the structural identities; no third-party code."""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
from check import vd, fail_if

def coeffs(roots):
    f=[F(1)]
    for x in roots:
        g=[F(0)]*(len(f)+1)
        for j,v in enumerate(f):g[j]-=x*v;g[j+1]+=v
        f=g
    return f

def remainder(h,f):
    a=[F(0)]*h+[F(1)];d=len(f)-1
    while len(a)>d:
        c=a[-1];k=len(a)-1-d
        for j,v in enumerate(f):a[k+j]-=c*v
        while a and not a[-1]:a.pop()
    return a+[F(0)]*(d-len(a))

def det(mat):
    a=[list(map(F,row)) for row in mat];n=len(a);v=F(1)
    for i in range(n):
        pivot=next((j for j in range(i,n) if a[j][i]),None)
        if pivot is None:return F(0)
        if pivot!=i:a[i],a[pivot]=a[pivot],a[i];v=-v
        p=a[i][i];v*=p
        for j in range(i+1,n):
            q=a[j][i]/p
            for k in range(i+1,n):a[j][k]-=q*a[i][k]
    return v

def e2(vals):return sum(a*b for a,b in combinations(vals,2))

def run(name,e,r,J):
    n=len(e);J=set(J);Y=set(range(n))-J;s=len(J);m=n-s;p=s-r;q=m-r
    f=coeffs([e[j] for j in sorted(J)]);g=coeffs([e[j] for j in sorted(Y)])
    K=[remainder(h,f)[r:s]+remainder(h,g)[r:m] for h in range(r,n-r)]
    S=sum((-1)**sum(B)*vd(e,B)*vd(e,set(range(n))-set(B)) for B in combinations(sorted(J),r))
    Q=(-1)**(sum(J)+p*(p-1)//2)*vd(e,J)*vd(e,Y)*det(K)
    fail_if(S!=Q,name+' remainder quotient mismatch')
    out={'name':name,'n':n,'r':r,'s':s,'S':str(S),'det_K':str(det(K))}
    if n==2*r+2 and s==r+1:
        T=sum((-1)**sum(B)*vd(e,B)*vd(e,set(range(n))-set(B))*sum(e[j] for j in B) for B in combinations(sorted(J),r))
        pred=(-1)**sum(J)*vd(e,J)*vd(e,Y)*(e2([e[j] for j in Y])-e2([e[j] for j in J]))
        fail_if(T!=pred,name+' weighted column sum mismatch')
        out['T']=str(T)
    return out
cases=[
 ('n4_unbalanced',[0,1,2,3],1,{0,1}),
 ('n4_balanced',[0,1,2,3],1,{0,3}),
 ('n5_1x2',[0,1,2,4,6],1,{0,3}),
 ('n5_saturated',[0,1,2,4,6],2,{0,2,4}),
 ('n6_gapped',[0,1,2,3,4,6],2,{0,2,5}),
 ('n6_unsorted',[4,0,7,2,9,1],2,{1,3,4}),
 ('n7_2x3',[3,0,1,5,9,12,2],2,{0,2,5}),
 ('n8_standard',[0,1,2,3,4,5,6,7],3,{0,1,6,7}),
 ('n10_unsorted',[9,0,7,2,5,4,1,8,3,11],4,{0,2,5,7,9}),
 ('n12_unsorted',[9,0,7,2,5,4,1,8,3,11,6,14],5,{0,2,3,6,9,11}),
]
result=[run(*x) for x in cases]
path=Path(__file__).with_name('identity-results.json');path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
