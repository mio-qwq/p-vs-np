#!/usr/bin/env python3
"""Exact implementation checks accompanying universal proofs in RESULT.md."""
import sympy as sp
from math import comb

def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)

z, L, u = sp.symbols('z L u')

# The key nullspace basis identity is algebraic in generic distinct nodes.
for n in range(3, 7):
    a = list(range(n))
    m = n-1
    gp = [sp.prod(ai-aj for aj in a if aj != ai) for ai in a]
    for j in range(m+1):
        b = sum(sp.Rational(ai**j, gi) for ai, gi in zip(a,gp))
        require(b == (1 if j == m else 0), 'barycentric moments')
    for k in range(1,m):
        null = sp.Matrix([[sp.Rational(ai**j,gi) for ai,gi in zip(a,gp)] for j in range(k)])
        require(null.rank() == k, 'moment rank')
        for degree in range(m-k+1):
            require(null*sp.Matrix([ai**degree for ai in a]) == sp.zeros(k,1), 'nullspace polynomial basis')

# Independently verify the exact span criterion for arbitrary target polynomials,
# including targets that fail it. This tests both directions rather than powers.
for a,t,r in [([-3,-1,2,4],5,1), ([-3,-1,2,4],5,2), ([-4,-1,1,3,7],7,2), ([-4,-1,1,3,7],4,2)]:
    n, m = len(a), len(a)-1
    s, v = t-r, m-r
    G = sp.prod(1-ai*z for ai in a)
    gp = [sp.prod(ai-aj for aj in a if aj != ai) for ai in a]
    P = sum(sp.Integer(i+1)*z**(v-i) for i in range(v+1))
    weights = [P.subs(z,ai)/gi for ai,gi in zip(a,gp)]
    Y = sp.Poly(sp.expand(sum(w*(L+ai)**t for w,ai in zip(weights,a))),L).monic().as_expr()
    for target in [Y, sp.expand(Y+1), sp.expand(Y+L**max(0,s-1))]:
        coeff = [sp.expand(target).coeff(L,s-j) for j in range(s+1)]
        F = sum(coeff[j]*sp.Rational(comb(t,r),comb(t,r+j))*z**j for j in range(s+1))
        GF = sp.Poly(sp.expand(G*F),z)
        criterion = all(GF.nth(j)==0 for j in range(v+1,s+1))
        M=sp.Matrix([[sp.expand((L+ai)**t).coeff(L,j) for ai in a] for j in range(t+1)])
        rhs=sp.Matrix([sp.expand(target).coeff(L,j) for j in range(t+1)])
        direct = M.rank()==M.row_join(rhs).rank()
        require(criterion==direct,'span criterion equivalence')

# Independent exact audit of adversarial n=9,d=6 algebraic example.
# Obtain h2,h4,h6 by generating series, rather than copying them.
series=sp.series(1/((1-z)*(1-u*z)*(1-4*u*z)*(1-9*u*z)),z,0,4).removeO()
F=sp.Poly(sum(sp.binomial(14,6-2*j)*series.coeff(z,j)*L**(6-2*j) for j in range(4)),L)
y=sp.symbols('y')
A=sp.Integer(3003)
B=sp.Integer(1001)*(14*u+1)
C=sp.Integer(91)*(147*u**2+14*u+1)
D=1408*u**3+147*u**2+14*u+1
require(sp.expand(F.as_expr()-(A*L**6+B*L**4+C*L**2+D))==0,'adversarial translation')
P=12827754466*u**6+6383624352*u**5+1082672647*u**4+114597802*u**3+4936407*u**2+164108*u-236
require(sp.expand(sp.discriminant(A*y**3+B*y**2+C*y+D,y)-364364*P)==0,'discriminant polynomial')
require(P.subs(u,sp.Rational(1,729))<0<P.subs(u,sp.Rational(1,700)),'isolating interval')
require(all(c>0 for c in sp.Poly(sp.diff(P,u),u).all_coeffs()),'unique positive discriminant root')
E=sp.expand(B**2-3*A*C)
rr=sp.cancel((9*A*D-B*C)/(2*E))
ss=sp.cancel(-B/A-2*rr)
for c in sp.Poly(A*y**3+B*y**2+C*y+D-A*(y-rr)**2*(y-ss),y).all_coeffs():
    num=sp.fraction(sp.cancel(c))[0]
    require(sp.rem(num,P,u)==0,'factorization modulo P')
require(sp.expand(E-91091*(833*u**2+182*u+2))==0,'nontriple root')
num_s=613456*u**3+225939*u**2+12600*u-10
num_diff=389563*u**3+185073*u**2+9345*u-106
require(num_s.subs(u,sp.Rational(1,729))>0,'s negative')
require(num_diff.subs(u,sp.Rational(1,700))<0,'r<s')
require(all(c>0 for c in sp.Poly(sp.diff(num_s,u),u).all_coeffs()),'s numerator monotonic')
require(all(c>0 for c in sp.Poly(sp.diff(num_diff,u),u).all_coeffs()),'difference numerator monotonic')

# Independently verify finite hypergeometric/Riccati recurrence symbolically.
n,c=sp.symbols('n c',positive=True)
for halfdegree in range(2,9):
    q=halfdegree
    bs=[c**j*sp.rf(n,2*j)*sp.binomial(q,j)/sp.ff(2*q,2*j) for j in range(q+1)]
    for j in range(1,q+1):
        require(sp.factor(2*j*(2*q-2*j+1)*bs[j]-c*(n+2*j-2)*(n+2*j-1)*bs[j-1])==0,'quadratic-base ratio')

print('PASS: barycentric nullspace, exact span criterion, repeated-root counterexample, quadratic-base recurrence')
