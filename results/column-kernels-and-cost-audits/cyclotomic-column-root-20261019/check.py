#!/usr/bin/env python3
"""Independent raw-permutation certificates for the arithmetic staircase theorem.

Only Python's standard library and exact rational arithmetic are used.
The finite cases corroborate the separate universal complex-pole proof.
"""
from fractions import Fraction as F
from itertools import permutations
from math import comb
from pathlib import Path
import json


def require(ok, message):
    if not ok:raise RuntimeError(message)


def trim(p):
    while len(p)>1 and p[-1]==0:p.pop()
    return p


def add(p,q):
    out=[F(0)]*max(len(p),len(q))
    for i,x in enumerate(p):out[i]+=x
    for i,x in enumerate(q):out[i]+=x
    return trim(out)


def mul(p,q):
    out=[F(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]+=x*y
    return trim(out)


def shifted(a,e):
    return [F(comb(e,j))*a**(e-j) for j in range(e+1)]


def raw_terms(a,e,c):
    n=len(a);cache=[[shifted(x,p) for p in e] for x in a]
    T=[[F(0)] for _ in a]
    for perm in permutations(range(n)):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        term=[F(sign)]
        for row,col in enumerate(perm):term=mul(term,cache[row][col])
        row=perm.index(c)
        T[row]=add(T[row],term)
    return T


def pivot_degrees(T):
    n=len(T);degree=max(map(len,T))
    A=[p+[F(0)]*(degree-len(p)) for p in T]
    row=0;pivots=[]
    for col in range(degree):
        pivot=next((r for r in range(row,n) if A[r][col]),None)
        if pivot is None:continue
        A[row],A[pivot]=A[pivot],A[row]
        scale=A[row][col];A[row]=[x/scale for x in A[row]]
        for r in range(row+1,n):
            scale=A[r][col]
            if scale:A[r]=[x-scale*y for x,y in zip(A[r],A[row])]
        pivots.append(col);row+=1
        if row==n:break
    return pivots


def determinant(A):
    A=[list(row) for row in A];n=len(A);out=F(1)
    for j in range(n):
        pivot=next((r for r in range(j,n) if A[r][j]),None)
        if pivot is None:return F(0)
        if pivot!=j:A[j],A[pivot]=A[pivot],A[j];out=-out
        scale=A[j][j];out*=scale
        for r in range(j+1,n):
            factor=A[r][j]/scale
            for c in range(j+1,n):A[r][c]-=factor*A[j][c]
    return out


def solve(A,b):
    n=len(A);A=[list(row)+[value] for row,value in zip(A,b)]
    for j in range(n):
        pivot=next((r for r in range(j,n) if A[r][j]),None)
        require(pivot is not None,"certificate system is singular")
        A[j],A[pivot]=A[pivot],A[j]
        scale=A[j][j];A[j]=[x/scale for x in A[j]]
        for r in range(n):
            if r==j:continue
            factor=A[r][j]
            if factor:A[r]=[x-factor*y for x,y in zip(A[r],A[j])]
    return [row[-1] for row in A]


def check(label,a,m,h,k,common_shift=0):
    a=list(map(F,a));n=len(a)
    require(n>=3 and m>=3 and a==sorted(set(a)),"invalid offsets or dimensions")
    background=[h+m*j for j in range(n-1)]
    require(h>=0 and k>=0 and k not in background,"invalid exponents")
    e=sorted(background+[k]);c=e.index(k)
    T=raw_terms(a,e,c)
    for row in range(n):
        factored=[F((-1)**(row+c))]
        factored=mul(factored,shifted(a[row],k))
        for t in range(n):
            if t!=row:factored=mul(factored,shifted(a[t],h))
        for i in range(n):
            for j in range(i+1,n):
                if row in (i,j):continue
                difference=add(shifted(a[j],m),[-x for x in shifted(a[i],m)])
                factored=mul(factored,difference)
        require(T[row]==factored,"raw cofactor differs from staircase Vandermonde")
    pivots=pivot_degrees(T)
    require(len(pivots)==n,"exact coefficient matrix is not full rank")
    minor=[[p[d] if d<len(p) else F(0) for p in T] for d in pivots]
    det=determinant(minor)
    require(det!=0,"reported rank minor vanishes")
    dual=solve(list(map(list,zip(*minor))),[F(1)]*n)
    require(all(sum(dual[j]*minor[j][s] for j in range(n))==1 for s in range(n)),
            "rational dual does not have value one on every column")
    if common_shift:
        shifted_T=raw_terms(a,[v+common_shift for v in e],c)
        common=[F(1)]
        for x in a:common=mul(common,shifted(x,common_shift))
        require(all(q==mul(common,p) for p,q in zip(T,shifted_T)),
                "common exponent shift identity failed")
    return {"label":label,"offsets":list(map(str,a)),"m":m,"h":h,"k":k,
            "ell":k-h,"exponents":e,"column":c,"rank":n,
            "pivot_degrees":pivots,"nonzero_coefficient_minor":str(det),
            "dual_coefficients_on_pivot_degrees":list(map(str,dual)),
            "dual_value_on_every_column":"1",
            "common_shift_checked":common_shift}


def main():
    cases=[
        ('m3_nontrivial_phase',[-3,-1,1,3],3,0,1,0),
        ('m4_former_half_phase',[-3,-1,1,3],4,0,2,0),
        ('m6_former_half_phase',[-4,-1,2,5],6,0,3,0),
        ('negative_ell',[-4,-1,2,5],3,4,0,0),
        ('common_shift',[-3,-1,1,3],3,0,1,2),
        ('unit_phase',[-4,-1,2,5],3,0,9,0),
        ('five_rational_rows',[F(-5,2),F(-1,3),F(1,2),F(7,4),F(11,3)],3,0,4,0),
        ('three_rows_negative_half_phase',[-2,0,3],4,3,1,0),
    ]
    results=[check(*case) for case in cases]
    report={"status":"PASS","cases":results,
        "scope":"Exact finite raw-cofactor and nonzero-minor certificates; the universal theorem is proved separately."}
    Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
