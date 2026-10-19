#!/usr/bin/env python3
"""Independent exact signed-permutation audit of PROOF.md; no numerical tests."""
import itertools
import math
from fractions import Fraction
import sympy as sp

X = sp.Symbol('X')

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def delta(v):
    return sp.prod(v[j] - v[i] for i in range(len(v)) for j in range(i + 1, len(v)))

def poly_det(rows):
    n = len(rows)
    result = sp.Poly(0, X)
    for perm in itertools.permutations(range(n)):
        sign = (-1) ** sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = sp.Poly(sign, X)
        for i, j in enumerate(perm):
            term *= rows[i][j]
        result += term
    return result

def evaluate(a, e, i, p, c):
    n, m, k = len(a), len(a)-1, e[c]
    b = sorted(e[:c] + e[c+1:])
    S, A = sum(e), sum(a)
    d = S-k-m*(m-1)//2
    D = k+d
    H = math.prod(math.factorial(h) for h in range(m))
    R = sp.prod(sp.Rational(a[s]-a[i], a[s]-a[p]) for s in range(n) if s not in (i,p))
    L = [(-1)**(s+c)*delta(a[:s]+a[s+1:])*delta(e[:c]+e[c+1:])*sp.Rational(1,H) for s in range(n)]
    B1, B2 = sum(b), sum(x*x for x in b)
    v = (B2-sp.Rational(B1*B1,m)-sp.Rational(m*(m*m-1),12))/(m*(m*m-1))
    require(v >= 0, 'Exact check failed: v >= 0')
    require((v == 0) == all(b[h] == b[0]+h for h in range(m)), 'Exact check failed: (v == 0) == all(b[h] == b[0]+h for h in range(m))')
    V = [[sp.Poly((X+a[s])**e[j], X) for j in range(n)] for s in range(n)]
    full = poly_det(V)
    T=[]
    for s in range(n):
        minor = [[V[u][j] for j in range(n) if j != c] for u in range(n) if u != s]
        T.append((-1)**(s+c)*V[s][c]*poly_det(minor))
        require(T[s].degree() == D, 'Exact check failed: T[s].degree() == D')
        require(T[s].LC() == L[s], 'Exact check failed: T[s].LC() == L[s]')
        beta = sp.Rational(d,m)*(A-a[s])+k*a[s]
        require(T[s].nth(D-1)/L[s] == beta, 'Exact check failed: T[s].nth(D-1)/L[s] == beta')
    require(L[p]/L[i] == -R, 'Exact check failed: L[p]/L[i] == -R')
    masked = [row[:] for row in V]
    masked[i][c] = sp.Poly(0,X)
    masked[p][c] = sp.Poly(0,X)
    P=poly_det(masked)
    require(P == full-T[i]-T[p], 'Exact check failed: P == full-T[i]-T[p]')
    require(full.degree() == D-m, 'Exact check failed: full.degree() == D-m')
    require(full.LC() == delta(a)*delta(e)*sp.Rational(1,math.prod(math.factorial(h) for h in range(n))), 'Exact check failed: full.LC() == delta(a)*delta(e)*sp.Rational(1,math.prod(math.factorial(h) for h in range(n)))')
    if R != 1:
        require(P.degree() == D, 'Exact check failed: P.degree() == D')
        require(P.LC() == L[i]*(R-1), 'Exact check failed: P.LC() == L[i]*(R-1)')
    elif n*k != D:
        require(P.degree() == D-1, 'Exact check failed: P.degree() == D-1')
        require(P.LC() == -L[i]*(a[i]-a[p])*(k-sp.Rational(d,m)), 'Exact check failed: P.LC() == -L[i]*(a[i]-a[p])*(k-sp.Rational(d,m))')
    else:
        require(v > 0, 'Exact check failed: v > 0')
        alpha = (k*(k-1)+(m-1)*v)/2
        beta = k*k-v
        for s in range(n):
            others=[a[t] for t in range(n) if t != s]
            Q = sp.binomial(k,2)*a[s]**2+k*k*a[s]*(A-a[s])
            Q += alpha*sum(z*z for z in others)
            Q += beta*sum(others[u]*others[t] for u in range(m) for t in range(u+1,m))
            require(T[s].nth(D-2)/L[s] == Q, 'Exact check failed: T[s].nth(D-2)/L[s] == Q')
        qdiff=T[i].nth(D-2)/L[i]-T[p].nth(D-2)/L[p]
        require(qdiff == v*(a[i]-a[p])*(A-sp.Rational(n,2)*(a[i]+a[p])), 'Exact check failed: qdiff == v*(a[i]-a[p])*(A-sp.Rational(n,2)*(a[i]+a[p]))')
        if n >= 4 and A != sp.Rational(n,2)*(a[i]+a[p]):
            require(P.degree() == D-2, 'Exact check failed: P.degree() == D-2')
            require(P.LC() == -L[i]*v*(a[i]-a[p])*(A-sp.Rational(n,2)*(a[i]+a[p])), 'Exact check failed: P.LC() == -L[i]*v*(a[i]-a[p])*(A-sp.Rational(n,2)*(a[i]+a[p]))')
    return P,full,T,D,v

# Independent symbolic simplification of the confluent-alternant variance identity.
m_sym, B1_sym, B2_sym = sp.symbols('m B1 B2', nonzero=True)
d_sym=B1_sym-m_sym*(m_sym-1)/2
v_sym=(B2_sym-B1_sym**2/m_sym-m_sym*(m_sym**2-1)/12)/(m_sym*(m_sym**2-1))
E2_sym=((m_sym*(m_sym+1)/2)**2-m_sym*(m_sym+1)*(2*m_sym+1)/6)/2
alpha_sym=((B1_sym**2+B2_sym)/2-m_sym*(m_sym+1)*B1_sym/2+E2_sym)/(m_sym*(m_sym+1))
require(sp.factor(2*alpha_sym+d_sym/m_sym-(d_sym/m_sym)**2-(m_sym-1)*v_sym) == 0, 'Exact check failed: sp.factor(2*alpha_sym+d_sym/m_sym-(d_sym/m_sym)**2-(m_sym-1)*v_sym) == 0')

cases = [
    ('formula (2), n=3', [0,2,5], [0,1,4], 0,2,1),
    ('formula (3), n=4', [0,1,2,3], [0,1,2,3], 0,3,0),
    ('formula (4), n=5', [0,1,2,4,6], [0,1,2,3,5], 0,3,1),
    ('formula (4), reversed rows and columns', [6,4,2,1,0], [5,3,2,1,0], 4,1,3),
    ('residual n=4', [0,1,2,3], [0,1,2,4], 0,3,1),
    ('residual n=5', [0,2,4,14,15], [0,1,2,3,5], 0,3,1),
    ('deeper residual n=5', [0,2,4,14,15], [0,7,10,17,22], 0,3,2),
]
for name,a,e,i,p,c in cases:
    P,F,T,D,v=evaluate(a,e,i,p,c)
    if name == 'residual n=4':
        require(P.as_expr() == 12*(2*X+3), 'Exact check failed: P.as_expr() == 12*(2*X+3)')
    if name == 'residual n=5':
        require(P.as_expr().expand() == (-480480*(49*X**2+446*X-1680)).expand(), 'Exact check failed: P.as_expr().expand() == (-480480*(49*X**2+446*X-1680)).expand()')
    if name == 'deeper residual n=5':
        removed=F-P
        require(D == 50, 'Exact check failed: D == 50')
        require(all(removed.nth(j) == 0 for j in range(47,51)), 'Exact check failed: all(removed.nth(j) == 0 for j in range(47,51))')
        require(removed.degree() == 46 and removed.LC() == 447990903360000, 'Exact check failed: removed.degree() == 46 and removed.LC() == 447990903360000')
        require(F.LC() == 990593604000000, 'Exact check failed: F.LC() == 990593604000000')
        require(P.degree() == 46 and P.LC() == 542602700640000, 'Exact check failed: P.degree() == 46 and P.LC() == 542602700640000')
    print(f'PASS: {name}; D={D}, deg P={P.degree()}, v={v}')
print('All exact identities and reported examples passed.')
