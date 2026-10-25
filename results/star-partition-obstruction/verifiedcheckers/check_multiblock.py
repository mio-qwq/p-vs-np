"""Locally authored exact binomial certificate; no external code or float use."""
from math import comb
from fractions import Fraction
import json

def count(n,a,c):
    N=n-a-c
    out=0
    for x in range(a+1):
        for y in range(c+1):
            mul=comb(a,x)*comb(c,y)
            for z in range(N+1):
                T=lambda w:int(w>=n//2)
                d=T(a-x+c-y+z)-T(a-x+y+z)-T(x+c-y+z)+T(x+y+z)
                assert d in (-1,0,1)
                if d: out+=mul*comb(N,z)
    return out

def run(n,r,b):
    assert n%2==0 and r%2==0 and r*b<=n and n-r>=12
    h=r//2
    numerator=0
    for a in range(1,h+1):
        for c in range(1,h+1):
            v=count(n,a,c)
            numerator+=comb(h,a)*comb(h,c)*b**(a+c)*v
            # Supplier's support-conditional bound squared, avoiding sqrt.
            assert v*v*2048**2*a*c*(n-a-c)>=2**(2*n)
    p=Fraction(numerator,(b+1)**r*2**n)
    assert p*p*4096**2*r*r*n>=1
    if (n,r,b)==(14,2,7):assert p==Fraction(21021,65536)
    return dict(n=n,r=r,b=b,probability=str(p),conditional_and_global_bounds=True)

if __name__=='__main__':
    cases=[(14,2,7),(16,2,7),(16,4,3),(20,4,3),(24,6,3),
           (32,8,3),(32,4,7),(40,8,3),(64,8,7),(64,16,3)]
    print(json.dumps({'status':'PASS','arithmetic':'exact integers/Fraction',
                      'cases':[run(*c) for c in cases]},indent=2))
