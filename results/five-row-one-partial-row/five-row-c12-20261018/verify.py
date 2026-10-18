#!/usr/bin/env python3
"""Exact C12 certificate for the five-row one-partial-row theorem.

Derives coefficients in two quotient rings and checks every elimination,
positivity certificate and finite discriminant exclusion in PROOF.md.
No exponent sampling or mask search. No imports from earlier investigations.
"""
import itertools
import json
import math
import sys
from pathlib import Path
import sympy as S

x,y,d,T,E2,E4,rho,q,h=S.symbols('x y d T E2 E4 rho q h')
R=(3*d-15)/2
B=d*R-d*d
checks=[]
def check(name,actual,expected=0):
    residual=S.factor(actual-expected)
    if residual != 0:
        raise ValueError(f'{name}: residual = {residual}')
    checks.append(name)

def require(name,condition):
    if not condition:
        raise ValueError(name)
    checks.append(name)

# The offset and exponent evaluation maps contribute exactly V(b), V(r,s,t).
qx=x**4+E2*x*x+E4
qy=y**3-R*y*y+B*y-T
px=[S.Poly(S.rem(x**k,qx,x),x) for k in range(10)]
py=[S.Poly(1,y)]
for k in range(1,10):
    py.append(S.Poly(S.expand(S.rem(py[-1].as_expr()*(y-k+1)/k,qy,y)),y))
fall=[S.prod(d-j for j in range(k))/S.factorial(k) for k in range(10)]
# M[row][column] is a coefficient list after factoring z**row.
M=[[[S.expand(px[k].nth(i)*fall[k]) if k else S.Integer(0) for k in range(i,i+7)]]+
   [[S.expand(px[k].nth(i)*py[k].nth(j)) for k in range(i,i+7)] for j in range(3)]
   for i in range(4)]
def convolve(a,b,n):
    out=[S.Integer(0)]*(n+1)
    for i,aa in enumerate(a):
        if aa != 0:
            for j,bb in enumerate(b[:n-i+1]):
                if bb != 0:
                    out[i+j]+=aa*bb
    return [S.expand(v) for v in out]
def coefficient(k,full=False):
    n=k-6
    out=0
    for p in itertools.permutations(range(4)):
        inv=sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        prod=[S.Integer(1)]
        for i,j in enumerate(p):
            series=M[i][j][:n+1].copy()
            if full and i==0 and j==1:
                series[0]=S.Integer(0)
            prod=convolve(prod,series,n)
        out+=(-1)**inv*prod[n]
    return S.factor(out)

A=5*T+4*d*d-460
P=68*T+74*d*d-3050
Q=2*T-74*d*d+3050
N=(33*d*d-600*d+7335)*T+25*d**4-480*d**3+2830*d*d+55200*d-630695
K=(468*d*d-8160*d+90060)*T+490*d**4-8880*d**3+75580*d*d+366000*d-4015910
J=(232*d*d-240*d-6760)*T-490*d**4+8880*d**3-75580*d*d-366000*d+4015910
pair10=-d*T*(A*E2**2-P*E4)/20160
full10=d*T*T*E4/288
pair12=E2*d*T*(N*E2**2-K*E4)/4838400
if '--negative-control' in sys.argv:
    pair12+=1
full12=-E2*E4*d*T*T*(d*d-12*d+119)/6912
comp12=-E2*d*T*(N*E2**2+J*E4)/4838400
for k in [6,7,8,9,11]:
    check(f'pair C{k} under prior necessary relations',coefficient(k))
    check(f'full C{k} under prior necessary relations',coefficient(k,True))
check('pair C10',coefficient(10),pair10)
check('full C10',coefficient(10,True),full10)
check('complement C10',full10-pair10,d*T*(A*E2**2+Q*E4)/20160)
check('pair C12',coefficient(12),pair12)
check('full C12',coefficient(12,True),full12)
check('complement C12',full12-pair12,comp12)

H=(48*d*d-24240)*T*T+(90*d**4-55860*d*d+1875930)*T+55*d**6-28125*d**4+2236245*d*d-38150575
C=(24235-547*d*d)*T*T+(-435*d**4+37590*d*d-1039395)*T+55*d**6-28125*d**4+2236245*d*d-38150575
check('pair elimination without denominators',A*K-P*N,2*H)
check('complement elimination without denominators',Q*N-A*J,2*C)
check('pair resultant',S.resultant(A-P*rho,N-K*rho,rho),2*H)
check('complement resultant',S.resultant(A+Q*rho,N+J*rho,rho),2*C)

F=41*q**4-11300*q**3-5027466*q*q-242872100*q+2999439785
check('pair T discriminant',S.discriminant(H,T),-60*F.subs(q,d*d))
Fshift=41*h**4+75456*h**3+45880320*h*h+9229344768*h+5573836800
check('pair positivity beyond d=23',F.subs(q,529+h),Fshift)
require('pair positivity certificate coefficients',all(v>0 for v in S.Poly(Fshift,h).all_coeffs()))

lo=92-S.Rational(4,5)*d*d
Trho=(460-4*d*d+(74*d*d-3050)*rho)/(5+2*rho)
check('complement solve C10',A.subs(T,Trho)+Q.subs(T,Trho)*rho)
check('complement T above lower endpoint',Trho-lo,42*rho*(9*d*d-385)/(5*(5+2*rho)))
check('complement lower endpoint sign',C.subs(T,lo),S.Rational(21,25)*(9*d*d-385)*(7*d**4+10*d*d-220625))
check('complement lower endpoint second factor positive',
      (7*q*q+10*q-220625).subs(q,625+h),7*h*h+8760*h+2520000)
C0shift=55*h**3+75000*h*h+31533120*h+3800908800
check('complement C0 positive beyond d=25',C.subs(T,0).subs(d*d,625+h),C0shift)
require('complement C0 certificate coefficients',all(v>0 for v in S.Poly(C0shift,h).all_coeffs()))
Mbound=(d*d-18*d+17)/2
check('integer-positive-root product bound',B-R+1,Mbound)
check('product bound positive beyond d=25',Mbound.subs(d,25+h),(h*h+32*h+192)/2)
CMshift=-S.Rational(1197,4)*h**6-S.Rational(72099,2)*h**5-1756644*h**4-44343384*h**3-613489632*h*h-4440240000*h-13283343360
check('complement C(M) negative beyond d=25',C.subs(T,Mbound).subs(d,25+h),CMshift)
require('complement C(M) certificate coefficients',all(v<0 for v in S.Poly(CMshift,h).all_coeffs()))

# Exhaustion is over a rigorously bounded list of d, not over masks or gaps.
# An integer root of a nondegenerate integral quadratic requires a square
# discriminant: Delta=(2*a*T+b)**2. Rational roots require the same.
tables={}
for label,poly,ds in [('pair',H,range(1,23,4)),('complement',C,range(1,25,2))]:
    table=[]
    for D in ds:
        f=S.Poly(poly.subs(d,D),T).primitive()[1]
        if f.LC()<0:
            f=-f
        require(f'{label} d={D} remains quadratic',f.degree()==2)
        disc=int(S.discriminant(f.as_expr(),T))
        root=math.isqrt(disc) if disc>=0 else None
        require(f'{label} d={D} negative or nonsquare discriminant',disc<0 or root*root<disc<(root+1)*(root+1))
        table.append({'d':D,'primitive_quadratic':str(f.as_expr()),'discriminant':disc,'floor_sqrt':root})
    tables[label]=table

payload={'status':'PASS','checks':len(checks),'names':checks,'method':'exact quotient-ring C12, polynomial identities, positivity certificates and bounded integer discriminants','sympy':S.__version__,'optimized':not __debug__,'discriminant_tables':tables}
out=Path(__file__).with_name('verification_optimized.json' if not __debug__ else 'verification.json')
out.write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps(payload,indent=2))
