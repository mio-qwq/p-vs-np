#!/usr/bin/env python3
"""Exact signed-permutation checks; no symbolic determinant library required."""
from fractions import Fraction as F
from itertools import permutations
from math import comb, factorial, prod
from pathlib import Path
import json
import random

ROOT=Path(__file__).resolve().parents[1]

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def trim(p):
    while len(p)>1 and p[-1]==0:
        p.pop()
    return p

def mul(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j]+=x*y
    return trim(out)

def addto(out,p,sgn=1):
    for j,x in enumerate(p): out[j]+=sgn*x

def coefficient(p,h):
    return p[h] if 0<=h<len(p) else 0

def delta(a):
    return prod(a[j]-a[i] for i in range(len(a)) for j in range(i+1,len(a)))

def degree(p):
    return len(trim(p.copy()))-1 if any(p) else -1

def direct(a,e,i,p,c):
    n=len(a); total=sum(e)
    table=[[[comb(k,h)*v**(k-h) for h in range(k+1)] for k in e] for v in a]
    fibers=[[0]*(total+1) for _ in range(3)]
    terms=[[0]*(total+1) for _ in a]
    full=[0]*(total+1)
    for perm in permutations(range(n)):
        sign=(-1)**sum(perm[u]>perm[v] for u in range(n) for v in range(u+1,n))
        term=[1]
        for row,col in enumerate(perm): term=mul(term,table[row][col])
        red=sum((row==i and col!=c) or (row==p and col==c) for row,col in enumerate(perm))
        require(0<=red<=2,'unexpected red count')
        addto(fibers[red],term,sign)
        addto(terms[perm.index(c)],term,sign)
        addto(full,term,sign)
    return [trim(x) for x in fibers],[trim(x) for x in terms],trim(full)

def asstr(x):
    return str(x)

def check_case(case):
    a=case['a']; e=case['e']; i=case.get('i',0);p=case['p'];c=case['c']
    n=len(a);m=n-1;k=e[c];d=sum(e)-k-comb(m,2);D=k+d;A=sum(a)
    require(len(set(a))==n and len(set(e))==n,'distinctness')
    require(a[i]==min(a) or a[i]==max(a),'separation')
    R=prod(F(a[s]-a[i],a[s]-a[p]) for s in range(n) if s not in (i,p))
    remaining=[v for j,v in enumerate(e) if j!=c]
    B1=sum(remaining);B2=sum(v*v for v in remaining)
    v=F(B2-F(B1*B1,m)-F(m*(m*m-1),12),m*(m*m-1))
    mu=F(d,m)
    alpha=(mu*mu-mu+(m-1)*v)/2
    beta=F(d*(d-1)-2*m*alpha,m*(m-1))
    H=prod(factorial(h) for h in range(m))
    L=[F((-1)**(s+c)*delta([x for row,x in enumerate(a) if row!=s])*delta(remaining),H) for s in range(n)]
    fibers,terms,full=direct(a,e,i,p,c)
    require(degree(full)==D-m,'full alternant degree')
    require(fibers[0]==terms[i] and fibers[2]==terms[p],'outer fiber identity')
    for h in range(sum(e)+1):
        require(coefficient(fibers[1],h)==coefficient(full,h)-coefficient(terms[i],h)-coefficient(terms[p],h),'middle identity')
    for s in range(n):
        require(degree(terms[s])==D,'cofactor exact degree')
        require(coefficient(terms[s],D)==L[s],'cofactor leading constant')
        normalized_first=mu*(A-a[s])+k*a[s]
        require(coefficient(terms[s],D-1)==L[s]*normalized_first,'cofactor first correction')
        other=[x for row,x in enumerate(a) if row!=s]
        normalized_second=F(k*(k-1),2)*a[s]**2+k*mu*a[s]*(A-a[s])+alpha*sum(x*x for x in other)+beta*sum(other[u]*other[w] for u in range(m) for w in range(u+1,m))
        require(coefficient(terms[s],D-2)==L[s]*normalized_second,'cofactor second correction')
    require(L[p]==-R*L[i],'ratio formula')
    require(coefficient(fibers[1],D)==L[i]*(R-1),'equation (2)')
    if R!=1:
        branch='leading'; expected=D
    elif n*k!=D:
        branch='first correction';expected=D-1
        require(coefficient(fibers[1],D-1)==-L[i]*(a[i]-a[p])*(k-mu),'equation (3)')
    else:
        require(v>0,'strict exponent variance at resonance')
        require(n>=4,'n3 leading equality impossible')
        want=-L[i]*v*(a[i]-a[p])*(A-F(n,2)*(a[i]+a[p]))
        require(coefficient(fibers[1],D-2)==want,'equation (4)')
        if want:
            branch='second correction';expected=D-2
        else:
            branch='residual illustrative';expected=case.get('degree',degree(fibers[1]))
    require(degree(fibers[1])==expected,'predicted degree')
    if 'middle' in case:
        require(fibers[1]==case['middle'],'exact expected middle polynomial')
    require(all(any(poly) for poly in fibers),'all illustrative fibers nonzero')
    return {'name':case['name'],'n':n,'offsets':a,'exponents':e,'i':i,'p':p,'c':c,'R':asstr(R),'v':asstr(v),'D':D,'degrees':[degree(x) for x in fibers],'branch':branch,'middle':list(map(asstr,fibers[1])) if case.get('record_full') else None}

def main():
    cases=[
      {'name':'n3 generic','a':[0,1,4],'e':[0,2,5],'p':2,'c':1},
      {'name':'prior leading cancellation','a':[0,1,2,3],'e':[0,1,2,3],'p':3,'c':3,'middle':[-42,-54,-18],'record_full':True},
      {'name':'n4 resonance','a':[0,1,2,3],'e':[0,1,2,4],'p':3,'c':1,'degree':1,'middle':[36,24],'record_full':True},
      {'name':'n5 second correction','a':[0,1,2,4,6],'e':[0,1,2,3,5],'p':3,'c':1,'record_full':True},
      {'name':'n5 simultaneous residual','a':[0,2,4,14,15],'e':[0,1,2,3,5],'p':3,'c':1,'degree':2,'middle':[807206400,-214294080,-23543520],'record_full':True},
      {'name':'n5 four-top-coefficient cancellation','a':[0,2,4,14,15],'e':[0,7,10,17,22],'p':3,'c':2,'degree':46,'record_full':True},
      {'name':'n5 exponent-shifted second correction','a':[0,1,2,4,6],'e':[3,4,5,6,8],'p':3,'c':1},
      {'name':'n5 reflected second correction','a':[0,-1,-2,-4,-6],'e':[0,1,2,3,5],'p':3,'c':1},
      {'name':'n5 reordered second correction','a':[4,0,6,1,2],'e':[5,2,1,0,3],'i':1,'p':0,'c':2},
      {'name':'n6 generic','a':[0,1,2,3,4,5],'e':[0,1,2,3,4,5],'p':5,'c':4},
    ]
    rng=random.Random(20261019)
    for t in range(30):
        n=3+t%3
        a=sorted(rng.sample(range(-8,14),n)); e=rng.sample(range(n+4),n)
        cases.append({'name':f'random {t+1}','a':a,'e':e,'p':rng.randrange(1,n),'c':rng.randrange(n)})
    results=[check_case(case) for case in cases]
    summary={'status':'passed','case_count':len(results),'checks':'exact integer signed-permutation determinant expansion; all cofactor first/second coefficients; all theorem branches; full residual certificates','cases':results}
    dest=ROOT/'checker'/'results.json';dest.write_text(json.dumps(summary,indent=2)+'\n')
    print(f'PASS: {len(results)} exact cases; all three sufficient-condition branches and residual certificates verified.')
    print(dest)

if __name__=='__main__': main()
