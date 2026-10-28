#!/usr/bin/env python3
"""Reconstruct C3--C7 from direct Taylor alternants and check the C7 obstruction.

Only SymPy and the Python standard library are used.  Prior coefficients are
read as data only after the universal coefficients have been derived afresh.
No formula is divided by mu.  All checks remain active with python -O.
Paths are relative to this file, not the working directory.  Writes only stdout.
"""
import hashlib
import itertools
import json
from math import isqrt
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / 'inputs'
checks = []

def need(condition, label):
    if not condition:
        raise RuntimeError(label)
    checks.append(label)


def zero(expression, label):
    need(s.cancel(expression) == 0, label)


r1, r2, r3 = s.symbols('r1 r2 r3')
nodes = (r1, r2, r3)
e1, e2, e3 = s.symbols('e1 e2 e3')
B, C, u, v, a = s.symbols('B C u v a')
V = (r2-r1)*(r3-r1)*(r3-r2)

def symmetric_quotient(expression):
    quotient, remainder = s.div(s.Poly(s.expand(expression), nodes, domain=s.QQ),
                                s.Poly(V, nodes, domain=s.QQ))
    if not remainder.is_zero:
        raise RuntimeError('nonzero alternant remainder')
    symmetric, remainder, mapping = s.symmetrize(quotient.as_expr(), nodes, formal=True)
    if remainder != 0:
        raise RuntimeError('alternant quotient is not symmetric')
    return s.expand(symmetric.subs({var: out for (var, _), out in
                                    zip(mapping, (e1, e2, e3))}))


def binomial_polynomial(value, degree):
    return s.prod(value-j for j in range(degree))/s.factorial(degree)


# Exact Laplace normalization: after the shared-exponent and offset shifts,
# the two partial rows are (1,1,0,0,0) and (1,0,f,0,0), f=(1+z)^C.
# Full-row entries are left algebraically independent except column a=1.
f = s.symbols('f')
entries = s.symbols('b1 c1 d1 e_1 b2 c2 d2 e_2 b3 c3 d3 e_3')
full_rows = [[1, *entries[4*i:4*i+4]] for i in range(3)]
full = s.Matrix(full_rows)
masked = s.Matrix([[1, 1, 0, 0, 0], [1, 0, f, 0, 0], *full_rows])
minor = lambda column: full[:, [column, 3, 4]].det()
zero(masked.det()-f*(minor(0)-minor(1))+minor(2),
     'exact five-row Laplace normalization')

# Cauchy--Binet: an offset alternant times an exponent-binomial alternant.
# Each exponent alternant includes (D-a)(E-a)(E-D).  Dividing by E-D
# leaves a^2-u*a+v.  No stored coefficient enters this construction.
parts = {}
for degrees in itertools.combinations(range(7), 3):
    if sum(degrees) > 7:
        continue
    offset = symmetric_quotient(s.det(s.Matrix([[r**k for r in nodes] for k in degrees])))
    exponent = symmetric_quotient(s.det(s.Matrix([
        [binomial_polynomial(r, k) for r in nodes] for k in degrees])))
    parts[degrees] = (offset, exponent)
T = {}
for n in range(3, 8):
    expression = sum(offset*exponent.subs(
        {e1: a+u, e2: a*u+v, e3: a*v}, simultaneous=True)
        for degrees, (offset, exponent) in parts.items() if sum(degrees) == n)
    T[n] = s.Poly(s.expand((a*a-u*a+v)*expression), a)
original = {}
raw = {}
for n in range(3, 8):
    original[n] = s.expand(T[n].eval(0)-T[n].eval(B)-sum(
        binomial_polynomial(-C, j)*T[n-j].eval(C) for j in range(n-2)))
    raw[n] = s.Poly(s.expand(original[n].subs(v, u*(B+C)-B*B-C*C)),
                    B, C, u, e1, e2, e3)
zero(original[3]-(u*(B+C)-B*B-C*C-v)/2, 'C3 before any C3 substitution')

# Comparison happens only after all five universal coefficients are derived.
raw_path = INPUTS/'raw_coefficients.json'
prior = json.loads(raw_path.read_text())
for n in range(3, 8):
    need(raw[n] == s.Poly(s.sympify(prior[str(n)]), B, C, u, e1, e2, e3),
         'fresh C%d equals prior raw data' % n)

x, y = u-B, u-C
lv, av, vv = x+y, x*y, u*(B+C)-B*B-C*C
zero(raw[4].as_expr()+B*C*(lv*e1-3*x)/6, 'undivided C4 identity')
# Multiplication by L^2 is harmless once C4 has excluded L=0; K is not divided.
c5_identity = B*C*(lv**2*(av+2*lv)*(e1**2-3*e2)-9*av*(vv+lv))/(36*lv**2)
zero((raw[5].as_expr()-c5_identity).subs(e1, 3*x/lv),
     'C5 after C4, without dividing by K')

# Verify the algebraic low cases, with no height cutoff or reality assumption.
zero((lv.subs(u, (B+C)/2)*e1-3*x.subs(u, (B+C)/2))-3*(B-C)/2,
     'L=0 makes C4 a nonzero multiple of B-C')
z = s.symbols('z')
zero(z*z-B*z+C*(B-C)-(z-C)*(z-(B-C)), 'A=0 x branch forces exponent C')
zero(z*z-C*z+B*(C-B)-(z-B)*(z-(C-B)), 'A=0 y branch forces exponent B')
L, A, t, delta, m, p, q, R, Z = s.symbols('L A t delta m p q R Z')
zero(((u-L)*L+2*A+L).subs(A, -2*L)-L*(u-L-3),
     'K=0 and C5 force u=L+3')
xx, yy = s.symbols('x y')
zero((xx+2)*(yy+2)-4-(xx*yy+2*(xx+yy)), 'K=0 signed factor equation')
k_cases = []
for f in (-4, -2, -1, 1, 2, 4):
    g = 4//f
    X, Y = f-2, g-2
    if X == Y or X*Y == 0:
        continue
    Lv = X+Y
    U, Vv = Lv+3, -Lv
    discriminant = U*U-4*Vv
    need(discriminant == 0 or isqrt(discriminant)**2 != discriminant,
         'K=0 factor %d gives repeated or noninteger roots' % f)
    k_cases.append([X, Y, U, Vv, discriminant])
need(sorted(pair[:2] for pair in k_cases) == [[-6, -3], [-3, -6], [-1, 2], [2, -1]],
     'complete K=0 signed integer divisor list')

# Independent polynomial transformation of fresh C6/C7.  Termwise multiply
# by L^5 before substituting m=(L+delta)/(2L), then reduce delta^2=L^2-4A.
def reduce_delta(expression, relation):
    numerator, denominator = s.fraction(s.cancel(expression))
    reduced = s.rem(s.Poly(numerator, delta), s.Poly(relation, delta)).as_expr()
    return s.cancel(reduced/denominator)

free = {}
for n in (6, 7):
    expression = s.cancel(raw[n].as_expr()/(B*C))
    centered = s.Poly(s.expand(expression.subs(
        {e1: 3*m, e2: 3*m*m-p, e3: m*m*m-m*p+q}, simultaneous=True)),
        B, C, u, m, p, q)
    out = 0
    for (ib, ic, iu, im, ip, iq), coefficient in centered.terms():
        out += coefficient*(u-L/2-delta/2)**ib*(u-L/2+delta/2)**ic*u**iu \
            *((L+delta)/2)**im*L**(5-im)*p**ip*q**iq
    free[n] = reduce_delta(s.expand(out), delta**2-L**2+4*A)/L**5
    # C4 fixes m, C5 fixes p. q remains FREE, including the mu=0 branch.
    free[n] = free[n].subs({A: L*R, u: L+Z-2*R-1,
                            p: 3*R*Z/(L*(R+2))}, simultaneous=True)
    free[n] = reduce_delta(free[n], delta**2-L*(L-4*R))

formula_path = INPUTS/'C7_FORMULAS.json'
formula = json.loads(formula_path.read_text())
mu, eta, Q, N, Phi = [s.sympify(formula[name]) for name in ('mu', 'eta', 'Q', 'N', 'Phi')]
zero(Phi-mu*N-5*(R+2)*(L-4*R)*eta*Q, 'compact Phi definition')
c6 = L*mu*q/120+R*delta*eta/(24*L*(R+2))
c7 = (L+Z-2*R-7)*c6/2+delta*Q*q/240-R*N/(240*L*(R+2)**2)
zero(free[6]-c6, 'fresh C6 free-q compact identity')
zero(free[7]-c7, 'fresh C7 free-q compact identity')
syzygy = mu*c7-(mu*(L+Z-2*R-7)/2+delta*Q/(2*L))*c6 \
         +R*Phi/(240*L*(R+2)**2)
zero(reduce_delta(syzygy, delta**2-L*(L-4*R)), 'mu-undivided C6/C7 syzygy')
P7 = s.Poly(s.cancel(L**5*Phi.subs({R: A/L, Z: t+2*A/L+1}, simultaneous=True)),
             L, A, t, domain=s.ZZ)
need(len(P7.terms()) == 112 and P7.degree_list() == (8, 6, 6),
     'P7 is the 112-term integer polynomial of degrees 8,6,6')
print(json.dumps({
    'status': 'PASS', 'checks': checks, 'C3_before_substitution': str(original[3]),
    'fresh_coefficient_term_counts': {str(n): len(raw[n].terms()) for n in range(3, 8)},
    'K0_integer_cases': k_cases, 'P7_terms': len(P7.terms()),
    'no_mu_division': True, 'q_remains_free': True,
    'scope': 'Exact C3-C7 necessity for the specified overlap mask over complex offsets; not a formal proof-assistant or human-peer-review claim.',
    'input_sha256': {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                     for path in (raw_path, formula_path)},
}, indent=2, sort_keys=True))
