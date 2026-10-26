#!/usr/bin/env python3
"""Independent, locally authored integer-only exhaustive certificate.
No downloaded code, external packages, network calls, or floating arithmetic.
"""
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

B = 7
N = 1 << (2 * B)
E = [0] + [1 << i for i in range(B)]
SHIFTS = [u ^ (v << B) for u in E for v in E]
ERRORS = [(u, v << B) for u in E for v in E]

def syndrome7(x):
    result = 0
    for i in range(B):
        if x & (1 << i):
            result ^= i + 1
    return result

def syndrome(x):
    return syndrome7(x & 127) | (syndrome7(x >> B) << 3)

def fwht(a):
    a = list(a)
    step = 1
    while step < len(a):
        for start in range(0, len(a), 2 * step):
            for j in range(start, start + step):
                x, y = a[j], a[j + step]
                a[j], a[j + step] = x + y, x - y
        step *= 2
    return a

def xor_convolve(a, b):
    z = fwht([x*y for x,y in zip(fwht(a), fwht(b))])
    assert all(x % len(a) == 0 for x in z)
    return [x // len(a) for x in z]

def direct_indicator(c, u, v, t=0):
    # Deliberately recompute actual Hamming weights, not table lookups.
    def gate(x):
        return int((x ^ t).bit_count() >= B)
    return int(gate(c) - gate(c ^ u) - gate(c ^ v) + gate(c ^ u ^ v) != 0)

def main():
    truth = [int(x.bit_count() >= B) for x in range(N)]
    q = []
    for x in range(N):
        q.append(sum(truth[x] - truth[x ^ u] - truth[x ^ v] + truth[x ^ u ^ v] != 0
                     for u, v in ERRORS))
    cosets = [[] for _ in range(64)]
    for x in range(N):
        cosets[syndrome(x)].append(x)
    assert all(len(c) == 256 for c in cosets)
    assert len(set(SHIFTS)) == 64
    assert sorted(map(syndrome, SHIFTS)) == list(range(64))
    # Explicit bijection certificate in every translated code coset.
    for coset in cosets:
        seen = bytearray(N)
        for c in coset:
            for t in SHIFTS:
                assert not seen[c ^ t]
                seen[c ^ t] = 1
        assert all(seen)
    mask = [int(x in set(SHIFTS)) for x in range(N)]
    h = xor_convolve(q, mask)
    # Independent direct aggregation at representative ambient centers.
    representatives = sorted(set(SHIFTS + [0, 127, 128, 8191, 16383, 0x1555, 0x2aaa]))
    for c in representatives:
        assert h[c] == sum(direct_indicator(c,u,v,t) for t in SHIFTS for u,v in ERRORS)
        assert q[c] == sum(direct_indicator(c,u,v) for u,v in ERRORS)
    # Complete direct XOR sum cross-check against transformed convolution.
    assert all(h[c] == sum(q[c ^ t] for t in SHIFTS) for c in range(N))
    raw_single = [sum(q[c] for c in cs) for cs in cosets]
    raw_family = [sum(h[c] for c in cs) for cs in cosets]
    p = Fraction(2 * B * B * math.comb(2 * B, B), (B+1)**2 * 4**B)
    assert p == Fraction(21021, 65536)
    assert Fraction(sum(q), N * len(ERRORS)) == p
    assert set(raw_family) == {336336}
    expected = 64 * p
    assert expected == Fraction(21021, 1024)
    assert all(Fraction(v,256*64) == expected for v in raw_family)
    # Negative control: deleting the zero translation destroys exact constancy.
    deleted = [a-b for a,b in zip(raw_family,raw_single)]
    assert len(set(deleted)) > 1
    # Optional full weight-at-most-two family: lower bound, not constancy.
    full_shifts = [x for x in range(N) if x.bit_count() <= 2]
    assert len(full_shifts) == 106 and set(SHIFTS) <= set(full_shifts)
    full_mask = [int(x.bit_count() <= 2) for x in range(N)]
    full_h = xor_convolve(q,full_mask)
    full_raw = [sum(full_h[c] for c in cs) for cs in cosets]
    assert min(full_raw) >= 336336
    assert len(set(full_raw)) > 1
    out = {
        'status':'PASS', 'arithmetic':'integers and fractions only',
        'n':14, 'b':7, 'r':2, 'cosets':64, 'centers_per_coset':256,
        'error_pairs':64, 'translated_gates':64,
        'global_single_gate_residual_count':sum(q),
        'global_single_gate_total':N*64, 'p7':str(p),
        'per_coset_family_raw_numerators':raw_family,
        'per_coset_family_denominator':256*64,
        'per_coset_family_expectation':str(expected),
        'single_gate_per_coset_numerators':raw_single,
        'single_gate_per_coset_expectation_range':[str(Fraction(min(raw_single),256*64)),str(Fraction(max(raw_single),256*64))],
        'family_pointwise_error_sum_range':[min(h),max(h)],
        'direct_truth_representative_centers':representatives,
        'direct_truth_indicator_checks':len(representatives)*64*65,
        'all_center_direct_xor_sum_checks':N,
        'every_coset_transversal_bijection_checked':True,
        'deleting_zero_translation_produces_distinct_coset_totals':len(set(deleted)),
        'full_weight_at_most_two_family': {
            'gates':len(full_shifts), 'distinct_coset_totals':sorted(set(full_raw)),
            'expectation_range':[str(Fraction(min(full_raw),16384)),str(Fraction(max(full_raw),16384))],
            'at_least_cross_transversal_bound':True, 'constant':False},
        'scope':'sum of nonzero anchored mixed-residual indicators; fixed 7+7 partition; not signed cancellation, circuit lower bounds, or partition-uniform claims',
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__ == '__main__':
    main()
