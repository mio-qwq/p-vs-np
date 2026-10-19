#!/usr/bin/env python3
"""Exact finite checks for the all-degree proofs in ROOT_GEOMETRY.md."""
import math
import sympy as sp

L, z, t = sp.symbols('L z t')

def require(value, label):
    if not value:
        raise RuntimeError(label)

def symbol(knots):
    g = sp.prod(t-a for a in knots)
    gp = sp.diff(g,t)
    return sp.expand(sum(z**a/gp.subs(t,a) for a in knots))

def htranslated(knots,d):
    h = [sp.Integer(1)] + [sp.Integer(0)]*d
    for a in knots:
        x = L+a
        h = [sp.expand(sum(h[k-j]*x**j for j in range(k+1))) for k in range(d+1)]
    return h[d]

def divided_difference(knots,d):
    g = sp.prod(t-a for a in knots)
    gp = sp.diff(g,t)
    return sp.expand(sum((L+a)**(len(knots)+d-1)/gp.subs(t,a) for a in knots))

for n in range(2,10):
    S=list(range(n))
    require(sp.expand(symbol(S)-(z-1)**(n-1)/math.factorial(n-1))==0, ('arithmetic symbol',n))
for r in range(1,8):
    S=[k for k in range(2*r+1) if k!=r]
    expected=sp.Rational(r, math.factorial(2*r))*(z-1)**(2*r-1)*(z+1)
    require(sp.expand(symbol(S)-expected)==0, ('central-deletion symbol',r))
for S in [list(range(2)),list(range(3)),list(range(5)),[0,1,3,4],[0,1,2,4,5,6]]:
    for d in [1,2,3,4,6,8,12]:
        H=htranslated(S,d)
        require(sp.expand(H-divided_difference(S,d))==0,('divided difference',S,d))
        require(sp.degree(sp.gcd(H,sp.diff(H,L)),L)==0,('squarefree',S,d))
        # Centered polynomial has parity d, as forced by its vertical root line and reality.
        centered=sp.expand(H.subs(L,L-sp.Rational(max(S),2)))
        require(sp.expand(centered.subs(L,-L)-(-1)**d*centered)==0,('center parity',S,d))
print('PASS: exact symbols, divided differences, squarefreeness, and centered parity checks.')
