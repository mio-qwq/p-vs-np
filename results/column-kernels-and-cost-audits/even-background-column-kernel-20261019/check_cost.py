#!/usr/bin/env python3
"""Exact realization of Laurent residues as coefficient certificates."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json

from check import require, raw_terms, product, multiply, residue_data


def translate(p, alpha):
    return [sum(p[d]*comb(d,r)*alpha**(d-r)
                for d in range(r,len(p))) for r in range(len(p))]


def residue_coefficients(Q, alpha, degree, beta):
    shifted=translate(Q,alpha)
    m=next(i for i,x in enumerate(shifted) if x)
    require(m>0,"requested point is not a root")
    q=shifted[m:]
    v=[1/q[0]]
    for j in range(1,m):
        v.append(-sum((q[i] if i<len(q) else 0)*v[j-i]
                      for i in range(1,j+1))/q[0])
    coeff=[]
    for d in range(degree+1):
        value=sum(F(comb(d,r),2**d)*alpha**(d-r)*v[m-1-r]
                  for r in range(min(d,m-1)+1))
        coeff.append(value/beta)
    return coeff,m


def dot(coeff,p):
    return sum(x*y for x,y in zip(coeff,p))


def check(a,k):
    a=list(map(F,a));n=len(a)
    e=sorted(list(range(0,2*n-3,2))+[k]);c=e.index(k)
    T=raw_terms(a,e,c)
    degree=max(len(p) for p in T)-1
    delta=product(a[j]-a[i] for i in range(n) for j in range(i+1,n))
    K=F((-1)**(n-1+c),2**k)*delta
    Q=[K]
    for i in range(n):
        for j in range(i+1,n):Q=multiply(Q,[a[i]+a[j],F(1)])
    hp,groups=residue_data(a,k)
    coefficient_rows=[];rows=[];multiplicities=[]
    for j in range(1,n):
        pairs=groups[a[0]+a[j]]
        beta=next(b for s,t,b in pairs if (s,t)==(0,j))
        coeff,m=residue_coefficients(Q,-a[0]-a[j],degree,beta)
        actual=[dot(coeff,p) for p in T]
        expected=[F(0)]*n
        for s,t,b in pairs:
            expected[s]+=b/beta;expected[t]+=b/beta
        require(actual==expected,"coefficient residue differs from direct residue")
        require(m==len(pairs),"global pole multiplicity mismatch")
        coefficient_rows.append(coeff);rows.append(actual);multiplicities.append(m)
    M=max([F(1)]+[abs(v) for row in rows for v in row])
    epsilon=1/(2*M+2)
    coeff=[sum(epsilon**j*coefficient_rows[j][d] for j in range(n-1))
           for d in range(degree+1)]
    values=[dot(coeff,p) for p in T]
    require(all(v>0 for v in values),"coefficient certificate is not strictly positive")
    return {"offsets":list(map(str,a)),"exponents":e,"pole_multiplicities":multiplicities,
            "coefficient_certificate":list(map(str,coeff)),
            "positive_values":list(map(str,values))}


def main():
    cases=[([-3,-1,1,3],1),([-4,-2,0,2,4],3),
           ([F(-3,2),F(-1,3),F(2,3),F(7,4)],5)]
    results=[check(a,k) for a,k in cases]
    Path(__file__).with_name('cost-results.json').write_text(
        json.dumps({"status":"PASS","cases":results},indent=2)+'\n')
    print('PASS: exact Laurent coefficient certificates, including repeated global roots')


if __name__=='__main__':main()
