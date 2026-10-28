# Independent complete finite enumeration review

Date: 2026-10-27. **PASS for the exact finite claim below.** This is an independent engine, not a replay/import of the root search implementation. No repository code was executed and no remote state was changed.

## Verified finite claim

For every canonical integer exponent tuple `(a,b,c,d,e)=(0,B,C,D,E)` with five distinct entries, `B<C`, `D<E`, span at most **1632**, and

`DE=(D+E)(B+C)-B^2-C^2`,

there is no tuple with `L*A*(A+2L) != 0` and `P7(L,A,t)=0`, where

`u=D+E, x=u-B, y=u-C, L=x+y, A=xy, t=u-L`,

and `P7=L^5 Phi(L,A/L,t+2A/L+1)` uses the supplied exact C7 polynomial. Every accepted tuple in all 30 canonical order types was considered. Exactly 17 order types have C3 tuples; the other 13 have zero C3 tuples in this complete domain. No prior 24-order theorem was used by the all-order engine.

The certificate is finite because the independently reviewed structural theorem supplies the universal height **1632**, rather than because a numerical experiment chose a cutoff. The engine itself establishes a bounded integer-polynomial fact; combining it into a determinant theorem additionally uses that structural theorem and the independently derived necessary coefficient identities. The parent is auditing that interface separately.

## Counts

| Stage | All 30 orders | Six formerly remaining orders |
|---|---:|---:|
| B,C outer pairs | 3,992,688 | 3,992,688 |
| Signed C3 factor pairs tested | 208,231,036 | 208,231,036 |
| Distinct C3 tuples within span | 19,658,082 | 6,824,412 |
| L=0 | 3,540 | 0 |
| A=0 after L exclusion | 0 | 0 |
| K=A+2L=0 after L,A exclusions | 6 | 6 |
| L*A*K nonzero | 19,654,536 | 6,824,406 |
| P7=0 mod101 | 220,631 | 76,365 |
| P7=0 mod101 and mod103 | 2,432 | 863 |
| P7 exactly zero | **0** | **0** |

The regular domain contains two M=0 tuples, 37 Z=0 tuples and 32 R=-4 tuples. These were **counted and retained**, not discarded. The six-order subset contains respectively 1,37,21. The two M=0 tuples and all six K=0 tuples also have direct low-coefficient contradiction certificates described below. Thus the final determinant argument need not apply a regular C7 formula at M=0.

## Coverage proof

After shifting exponent a to zero, any span-at-most-H tuple obeys `-H<=B<C<=H`, `B,C!=0`, `C-B<=H`. These inequalities are precisely the span restriction for `{0,B,C}`. Set `S=B+C`. C3 is equivalent to

`(D-S)(E-S)=2BC`.

Because BC is nonzero, every factor h=D-S is a nonzero signed divisor of n=2BC and k=E-S is its exact complementary factor n/h. The engine generates every positive divisor v of |n| once, then both h=-v and h=v, accepting only h<k. Therefore every D<E solution occurs once, including negative-negative factors when n>0 and both absolute-value orientations when n<0. It retains precisely the five-distinct tuples of total span <=H. No divisibility, parity, primitive-shape, sign, real-offset or discriminant filter is silently applied. The code verifies the original C3 equation on every accepted tuple.

The B,C divisor loop and the small brute-force checker are structurally different. At H=40 the checker loops B,C,D and solves the linear equation

`E=[D(B+C)-B^2-C^2]/[D-B-C]`.

The denominator-zero case has numerator 2BC!=0, so has no solutions. The brute set equals all **3,402** divisor-engine tuples, with no duplicates. Omitting the negative-negative factor branch loses **1,081** tuples, so that known-danger negative control is nonvacuous and detected.

## Exact polynomial and sieve checks

`generate.py` reads the factored Phi from the 0654 input data, substitutes R=A/L and Z=t+2A/L+1, and proves symbolically that L^5 times the expression is an integer polynomial with 112 terms. It agrees identically with the independently supplied global-C8 expanded P7. P8 is also independently reconstructed from U,V and agrees with its supplied expanded version, but no C8 sieve was needed because P7 leaves no zero.

The C++ engine uses the expanded polynomial modulo 101 and 103 **without modular division**. In particular L=0 mod p is retained unless the integer L itself is zero, which is a separately recorded low-coefficient case. Modular evaluations are cached by the residue triple `(L,A,t)`; no tuple data are used as a replacement for the polynomial. All arithmetic is exact.

`verify.py` evaluates every modular survivor by Python arbitrary-precision integers from the sparse P7 terms. It additionally evaluates a separately handwritten factored Phi expression with `fractions.Fraction` at every survivor. The exact expressions agree at all 2,432 all-order survivors (and all 863 six-order survivors), and every value is nonzero. The survivor tuple sets equal the root's independently generated sets exactly; file hashes differ because the formats differ.

At H=40 the direct Python big-integer sieve counts at both primes agree with every per-order C++ sieve count, including all low/singular categories. Ordinary and optimized Python outputs agree. A complete `-fsanitize=undefined -fno-sanitize-recover=all` C++ all-order replay finishes without diagnostics and reproduces every count and survivor set.

## Direct exceptional-coefficient checks

`check_singular_direct.py` builds Taylor alternants directly: for each 0<=i<j<k with i+j+k<=6 it divides the determinant of node powers by the full-offset Vandermonde, converts the quotient to elementary symmetric functions e1,e2,e3, and multiplies by the determinant of ordinary generalized-binomial coefficients in the exponent columns. This does not import a stored generic coefficient table. It computes

`T_n(a)=[z^n]det[(1+r_i z)^a,(1+r_i z)^D,(1+r_i z)^E]/[(E-D)V]`

and then the normalized sparse determinant coefficients

`C_n=T_n(0)-T_n(B)-sum_j binom(-C,j)T_(n-j)(C)`.

For all six K=0 tuples, C4 gives e1=1 and the following C5 constants, independent of e2:

| (B,C,D,E) | C5 |
|---|---:|
| (-52,-49,-45,-10) | -62426 |
| (-35,-32,-27,-11) | -17920 |
| (-30,-27,-21,-12) | -10935 |
| (-28,-25,-18,-13) | -8750 |
| (5,8,-7,9) | 160 |
| (22,25,-8,27) | 6875 |

For both regular M=0 tuples, C4 and C5 fix e1 and e2; C6 is a nonzero constant independent of e3:

| (B,C,D,E) | (L,A,t) | C6 |
|---|---|---:|
| (-22,-1,-67,-24) | (-159,6210,68) | -4215865500/1379219 |
| (-3,2,-4,3) | (-1,-6,0) | -2355/2 |

These contradictions hold over complex offsets as well as real offsets. For the 3,540 L=0 cases the undivided generic C4 condition `BC(Le1-3x)=0` forces x=y=0, contradicting B!=C; the parent has a separate generic coefficient audit. A=0 has no tuples in this enumeration and is also excluded algebraically by exponent collision under C3.

## Arithmetic safety and reproducibility

The maximal SPF index is 2H^2=5,326,848, within signed int. Divisor multiplication only produces divisors of this index. Exponent-derived expressions and M are computed using signed 64-bit integers, and the full run is UBSan-clean. Modular powers are at most 102; each modular term has magnitude at most 102^4, and the sum of 112 terms is less than 2^34. Exact P7 evaluation is Python arbitrary precision, not fixed-width arithmetic or floating point.

Environment: g++ (Debian 14.2.0-19) 14.2.0; Python 3.12.14; SymPy 1.14.0. No Boost library was available, so exact survivor evaluation was deliberately separated into Python; this is not an unverified bigint fallback.

Reproduce in this directory:

```
python generate.py
g++ -O3 -std=c++17 -Wall -Wextra enumerate.cpp -o enumerate
./enumerate 40 dump > RUN40.log
./enumerate 40 all > ALL_ORDERS40.log
./enumerate 1632 > RUN1632.log
./enumerate 1632 all > ALL_ORDERS1632.log
python verify.py
python verify.py allorders-
python check_singular_direct.py
```

`AUDIT.json` holds all per-order counts and review controls. `allorders-EXACT_P7_VALUES.json` holds every exact all-order survivor value. `allorders-flags-1632.tsv` preserves every exceptional-domain flag, including L=0, K=0, M=0, Z=0 and R=-4. `POLYNOMIAL_CHECK.json` records formula-input hashes. No result here concerns arbitrary masks, real noninteger exponents, circuit lower bounds, or P versus NP.
