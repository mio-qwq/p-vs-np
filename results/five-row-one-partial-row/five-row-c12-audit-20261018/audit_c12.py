#!/usr/bin/env python3
"""Independent exact audit by two Cauchy--Binet expansions and Schur determinants.
No quotient-ring calculation or imported exploratory implementation is used.
"""
import itertools, json, math, sys
from functools import lru_cache
from pathlib import Path
import sympy as S
from sympy.functions.combinatorial.numbers import stirling

ROOT=Path(__file__).parent
SOURCE=ROOT.parent/'five-row-c12-20261018'
d,T,E2,E4,rho,q,y=S.symbols('d T E2 E4 rho q y')
R=(3*d-15)/2; B=d*R-d*d
checks=[]
def equal(label,a,b):
    residual=S.factor(a-b)
    if residual != 0: raise ValueError(f'{label}: {residual}')
    checks.append(label)

def schur(ks,es):
    """det(x_j**k_i)/V(x), evaluated at elementary symmetric functions es."""
    n=len(es); lam=tuple(reversed(tuple(k-i for i,k in enumerate(ks))))
    max_h=max(lam)+n-1
    h=[S.Integer(1)]
    for k in range(1,max_h+1):
        h.append(S.expand(sum((-1)**(j-1)*es[j-1]*h[k-j] for j in range(1,min(n,k)+1))))
    def H(k): return h[k] if k>=0 else S.Integer(0)
    return S.expand(S.det(S.Matrix([[H(lam[i]-i+j) for j in range(n)] for i in range(n)])))

@lru_cache(None)
def falling_schur(ks):
    """det(binomial(x_j,k_i))/V(x), in formal elementary coordinates.
    Expand falling factorials into monomials, then Cauchy--Binet again.
    """
    n=len(ks); es=S.symbols('a1:'+str(n+1)); out=0
    coeff=lambda k,l: (-1)**(k-l)*stirling(k,l,kind=1)/S.factorial(k) if l<=k else S.Integer(0)
    for ls in itertools.combinations(range(max(ks)+1),n):
        if any(l>k for l,k in zip(ls,ks)): continue
        cm=S.det(S.Matrix([[coeff(k,l) for l in ls] for k in ks]))
        if cm != 0: out+=cm*schur(ls,es)
    return S.Poly(S.expand(out),*es)

def evaluate(poly,es):
    return S.expand(poly.as_expr().subs(dict(zip(poly.gens,es)), simultaneous=True))

def pair_coefficient(total):
    n=4; out=0
    offset_es=(0,E2,0,E4)
    esd=(d+R,d*R+B,d*B+T,d*T)
    es0=(R,B,T,0)
    for ks in itertools.combinations(range(total-2),n):
        if sum(ks)!=total: continue
        offset=schur(ks,offset_es)
        if offset==0: continue
        f=falling_schur(ks)
        # Both exponent Vandermonde ratios equal T under B=dR-d^2.
        out += offset*T*(evaluate(f,esd)-evaluate(f,es0))
    return S.factor(out)

def full_coefficient(total):
    n=5; out=0
    offset_es=(0,E2,0,E4,0)
    exponent_es=(d+R,d*R+B,d*B+T,d*T,0)
    for ks in itertools.combinations(range(total-5),n):
        if sum(ks)!=total: continue
        offset=schur(ks,offset_es)
        if offset==0: continue
        out+=offset*evaluate(falling_schur(ks),exponent_es)
    return S.factor(E4*d*T*T*out)

source=json.loads((SOURCE/'coefficients.json').read_text())
computed={}
for k in (10,12):
    for label,fn in [('pair',pair_coefficient),('full',full_coefficient)]:
        key=f'{label}{k}'; computed[key]=fn(k)
        equal(key,computed[key],S.sympify(source[key]))
        print(key,computed[key],flush=True)
computed['comp12']=S.factor(computed['full12']-computed['pair12'])
equal('comp12 subtraction',computed['comp12'],S.sympify(source['comp12']))
if '--negative-control' in sys.argv:
    equal('deliberately corrupted C12',computed['pair12'],S.sympify(source['pair12'])+1)

A=5*T+4*d*d-460; P=68*T+74*d*d-3050
N=S.expand(computed['pair12']*4838400/(E2*T*d)).subs({E2:1,E4:0})
K=-S.expand(computed['pair12']*4838400/(E2*T*d)).coeff(E4)
f10=A-P*rho; f12=N-K*rho
half=48*T*T*d*d-24240*T*T+90*T*d**4-55860*T*d*d+1875930*T+55*d**6-28125*d**4+2236245*d*d-38150575
# Multiplicative identity establishes necessity without dividing by P or K.
equal('pair elimination identity K*C10-P*C12',K*f10-P*f12,2*half)
F=41*q**4-11300*q**3-5027466*q*q-242872100*q+2999439785
a=48*d*d-24240; b=90*d**4-55860*d*d+1875930; c=55*d**6-28125*d**4+2236245*d*d-38150575
equal('pair half-resultant discriminant',b*b-4*a*c,-60*F.subs(q,d*d))
equal('integer-root square identity',(2*a*T+b)**2-(b*b-4*a*c),4*a*half)
shifted=S.Poly(S.expand(F.subs(q,529+y)),y)
if not all(c>0 for c in shifted.all_coeffs()): raise ValueError('F(529+y) not coefficient-positive')
checks.append('F(529+y) has strictly positive coefficients')
small=[]
for dd in (1,5,9,13,17,21):
    delta=int((-60*F).subs(q,dd*dd))
    if delta<0:
        item={'d':dd,'discriminant':delta,'exclusion':'negative'}
    else:
        floor=math.isqrt(delta)
        if floor*floor==delta: raise ValueError(f'd={dd} has square discriminant')
        item={'d':dd,'discriminant':delta,'floor_sqrt':floor,'lower_square':floor*floor,'upper_square':(floor+1)**2,'exclusion':'strictly between consecutive squares'}
    small.append(item)
    checks.append(f'pair d={dd} excluded by discriminant')
print('F(529+y)=',shifted.as_expr(),flush=True)
print(json.dumps(small,indent=2),flush=True)
receipt={'status':'PASS','method':'double Cauchy-Binet with monomial and Schur expansion','sympy':S.__version__,'checks':checks,'computed':{k:str(v) for k,v in computed.items()},'pair_half_resultant':str(half),'pair_discriminant':str(-60*F),'F_shift529':str(shifted.as_expr()),'finite_exclusions':small}
(ROOT/'audit_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS:',len(checks),'checks',flush=True)
