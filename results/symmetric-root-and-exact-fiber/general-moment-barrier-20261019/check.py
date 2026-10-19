#!/usr/bin/env python3
"""Exact algebra checks. Universality is proved in PROOF.md, not by finite tests."""
from fractions import Fraction as F
from math import factorial, comb
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parent

def require(cond, message):
    if not cond:
        raise RuntimeError(message)

v,t=s.symbols('v t', nonnegative=True)
cert={}
for name,j,expr in [
    ('negative_value_pair',v+3,lambda j:(2*j+2)*(2*j+1)-4),
    ('positive_derivative_pair',v+3,lambda j:(2*j)*(2*j+1)-4),
    ('positive_lower_endpoint_pair',v+2,lambda j:(2*j+2)*(2*j+1)-2),
]:
    p=s.Poly(s.expand(expr(j)),v)
    coeff=list(reversed(p.all_coeffs()))
    require(all(x>0 for x in coeff), name)
    cert[name]={'variable':'v >= 0','coefficients_ascending':[int(x) for x in coeff]}
require(F(1)-2+F(2,3)==-F(1,3),'negative endpoint')
require(1-F(4,6)==F(1,3),'derivative lower bound')

# Exact tests of (5), log-concavity, endpoint signs and derivative bound.
def test_sequence(name,m,b):
    require(len(b)==m+1 and all(q>0 for q in b),name+' positive moments')
    require(all(b[j]**2>=b[j-1]*b[j+1] for j in range(1,m)),name+' moment LC')
    N=2*m
    mu=[b[j]*factorial(2*j) for j in range(m+1)]
    c=[F(factorial(N))*b[m-j] for j in range(m+1)]
    require(all(c[j]==factorial(2*j)*comb(N,2*j)*mu[m-j] for j in range(m+1)),name+' coefficient identity')
    d=[c[j]*c[0]**(j-1)/c[1]**j for j in range(m+1)]
    require(d[0]==d[1]==1,name+' normalized first terms')
    require(all(d[j+1]<=d[j] for j in range(m)),name+' coefficient decrease')
    end=sum((-1)**j*d[j]*F(4)**j/factorial(2*j) for j in range(m+1))
    low=sum((-1)**j*d[j]*F(2)**j/factorial(2*j) for j in range(m+1))
    bracket=sum((-1)**(j+1)*d[j]*F(4)**(j-1)/factorial(2*j-1) for j in range(1,m+1))
    require(end<=-F(1,3),name+' F(2)')
    require(bracket>=F(1,3),name+' derivative bracket')
    require(low==0 if m==1 else low>0,name+' lower endpoint')
    return {'name':name,'N':N,'F_at_2':str(end),'derivative_bracket_at_2':str(bracket)}

tests=[]
for m in [1,2,3,8,16]:
    # Uniform[-1,1], standard Gaussian, centered Laplace of scale one.
    tests.append(test_sequence('uniform',m,[F(1,factorial(2*j+1)) for j in range(m+1)]))
    tests.append(test_sequence('gaussian',m,[F(1,2**j*factorial(j)) for j in range(m+1)]))
    tests.append(test_sequence('laplace',m,[F(1) for j in range(m+1)]))

# Exact genuine-distribution counterexample when normalized LC is dropped.
masses=[(F(0),F(8,9)),(F(3),F(1,18)),(F(-3),F(1,18))]
mu=[sum(p*x**k for x,p in masses) for k in range(5)]
z=s.symbols('z')
P=sum(s.Rational(mu[k].numerator,mu[k].denominator)*comb(4,k)*z**(4-k) for k in range(5))
require(s.expand(P-(z*z+3)**2)==0,'discrete counterexample')
require(F(mu[2],2)**2<F(mu[0])*F(mu[4],24),'counterexample fails normalized LC')

cert['normalization']={'F_at_2_upper':'-1/3','derivative_bracket_lower':'1/3'}
cert['regression_tests']=tests
(ROOT/'certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
print('PASS: universal pair identities, normalization, 15 exact regression cases, and scope counterexample.')
