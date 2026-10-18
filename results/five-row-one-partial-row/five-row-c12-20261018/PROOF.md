# The five-row determinant with one nonempty partial row is nonzero

18 October 2026. This is a mathematical proof with an exact symbolic certificate and an independent symbolic-algebra audit. The audit is `../five-row-c12-audit-20261018/AUDIT.md`; it reconstructs the coefficients by a different method and independently checks the complete exclusion. This is not proof-assistant verification.

## Theorem and scope

Let `a0,...,a4` be distinct real numbers and let `e0,...,e4` be distinct nonnegative integers. Let `A` be a binary 5-by-5 matrix with four full rows and with the remaining row nonempty. Then

`det[A_ij (x+a_i)^e_j]`

is not identically zero as a polynomial in `x`.

This completes the **one-partial-row subclass** only. Nothing here resolves arbitrary five-row binary masks, colored ASNC, complexity, novelty, or P versus NP. All computations and files are local.

The new step is a general coefficient-12 obstruction. Its elimination gives a quadratic in the integer product of three normalized exponents. Exact sign bounds reduce both support sizes to a finite list of gaps, and every remaining quadratic has negative or nonsquare discriminant. No finite search over masks or unbounded exponent tuples is used.

## 1. Previously established necessary reduction

The coefficient-6 through coefficient-10 calculation and the parity argument were derived and independently audited in `../five-row-cancellation-20261018/PROOF.md` and `AUDIT.md`. Here is the complete reduction needed by this proof.

Coefficient convention: with `z=1/x`, write `F_A(z)=det[A_ij(1+a_i z)^e_j]=sum_k C_k z^k`. Throughout this proof, "coefficient k" means `C_k`, not the coefficient of `x^k`. Identity-zero of the original determinant implies every `C_k=0`. The same convention is used after translating offsets and normalizing exponents.

Permuting rows or columns changes the determinant only by a sign, so put the partial row first and order columns as convenient. Translating the variable puts that row's offset at zero without affecting identity-zero. A partial row with one retained column has a nonzero coefficient 6: it is the product of the four-offset and four-exponent Vandermondes divided by `0!1!2!3!=12`, up to sign. A row with four retained columns has the negative of its singleton complement's coefficient 6, because the full determinant begins at coefficient 10. A full fifth row has nonzero leading coefficient 10, equal to the product of the five-offset and five-exponent Vandermondes divided by `0!1!2!3!4!=288`. Thus only support sizes two and three need consideration. The only remaining support size, zero, is excluded by the theorem's nonempty-row hypothesis.

For size two, select its retained pair. For size three, select its omitted pair. Put the smaller selected exponent first, subtract it from every exponent, and permute columns so the normalized exponent list is

`(0,d,r,s,t)`, with `d>0` an integer.

The integers `r,s,t` are distinct, nonzero, and different from `d`. They may be negative. This normalization multiplies the original determinant by a nonzero rational function, so identity-zero is preserved. Formal binomial series at infinity apply to negative integer exponents; no evaluation at a pole is used in the coefficient argument.

Write

`R=r+s+t`, `B=rs+rt+st`, `T=rst`.

After this ordering, let `b1,...,b4` be the full-row offsets and define `V(b)=product_{i<j}(b_j-b_i)`, `V(r,s,t)=(s-r)(t-r)(t-s)`. Where normalized coefficients are used, `c_k=C_k/[V(b)V(r,s,t)]`; both divisors are nonzero.

In particular, `T` is a nonzero integer. If the determinant were zero, coefficients 6 through 9 force

`B=dR-d²`, `R=(3d-15)/2`,

and the other four offsets must be, up to row order,

`(-u,u,-v,v)`, with `u,v>0` and `u!=v`.

Consequently `d` is odd. Put

`E2=-(u²+v²)<0`, `E4=u²v²>0`, `rho=E4/E2²`.

Then `0<rho<1/4`. The preceding reduction uses only justified divisions: nonzero Vandermonde factors, `dT`, `E2`, and `d²+95`. For reference, if `c_k` denotes the pair coefficient divided by `V(b1,...,b4)V(r,s,t)`, its successive identities are

- `c6=-d(d²-dR+B)/12`;
- after `B=dR-d²`, `c7=E1Td/48`;
- after also `E1=0`, `c8=E2Td(2R-3d+15)/720`;
- after also `R=(3d-15)/2`, `c9=-E3Td(d²+95)/1920`.

Real offsets give `E2<0` when `E1=0`. Thus `E3=0`, and the offset polynomial `X⁴+E2X²+E4` is even, forcing the opposite pairs.

For a retained pair, one additionally has `d=1 mod 4`. Indeed, if `d=3 mod 4`, the sum and pair-sum congruences imply that exactly one of `r,s,t` is odd. The cofactor at the center therefore has two even and two odd exponents. Opposite-row sums and differences split it into two nonzero 2-by-2 generalized Vandermonde determinants at positive distinct `u,v`. Evaluating the partial row `(1,x^d,0,0,0)` at `x=0` then contradicts zero. Negative cofactor exponents cause no problem because their bases at the center are nonzero.

No parity restriction beyond oddness is needed for the complementary three-column case.

## 2. New coefficient-12 identities

Use the same normalized coefficients. The pair determinant and its complementary triple determinant sum to the full determinant, by linearity in their first row. All three normalized series are even: replacing `z=1/x` by `-z` swaps both opposite row pairs, with total sign positive.

Define

`A=5T+4d²-460`,

`P=68T+74d²-3050`,

`Q=2T-74d²+3050`,

`N=(33d²-600d+7335)T + 25d⁴-480d³+2830d²+55200d-630695`,

`K=(468d²-8160d+90060)T + 490d⁴-8880d³+75580d²+366000d-4015910`,

`J=(232d²-240d-6760)T - 490d⁴+8880d³-75580d²-366000d+4015910`.

The coefficient-10 identities are

`c10(pair)=-dT(A E2²-P E4)/20160`,

`c10(full)=dT²E4/288`,

`c10(complement)=dT(A E2²+Q E4)/20160`.

The new exact identities are

`c12(pair)=E2 dT(N E2²-K E4)/4838400`,

`c12(full)=-E2 E4 dT²(d²-12d+119)/6912`,

`c12(complement)=-E2 dT(N E2²+J E4)/4838400`.

Thus a zero retained-pair determinant requires

`A-P rho=0`, `N-K rho=0`,

whereas a zero complementary-triple determinant requires

`A+Q rho=0`, `N+J rho=0`.

Only `E2`, `E2²`, `d` and `T`, already proved nonzero, have been divided out. The relations depend only on `rho`, so they are invariant under common nonzero offset scaling.

### Exact derivation method

The certificate reconstructs these identities, rather than loading coefficient output. Reduce powers of an offset variable `X` modulo `X⁴+E2X²+E4`; evaluating its degree-at-most-three remainders at the four offsets factors out their Vandermonde. Reduce the polynomial `binomial(Y,k)` modulo `Y³-RY²+BY-T`; evaluation at `r,s,t` similarly factors out their Vandermonde.

The resulting 4-by-4 remainder matrix has first column corresponding to `(1+Xz)^d-1`, and the other three columns correspond to the coefficients of `1,Y,Y²` in the outside-exponent remainder. Its determinant is precisely the doubly normalized retained-pair series. For the full determinant, replace each outside column evaluation by `(1+Xz)^e-1`, which simply removes its degree-zero contribution. Subtract to obtain the complement.

After factoring `z^i` from remainder row `i=0,1,2,3`, only six further degrees are needed for coefficient 12. This is a finite exact polynomial calculation. The checker also verifies all coefficients 6 through 9 and 11 vanish under the prior necessary relations and recovers both coefficient-10 identities.

## 3. Eliminate rho without dividing by its coefficients

Put

`H=(48d²-24240)T² +(90d⁴-55860d²+1875930)T +55d⁶-28125d⁴+2236245d²-38150575`,

`C=(24235-547d²)T² +(-435d⁴+37590d²-1039395)T +55d⁶-28125d⁴+2236245d²-38150575`.

Exact polynomial identities give

`AK-PN=2H`, `QN-AJ=2C`.

Therefore the retained-pair equations imply `H=0`, and the complementary-triple equations imply `C=0`. This implication also covers every zero-slope or zero-denominator case: there is no division by `P`, `Q`, `K` or `J`, and no assertion that the resultant condition is sufficient.

## 4. Retained pairs: a uniform upper bound and exact exhaustion

The discriminant of `H`, considered as a quadratic in `T`, is

`Delta_H=-60F(d²)`,

where

`F(q)=41q⁴-11300q³-5027466q²-242872100q+2999439785`.

The exact positive-coefficient expansion

`F(529+h)=41h⁴+75456h³+45880320h²+9229344768h+5573836800`

is strictly positive for every `h>=0`. Hence `d>=23` gives a negative discriminant and no real root of `H`. Its leading coefficient is nonzero there because `d²>505`.

The parity restriction leaves only `d=1,5,9,13,17,21`. Divide each integral quadratic by its nonzero integer content and choose positive leading coefficient. The following table lists its discriminant and, when nonnegative, the integer `n` such that `n²<Delta<(n+1)²`.

| d | Primitive quadratic | Delta | n |
|---|---|---:|---:|
| 1 | `21T²-1580T+31200` | -124400 | negative |
| 5 | `4T²-93T-180` | 11529 | 107 |
| 9 | `159T²+16080T+96200` | 197383200 | 14049 |
| 13 | `14T²+4335T+171900` | 9165825 | 3027 |
| 17 | `9T²+5860T+358800` | 21422800 | 4628 |
| 21 | `24T²+41055T-1526500` | 1832057025 | 42802 |

If `aT²+bT+c=0` for integer `T`, then its discriminant equals `(2aT+b)²`. Every table entry contradicts this. Thus no retained-pair case can vanish identically.

## 5. Complementary triples: positivity forces a second upper bound

Assume `d>=25`. The coefficient of `T²` in `C` is negative. The coefficient-10 relation can be solved using the strictly positive denominator `5+2rho`:

`T=(460-4d²+(74d²-3050)rho)/(5+2rho)`.

Set `Tlo=92-4d²/5`. Then

`T-Tlo=42rho(9d²-385)/(5(5+2rho))>0`.

Three exact signs locate the roots of `C`.

First,

`C(Tlo)=21(9d²-385)(7d⁴+10d²-220625)/25>0`.

Indeed, with `h=d²-625>=0`, the second factor is `7h²+8760h+2520000>0`.

Second, with that same `h`,

`C(0)=55h³+75000h²+31533120h+3800908800>0`.

Because `C` opens downward and is positive at zero, it has exactly two real roots `alpha<0<beta`, and is positive precisely between them. Positivity at the negative number `Tlo` gives `alpha<Tlo<0`. Since `T>Tlo` and `C(T)=0`, necessarily `T=beta>0`.

Now `R=(3d-15)/2>0` and `B=d(d-15)/2>0`. The real nonzero numbers `r,s,t` have product `T>0`. They must all be positive. Otherwise they would have the form `-a,-b,c` with `a,b,c>0`; `R>0` would give `c>a+b`, and therefore `B=ab-c(a+b)<0`, a contradiction.

As positive integers they are all at least 1. Evaluate their monic cubic at 1:

`(1-r)(1-s)(1-t)=1-R+B-T<=0`.

Consequently

`T>=M=(d²-18d+17)/2`.

Here `M>0` for `d>=25`; at `d=25+y` its value is `(y²+32y+192)/2`.

Third, the exact expansion at `d=25+y`, `y>=0`, is

`C(M)=-1197y⁶/4-72099y⁵/2-1756644y⁴-44343384y³-613489632y²-4440240000y-13283343360<0`.

Since `M>0` and `C` is positive on `(0,beta)`, this forces `M>beta=T`, contrary to `T>=M`. This excludes every `d>=25`.

## 6. Complementary triples: the remaining finite list

Oddness now leaves `d=1,3,...,23`. The primitive quadratics and their discriminants are:

| d | Primitive quadratic | Delta | n with n²<Delta<(n+1)² |
|---|---|---:|---:|
| 1 | `329T²-13920T-499200` | 850713600 | 29166 |
| 3 | `1207T²-46020T-1266400` | 8232019600 | 90730 |
| 5 | `11T²-387T+1080` | 102249 | 319 |
| 7 | `107T²+10080T-432000` | 286502400 | 16926 |
| 9 | `193T²+8160T+118400` | -24819200 | negative |
| 11 | `437T²+29790T+853200` | -603949500 | negative |
| 13 | `1421T²+148140T+4125600` | -1504450800 | negative |
| 15 | `2471T²+365088T+8308480` | 51168231424 | 226203 |
| 17 | `143T²+28320T+441600` | 549427200 | 23439 |
| 19 | `401T²+102220T+714400` | 9303030800 | 96452 |
| 21 | `6781T²+2158170T-6106000` | 4823316892900 | 2196205 |
| 23 | `11047T²+4286880T-59011200` | 20984927040000 | 4580930 |

Again, none can have integer `T`. Therefore no complementary-triple case can vanish identically. Together with Sections 1 and 4, this proves the theorem.

## Reproduction, exactness and limits

Run locally in this directory:

```text
python verify.py
python -O verify.py
python verify.py --negative-control
```

The first two runs must pass. The third deliberately corrupts the asserted pair coefficient-12 formula and must fail. The checker uses explicit exceptions, so optimized Python does not disable any check. It writes separate normal and optimized JSON receipts with the exact discriminant tables.

The proof's finite tables are exhaustive because the preceding symbolic inequalities establish the respective bounds on `d`; they are not extrapolation from samples. No enumerations of masks or exponent triples are performed. The coefficient identities hold for signed normalized integer exponents. The strict real-offset range and all divisions have been justified above.

The original independent audit covers the necessary reduction through coefficient 10. The new audit in `../five-row-c12-audit-20261018/AUDIT.md` independently reconstructs coefficients through 12 using double Cauchy–Binet expansions and Schur polynomials, rechecks the earlier reduction, and verifies the elimination, signs, finite tables and complete proof. Both implementations use SymPy 1.14.0, so their algorithmic independence does not constitute separate proof-kernel verification.
