# Exact exclusion of the next symmetric five-row candidate

18 October 2026. Exponents (0,5,9,12,14), partial row retains exponent values 5,14, offsets (0,-1,1,-v,v). Let v>0 satisfy 209v^4-1226v^2+209=0. These are the proposed rho=209/1644 values, with distinct real offsets.

An independent raw permutation/binomial expansion gives zero coefficients of lambda^(40-r) for 6<=r<=11 after reducing by that equation. Lower r coefficients vanish by the full four-row-minor degree lemma.

The coefficient of lambda^28 (r=12) is

 90288v^11-719280v^9+628992v^7+628992v^5-719280v^3+90288v.

Its exact remainder modulo 209v^4-1226v^2+209 is

 v * (115205932800/43681 - 137735637131520/9129329 * v^2).

This is nonzero at either allowed positive v: v^2 solves 209q^2-1226q+209=0, with discriminant 1328352 strictly between 1152^2 and 1153^2, so q is irrational. The parenthesized nonconstant rational-linear expression cannot vanish there. Both q roots are positive, distinct and different from 1 (product 1, sum 1226/209>2), so the offsets satisfy distinctness.

Thus this candidate is not an identically zero determinant. The checker expands the actual mask directly; it does not use the necessary-condition symbolic formulas from the other investigation. This proves only this candidate's exclusion and does not settle the five-row problem.
