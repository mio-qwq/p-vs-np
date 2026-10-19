#!/usr/bin/env python3
"""Exact certificate for the degree-eight quartic-square obstruction.

No floating-point calculations. Explicit checks survive python -O.
"""
import json
from pathlib import Path
import sympy as s


def require(condition, message):
    if condition is not True and condition != True:
        raise RuntimeError(message)


def equal(a, b, message):
    require(s.cancel(a-b) == 0, message)


n, L, b, c, d, x, y, u, v, t = s.symbols('n L b c d x y u v t')
Q = L**4+b*L**2+c*L+d
P = s.Poly(Q**2, L)
hh = [s.Integer(1)] + [s.factor(P.coeff_monomial(L**(8-r))*s.rf(n,r)/s.ff(8,r)) for r in range(1,9)]
p = [n]
for r in range(1,9):
    p.append(s.factor(r*hh[r]-sum(p[j]*hh[r-j] for j in range(1,r))))
parameters = {b:14/(n*(n+1)), c:56*x/(n*(n+1)*(n+2))}
parameters[d] = s.solve(p[4].subs(parameters)-y,d)[0]
p = [s.factor(q.subs(parameters)) for q in p]
equal(p[1],0,'p1 normalization')
equal(p[2],1,'p2 normalization')
equal(p[3],x,'p3 normalization')
equal(p[4],y,'p4 normalization')
k = (n**2+22*n+42)/(3*n*(n+1))
e = (3*n**3+51*n**2+216*n+280)/(5*n*(n+1)*(n+2))
f = (n**2+15*n+35)/(n*(n+1))
g = -(n**4+44*n**3+491*n**2+1624*n+1470)/(15*n**2*(n+1)**2)
h = (17*n**4+382*n**3+3127*n**2+11162*n+14700)/(2*n*(n+1)*(n+2)*(n+3))
i = -(n**6+105*n**5+2236*n**4+20121*n**3+87205*n**2+175056*n+123480)/(3*n**2*(n+1)**2*(n+2)*(n+3))
j = (n**8+36*n**7+1186*n**6+22196*n**5+212774*n**4+1071874*n**3+2822309*n**2+3588564*n+1728720)/(30*n**3*(n+1)**3*(n+2)*(n+3))
ell = 4*(3*n**3+44*n**2+167*n+196)/(15*n*(n+1)*(n+2))
equal(p[5],k*x,'p5 formula')
equal(p[6],e*x*x+f*y+g,'p6 formula')
equal(p[8],h*y*y+i*y+j-ell*x*x,'p8 formula')


def positive_polynomial(expr, variable, label, strict=True):
    poly=s.Poly(s.expand(expr),variable)
    coeffs=poly.all_coeffs()
    require(all(q>0 if strict else q>=0 for q in coeffs),label)
    return [str(q) for q in coeffs]


def positive_rational(expr,label,shift=0):
    numerator,denominator=s.cancel(expr).as_numer_denom()
    dc=positive_polynomial(denominator,n,label+' denominator',strict=False)
    require(any(s.Rational(q)>0 for q in dc),label+' denominator nonzero')
    nc=positive_polynomial(numerator.subs(n,v+shift),v,label+' shifted numerator')
    return {'numerator':str(s.factor(numerator)), 'denominator':str(s.factor(denominator)),
            'shift':shift, 'shifted_numerator_coefficients_descending':nc}

certificate={'identity_checks':'passed','basic_positivity':{},'large_n':{},'finite_n':{}}
for name,expr in [('k',k),('e',e),('f',f),('-g',-g),('ell',ell),('h-1',h-1)]:
    certificate['basic_positivity'][name]=positive_rational(expr,name)
y0=s.factor(-g/f)
certificate['basic_positivity']['k²-e*y0']=positive_rational(k*k-e*y0,'k²-e*y0')
F=(h-1)*y*y+i*y+j
J=F-ell*y
G=F*(k*k-e*y)-ell*(f*y*y+g*y)
R=s.factor(e*F/ell+f*y+g)
T=R*R-y**3
for q in range(5):
    coefficient=s.factor(s.diff(T,y,q).subs(y,y0)/s.factorial(q))
    certificate['large_n'][f'T coefficient u^{q}']=positive_rational(coefficient,f'T coefficient {q}',24)
certificate['large_n']['R(y0)']=positive_rational(R.subs(y,y0),'R(y0)',24)
U=3/n+s.Rational(1,10)
for N in range(4,24):
    scalars={name:s.factor(expr.subs(n,N)) for name,expr in {
        'U-y0':U-y0,'J(U)':J.subs(y,U),'Jprime(U)':s.diff(J,y).subs(y,U),
        'k²-e*U':k*k-e*U}.items()}
    for name,value in scalars.items():require(value>0,f'n={N}: {name}')
    transformed=s.cancel(G.subs(n,N).subs(y,(y0.subs(n,N)+U.subs(n,N)*t)/(1+t))*(1+t)**3)
    coeffs=positive_polynomial(transformed,t,f'n={N}: transformed G')
    certificate['finite_n'][str(N)]={**{a:str(b) for a,b in scalars.items()},
                                     'G_coefficients_descending':coeffs}
for N in (2,3):
    require(y0.subs(n,N)>s.Rational(1,2),f'n={N}: y0>1/2')
certificate['small_n']={str(N):str(y0.subs(n,N)) for N in (2,3)}
Path(__file__).with_name('certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
print('PASS: exact coefficient identities; all n>=24 coefficient certificates; finite n=4..23 certificates; n=2,3 bound.')
