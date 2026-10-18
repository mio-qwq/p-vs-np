#!/usr/bin/env python3
"""Exact certificates for one structural family, not an all-colorings search.
Only Python standard library. Run normally and with python -O.
"""
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def add(a, b):
    out = [0] * max(len(a), len(b))
    for i, x in enumerate(a): out[i] += x
    for i, x in enumerate(b): out[i] += x
    while len(out) > 1 and out[-1] == 0: out.pop()
    return out

def mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): out[i+j] += x*y
    while len(out) > 1 and out[-1] == 0: out.pop()
    return out

def term(a, e):
    return [math.comb(e, d) * a**(e-d) for d in range(e+1)]

def parity(p):
    return (-1)**sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p)))

def vandermonde(values):
    return math.prod(values[j]-values[i] for i in range(len(values)) for j in range(i+1, len(values)))

def permutation_polynomial(a, e, p):
    out = [parity(p)]
    for i, j in enumerate(p): out = mul(out, term(a[i], e[j]))
    return out

def direct(a, e, red):
    n = len(a)
    k = len(red)
    polynomials = [[0] for _ in range(k+1)]
    counts = [[0, 0] for _ in range(k+1)]
    supports = [set() for _ in range(k+1)]
    moment_sums = [[0, 0, 0, 0] for _ in range(k+1)]
    for p in itertools.permutations(range(n)):
        t = sum((i, p[i]) in red for i in range(n))
        sg = parity(p)
        counts[t][0 if sg == 1 else 1] += 1
        supports[t].update(enumerate(p))
        polynomials[t] = add(polynomials[t], permutation_polynomial(a, e, p))
        s1, s2, s3 = (sum(e[p[i]] * a[i]**q for i in range(n)) for q in (1, 2, 3))
        values = [1, s1, (s1*s1-s2)//2, (s1**3-3*s1*s2+2*s3)//6]
        for q, value in enumerate(values): moment_sums[t][q] += sg*value
    return polynomials, counts, supports, moment_sums

# Independent determinant: sparse bivariate polynomials and recursive Laplace
# expansion. This does not reuse permutation signs/products or the minor formula.
def bivar_add(a, b, sign=1):
    out = dict(a)
    for mon, value in b.items():
        out[mon] = out.get(mon, 0) + sign*value
        if not out[mon]: del out[mon]
    return out

def bivar_mul(a, b):
    out = {}
    for (z1, x1), v1 in a.items():
        for (z2, x2), v2 in b.items():
            key = z1+z2, x1+x2
            out[key] = out.get(key, 0) + v1*v2
    return {key: value for key, value in out.items() if value}

def determinant(matrix):
    if not matrix: return {(0,0): 1}
    out = {}
    for j, entry in enumerate(matrix[0]):
        minor = [row[:j]+row[j+1:] for row in matrix[1:]]
        out = bivar_add(out, bivar_mul(entry, determinant(minor)), (-1)**j)
    return out

def raw_matrix(a, e, red):
    return [[{(int((i,j) in red), q): math.comb(e[j], q)*a[i]**(e[j]-q)
              for q in range(e[j]+1) if math.comb(e[j], q)*a[i]**(e[j]-q)}
             for j in range(len(e))] for i in range(len(a))]

def predicted(a, e, red, t):
    n, k = len(a), len(red)
    rows = sorted(set(range(n)) - {i for i,j in red})
    cols = sorted(set(range(n)) - {j for i,j in red})
    completion = dict(red)
    completion.update(zip(rows, cols))
    sg = parity(tuple(completion[i] for i in range(n)))
    m = n-k
    lc = Fraction(sg * (-1)**(k-t) * math.comb(k,t) * vandermonde([a[i] for i in rows]) * vandermonde([e[j] for j in cols]), math.prod(math.factorial(q) for q in range(m)))
    return sum(e)-math.comb(m,2), lc

def check_case(name, a, e, red, canonical=False):
    n,k = len(a),len(red)
    require(len({i for i,j in red}) == k and len({j for i,j in red}) == k, 'red edges are not a matching')
    polys, counts, supports, moments = direct(a,e,red)
    raw = determinant(raw_matrix(a,e,red))
    require(raw == {(t,q):v for t,p in enumerate(polys) for q,v in enumerate(p) if v}, f'{name}: independent determinant mismatch')
    output = []
    for t,p in enumerate(polys):
        degree, lc = predicted(a,e,red,t)
        require(len(p)-1 == degree and p[-1] == lc, f'{name}, t={t}: leading term mismatch')
        require(sum(counts[t]) > 0, 'a target is empty')
        if n-k>=2: require(counts[t][0] == counts[t][1], 'parity imbalance')
        if canonical and 1<=t<=k-1 and n-k>=2:
            expected = {(i,j) for i in range(n) for j in range(n) if not (t==k-1 and i<k and j<k and i!=j)}
            require(supports[t] == expected, f'{name}, t={t}: support mismatch')
            require(all((i,i) in supports[t] for i in range(n)), 'identity does not witness support leakage')
        output.append({'target':t, 'even':counts[t][0], 'odd':counts[t][1], 'support_edges':len(supports[t]), 'degree':degree, 'leading_coefficient':int(lc) if lc.denominator==1 else str(lc), 'coefficients_low_to_high':p, 'first_four_signed_coefficient_moments':moments[t]})
    return {'name':name, 'row_offsets':a, 'column_exponents':e, 'red_edges':sorted(red), 'targets':output}

cases = [
    check_case('full_support_cubic_moment', list(range(6)), list(range(6)), {(0,0),(1,1),(2,2)}, True),
    check_case('upper_interior_support_boundary', list(range(5)), list(range(5)), {(0,0),(1,1)}, True),
    check_case('irregular_offsets_gaps_nonprincipal_red_matching', [-4,0,2,7,9], [0,1,3,5,7], {(0,3),(3,0)}, False),
    check_case('single_unmarked_vertex', list(range(4)), list(range(4)), {(0,0),(1,1),(2,2)}, True),
]
block = [[1,1,0], [1,0,1], [0,1,1]]
block_red = {(i,j) for i in range(3) for j in range(3) if block[i][j]}
block_polys, block_counts, block_supports, block_moments = direct(list(range(6)), list(range(6)), block_red)
block_raw = determinant(raw_matrix(list(range(6)), list(range(6)), block_red))
require(block_raw == {(t,q):v for t,p in enumerate(block_polys) for q,v in enumerate(p) if v}, 'block independent determinant mismatch')
block_det = sum(parity(p)*math.prod(block[i][p[i]] for i in range(3)) for p in itertools.permutations(range(3)))
require(block_det == -2, 'block determinant mismatch')
block_targets = []
for t,p in enumerate(block_polys):
    if t > 3:
        require(p == [0] and block_counts[t] == [0,0], 'impossible block target is populated')
        continue
    lc = (-1)**(3-t) * math.comb(3,t) * block_det * 2
    require(len(p)-1 == 12 and p[-1] == lc, 'block leading coefficient mismatch')
    require(block_counts[t][0] == block_counts[t][1], 'block parity imbalance')
    block_targets.append({'target':t, 'even':block_counts[t][0], 'odd':block_counts[t][1], 'support_edges':len(block_supports[t]), 'degree':12, 'leading_coefficient':lc, 'coefficients_low_to_high':p, 'first_four_signed_coefficient_moments':block_moments[t]})
cases.append({'name':'overlapping_red_edges_nonsingular_block', 'row_offsets':list(range(6)), 'column_exponents':list(range(6)), 'red_edges':sorted(block_red), 'red_block_determinant':block_det, 'targets':block_targets})
singular_red = {(0,0),(0,1),(1,0),(1,1)}
singular_polys, singular_counts, singular_supports, singular_moments = direct(list(range(4)), list(range(4)), singular_red)
singular_raw = determinant(raw_matrix(list(range(4)), list(range(4)), singular_red))
require(singular_raw == {(t,q):v for t,p in enumerate(singular_polys) for q,v in enumerate(p) if v}, 'singular boundary independent determinant mismatch')
require(singular_polys[1] == [-24,-60,-38,-12,-2], 'singular boundary differs')
singular_boundary = {'name':'singular_block_hypothesis_boundary', 'red_edges':sorted(singular_red), 'target':1, 'degree':4, 'leading_coefficient':-2, 'coefficients_low_to_high':singular_polys[1]}
main=cases[0]['targets'][1]
require(main['even']==117 and main['odd']==117, 'main counts differ')
require(main['degree']==12 and main['leading_coefficient']==6, 'main leading term differs')
require(main['first_four_signed_coefficient_moments']==[0,0,0,6], 'main moments differ')
require(main['support_edges']==36, 'main support is incomplete')
(HERE/'results.json').write_text(json.dumps({'status':'PASS', 'method':'exact independent permutation and raw Laplace computations on five theorem examples and one singular-block boundary; no all-colorings search', 'cases':cases, 'singular_boundary':singular_boundary}, indent=2)+'\n')
print('PASS: generalized formula, parity balance, exact support boundary, nonsingular red block, and independent coefficient equality on five theorem examples and one singular boundary.')
print('n=6, k=3, t=1: 117 even, 117 odd; full 36-edge support; degree 12; leading coefficient 6.')
print('P_1 coefficients low-to-high:', main['coefficients_low_to_high'])
