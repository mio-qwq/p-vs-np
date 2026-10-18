# Five-row partial-row obstruction and exact failed cancellation

18 October 2026. Scope: a genuine subclass of the general five-row problem, with arbitrary distinct integer exponent gaps. This is a mathematical derivation with an exact algebra checker, not an independently audited or proof-assistant-verified theorem. The general five-row masked determinant remains unresolved here.

## Result

Let four rows of a binary 5-by-5 mask be full and let the remaining row retain a nonempty set S of columns. The offsets are distinct and real, and the column exponents are distinct nonnegative integers.

If its translated-power determinant were identically zero, then:

1. The partial row retains exactly two or three columns.
2. After translating its offset to zero, the other offsets must be `(-u,u,-v,v)`, up to row order, with `u,v>0` and `u!=v`.
3. Take the retained pair when |S|=2, or the omitted pair when |S|=3. After subtracting the smaller exponent of that pair from every exponent and putting the pair first, the exponents have the form `(0,d,r,s,t)`, where d>0. The other three integers may be negative. Put `R=r+s+t`, `B=rs+rt+st`, `T=rst`. Necessarily

   `B=dR-d²`, and `R=(3d-15)/2`.

   In particular d is odd, and

   `r²+s²+t²=(R-d)²+d²`.

4. If |S|=2, necessarily `d=1 mod 4`.
5. Put `rho=u²v²/(u²+v²)²`, so `0<rho<1/4`, and `A=5T+4d²-460`. Further necessary equations are

   pair retained: `A=(68T+74d²-3050)rho`;

   pair omitted: `A+(2T-74d²+3050)rho=0`.

These are obstructions, not sufficient conditions for cancellation.

## Formal normalization and coefficient convention

Subtracting the smaller exponent of the chosen pair factors a nonzero rational function from each row. Thus zero versus nonzero is unchanged even when the remaining exponents become negative. The argument uses formal binomial series at infinity and never evaluates a negative power at its own zero.

Translate the partial row offset to zero. Let the other offsets be b1,...,b4, all nonzero and distinct. Put z=1/x and

`H(z)=det[A_ij (1+a_i z)^e_j]=sum C_k z^k`.

Let `V(b)=product_{i<j}(b_j-b_i)`, `V(r,s,t)=(s-r)(t-r)(t-s)`, and let E_i be the elementary symmetric polynomial of degree i in b1,...,b4. Both Vandermonde factors are nonzero.

For the two-retained-column mask, the first row is `(1,1,0,0,0)`. Its determinant is the difference of the four-row full alternants with exponent lists `(d,r,s,t)` and `(0,r,s,t)`. Denote the coefficients divided by `V(b)V(r,s,t)` by c_k. All coefficients below k=6 vanish.

Cauchy--Binet gives c_k by summing over `0<=k1<k2<k3<k4` of total k: the offset alternant divided by V(b), times the difference of the two binomial minors divided by V(r,s,t). Each coefficient is a finite polynomial even for signed exponents.

## Necessary equations, with all divisions justified

Direct exact expansion gives

`c6=-d(d²-dR+B)/12`.

Thus `B=dR-d²`. Under this equation,

`c7=E1*T*d/48`.

Since r,s,t,d are nonzero, T*d is nonzero; consequently E1=0.

Under the first two equations,

`c8=E2*T*d*(2R-3d+15)/720`.

Realness now gives `E2=-(b1²+b2²+b3²+b4²)/2<0`. Therefore `R=(3d-15)/2`.

Under these three equations,

`c9=-E3*T*d*(d²+95)/1920`.

Since `d²+95>0`, E3=0. The monic polynomial with roots b1,...,b4 is consequently `X⁴+E2 X²+E4`, an even polynomial. Its four distinct nonzero real roots occur in opposite pairs. Relabeling and changing signs gives offsets `(-u,u,-v,v)` with u,v>0 and u!=v. This proves the first three nontrivial obstructions.

For a three-retained-column mask, use the complementary pair. The two determinants sum to the full five-row determinant. The latter begins at coefficient 10, because the smallest five distinct nonnegative row degrees sum to 0+1+2+3+4=10. Hence coefficients 6 through 9 of the complementary mask are the negatives of the displayed expressions, and exactly the same necessary equations follow.

If |S|=1, its c6 is a single nonzero four-exponent Vandermonde divided by 12. If |S|=4, its coefficient 6 is the negative of that for its singleton complement. If |S|=5, the full generalized Vandermonde has a nonzero coefficient 10. These exclude the other nonempty cardinalities.

## Parity obstruction for two retained columns

If d=3 mod 4, R=(3d-15)/2 is odd and B=dR-d² is even. Among r,s,t the number k of odd integers must satisfy k odd and binomial(k,2) even, so k=1. The four cofactor exponents d,r,s,t therefore comprise two even and two odd integers.

At x=0, the normalized partial row `(1,x^d,0,0,0)` is `(1,0,0,0,0)`. All other row bases are nonzero. The cofactor with offsets `(-u,u,-v,v)` and exponents d,r,s,t is nonzero: sum and difference within each opposite row pair split it into a 2-by-2 block for even exponents and another for odd exponents. Each block has determinant, up to nonzero factors, `u^alpha v^beta-u^beta v^alpha`, nonzero for distinct integer alpha,beta of the same parity and distinct positive u,v. Thus the full determinant is nonzero, a contradiction. This argument is valid for negative cofactor exponents as well.

A related optional filter for a three-retained-column candidate: factor the smallest retained exponent from all rows and evaluate at the partial row's root. If deleting that minimum exponent leaves two even and two odd exponents, the same cofactor argument excludes the candidate.

## Coefficient 10 and the real-offset interval

Under all the necessary equations through coefficient 9, exact expansion gives

`c10(pair)=-dT[(5T+4d²-460)E2²-(68T+74d²-3050)E4]/20160`.

The coefficient of the full five-row determinant, with the same normalization, is `dT² E4/288`. Subtraction therefore gives

`c10(complement)=dT[(5T+4d²-460)E2²+(2T-74d²+3050)E4]/20160`.

Since `E2²>0`, division gives the rho conditions in the result. The strict interval follows from `(u²-v²)²>0`, with u,v nonzero. No division by either displayed coefficient of rho is needed; its zero case remains covered by the equation itself.

## An engineered cancellation that survives through coefficient 10 and then fails

Take exponent set `(0,3,5,8,9)`, partial-row support `{0,3,9}` (these are exponent values), and other offsets `(-1,1,-v,v)`. The center offset is zero. The omitted pair is (5,8), so the normalized exponents are `(0,3,-5,-2,4)` after column permutation: d=3, R=-3, B=-18, T=40. All necessary equations through coefficient 9 hold for every v. The determinant has total exponent sum 25.

Its coefficient of x^15 is

`-864 v(v²-1)² (v⁴-9v²+1)`.

Thus choose the genuinely distinct real symmetric offsets with

`v²=(9+sqrt(77))/2` or `(9-sqrt(77))/2`.

This kills that coefficient as well. Reflection symmetry makes the determinant odd in x, so there is no x^14 coefficient. But its x^13 coefficient is

`36 v(v²-1)²(v²+1)(23v⁴-282v²+23)`.

Modulo `v⁴-9v²+1`, the final factor is `-75v²`, and the coefficient becomes

`-2700 v³(v²-1)²(v²+1)`,

which is nonzero for either allowed positive value of v. Thus this construction is exactly ruled out; no numerical test is involved.

For comparison, the two-retained-column mask on the same exponent pair already fails at coefficient 10: after necessary normalization, its residual is proportional to `-224(u⁴+v⁴)-784u²v²`, which cannot vanish for nonzero real u,v.

A second useful arithmetic branch is d=7 and `(r,s,t)=(-5,2,6)`, corresponding after a common shift to exponent set `{0,5,7,11,12}`. The two-retained-column mask is ruled out by the general parity argument. The three-retained-column complement would require `-564(u⁴+v⁴)-1824u²v²=0`, which is impossible. This is an exact exclusion of that exponent branch for every set of distinct real offsets, because any zero determinant would first have forced the symmetric-offset reduction.

## Explicit residual branch, not resolved here

The necessary conditions do not already prove the one-partial-row subclass. For example, take the retained-pair normalization

`d=9, (r,s,t)=(-5,4,7), T=-140`.

This has R=6 and B=-27 as required, and d=1 mod 4. Its coefficient-10 condition is

`rho=209/1644`,

which lies strictly between zero and one quarter and hence is compatible with distinct real opposite offset pairs. The original nonnegative exponent set is `{0,5,9,12,14}`, with the partial row retaining exponents `{5,14}`. This is only an unresolved candidate for further obstruction, not a counterexample. The next useful exact test is coefficient 12 or the center cofactor's low-order derivatives. No search over larger gaps was performed in the certified argument.

## Verification and limitations

Run `python verify.py` in this directory. It reconstructs the required coefficients using exact binomial minors and Schur polynomials, checks their reductions without relying on numerical exponent/offset samples, checks the full-determinant coefficient, and verifies the engineered candidate's two leading coefficients. It does not import the earlier four-row work. `python -O verify.py` also runs the same explicit checks. A `--negative-control` option deliberately corrupts c9 and must fail.

The general five-row mask case remains open in this work. Even the one-partial-row subclass is not completely proved: the listed conditions leave additional arithmetic/symmetric branches. No absence in a finite sample is reported as a theorem. No claim about colored ASNC, complexity, novelty, or P versus NP is made. All files and computations are local-only.
