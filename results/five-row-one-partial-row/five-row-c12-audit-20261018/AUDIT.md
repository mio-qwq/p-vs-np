# Independent audit: complete five-row one-partial-row subclass

18 October 2026.

## Verdict and precise scope

**PASS.** The coefficient-12 identities, both elimination quadratics, and the complete arithmetic exclusions are correct. Together with the independently rechecked coefficient-6 through coefficient-9 reduction and the parity argument, they prove:

> A binary 5-by-5 mask with at least four full rows and a nonempty remaining row, distinct real row offsets, and five distinct nonnegative integer column exponents has a translated-power determinant that is not identically zero.

The arbitrary five-row mask problem remains outside this result. An empty remaining row is correctly excluded from the theorem. This is an independently implemented symbolic-algebra audit, not a proof-assistant certificate, novelty assessment, or complexity claim. Both implementations use SymPy 1.14.0.

## Independent coefficient computation

The source exploration uses polynomial quotient rings and convolution of a remainder-matrix determinant. This audit uses **two Cauchy–Binet expansions with Schur polynomials** instead. It neither imports nor executes the source exploration or its checker.

For increasing four-tuples k=(k1,k2,k3,k4), write

    Q_k(e1,e2,e3,e4) = det[binomial(e_j,k_i)] / V(e).

Expand each binomial polynomial into monomials using signed Stirling numbers of the first kind divided by k_i!. A second Cauchy–Binet expansion expresses Q_k as a finite sum of exact coefficient minors times ordinary Schur polynomials in the four exponents. Schur polynomials are evaluated from their elementary symmetric functions through the complete-homogeneous recurrence and the Jacobi–Trudi determinant.

The first Cauchy–Binet expansion of the translated-power determinant then multiplies these normalized exponent minors by the Schur polynomials in the four offsets. Under B=dR-d², the two exponent Vandermonde ratios are both T:

    V(d,r,s,t)/V(r,s,t) = (r-d)(s-d)(t-d) = T,
    V(0,r,s,t)/V(r,s,t) = rst = T.

Thus the normalized pair coefficient is obtained by summing, over sum(k)=the requested coefficient degree, the offset Schur polynomial times T[Q_k(d,r,s,t)-Q_k(0,r,s,t)]. The full five-row coefficients are calculated analogously with five-variable Schur polynomials and Vandermonde factor E4*d*T². Every calculation is symbolic; there are no numerical samples or fitted coefficients.

`audit_reduction.py` separately rechecks the general C6–C9 identities by the same independent method, with R,B,E1,E2,E3,E4 initially free. `audit_c12.py` checks the pair and full C10 and C12 identities after the necessary reductions. The coefficient formulas match exactly.

## Normalization and all possible divisions

Translate the partial-row offset to zero, choose the retained pair if its support has size two or the omitted pair if its support has size three, and subtract the smaller exponent of that pair. The exponents are (0,d,r,s,t), where d is a positive integer and r,s,t are distinct integers, none equal to 0 or d. Negative outside exponents are legitimate: normalization only factors a nonzero rational function, and fixed formal coefficients at infinity use polynomial binomial coefficients.

The prior reduction gives

    B=dR-d², R=(3d-15)/2, E1=E3=0,
    E2<0, E4>0, T=rst != 0.

Its divisions are justified by d>0, T != 0, E2<0 and d²+95>0. The nonzero real distinct offsets are necessarily (-u,u,-v,v), with u,v>0 and u != v. Consequently

    rho=E4/E2²=u²v²/(u²+v²)², 0<rho<1/4.

Both Vandermonde divisors are nonzero. Dividing the C10/C12 formulas by their indicated scalar factors loses no solutions because d, T and E2 are nonzero. No coefficient of rho is divided out during elimination.

The equation for R implies d is odd. In the retained-pair case the previously audited parity argument also gives d=1 modulo 4. Briefly, d=3 modulo 4 forces exactly one of r,s,t odd, so the four cofactor exponents d,r,s,t have two even and two odd values. At the partial-row root, opposite-pair sum/difference operations split the cofactor into two nonzero generalized 2-by-2 Vandermonde blocks. This contradicts zero determinant. Negative integer cofactor exponents cause no singularity because all four cofactor bases are nonzero there.

## C12 identities and division-free elimination

Define

    A = 5T+4d²-460,
    P = 68T+74d²-3050,
    Q = 2T-74d²+3050,
    N = (33d²-600d+7335)T
        +25d⁴-480d³+2830d²+55200d-630695,
    K = (468d²-8160d+90060)T
        +490d⁴-8880d³+75580d²+366000d-4015910,
    L = 700T(d²-12d+119)-K.

The independently reconstructed coefficients are

    c12(pair) = E2*d*T*(E2²*N-E4*K)/4838400,
    c12(full) = -E2*E4*d*T²*(d²-12d+119)/6912,
    c12(complement) = -E2*d*T*(E2²*N+E4*L)/4838400.

Thus necessary pair equations are f10=A-P*rho=0 and f12=N-K*rho=0. The exact polynomial identity

    K*f10-P*f12 = 2 H_d(T)

holds, where

    H_d(T) = (48d²-24240)T²
             +(90d⁴-55860d²+1875930)T
             +55d⁶-28125d⁴+2236245d²-38150575.

The necessary complement equations are g10=A+Q*rho=0 and g12=N+L*rho=0. Their exact identity is

    Q*g12-L*g10 = 2 C_d(T),

where

    C_d(T) = (24235-547d²)T²
             +(-435d⁴+37590d²-1039395)T
             +55d⁶-28125d⁴+2236245d²-38150575.

These identities prove necessity even when P,K,Q or L is zero. A resultant need not be sufficient here; only these necessary consequences are used.

## Complete retained-pair exclusion

The discriminant of H_d is -60F(d²), with

    F(q)=41q⁴-11300q³-5027466q²-242872100q+2999439785.

The exact shifted expansion is

    F(529+y)=41y⁴+75456y³+45880320y²+9229344768y+5573836800.

All coefficients are strictly positive. Therefore d>=23 gives negative discriminant, excluding every real T. The remaining positive d=1 modulo 4 values are 1,5,9,13,17,21.

For any integer polynomial aT²+bT+c with an integer root, the identity

    (2aT+b)² = b²-4ac

makes its discriminant a nonnegative integer square. This necessity does not divide by a. The following exhaustive exact table rules out all remaining d; n denotes floor(sqrt(discriminant)), so each positive row satisfies n²<discriminant<(n+1)².

| d | Discriminant of H_d | n or reason |
|---:|---:|---:|
| 1 | -165091737600 | negative |
| 5 | 382504550400 | 618469 |
| 9 | 3233926348800 | 1798312 |
| 13 | 12164003020800 | 3487693 |
| 17 | 28430283571200 | 5332005 |
| 21 | 30016422297600 | 5478724 |

## Complete complementary-three-column exclusion

For d>=25, the C10 equation uniquely gives

    T = [460-4d²+(74d²-3050)rho]/(5+2rho).

Here 5+2rho>0, so there is no exceptional denominator. Put ell=92-4d²/5. Direct subtraction yields

    T-ell = 42(9d²-385)rho/[5(5+2rho)] > 0.

The quadratic C_d has negative leading coefficient. Its constant term is positive for q=d²>=625, since

    C_d(0) at q=625+y
      =55y³+75000y²+31533120y+3800908800 > 0.

It follows that C_d has one negative and one positive real root. Also ell<0, and

    C_d(ell) = 21(9d²-385)(7d⁴+10d²-220625)/25 > 0.

The two factors in the last expression are positive for d>=25, as checked by positive-coefficient expansions at d=25+y. Therefore the negative root lies strictly below ell. Since the necessary T obeys T>ell and C_d(T)=0, it must equal the positive root. In particular T>0.

For this range, R>0 and B>0. Since r,s,t are real, nonzero and have positive product T, they are either all positive or exactly two are negative. If they were (-u,-v,w), with u,v,w>0, then R>0 would imply w>u+v, and

    B=uv-w(u+v)
      =-(u²+uv+v²)-(w-u-v)(u+v) < 0,

contradicting B>0. Thus all three are positive integers, hence each is at least 1. It follows that

    0 <= (r-1)(s-1)(t-1) = T-B+R-1,
    T >= B-R+1 = M=(d²-18d+17)/2 > 0.

However, the exact expansion at d=25+y is

    -C_d(M) = 1197y⁶/4+72099y⁵/2+1756644y⁴
              +44343384y³+613489632y²
              +4440240000y+13283343360 > 0.

Since M>0, C_d(0)>0 and C_d is concave with precisely one positive root, C_d(M)<0 places that positive root strictly below M. This contradicts T>=M. Every d>=25 is therefore excluded.

All remaining d are the odd integers 1,3,...,23. Divide each specialized C_d by the positive gcd of its integer coefficients, obtaining a primitive integer quadratic. A root in integers still requires the primitive discriminant to be a nonnegative integer square. The table below is exhaustive; the exact primitive coefficients, gcds, and consecutive-square bounds are stored in `complement_receipt.json`.

| d | Primitive discriminant | n or reason |
|---:|---:|---:|
| 1 | 850713600 | 29166 |
| 3 | 8232019600 | 90730 |
| 5 | 102249 | 319 |
| 7 | 286502400 | 16926 |
| 9 | -24819200 | negative |
| 11 | -603949500 | negative |
| 13 | -1504450800 | negative |
| 15 | 51168231424 | 226203 |
| 17 | 549427200 | 23439 |
| 19 | 9303030800 | 96452 |
| 21 | 4823316892900 | 2196205 |
| 23 | 20984927040000 | 4580930 |

This completes the three-retained-column branch. No finite experimental search over exponent triples is used: the infinite range has an explicit analytic exclusion and the finite range is excluded by exact discriminants.

## Other support sizes and final theorem

For support size one, the leading four-row cofactor coefficient is a nonzero exponent Vandermonde times the nonzero offset Vandermonde. For support size four, its complement is a singleton and the full determinant contributes nothing before degree 10, so the same leading coefficient is nonzero up to sign. Support size five is the full alternant and has a nonzero leading generalized-Vandermonde coefficient. The new pair and complement arguments exclude sizes two and three. Every nonempty support is therefore covered.

## Reproduction and limitations

Run in this directory:

    python audit_c12.py
    python audit_complement.py
    python audit_reduction.py
    python audit_final_tables.py

Each command also passes with `python -O`; its normal and optimized stdout logs are byte-identical. The checkers raise explicit exceptions and do not rely on Python `assert`. The C12 checker performs 15 checks, the complement checker 31 checks, the prior reduction checker four checks, and the final-text checker verifies all 18 printed quadratic/discriminant rows.

Both deliberate corruptions fail with nonzero exit code and residual -1:

    python audit_c12.py --negative-control
    python audit_complement.py --negative-control

The source data are read only; all audit code, reports, and receipts are local to this audit directory. No remote writes were made. The coefficient data are compared against independently reconstructed formulas, rather than used as the reconstruction input. The complement checker consumes the independently reconstructed coefficient receipt.

The report also verifies the finalized source `five-row-c12-20261018/PROOF.md`, whose hash is recorded below. Its formal coefficient convention, row/column permutation invariance, support-size coverage and every required real-offset assumption have been reviewed. Later changes would require renewed review. The arbitrary five-row mask problem remains outside this result.

## Reviewed source hashes

- `five-row-c12-20261018/PROOF.md`: `910d2402ff79ab239f8c9072afd70c61b90b1b3b779f40fec3029d77fc767219`
- `five-row-c12-20261018/verify.py`: `187230c31c5cf8da5bd5b4e4e0b119987e69e638e5db02d126c3583aa61238f1`
- `five-row-c12-20261018/coefficients.json`: `aed949a2edfd4594c886e42f9d28f52b3e040523b8d2bcad45486bf3f009f6bb`
- `five-row-c12-20261018/elimination.json`: `2332bdb3d8f9798574d2a78fd2dd316ab70f30c1d9ef492e077abb9473aba173`
- `five-row-c12-20261018/explore.py`: `315b1ef91276aed260a44bd1470f4244dbc6c0f7cb2447525e4f9cef582393f5`
- `five-row-cancellation-20261018/PROOF.md`: `09562d66d49a7d35a4193444487e53a00d7ad1922bcb8ccc565d4cc1ddc58179`
