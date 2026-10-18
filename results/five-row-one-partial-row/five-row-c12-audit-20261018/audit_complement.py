#!/usr/bin/env python3
"""Exact independent algebra and complete finite discriminant check for complement."""
import json,math,sys
from pathlib import Path
import sympy as S
ROOT=Path(__file__).parent
d,T,q,y,rho,E2,E4=S.symbols('d T q y rho E2 E4')
checks=[]
def equal(label,a,b):
    res=S.factor(a-b)
    if res != 0: raise ValueError(f'{label}: {res}')
    checks.append(label)
def positive_coeffs(label,p):
    cs=S.Poly(p,y).all_coeffs()
    if not all(c>0 for c in cs): raise ValueError(f'{label}: {cs}')
    checks.append(label)
receipt=json.loads((ROOT/'audit_receipt.json').read_text())
computed={k:S.sympify(v) for k,v in receipt['computed'].items()}
A=5*T+4*d*d-460; Q=2*T-74*d*d+3050
N=S.expand(computed['pair12']*4838400/(E2*T*d)).subs({E2:1,E4:0})
L=S.expand(-computed['comp12']*4838400/(E2*T*d)).coeff(E4)
f10=A+Q*rho; f12=N+L*rho
C=(24235-547*d*d)*T*T+(-435*d**4+37590*d*d-1039395)*T+55*d**6-28125*d**4+2236245*d*d-38150575
equal('complement C12 normalization',-computed['comp12']*4838400/(E2*T*d),N*E2**2+L*E4)
equal('complement elimination identity Q*C12-L*C10',Q*f12-L*f10,2*C)
a=24235-547*d*d; b=-435*d**4+37590*d*d-1039395; c=55*d**6-28125*d**4+2236245*d*d-38150575
G=61913*q**4-19914500*q**3+1987324662*q*q-75679352900*q+955731741305
equal('complement half-resultant discriminant',b*b-4*a*c,5*G.subs(q,d*d))
equal('integer root square identity',(2*a*T+b)**2-(b*b-4*a*c),4*a*C)
solved=(460-4*d*d+(74*d*d-3050)*rho)/(5+2*rho)
lo=92-S.Rational(4,5)*d*d
equal('C10 solve without singularity',f10.subs(T,solved),0)
equal('positive difference above lower bound',solved-lo,42*(9*d*d-385)*rho/(5*(5+2*rho)))
equal('quadratic at lower bound',C.subs(T,lo),S.Rational(21,25)*(9*d*d-385)*(7*d**4+10*d*d-220625))
positive_coeffs('9d^2-385 positive for d>=25',S.expand((9*d*d-385).subs(d,25+y)))
positive_coeffs('7d^4+10d^2-220625 positive for d>=25',S.expand((7*d**4+10*d*d-220625).subs(d,25+y)))
positive_coeffs('C0 positive for q>=625',S.expand(c.subs(d*d,q).subs(q,625+y)))
positive_coeffs('quadratic leading coefficient negative for d>=25',S.expand((-a).subs(d,25+y)))
positive_coeffs('lower bound negative for d>=25',S.expand((-lo).subs(d,25+y)))
R=(3*d-15)/2; B=d*R-d*d; M=(d*d-18*d+17)/2
equal('integer positive-root product lower bound',B-R+1,M)
positive_coeffs('R positive for d>=25',S.expand(R.subs(d,25+y)))
positive_coeffs('B positive for d>=25',S.expand(B.subs(d,25+y)))
positive_coeffs('M positive for d>=25',S.expand(M.subs(d,25+y)))
negative_M=S.expand(-C.subs(T,M).subs(d,25+y))
positive_coeffs('C(M) negative for d>=25',negative_M)
u,v,w=S.symbols('u v w')
equal('two-negative-root B inequality decomposition',u*v-w*(u+v),-(u*u+u*v+v*v)-(w-u-v)*(u+v))
r,s,t=S.symbols('r s t')
equal('integer positive-root product identity',(r-1)*(s-1)*(t-1),r*s*t-(r*s+r*t+s*t)+(r+s+t)-1)
small=[]
for dd in range(1,24,2):
    coeff=[int(p.subs(d,dd)) for p in (a,b,c)]
    content=math.gcd(*coeff)
    aa,bb,cc=[p//content for p in coeff]
    if aa==0: raise ValueError(f'd={dd} leading coefficient zero')
    delta=bb*bb-4*aa*cc
    full_delta=int((b*b-4*a*c).subs(d,dd))
    if full_delta!=delta*content*content: raise ValueError('content square identity failed')
    item={'d':dd,'primitive_coefficients':[aa,bb,cc],'content':content,'primitive_discriminant':delta}
    if delta<0: item['exclusion']='negative'
    else:
        root=math.isqrt(delta)
        if root*root==delta: raise ValueError(f'd={dd} has square discriminant')
        item.update({'floor_sqrt':root,'lower_square':root*root,'upper_square':(root+1)**2,'exclusion':'strictly between consecutive squares'})
    small.append(item); checks.append(f'complement d={dd} excluded by discriminant')
if '--negative-control' in sys.argv:
    equal('deliberately corrupted complementary resultant',Q*f12-L*f10,2*C+1)
payload={'status':'PASS','checks':checks,'half_resultant':str(C),'discriminant':str(5*G),'C_at_lower_bound':str(S.factor(C.subs(T,lo))),'C0_shift625':str(S.expand(c.subs(d*d,q).subs(q,625+y))),'negative_C_M_shift25':str(negative_M),'finite_exclusions':small}
(ROOT/'complement_receipt.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps(payload,indent=2))
print('PASS:',len(checks),'checks')
