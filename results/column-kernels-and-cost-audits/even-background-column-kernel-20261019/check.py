#!/usr/bin/env python3
"""Exact raw-permutation checks for the consecutive-even background theorem."""
from fractions import Fraction as F
from itertools import permutations
from math import comb
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def add(a,b):
    out=[F(0)]*max(len(a),len(b))
    for i,x in enumerate(a): out[i]+=x
    for i,x in enumerate(b): out[i]+=x
    return trim(out)


def trim(a):
    while len(a)>1 and a[-1]==0: a.pop()
    return a


def multiply(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]+=x*y
    return trim(out)


def power_shift(a,e):
    return [F(comb(e,j))*a**(e-j) for j in range(e+1)]


def product(values):
    out=F(1)
    for value in values: out*=value
    return out


def raw_terms(a,e,c):
    n=len(a)
    cached=[[power_shift(x,p) for p in e] for x in a]
    terms=[[F(0)] for _ in a]
    for p in permutations(range(n)):
        sign=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term=[F(sign)]
        for s,col in enumerate(p): term=multiply(term,cached[s][col])
        s=p.index(c)
        terms[s]=add(terms[s],term)
    return terms


def rank(columns):
    n=len(columns)
    d=max(map(len,columns))
    matrix=[[col[h] if h<len(col) else F(0) for col in columns] for h in range(d)]
    r=0
    for c in range(n):
        pivot=next((i for i in range(r,d) if matrix[i][c]),None)
        if pivot is None: continue
        matrix[r],matrix[pivot]=matrix[pivot],matrix[r]
        v=matrix[r][c]
        matrix[r]=[x/v for x in matrix[r]]
        for i in range(d):
            if i!=r and matrix[i][c]:
                v=matrix[i][c]
                matrix[i]=[x-v*y for x,y in zip(matrix[i],matrix[r])]
        r+=1
    return r


def residue_data(a,k):
    n=len(a)
    hp=[product(a[s]-a[t] for t in range(n) if t!=s) for s in range(n)]
    groups={}
    for s in range(n):
        for t in range(s+1,n):
            direct_s=(a[s]-a[t])**k/(hp[s]*product(a[r]-a[t]
                         for r in range(n) if r not in [s,t]))
            direct_t=(a[t]-a[s])**k/(hp[t]*product(a[r]-a[s]
                         for r in range(n) if r not in [s,t]))
            beta=(-1)**(n-1)*(a[s]-a[t])**(k+1)/(hp[s]*hp[t])
            require(direct_s==beta,"s residue mismatch")
            require(direct_t==(-1)**(k+1)*beta,"t residue mismatch")
            groups.setdefault(a[s]+a[t],[]).append((s,t,beta))
    for q,pairs in groups.items():
        vertices=[v for s,t,beta in pairs for v in [s,t]]
        require(len(vertices)==len(set(vertices)),"colliding pairs share a vertex")
    return hp,groups


def check(a,k,d=0):
    a=[F(x) for x in a]
    n=len(a)
    e=sorted(list(range(0,2*n-3,2))+[k])
    require(len(e)==n and len(set(e))==n,"invalid exponents")
    c=e.index(k)
    polynomials=raw_terms(a,e,c)
    hp,groups=residue_data(a,k)
    delta=product(a[j]-a[i] for i in range(n) for j in range(i+1,n))
    K=F((-1)**(n-1+c),2**k)*delta
    for s in range(n):
        rhs=[F(comb(k,h))*(2*a[s])**(k-h) for h in range(k+1)]
        for i in range(n):
            for j in range(i+1,n):
                if s not in [i,j]: rhs=multiply(rhs,[a[i]+a[j],F(1)])
        rhs=[K*x/hp[s] for x in rhs]
        lhs=[x/F(2**h) for h,x in enumerate(polynomials[s])]
        require(trim(lhs)==trim(rhs),"cleared rational factorization mismatch")
    result={"offsets":[str(x) for x in a],"exponents":e,"column":c,
            "rank":rank(polynomials),"colliding_pair_sum_groups":
            sum(len(p)>1 for p in groups.values())}
    if k%2:
        rows=[]
        for j in range(1,n):
            pairs=groups[a[0]+a[j]]
            beta0=next(beta for s,t,beta in pairs if s==0 and t==j)
            row=[F(0)]*n
            for s,t,beta in pairs:
                row[s]+=beta/beta0
                row[t]+=beta/beta0
                require(t<=j and ((s,t)==(0,j) or t<j),"nontriangular pair")
            require(row[0]==row[j]==1 and all(x==0 for x in row[j+1:]),
                    "nontriangular normalized residue")
            rows.append(row)
        M=max([F(1)]+[abs(x) for row in rows for x in row])
        epsilon=1/(2*M+2)
        positive=[sum(epsilon**j*rows[j][s] for j in range(n-1)) for s in range(n)]
        require(all(x>0 for x in positive),"explicit positive functional failed")
        result.update({"residue_rows":[[str(x) for x in row] for row in rows],
                       "M":str(M),"epsilon":str(epsilon),
                       "positive_functional_values":[str(x) for x in positive]})
    else:
        require(result["rank"]==n,"even-power control not independent")
    if d:
        shifted=raw_terms(a,[x+d for x in e],c)
        common=[F(1)]
        for x in a: common=multiply(common,power_shift(x,d))
        for s in range(n):
            require(shifted[s]==multiply(common,polynomials[s]),"common shift failure")
        result["verified_common_exponent_shift"]=d
    if n==7 and a==list(map(F,range(7))) and k==1:
        u=[-1,1,1,0,-1,-1,1]
        combination=[F(0)]
        for weight,p in zip(u,polynomials): combination=add(combination,[weight*x for x in p])
        require(combination==[0] and result["rank"]==6,"seven-row kernel mismatch")
        require(sum(F(v)*q for v,q in zip(u,positive))==0,"dual/kernel orthogonality failure")
        result["sharpness_kernel"]=u
        result["polynomials"]=[[str(x) for x in p] for p in polynomials]
    return result


def main():
    cases=[([-2,0,3],1,0),([-4,-1,2,6],3,0),([-3,-1,1,3],7,0),
           ([-3,-1,1,3],6,0),([-4,-2,0,2,4],8,0),
           ([F(-3,2),F(-1,3),F(2,3),F(7,4)],5,2),(list(range(7)),1,0)]
    output=[]
    for a,k,d in cases:
        result=check(a,k,d)
        output.append(result)
        print(json.dumps({key:result[key] for key in ["offsets","exponents","rank"]}),flush=True)
    report={"status":"PASS","cases":output,
            "scope":"exact finite certificates supporting a separate all-size proof"}
    Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
    print("PASS: raw expansions, rational factorization, colliding-pole residues, positive functionals, and sharpness kernel")


if __name__=='__main__': main()
