# Bounded C3 engine source audit

2026-10-27. **PASS**, for `root/make_bounded_search.py`, `root/bounded_c3_search.cpp`, and the all-30 extension `root/bounded_c3_all_orders.cpp`. This is source review plus independent small-height controls, not this reviewer's duplicate full run.

## Coverage and uniqueness

The outer loop takes every `-H<=B<C<=H`, skips only zero B/C and `span(0,B,C)>H`, and has no hidden congruence restriction. Setting S=B+C, C3 is equivalent to `(D-S)(E-S)=2BC`. The merged prime factorizations of |B| and |C| plus one factor 2 generate every positive divisor of |2BC| exactly once. Taking both signs generates every nonzero integer divisor h. Then k=2BC/h is exact; h<k selects each unordered signed pair once, corresponding exactly to D<E. Both same-negative and same-positive branches are retained when BC>0, and both absolute-value orientations are retained when BC<0.

The preliminary interval `[max(0,C)-H, min(0,B)+H]` is necessary for each of D,E to fit with `{0,B,C}`. The subsequent actual five-value span check is necessary and sufficient. D!=E follows from h<k; the explicit exclusions D/E=0,B,C plus B<C and B,C!=0 establish all five values distinct. No candidate is removed by an unlicensed denominator test. L=0, A=0 and K=0 are counted and handled by the separate universal guard proof; no M, Z, Q or R+4 case is removed.

All-30 labels were freshly enumerated from the 120 permutations under b<c,d<e. Exact source comparison shows that the all-30 version changes only these labels and the corresponding array/loop dimensions; its numerical core is unchanged.

## Signed integer and array safety at H<=1632

* `|2BC| <= 2H^2 = 5,326,848`. Every generated prime power and divisor is at most this number, as is |k|. All divisor products are exact divisors of |2BC|, so intermediate multiplication stays within this bound.
* `|B+C|<=3264`, so even the prefilter D,E magnitudes are below 5,330,112. All fit signed 32-bit int. `N` is explicitly formed with `2LL` and is int64.
* After the span filter all B,C,D,E magnitudes are at most1632 because zero is one of the five values. Hence |u|<=3264, |x|,|y|<=4896, |L|<=9792, and |t|<=6528. A=x*y is explicitly int64. All C3 validation products are explicitly promoted with `1LL`.
* The polynomial has 112 terms with maximum coordinate degrees `(8,6,6)` and maximum absolute coefficient140850. The arrays have sizes10,8,8, so every access is in bounds; every literal coefficient fits int32.
* For p=101 or103, each reduced multiplicand is at most102. Polynomial-table inner products are reduced before the next multiplication; sums stay below10507. Horner intermediates stay below10507. The largest table has103^3=1,092,727 entries and all computed indices are inside it.
* The height guard rejects values outside1..1632. The uint64 counters comfortably cover the finite search size.

## Modular polynomial tables

For each residue pair(l,a), the implementation accumulates

`c_j = sum_{terms with t-degree j} coefficient*l^(L-degree)*a^(A-degree) mod p`.

The subsequent descending Horner loop from7 to0 evaluates `sum c_j t^j`; c_7 is simply zero because the actual t-degree is6. Thus the table stores exactly `P(l,a,t)==0 mod p` for every residue triple. Negative original inputs are reduced by the signed-safe `mod` function. There is no modular division, so primes dividing L or K do not create an omitted branch.

The generated term dictionary was independently compared, term for term, to a fresh expansion of the compact Phi certificate under `P=L^5 Phi(L,A/L,t+2A/L+1)`. All112 terms and coefficients match exactly. This comparison also verifies the intermediate PHI_LAT.txt source, rather than trusting its filename.

## Execution controls

Both six-order and all-30 binaries ran at H=80 under `-fsanitize=undefined,bounds -fno-sanitize-recover=all -D_GLIBCXX_ASSERTIONS`, without diagnostics. An independent direct-E loop (no divisor generation), using arbitrary-precision evaluation of the freshly reconstructed P, matches every aggregate counter, all per-order counters, and every modular survivor in both runs. All six K=0 tuples were listed explicitly and have nonzero `v+L`.

A portable final verifier should also require that the survivor TSV row count equals the reported final modular counter, and reject duplicate rows. This closes ordinary output-truncation failures, since the source checks initial stream opening but does not explicitly test the stream after every write. The independent full engine and exact final survivor comparison provide the relevant evidence for the present result; this is not a mathematical gap in the enumerator.
