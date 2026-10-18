#!/usr/bin/env python3
"""Exact certificate checker; no sampling and no imported exploration code."""
import itertools
import json
import sys
from pathlib import Path
import sympy as sp

d,r,s,t=sp.symbols('d r s t')
R,B,T=sp.symbols('R B T')
E1,E2,E3,E4=sp.symbols('E1 E2 E3 E4')
results=[]

def check(name, lhs, rhs):
    residual=sp.factor(sp.together(lhs-rhs))
    if residual != 0:
        raise ValueError(f'{name}: residual = {residual}')
    results.append(name)

def vandermonde(a):
    return sp.prod(a[j]-a[i] for i in range(len(a)) for j in range(i+1,len(a)))

def binomial_poly(e,k):
    return sp.prod(e-j for j in range(k))/sp.factorial(k)

h={0:sp.Integer(1)}
ees={1:E1,2:E2,3:E3,4:E4}
for k in range(1,5):
    h[k]=sp.expand(sum((-1)**(j-1)*ees[j]*h[k-j] for j in range(1,min(k,4)+1)))

def schur_from_degrees(ks):
    lam=list(reversed([ks[i]-i for i in range(4)]))
    lam=[n for n in lam if n]
    if not lam:
        return sp.Integer(1)
    return sp.expand(sp.Matrix([[h.get(lam[i]-i+j,0) for j in range(len(lam))] for i in range(len(lam))]).det())

def pair_coefficient(k):
    answer=0
    for ks in itertools.combinations(range(k+1),4):
        if sum(ks)!=k:
            continue
        minors=[]
        for exponents in [(d,r,s,t),(0,r,s,t)]:
            minors.append(sp.Matrix([[binomial_poly(e,j) for e in exponents] for j in ks]).det())
        answer+=schur_from_degrees(ks)*sp.cancel((minors[0]-minors[1])/vandermonde([r,s,t]))
    symmetric,remainder,mapping=sp.symmetrize(sp.expand(answer),[r,s,t],formal=True)
    check(f'C{k} symmetric in outside exponents',remainder,0)
    return sp.expand(symmetric.subs({mapping[0][0]:R,mapping[1][0]:B,mapping[2][0]:T}))

cs={k:pair_coefficient(k) for k in range(6,11)}
check('C6 general',cs[6],-d*(d*d-d*R+B)/12)
bsub={B:d*R-d*d}
check('C7 after C6',cs[7].subs(bsub),E1*T*d/48)
check('C8 after C6,C7',cs[8].subs(bsub).subs(E1,0),E2*T*d*(2*R-3*d+15)/720)
common={R:(3*d-15)/2,E1:0}
claim9=-E3*T*d*(d*d+95)/1920
if '--negative-control' in sys.argv:
    claim9+=1
check('C9 after C6,C7,C8',cs[9].subs(bsub).subs(common),claim9)
claim10=-d*T*((5*T+4*d*d-460)*E2**2-(68*T+74*d*d-3050)*E4)/20160
check('C10 after C6 through C9',cs[10].subs(bsub).subs(common).subs(E3,0),claim10)
check('outside cubic product relation',(r-d)*(s-d)*(t-d),r*s*t-d*(r*s+r*t+s*t)+d*d*(r+s+t)-d**3)
full=E4*d*T*(T-d*B+d*d*R-d**3)/288
check('full determinant C10 under C6',full.subs(bsub),d*T*T*E4/288)
comp=d*T*((5*T+4*d*d-460)*E2**2+(2*T-74*d*d+3050)*E4)/20160
check('complement C10',full.subs(bsub)-claim10,comp)
u,v=sp.symbols('u v')
check('rho strict interval identity',(u*u+v*v)**2-4*u*u*v*v,(u*u-v*v)**2)
check('d7 pair C10 residual',((5*T+4*d*d-460)*(u*u+v*v)**2-(68*T+74*d*d-3050)*u*u*v*v).subs({d:7,T:-60}),-564*(u**4+v**4)+2376*u*u*v*v)
check('d7 complement C10 residual',((5*T+4*d*d-460)*(u*u+v*v)**2+(2*T-74*d*d+3050)*u*u*v*v).subs({d:7,T:-60}),-564*(u**4+v**4)-1824*u*u*v*v)
check('d3 pair C10 residual',((5*T+4*d*d-460)*(u*u+v*v)**2-(68*T+74*d*d-3050)*u*u*v*v).subs({d:3,T:40}),-224*(u**4+v**4)-784*u*u*v*v)

# Reconstruct the example with its original nonnegative exponents.
exponents=[0,3,5,8,9]
bs=[-1,1,-v,v]
support={0,1,4}
def candidate_coefficient(k):
    out=0
    for ks in itertools.combinations(range(k+1),4):
        if sum(ks)!=k:
            continue
        offset_det=sp.Matrix([[b**j for j in ks] for b in bs]).det()
        for omitted in support:
            es=[e for j,e in enumerate(exponents) if j!=omitted]
            minor=sp.Matrix([[sp.binomial(e,j) for e in es] for j in ks]).det()
            out+=(-1)**omitted*offset_det*minor
    return sp.factor(out)
for k in range(10):
    check(f'engineered candidate C{k}',candidate_coefficient(k),0)
c10=-864*v*(v*v-1)**2*(v**4-9*v*v+1)
c12=36*v*(v*v-1)**2*(v*v+1)*(23*v**4-282*v*v+23)
check('engineered candidate C10',candidate_coefficient(10),c10)
check('engineered candidate C11',candidate_coefficient(11),0)
check('engineered candidate C12',candidate_coefficient(12),c12)
check('engineered candidate nonzero next factor',sp.rem(23*v**4-282*v*v+23,v**4-9*v*v+1,v),-75*v*v)

payload={'status':'PASS','checks':len(results),'names':results,'sympy':sp.__version__,'optimized':not __debug__}
Path(__file__).with_name('verification_optimized.json' if not __debug__ else 'verification.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps(payload,indent=2))
