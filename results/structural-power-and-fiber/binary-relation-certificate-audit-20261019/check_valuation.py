#!/usr/bin/env python3
"""Independent audit of the supplied short valuation certificate.
Reconstructs exact coefficients by Newton interpolation of our integer values.
"""
from fractions import Fraction
from itertools import permutations
import json
from pathlib import Path
from check import require, evaluation_vector, sign_by_cycles, all_subset_sums

HERE = Path(__file__).resolve().parent

def interpolate(values):
    degree = len(values)-1
    coefficients = [Fraction(0)] * (degree+1)
    basis = [Fraction(1)]
    differences = list(values)
    for k in range(degree+1):
        for d, value in enumerate(basis):
            coefficients[d] += differences[0] * value
        differences = [b-a for a,b in zip(differences, differences[1:])]
        if k < degree:
            next_basis = [Fraction(0)] * (len(basis)+1)
            for d,value in enumerate(basis):
                next_basis[d] -= k*value/(k+1)
                next_basis[d+1] += value/(k+1)
            basis = next_basis
    require(all(c.denominator == 1 for c in coefficients), 'nonintegral reconstructed coefficient')
    return tuple(int(c) for c in coefficients)

def main():
    ps = list(permutations(range(4)))
    unsigned = {p: interpolate(evaluation_vector(p)) for p in ps}
    signed = {p: tuple(sign_by_cycles(p)*c for c in unsigned[p]) for p in ps}
    expected = [([18,24,108],[12,54,72]), ([4,27,72],[8,9,108]),
                ([3,8,54],[2,24,27]), ([2,9,12],[3,4,18])]
    tables = []
    for r in range(4):
        group = [p for p in ps if p[0] == r]
        require(all(all(signed[p][k] == 0 for k in range(r)) for p in group), 'valuation failed')
        plus = sorted(signed[p][r] for p in group if signed[p][r]>0)
        minus = sorted(-signed[p][r] for p in group if signed[p][r]<0)
        require((plus,minus) == expected[r], 'leading scalar table mismatch')
        tables.append({'r':r, 'positive':plus, 'negative':minus})
    fixed = [
        ([(0,1,2,3),(0,1,3,2),(0,2,1,3),(0,3,1,2)], (0,-18,-39,-29,-9,-1,0)),
        ([(1,2,0,3),(1,3,0,2)], (0,18,48,44,16,2,0)),
        ([(3,0,1,2),(3,0,2,1),(3,1,0,2),(3,2,0,1)], (0,0,0,0,3,1,0))]
    for matchings, vector in fixed:
        require(tuple(sum(signed[p][k] for p in matchings) for k in range(7)) == vector,
                'displayed branch polynomial mismatch')
    even = [unsigned[p][:5] for p in ps if sign_by_cycles(p) == 1]
    odd = [unsigned[p][:5] for p in ps if sign_by_cycles(p) == -1]
    es, os = all_subset_sums(even,5), all_subset_sums(odd,5)
    zero = (0,)*5
    require(set(es)&set(os) == {zero}, 'first-five-coefficient relation exists')
    require(es.count(zero)==os.count(zero)==1, 'nonempty truncated zero subset')
    result={'status':'PASS','method':'Newton interpolation of independently generated exact evaluation vectors',
            'tables':tables,'first_five_coefficients_suffice':True,
            'displayed_F0_F1_F3_polynomials':'verified'}
    (HERE/'valuation-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: all four scalar tables, three displayed branch polynomials, and first-five-coefficient sufficiency.')

if __name__=='__main__': main()
