#!/usr/bin/env python3
"""Exact symbolic certificate for the degree-eight quartic-square obstruction.

No numerical rootfinding or sampled n values enter the proof. Every relevant
rational function has a positive-coefficient numerator and denominator after
n=v+2. Running with -O preserves every check.
"""
from pathlib import Path
import json
import sympy as S

ROOT = Path(__file__).resolve().parent
n, L, b, c, d, x, y, v = S.symbols('n L b c d x y v', real=True)

def require(test, message):
    if not test:
        raise RuntimeError(message)

def same(a, b):
    return S.cancel(a-b) == 0

# Recover complete homogeneous coefficients and real-knot power sums from P=Q².
P = S.Poly((L**4+b*L**2+c*L+d)**2, L)
hk = [S.Integer(1)] + [S.factor(P.coeff_monomial(L**(8-k))*S.rf(n,k)/S.ff(8,k)) for k in range(1,9)]
pk = [n]
for k in range(1,9):
    pk.append(S.factor(k*hk[k]-sum(pk[j]*hk[k-j] for j in range(1,k))))
require(pk[1] == 0, 'Centeredness failed')
params = {b:14/(n*(n+1)), c:56*x/(n*(n+1)*(n+2))}
params[d] = S.solve(pk[4].subs(params)-y,d)[0]
pp = [S.factor(q.subs(params)) for q in pk]
require(same(pp[2],1) and same(pp[3],x) and same(pp[4],y), 'Normalization failed')

# Explicit coefficients used in PROOF.md.
kappa = (n**2+22*n+42)/(3*n*(n+1))
e = (3*n**3+51*n**2+216*n+280)/(5*n*(n+1)*(n+2))
f = (n**2+15*n+35)/(n*(n+1))
g = -(n**4+44*n**3+491*n**2+1624*n+1470)/(15*n**2*(n+1)**2)
h = (17*n**4+382*n**3+3127*n**2+11162*n+14700)/(2*n*(n+1)*(n+2)*(n+3))
i = -(n**6+105*n**5+2236*n**4+20121*n**3+87205*n**2+175056*n+123480)/(3*n**2*(n+1)**2*(n+2)*(n+3))
j = (n**8+36*n**7+1186*n**6+22196*n**5+212774*n**4+1071874*n**3+2822309*n**2+3588564*n+1728720)/(30*n**3*(n+1)**3*(n+2)*(n+3))
ell = 4*(3*n**3+44*n**2+167*n+196)/(15*n*(n+1)*(n+2))
require(same(pp[5],kappa*x), 'p5 identity failed')
require(same(pp[6],e*x*x+f*y+g), 'p6 identity failed')
require(same(pp[8],h*y*y+i*y+j-ell*x*x), 'p8 identity failed')

F = (h-1)*y*y+i*y+j
R = S.factor(e*F/ell+f*y+g)
T = S.factor(R*R-y**3)
D = S.factor(kappa*kappa*(f*y+g)-y*y*(kappa*kappa-e*y))
y0 = S.factor(-g/f)
r = S.factor((n+53)/(n+50)*y0)

# Named rational expressions whose strict positivity proves both case splits.
exprs = [
    ('kappa_squared_minus_e_r',kappa*kappa-e*r),
    ('three_e_f_minus_kappa_squared',3*e*f-kappa*kappa),
    ('minus_D_at_r',-D.subs(y,r)),
]
for q in range(3):
    exprs.append((f'R_shift_coefficient_{q}', S.diff(R,y,q).subs(y,r)/S.factorial(q)))
for q in range(5):
    exprs.append((f'T_shift_coefficient_{q}', S.diff(T,y,q).subs(y,r)/S.factorial(q)))

witness = {'parameter_substitution':'n = v + 2, v >= 0', 'coefficient_order':'ascending powers of v', 'expressions':[]}
for name, expr in exprs:
    expr = S.factor(expr)
    num,den = expr.as_numer_denom()
    numer = S.Poly(S.expand(num.subs(n,v+2)),v,domain=S.QQ)
    denom = S.Poly(S.expand(den.subs(n,v+2)),v,domain=S.QQ)
    nc = list(reversed(numer.all_coeffs()))
    dc = list(reversed(denom.all_coeffs()))
    require(all(t>0 for t in nc), f'Nonpositive numerator coefficient: {name}')
    require(all(t>0 for t in dc), f'Nonpositive denominator coefficient: {name}')
    witness['expressions'].append({
        'name':name, 'rational_expression':str(expr),
        'numerator_coefficients':[str(t) for t in nc],
        'denominator_coefficients':[str(t) for t in dc],
        'numerator_degree':numer.degree(), 'denominator_degree':denom.degree(),
        'minimum_numerator_coefficient':str(min(nc)),
        'minimum_denominator_coefficient':str(min(dc)),
    })
    print(name, 'PASS', 'numerator degree',numer.degree(), 'minimum coefficient',min(nc))

# Basic positive multipliers and separator are also checked symbolically.
for name,expr in [('kappa',kappa),('e',e),('f',f),('ell',ell),('r',r)]:
    num,den=S.factor(expr).as_numer_denom()
    for part in [num,den]:
        require(all(q>0 for q in S.Poly(part.subs(n,v+2),v).all_coeffs()),f'{name} positivity failed')

# Verify expansions exactly, separately from sign checks.
u=S.symbols('u')
require(same(R.subs(y,r+u),sum(S.diff(R,y,q).subs(y,r)/S.factorial(q)*u**q for q in range(3))),'R Taylor identity failed')
require(same(T.subs(y,r+u),sum(S.diff(T,y,q).subs(y,r)/S.factorial(q)*u**q for q in range(5))),'T Taylor identity failed')
# D' is a positive quadratic whenever 3 e f > kappa².
require(same(S.diff(D,y), 3*e*(y-kappa*kappa/(3*e))**2 + kappa*kappa*(3*e*f-kappa*kappa)/(3*e)), 'D derivative identity failed')

(ROOT/'certificate.json').write_text(json.dumps(witness,indent=2)+'\n')
print('PASS: exact coefficient identities and 11 universal positivity certificates for every real n>=2.')
