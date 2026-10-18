#!/usr/bin/env python3
"""Exact coefficientwise identities for the one-partial-row theorem.

Uses only Python's standard library. No point evaluations or randomized tests.
Polynomials live in Q[p,q,r,a,b,c]; each equality compares every coefficient.
"""
from fractions import Fraction
from itertools import permutations, combinations
from math import factorial

N = 6
ZERO_MONOMIAL = (0,) * N

class Poly:
    def __init__(self, terms=None):
        self.terms = {m: Fraction(v) for m, v in (terms or {}).items() if v}
    @staticmethod
    def coerce(x):
        return x if isinstance(x, Poly) else Poly({ZERO_MONOMIAL: Fraction(x)})
    @staticmethod
    def variable(i):
        m = [0] * N
        m[i] = 1
        return Poly({tuple(m): 1})
    def __add__(self, other):
        result = dict(self.terms)
        for m, v in Poly.coerce(other).terms.items():
            result[m] = result.get(m, 0) + v
        return Poly(result)
    __radd__ = __add__
    def __neg__(self):
        return Poly({m: -v for m, v in self.terms.items()})
    def __sub__(self, other):
        return self + (-Poly.coerce(other))
    def __rsub__(self, other):
        return Poly.coerce(other) + (-self)
    def __mul__(self, other):
        result = {}
        for m, x in self.terms.items():
            for n, y in Poly.coerce(other).terms.items():
                t = tuple(i+j for i, j in zip(m, n))
                result[t] = result.get(t, 0) + x*y
        return Poly(result)
    __rmul__ = __mul__
    def __truediv__(self, scalar):
        return self * Fraction(1, scalar)
    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError('Only nonnegative integer powers are supported')
        result = Poly.coerce(1)
        for _ in range(n):
            result *= self
        return result
    def __eq__(self, other):
        return self.terms == Poly.coerce(other).terms

p, q, r, a, b, c = [Poly.variable(i) for i in range(N)]


def determinant(matrix):
    n = len(matrix)
    assert all(len(row) == n for row in matrix)
    result = Poly.coerce(0)
    for perm in permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i+1,n))
        term = Poly.coerce((-1) ** inversions)
        for i in range(n):
            term *= matrix[i][perm[i]]
        result += term
    return result


def choose(e, k):
    result = Poly.coerce(1)
    for t in range(k):
        result *= e-t
    return result/factorial(k)


def cofactor_sum(exponents, subset, ks):
    result = Poly.coerce(0)
    for j in subset:
        columns = [e for t, e in enumerate(exponents) if t != j]
        result += ((-1) ** j) * determinant([[choose(e,k) for e in columns] for k in ks])
    return result


def alternant(ks):
    return determinant([[u**k for k in ks] for u in (a,b,c)])


checked = 0

def check(label, lhs, rhs):
    global checked
    difference = lhs-rhs
    if difference != 0:
        raise AssertionError(f'{label}: {difference.terms}')
    checked += 1
    print('PASS:', label)


exponents = [Poly.coerce(0),p,q,r]
weights = [(q-p)*(r-p)*(r-q), -q*r*(r-q), p*r*(r-p), -p*q*(q-p)]
for j in range(4):
    check(f'degree-three singleton weight {j}', 2*cofactor_sum(exponents,[j],(0,1,2)), weights[j])
check('all four weights sum to zero', sum(weights), Poly.coerce(0))
check('pair {0,1} exact factor', weights[0]+weights[1], -p*(r-q)*(r+q-p))
check('pair {2,3} exact factor', weights[2]+weights[3], p*(r-q)*(r+q-p))
check('pair {1,2} exact factor', weights[1]+weights[2], r*(p-q)*(r-p-q))
check('pair {0,3} exact factor', weights[0]+weights[3], -r*(p-q)*(r-p-q))

V = (b-a)*(c-a)*(c-b)
s1 = a+b+c
s2 = a*b+a*c+b*c
h2 = a*a+b*b+c*c+s2
check('ordinary three-offset Vandermonde', alternant((0,1,2)), V)
check('degree-four offset alternant', alternant((0,1,3)), V*s1)
check('degree-five offset alternant (0,1,4)', alternant((0,1,4)), V*h2)
check('degree-five offset alternant (0,2,3)', alternant((0,2,3)), V*s2)
check('h2 equals s1 squared minus s2', h2, s1*s1-s2)
check('sum of squares identity', s1*s1, a*a+b*b+c*c+2*s2)

symmetric_exponents = [Poly.coerce(0),p,q,p+q]
B = p*q*(p-q)*(p+q)
for ks, expected in [((0,1,2), Poly.coerce(0)), ((0,1,3), B/6), ((0,1,4), B*(p+q-3)/12), ((0,2,3), B*(p+q-1)/12)]:
    check(f'exceptional middle pair C{ks}', cofactor_sum(symmetric_exponents,[1,2],ks), expected)
    check(f'exceptional endpoint pair C{ks}', cofactor_sum(symmetric_exponents,[0,3],ks), -expected)

middle_degree5 = sum(alternant(ks)*cofactor_sum(symmetric_exponents,[1,2],ks) for ks in ((0,1,4),(0,2,3)))
check('degree-five coefficient, without conditional substitution', middle_degree5, V*B*((p+q-3)*s1*s1+2*s2)/12)

# All possible triples contributing below degree six, and those contributing at
# degree six; this is enumeration of finite coefficient formula terms, not of
# exponent or offset values.
for ks in combinations(range(7),3):
    if sum(ks) < 6:
        check(f'full row has no coefficient from {ks}', cofactor_sum(exponents,range(4),ks), Poly.coerce(0))
full_degree6 = sum(alternant(ks)*cofactor_sum(exponents,range(4),ks) for ks in combinations(range(7),3) if sum(ks)==6)
exponent_V = p*q*r*(q-p)*(r-p)*(r-q)
check('full degree-six coefficient', full_degree6, a*b*c*V*exponent_V/12)
check('four-row binomial determinant', determinant([[choose(e,k) for e in exponents] for k in range(4)]), exponent_V/12)
check('four-offset Vandermonde including zero', determinant([[u**k for k in range(4)] for u in (Poly.coerce(0),a,b,c)]), a*b*c*V)

# Explicit sharpness outside R: exponents (0,1,2,3), partial entries {1,2}.
# The only binomial expansion indices available are 0,1,2,3, so these are all
# coefficients, rather than a truncation. Prove the full symbolic polynomial
# determinant has only
# coefficients -V*s1 and -V*s2 at degrees four and five; they both vanish for
# the three distinct cube roots of one.
small_exponents = list(map(Poly.coerce, [0,1,2,3]))
for degree in range(7):
    coefficient = sum((alternant(ks)*cofactor_sum(small_exponents,[1,2],ks) for ks in combinations(range(4),3) if sum(ks)==degree), Poly.coerce(0))
    expected = -V*s1 if degree==4 else -V*s2 if degree==5 else Poly.coerce(0)
    check(f'complex-boundary exact coefficient at degree {degree}', coefficient, expected)

print(f'All {checked} coefficientwise polynomial identities verified over Q[p,q,r,a,b,c].')
