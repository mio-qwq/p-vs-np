#!/usr/bin/env python3
"""Exact finite counterexample to minimum-centering restoring even-moment LC."""
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

c,t=s.symbols('c t')
a=[s.Rational(j,1000) for j in range(99)]+[s.Integer(100)]
n=len(a)
require(n==100 and len(set(a))==100,'100 distinct real knots')
p={k:sum(x**k for x in a) for k in range(1,7)}
h=[s.Integer(1)]
for k in range(1,7):
    h.append(s.factor(sum(p[j]*h[k-j] for j in range(1,k+1))/k))

# Independent multiplication of the actual 100 geometric factors.
g=[s.Integer(1)]+[s.Integer(0)]*6
for x in a:
    for k in range(1,7):
        g[k]+=x*g[k-1]
require(g==h,'power-sum recurrence versus geometric-factor multiplication')
mu=[s.factor(s.factorial(k)*h[k]/s.rf(n,k)) for k in range(7)]
M={k:s.Poly(sum(s.binomial(k,j)*mu[j]*(-c)**(k-j) for j in range(k+1)),c) for k in range(7)}
q=-M[5]
H=s.Poly(5*M[4].as_expr()**2-2*M[2].as_expr()*M[6].as_expr(),c)
lo=s.Rational(2173,1000);hi=s.Rational(2174,1000)
require(s.diff(q.as_expr(),c)==5*M[4].as_expr(),'q prime = 5 M4')
require(s.diff(M[6].as_expr(),c)==6*q.as_expr(),'P6 derivative = 6 q')
require(q.eval(lo)<0 and q.eval(hi)>0,'root isolating signs')
require(H.eval(lo)<0 and H.eval(hi)<0,'LC gap endpoint signs')
Ht=s.Poly(s.expand(H.as_expr().subs(c,lo+(hi-lo)*t)),t)
coeff=list(reversed(Ht.all_coeffs()))
require(coeff[0]<0 and all(x>0 for x in coeff[1:]),'all nonconstant translated coefficients positive')
require(sum(coeff)==H.eval(hi)<0,'negative value at t=1')
require(s.expand((M[4].as_expr()/s.factorial(4))**2-(M[2].as_expr()/s.factorial(2))*(M[6].as_expr()/s.factorial(6))-H.as_expr()/2880)==0,'normalized gap scaling')

# Exact rational majorant used only in the optional recovery criterion.
require((s.Rational(2,3)/(1-s.Rational(2,15)))==s.Rational(10,13),'even tail geometric bound')
v=s.symbols('v',nonnegative=True)
ratio_margin=s.Poly(s.expand(s.Rational(2,15)*(2*(v+2)+1)*(2*(v+2)+2)-4),v)
require(all(x>=0 for x in ratio_margin.all_coeffs()),'uniform even-tail ratio bound')

# A second exact interval check, not needed for the coefficient proof.
require(q.count_roots(lo,hi)==1,'independent exact q root count')
require(H.count_roots(lo,hi)==0,'independent exact H root count')

cert={
 'knots':{'count':n,'first_99':'j/1000, 0 <= j <= 98','last':'100'},
 'raw_moments_0_through_6':[str(x) for x in mu],
 'q_coefficients_ascending':[str(x) for x in reversed(q.all_coeffs())],
 'H_coefficients_ascending':[str(x) for x in reversed(H.all_coeffs())],
 'interval':[str(lo),str(hi)],
 'q_at_interval_endpoints':[str(q.eval(lo)),str(q.eval(hi))],
 'H_at_interval_endpoints':[str(H.eval(lo)),str(H.eval(hi))],
 'H_after_interval_substitution_ascending':[str(x) for x in coeff],
 'sign_certificate':'H(lo+(hi-lo)t) has negative constant coefficient and strictly positive remaining coefficients, but H(hi)<0. Thus H<0 on 0<=t<=1.',
 'exact_root_counts':{'q':1,'H':0},
 'scope':'Refutes restoration of normalized even-moment log-concavity by translating to the degree-six moment polynomial minimum; not a proper-power counterexample.'
}
(ROOT/'asymmetric_barrier_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
print('PASS: 100 distinct knots, independent moment constructions, exact isolating signs, global-minimum derivative identity, and strict LC-gap interval certificate.')
