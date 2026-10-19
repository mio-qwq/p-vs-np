#!/usr/bin/env python3
from fractions import Fraction as Q
from math import prod,factorial
from pathlib import Path
import json

def elementary_all(xs,r):
    a=[1]+[0]*r
    for x in xs:
        for j in range(r,0,-1):a[j]+=x*a[j-1]
    return a

def complete_all(xs,r):
    a=[1]+[0]*r
    for x in xs:
        for j in range(1,r+1):a[j]+=x*a[j-1]
    return a

def check(r,b,c):
    a=[b+c*j for j in range(2*r+2)]
    e=elementary_all(a[:r],r);h=complete_all(a[r:],r)
    q=[sum((Q((-1)**j*e[j]*h[l-j],prod(r-i for i in range(j))*prod(r+2+i for i in range(l-j))) for j in range(l+1)),Q(0)) for l in range(r+1)]
    pred=[Q(c**l*(r+1)**l,factorial(l)) for l in range(r+1)]
    if q!=pred:raise RuntimeError((r,b,c,q,pred))
    return {'r':r,'b':b,'c':c,'q':list(map(str,q))}

if __name__=='__main__':
    data=[check(r,b,c) for r in range(1,31) for b,c in [(0,1),(7,-3),(19,5)]]
    Path(__file__).with_name('qclosed-results.json').write_text(json.dumps(data,indent=2)+'\n')
    print('PASS: 90 affine families, all 0<=l<=r, 1<=r<=30.')
