# Independent audit: general four-row monic masked determinant

**Verdict: PASS.** Audited on 18 October 2026. This is an independent mathematical and exact-symbolic audit, not a formal proof-assistant verification.

## Frozen claim and source

For a binary 4×4 mask with a perfect matching, four distinct real offsets, and four distinct nonnegative integer exponents, the determinant of the masked powers `(x+a_i)^(e_j)` is a nonzero polynomial.

The audited source is the frozen `PROOF.md`, SHA-256:

`5bb505df254bda0212944fe3a02b25fcdcedbda032c4b5af0055f83009d0c5e5`.

No unresolved proof branch, denominator exception, or normalization gap was found. The proof applies to this auxiliary order-four determinant statement only. It establishes neither arbitrary-size masked nonvanishing nor a color-conditioned ASNC or complexity claim. No novelty claim is audited.

## Independence and exact checks

The audit's code does not import the source exploration code or checker. It independently constructs coefficients by row multilinearity: sum the determinants formed from each row's binomial-series coefficient over all compositions of the requested total degree. The source computation instead sums supported permutation products. Both use exact SymPy algebra.

The reproducible audit consists of:

- Exhaustive enumeration of all 65,536 binary 4×4 masks.
- Independent classification of all 512 binary 3×3 masks for the lower-order dependency.
- 168 named exact checks, including every coefficient identity used by the proof, prior vanishing coefficients for immediate cases, structural cofactors for both valuation arguments, all partial-row subsets, four centered derivative parity formulas, and polynomial identities behind the integer exclusions.
- Identical successful runs in ordinary Python and `python -O`.
- A negative control that adds one to the claimed last-orbit C6 formula. Both execution modes reject it with `Identity failed: 771515 C6; residual=-1` and exit status 1. Validation uses explicit exceptions and does not rely on `assert` statements.

The full run receipts are in `verification_runs.json`; the ordinary and optimized logs are retained. `identity_checks.json` records 38 named checks and `dependency_checks.json` records 130 named checks.

## Coverage audit

Among all 65,536 masks, exactly 37,823 have a perfect matching. Their allowed-edge component size distributions are:

- `(1,1,1,1)`: 13,032
- `(1,1,2)`: 9,288
- `(1,3)`: 8,160
- `(2,2)`: 558
- `(4)`: 6,785

Every allowed-edge component is balanced, directly checked. Every connected allowed-edge graph contains all original edges, directly checked. This is also consistent with the structural fact that deleting edges absent from every matching leaves every determinant term unchanged. Disconnected balanced components produce an exact product of smaller masked determinants after row and column permutations.

Among the 3,060 sorted multisets of nonzero row codes, the independent counts are 1,062 without a matching; 940 with nonzero binary determinant; 851 singular with disconnected allowed-edge graph; and 207 singular connected masks. Row and column permutations, without transposition, produce exactly the 23 representatives in the frozen proof. The full representative list and labeled orbit sizes are in `orbit_results.json`.

## Mathematical audit of reductions

1. **Permutations and normalization.** Column permutations carry their exponents. Subtracting the exponent of column zero factors a nonzero rational row product, so negative normalized exponents are legitimate. Their expansions at infinity are formal binomial series with finite polynomial coefficients at each order. An invertible affine variable change and nonzero column scalings give offsets `(0,1,b,c)` without assuming their order. No ordering of `p,q,r` is used in Sections 2–6. In the last orbit only, the first three columns have identical support and can be ordered and shifted to `0<p<q`.

2. **Lower orders.** The 3×3 matching counts are exactly 0,1,2,3,4,6. All four-matching masks are full minus one entry. Odd numbers of monic matching terms cannot cancel at top degree; two opposite-sign terms have different root multiplicity vectors; the full masks have nonzero Vandermonde leading coefficients; and the full-minus-one cofactor term has degree two higher than the full 3×3 determinant. These arguments also cover arbitrary distinct integer exponents after a common shift. Thus all reducible 4×4 masks are covered.

3. **Sparse valuations.** The relevant cofactors were independently reconstructed. At the root of one row base, every other row base is a unit. A difference of two distinct integer powers of distinct monic row bases has only simple zeros away from those bases' roots: its derivative at a zero is a nonzero multiple of the difference of their reciprocal values. This remains valid for negative powers. For `(3,5,11,13)`, the unit cofactors force `p,q<0` and `r<p,q`; simple zeros then force both `p-r=1` and `q-r=1`, contradicting distinctness. For `(3,5,10,15)`, they force `q<0`, `r<p`, and `p=±1`. The exact coefficient relations then give the excluded integer factor equations in the proof. The proof's simple-zero statement is used only for these monic row bases, not arbitrary proportional linear polynomials.

4. **Rational branches.** Every division is justified by distinctness or an explicitly treated exceptional case. In particular, the `A=0` and `B=0` branches of `(3,5,10,15)` are excluded before division; `q+1=0` and `r+1=0` in `(3,7,11,15)` violate exponent or offset distinctness; `T=0` in `(3,13,14,15)` leaves a nonzero C2; and `L=0` in `(7,7,11,13)` is inconsistent with its necessary C3 relation. The factors `u`, `2b-1`, `p-r`, and every displayed nonzero prefactor are covered.

5. **Integer exclusions.** The square-obstruction arguments in Sections 5–6 are valid for signed nonzero integer `p`. If an integer is a rational square, it is an integer square; hence the discriminant deductions are legitimate. The displayed even/odd consecutive-square bounds are exact and strictly positive on their stated ranges. The remaining `|p|=1` cases collide with existing exponents. The Section 4 expression `q(q+1)+r(r+1)` is strictly positive in the admissible integer branch.

6. **One partial row.** All 15 nonempty partial subsets were checked at degrees 0–3. The four weight formulas and all opposite-sign pair sums were reconstructed. The only proper-subset exception is the complementary pair with `r=p+q`. Its C4 and C5 formulas were independently verified with general offsets `(0,a,b,c)`, including the substitution `a+b+c=0`. Realness gives `ab+ac+bc=-(a²+b²+c²)/2<0`, closing the exception.

## Last orbit audit

For `(7,7,15,15)`, the independent reconstruction verifies C3, C4, and C6 exactly, including

`C6 = -b p q (b-1)(2b-1)(p-q) [A b(b-1)-2K] / 3240`.

The C4 relation forces `r=(p+q-3)/3>0`, since `0<p<q` and `r=0` is forbidden. It also gives `r<q`. With `s=(2b-1)²`, real and distinct offsets imply `s>0` and `s≠1`. The C6 constraint is exactly `A(s-1)=8K`. Centering and scaling give `(-1,1,-t,t)` with `t=√s>0`; swapping the two full rows changes only an overall sign. All four formulas for the derivative at zero, including their nonzero prefactors, were independently derived.

For both even, even/odd, and both odd exponents, the monotonicity or one-sign-change argument is valid, including `p=1` in the odd/odd branch. The remaining odd/even branch correctly uses C6 in addition to the derivative; the derivative alone can have another positive root and is not sufficient.

In that branch `q-2p` is a multiple of six. If it is zero, C6 forces the excluded `s=1`. If positive, the independently checked positive expansion of `K-5J+15` forces `s>1`, where the derivative expression is strictly negative. If negative, the independently checked expansion of `H-15J+45`, together with `p≥h+1`, forces `s≥3`; either the powers coincide and the derivative is nonzero, or their integer gap is at least one and the strict ratio bound makes it negative. All sign and boundary cases are covered.

## Reproduction

Run `python run_audit.py` in this directory with Python and SymPy installed. It executes the exhaustive and algebraic checks with and without optimization and both deliberate-failure controls. It writes the result JSON files and eight mode-specific logs. The script needs no network, external source checkout, or external proof-checker files.

The frozen source's SHA is recorded above. `SHA256.json` covers this report, the portable audit programs, run logs, and result files. A successful computational run is evidence for the algebra and finite classification; the analytic arguments were reviewed separately as described here.
