# Independent audit of the five-row partial-row obstructions

18 October 2026. **Verdict: PASS for the stated one-partial-row necessary conditions and the certified candidate exclusions.** No mathematical correction to the reviewed `PROOF.md` is required. This audit does **not** establish the general five-row theorem, or even complete the classification of the one-partial-row subclass. It is an independent algebraic/mathematical audit, not proof-assistant verification.

## Reviewed scope and independent method

The reviewed `PROOF.md` has SHA-256:

`09562d66d49a7d35a4193444487e53a00d7ad1922bcb8ccc565d4cc1ddc58179`

Its scope is a binary 5-by-5 mask with four full rows and one nonempty partial row, five distinct nonnegative integer exponents, and five distinct real offsets. The supplied `verify.py` and its PASS receipts were inspected. The independent calculations here neither import nor execute that checker or the exploratory scripts.

The new `audit_independent.py` recomputes the coefficient identities by **two polynomial quotient rings**, rather than the supplied checker's binomial-minor and Schur-polynomial calculation:

- Reduce offset powers modulo `X^4 - E1 X^3 + E2 X^2 - E3 X + E4`.
- Reduce outside-exponent binomial polynomials modulo `Y^3 - R Y^2 + B Y - T`.
- Evaluation at the four offsets and at the three outside exponents contributes precisely the two Vandermonde determinants. The resulting 4-by-4 remainder-matrix determinant therefore is the doubly normalized pair determinant.
- Extract its coefficients exactly, substituting only the previously established necessary equations. All remaining parameters stay symbolic. There are no numerical parameter samples.

This establishes the coefficient identities independently of the original implementation. Both implementations use SymPy 1.14.0, so they are algorithmically independent checks within the same computer-algebra system, not independent proof kernels.

The concrete examples are checked separately by expanding their original 5-by-5 polynomial determinants directly with an exact polynomial-domain determinant algorithm. This does not reuse either the general coefficient formulas or the original checker's Cauchy–Binet loop.

## C6–C10 and the complement sign

All five identities in `PROOF.md` pass. With `T=rst`, the consecutive normalized coefficients are:

1. `c6 = -d(d^2-dR+B)/12`.
2. After `B=dR-d^2`, `c7 = E1 T d/48`.
3. After also `E1=0`, `c8 = E2 T d(2R-3d+15)/720`.
4. After also `R=(3d-15)/2`, `c9 = -E3 T d(d^2+95)/1920`.
5. After also `E3=0`,
   `c10(pair) = -dT[(5T+4d^2-460)E2^2-(68T+74d^2-3050)E4]/20160`.

The full determinant first contributes at order 10. In the stated row and column order, its normalized leading coefficient is

`E4 d T (r-d)(s-d)(t-d)/288`.

The exponent relation gives `(r-d)(s-d)(t-d)=T`, so this becomes `E4 d T^2/288`. Consequently the complementary three-retained-column mask has exactly

`c10(complement) = dT[(5T+4d^2-460)E2^2+(2T-74d^2+3050)E4]/20160`.

The sign is correct: the complementary mask determinant plus the pair mask determinant equals the full determinant, by linearity in the partial row. Its orders 6–9 are therefore the negatives of the pair coefficients.

## Normalization, real offsets, and divisions

**Signed exponents are legitimate.** Subtracting the chosen pair's smaller exponent `m` from every exponent divides the determinant by the nonzero rational function `product_i (x+a_i)^m`. This preserves whether the determinant is the zero rational function. Integer powers have well-defined formal binomial expansions at infinity, including negative integer powers, and each fixed coefficient uses only finitely many terms.

The parity argument's evaluation at the partial row's root is also legitimate. In the normalized partial row the only nonzero entries are `1,x^d`, with `d>0`. Its other entries are identically zero; they do not require evaluation of negative powers. All remaining row bases are nonzero at that point, so their possibly negative integer powers are finite.

**Every required nonzero factor is justified.** The five exponent values are distinct, so `d>0`, the outside integers `r,s,t` are nonzero and mutually distinct, none equals `d`, and `T != 0`. The translated full-row offsets are distinct and nonzero, making both Vandermonde divisors nonzero.

The argument forcing opposite pairs is sound:

- Vanishing `c7` gives `E1=0`.
- For real offsets, `E2=(E1^2-sum_i b_i^2)/2=-sum_i b_i^2/2<0`.
- Thus `c8=0` gives `R=(3d-15)/2`.
- Since `d^2+95>0`, `c9=0` gives `E3=0`.
- The offset polynomial is then even. Each nonzero real root occurs with its negative. Four distinct nonzero real roots therefore have the form `-u,u,-v,v`, with `u,v>0` and `u != v`.

There is no hidden assumption that the original offsets were symmetric; symmetry is deduced from necessary coefficient vanishing. Singleton, four-retained, and full partial rows are excluded by the stated nonzero leading Vandermonde coefficients.

**The rho domain is exactly appropriate.** Here `E2=-(u^2+v^2)`, `E4=u^2v^2`, and

`rho=E4/E2^2=u^2v^2/(u^2+v^2)^2`.

Thus `rho>0`; the identity `(u^2+v^2)^2-4u^2v^2=(u^2-v^2)^2>0` gives `rho<1/4`. The endpoint 0 would require a zero offset, while 1/4 would require coincident opposite-pair magnitudes. Both are forbidden. The stated equations divide only by proven nonzero quantities, never by a coefficient of rho that might vanish.

## Parity restriction

The integer equation `R=(3d-15)/2` forces `d` odd. If `d=3 mod 4`, then `R` is odd and `B=dR-d^2` is even. If `k` outside exponents are odd, the congruences force `k` odd and `binomial(k,2)` even; among `k=1,3`, only `k=1` qualifies. Including odd `d`, the cofactor then has exactly two even and two odd exponents.

At the partial row root, sum/difference operations on each opposite offset pair separate the cofactor into even and odd 2-by-2 blocks. Each block is nonzero because its two exponents differ and `u/v` is a positive number different from 1. This reasoning remains valid for negative integer exponents. Thus the necessary restriction `d=1 mod 4` for a two-retained-column mask is correct. It is not asserted for the three-retained-column mask.

## Certified d=7 exclusion

For `d=7`, the necessary equations are `R=3`, `B=-28`, and `r^2+s^2+t^2=65`. Therefore every outside integer lies in `[-8,8]`. Exact enumeration of distinct sorted triples in this justified finite interval gives only

- `(-5,2,6)`;
- `(-4,0,7)`.

The second is inadmissible because outside exponents cannot equal either selected pair exponent `0,7`. Thus, beyond the wording of the original branch statement, `(-5,2,6)` is the only admissible d=7 triple up to permutation.

The pair-retained case is excluded by the parity argument. For its three-retained complement, `T=-60` gives the coefficient-10 residual

`-564(u^4+v^4)-1824u^2v^2`,

which is strictly negative for nonzero real `u,v`. This excludes **every admissible d=7 case within the one-partial-row subclass**, not the full five-row mask problem.

## Certified three-retained example (0,3,5,8,9)

Directly expanding the original determinant with offsets `(0,-1,1,-v,v)` and support consisting of exponent values `{0,3,9}` confirms that all powers above `x^15` vanish, and that

`[x^15]D = -864v(v^2-1)^2(v^4-9v^2+1)`,

`[x^14]D = 0`,

`[x^13]D = 36v(v^2-1)^2(v^2+1)(23v^4-282v^2+23)`.

The determinant is odd in `x`, as also verified directly. On `v^4-9v^2+1=0`, the last inner factor equals `-75v^2`, giving the nonzero coefficient

`-2700v^3(v^2-1)^2(v^2+1)`.

Both specified positive choices of `v` are nonzero and different from 1, so the nonvanishing is rigorous. The alternate two-retained mask on the selected pair has residual `-224(u^4+v^4)-784u^2v^2`, also verified exactly and strictly nonzero for real nonzero offsets.

## Additional independently checked d=9 candidate

The separate root result in [the separately published d=9 candidate result](https://github.com/mio-qwq/p-vs-np/blob/5036ebd403ec3497b9df0ca44ea8570f5d9b0c6e/results/cancellation-route-audits/next-candidate/RESULT.md) is also approved. `audit_next_candidate.py` directly expands the original determinant for exponents `(0,5,9,12,14)`, retained exponent values `{5,14}`, and offsets `(0,-1,1,-v,v)`.

Under `209v^4-1226v^2+209=0`, every coefficient above `x^28` vanishes, while

`[x^28]D = 90288v^11-719280v^9+628992v^7+628992v^5-719280v^3+90288v`.

Its remainder is precisely

`v(115205932800/43681 - 137735637131520 v^2/9129329)`.

The quadratic for `v^2` has discriminant `1328352`, strictly between `1152^2` and `1153^2`. Hence `v^2` is irrational, and it cannot be the rational zero of the displayed nonconstant rational-linear factor. Both permitted positive `v` have distinct nonzero offset magnitudes. This is a valid exact exclusion of this additional candidate only.

## Reproduction and receipts

Run, from this directory:

```text
python audit_independent.py
python -O audit_independent.py
python audit_next_candidate.py
python -O audit_next_candidate.py
```

All four runs pass. Normal and optimized stdout logs are byte-identical for each checker; neither checker relies on Python `assert`. The receipts are `audit_independent_receipt.json` and `audit_next_candidate_receipt.json`, with the corresponding normal and optimized `.log` files. No remote writes, numerical testing, unknown-source execution, or candidate search beyond the exact d=7 arithmetic exhaustiveness check was used in this audit.
