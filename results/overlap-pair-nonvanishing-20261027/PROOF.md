# Computer-assisted nonvanishing: five-row overlapping-pair mask

Status: integration of exact mathematical reductions and two independent exhaustive computations; final review receipts are recorded separately. This is one restricted determinant model, not P vs NP or a general circuit lower bound. No priority or human peer-review claim.

## Statement

Let a, b, c, d, e be pairwise distinct nonnegative integers and r1, ..., r5 pairwise distinct complex numbers. Let M(X) have entries (X+ri)^ej on a mask whose first two rows have supports {a, b} and {a, c}, and whose other three rows are full. Then det M(X) is not identically zero. Real offsets are included.

**All-integer corollary.** The same conclusion holds for arbitrary pairwise distinct integer exponents, with the determinant interpreted in C(X). If m is the least exponent, each row has the common nonzero rational factor (X+r_i)^m; factoring their product reduces to the nonnegative-integer statement. Thus no negative-exponent case is omitted.

**Packet map.** Sections 1–5 retain the integrated argument, with the two reviewed editorial nits corrected, English spacing polished, and local links supplied. Sections 6–8 supply its normalization, full structural proof, and complete compact C7 formulas so this document is standalone. Byte-for-byte originals and review receipts are in `reviews/`; independent AI-assisted reviews are not independent human peer review. Runtime and portable-edit details are in `README.md` and `PORTABILITY.md`.

## 1. A proved finite exponent bound

The self-contained `reviews/structural/PROOF.md` and independent `reviews/height/REVIEW.md` prove that any counterexample has every consecutive exponent gap at most 408, hence span at most 1632. This is independent of low-coefficient elimination.

The proof considers the 18 permitted determinant monomials, of equal total degree. In a minimal linear circuit of k <= 18 terms, divide their gcd to obtain equal-degree D polynomials supported on at most 5 roots. For n=k−1 and C=binom(n,2), proportional omitted-column Wronskians yield deg W >= kD−5C. Gaussian elimination to distinct leading degrees gives deg W <= nD−2C. Thus D <= 3C <= 408. A gap larger than 408 prevents circuits from crossing the associated row-assignment classes. Their spans form a direct sum. One class factors into nonzero proper minors, including only a specifically proved two-partial four-row minor, so its sum cannot vanish. No false general complex four-row assertion is imported.

Subtracting the least exponent preserves identity-zero by factoring nonzero row powers. The bound is on the span; subsequently subtracting the shared exponent a gives (0, B, C, D, E), with every entry in [−1632,1632] and total span <= 1632. Swapping b, c together with the two partial rows and swapping d, e preserve identity-zero; therefore assume B<C and D<E. Normalize the two partial offsets to 0,1 by an invertible affine change of X.

## 2. Necessary algebraic coefficient equations

Write u=D+E, v=DE, x=u−B, y=u−C, L=x+y, A=xy, t=u−L, K=A+2L. Direct normalized determinant expansion first gives

    v=u(B+C)−B²−C²=tL+2A.                        (C3)

The normalization divides only the nonzero full-offset Vandermonde, E−D and a power-series unit. Coefficient vanishing is therefore preserved. The later equations are algebraic over C and require no real positivity. Independent direct power/binomial alternants regenerate the universal coefficients through 8 in the sealed original work; the portable `scripts/check_coefficients.py` independently regenerates exactly C3–C7 needed here.

Let e1, e2, e3 be the elementary symmetric full offsets. The undivided C4 equation is BC(Le1−3x)=0, up to a nonzero constant. Thus L=0 would force x=y=0 and B=C, impossible. If A=0, say x=0, C3 forces one of D, E to equal C; the other case is symmetric, also impossible. Under C4, the undivided C5 equation is

    L²K(e1²−3e2)=9A(v+L).

If K=0, then v=−L and u=L+3. The integer equation (x+2)(y+2)=4 leaves, after x != y and A != 0, the pairs (-1,2), (2,-1), (-3,-6), (-6,-3). The first pair types give (u, v)=(4, −1), whose discriminant 20 is not an integer square. The others give (u, v)=(-6,9), forcing D=E. Thus L, A, K are nonzero in any candidate.

Set R=A/L, Z=t+2R+1, delta=x−y. Use the exact compact mu, eta, Q, N, Phi expressions in `inputs/C7_FORMULAS.json`. After C3–C5, with g6=C6/(BC), g7=C7/(BC), exact elimination gives

    mu*g7 − [mu*(u−6)/2 + delta*Q/(2L)]*g6
      = −R*Phi/[240L(R+2)²].

This identity uses delta²=L(L−4R), but never divides by mu. Consequently identity-zero implies Phi=0 even when mu=0, Z=0 or R=−4. Define

    P7(L,A,t)=L^5 Phi(L,A/L,t+2A/L+1) in Z[L,A,t].

It is the 112-term polynomial checked by both enumeration implementations and by a separately handwritten factored-Phi evaluator. Every candidate in the remaining domain with L, A, K all nonzero must satisfy P7=0. No assumption on the six formerly open order types is needed below: all 30 canonical orders are included.

## 3. Complete finite C3 parametrization

Equation C3 is equivalent to

    (D−B−C)(E−B−C)=2BC.

For every pair −1632 <= B<C <= 1632 with B, C nonzero and max(0, C)−min(0, B) <= 1632, enumerate every signed divisor h of 2BC, put k=2BC/h, and retain h<k. Set D=B+C+h, E=B+C+k. Retain exactly the tuples with all five entries distinct and span <= 1632. Both positive and negative divisors are included. This is equivalent in both directions to all integer C3 candidates in the proved height domain; the D−B−C=0 case is impossible because BC != 0.

## 4. Exact exhaustive certificate

Two independently implemented C++ signed-divisor engines agree, and independent small-height direct B, C, D-to-E enumeration controls the coverage. The counts for the full proved domain are:

- B, C pairs: 3,992,688.
- Distinct C3 tuples across all 30 canonical orders: 19,658,082.
- L=0: 3,540; A=0 after L exclusion: 0; K=0 after L, A exclusion: 6.
- Tuples with L, A, K all nonzero: 19,654,536.
- Survive exact P7 modulo 101: 220,631.
- Survive exact P7 modulo 101 and 103: 2,432.
- Satisfy P7=0 under arbitrary-precision integer evaluation: 0.

The second implementation also evaluates each of the 2,432 survivors using a separately handwritten rational factored Phi, obtaining exactly the same nonzero values after multiplying by L^5. Singular mu, Z, R+4 cases are not dropped. The root ordered survivor file has SHA-256 `b008f2a7ec55b6156c355ff6d2c83b11cf4580a42b6046ba1a823e7757dc83c5`; the independent file ordering differs but the tuple sets coincide exactly.

All modular filters are exact necessary conditions: a zero integer polynomial must vanish modulo both primes. All remaining cases are checked with unbounded Python integers. Fixed-width enumeration arithmetic has explicit bounds: |2BC| <= 5,326,848, and every generated divisor/prime power and pre-filter exponent value fits signed 32-bit; A uses 64-bit; modular products and indices are far smaller. Compiler optimizations do not change the stated integer operations. Independent source audit and sanitizer/small-domain controls are documented in the review packet.

## 5. Conclusion and limits

The structural argument excludes every larger exponent span. The exhaustive certificate excludes every remaining regular integer C3/P7 candidate; the three low-denominator cases were excluded algebraically. This proves the stated nonvanishing theorem for the overlapping-pair mask, including complex distinct offsets. It replaces the earlier 24/30 partial classification for this specific mask, not for arbitrary five-row masks.

The final theorem is computer-assisted, with explicit finite exact code and certificates. It is not a claim of Lean formalization, independent human review, general arithmetic circuit separation, or resolution of P vs NP.

## 6. Exact normalization and the coefficient certificate

Work after the affine normalization and subtracting the shared exponent a. With z=1/X, remove the nonzero common rational row powers. Let the full offsets be r_3, r_4, r_5, and set

    V = (r_4-r_3)(r_5-r_3)(r_5-r_4),
    F_h(z) = det[(1+r_i z)^h, (1+r_i z)^D, (1+r_i z)^E]_(i=3,4,5),
    G(z) = [F_0(z)-F_B(z)-(1+z)^(-C) F_C(z)]/V,
    C_n = [z^n]G(z)/(E-D).

Laplace expansion gives the normalized masked determinant as (1+z)^C V G. The factors V and E-D are nonzero constants, and (1+z)^C is a formal power-series unit even for negative integer C. All these normalizations preserve identity-zero. Every exponent-binomial coefficient is the polynomial

    binom(h,j) = h(h-1)...(h-j+1)/j!.

Cauchy–Binet expands F_h using triples 0 <= i<j<k: each term is the determinant of offset powers times the determinant of exponent-binomial coefficients. Offset alternants divide exactly by V; symmetric conversion gives polynomials in e1, e2, e3. The exponent alternant contains (D-h)(E-h)(E-D), so after dividing by E-D it is polynomial in h, u=D+E, v=DE. Thus every identity here is algebraic over C, not dependent on realness or numerical evaluation.

Before imposing C3, direct expansion gives

    C_3 = [u(B+C)-B²-C²-v]/2.

After C3, the exact fourth coefficient is

    C_4 = -BC(Le1-3x)/6.

After C3 and C4, the fifth coefficient is

    C_5 = BC/[36L²] * [L²K(e1²-3e2)-9A(v+L)].

This formula does not divide by K. Section 2 therefore excludes each of L=0, A=0, and K=0 algebraically before any corresponding division.

For LAK != 0 define m=x/L, p=e1²/3-e2, and q=e3-m³+mp; the full offsets shifted by m have cubic s³-p s-q. C4 fixes e1=3m and C5 fixes

    p = 3RZ/[L(R+2)].

Leave q free. In particular there is no division by mu. The exact subsequent identities are

    g6 = C_6/(BC) = L mu q/120 + R delta eta/[24L(R+2)],
    g7 = C_7/(BC) = (u-6)g6/2 + delta Q q/240
                                   - R N/[240L(R+2)²].

Substitution into the μ-undivided relation in Section 2 proves that every identity-zero candidate satisfies P7=0, including mu=0. `scripts/check_coefficients.py` derives all five coefficients afresh from alternating determinants before comparing the prior raw table. It checks these identities, the L/A/K exclusions, the exact Laplace normalization, and the 112-term integral expansion with explicit errors that remain active under `python -O`.

## 7. Full finite-height argument

The following is the complete mathematical core of the structural proof. The dated original and independent review are preserved in `reviews/structural/PROOF.md` and `reviews/height/REVIEW.md`. Their earlier partial-status descriptions predate the completed enumeration and are historical, not limitations of the combined result.

### 7.1. Equal-degree S-unit circuit lemma (proved here)

Let f_1,..., f_k be a minimally linearly dependent set over C of distinct
nonzero monomials in s distinct linear factors X-rho_1,..., X-rho_s, all of
the same total degree. Let g be their polynomial gcd, g_i=f_i/g, and D the
common degree of the g_i. Then

    D <= (s-2) * binom(k-1,2).

Here a minimal circuit has a relation with every coefficient nonzero, and
any k-1 of its elements are linearly independent. Put n=k-1 and
C=binom(n,2). All n-element omitted-column Wronskians are nonzero and
constant multiples of one another. Nonzero follows, for polynomials in
characteristic zero, by constant Gaussian elimination to a basis of
pairwise distinct degrees and the nonzero degree Vandermonde of their
leading terms. Proportionality follows by differentiating the minimal
constant-coefficient relation through derivative order n-1.

At rho_l some g_j has valuation zero, because gcd(g_1,..., g_k)=1. Use the
Wronskian omitting that j. Writing v_i, l=ord_(rho_l)(g_i), every determinant
term has valuation at least

    sum_i v_i,l - (0+1+...+(n-1)) = sum_i v_i,l - C.

The inequality remains valid when a derivative vanishes or when its
stated valuation lower bound is negative. Since all Wronskians are
proportional, one fixed W has all these valuation lower bounds. Since each
g_i has only the s listed roots and degree D,

    deg W >= sum_l ord_(rho_l) W >= k D - s C.             (1)

For the upper bound, perform constant changes of basis among the n
polynomials in one Wronskian, producing distinct degrees
0 <= d_1 < ... < d_n <= D. Therefore

    deg W <= sum_j d_j - C <= n D - 2 C.                 (2)

Combining (1) and (2) gives D <= (s-2)C. The additional C in (2), compared
with the coarser naive degree bound, is essential to the constant 408.

In particular, if two circuit members assign powers u and v to the same
linear factor, then |u-v| <= D: the largest such power minus the minimum
power in that factor is one summand of the residual degree of a member
attaining that largest power.

### 7.2. Apply the circuit lemma to the 18 determinant terms

There are precisely 18 permitted permutations: the partial rows have the
three distinct-column choices (a, c), (b, a), (b, c), and the three full rows
have 3! completions. Their monic polynomial terms are pairwise distinct:
different permutations assign different exponents to at least one of the
five distinct linear factors. All terms have the same total degree.

Every minimal linear circuit of these terms has k <= 18 and s <= 5. Hence any
two powers used at the same row within one circuit differ by at most

    (5-2) * binom(18-1,2) = 3*136 = 408.                  (3)

Suppose the sorted exponents have a consecutive gap greater than 408, and
split the columns at that gap into nonempty sets L and H. Give each
permutation term its row-assignment pattern: which rows use an L column
and which use an H column. A circuit cannot contain terms of different
patterns, since then at some row it would assign exponents differing by
more than 408, contradicting (3).

It follows that the vector spaces spanned by the different pattern classes
form a direct sum. For completeness: choose a basis from the terms of each
class. If the union of these bases were dependent, it would contain a
minimal circuit. Such a circuit cannot be contained in a single class
(the chosen class elements are independent) and cannot cross classes by
(3), a contradiction. Thus any relation among determinant terms splits
into relations separately within each row-assignment pattern. This is the
needed matroid/direct-sum step; no termwise linear independence is assumed.

### 7.3. One pattern has a nonzero block-factor determinant

One of L, H contains at least two of {a, b, c}; call that side S. Put both
partial rows and any |S|-2 full rows on side S. All remaining rows are full
and are put on the other side. There is a perfect matching in each block:
any two distinct columns from {a, b, c} match the two partial supports.

The signed sum of terms in precisely this assignment pattern is, up to an
overall sign, the product of the determinants of the two square blocks.
Their sizes are |S| and 5-|S|, both between 1 and 4. The second block is
full. The first has the two inherited partial rows, together with full
rows. Every such proper block is nonzero, as established next. Thus the
pattern sum is nonzero, contradicting the direct-sum conclusion from an
identity-zero full determinant.

#### Full blocks

For distinct exponents e_j and offsets r_i, the leading nonzero coefficient
at infinity of a full m by m generalized Vandermonde is the product of the
offset Vandermonde and exponent Vandermonde divided by
0!1!... (m-1)!, up to the chosen ordering sign. In particular the full
block determinant is not identically zero, also over C. This follows by
expanding (1+r_i z)^{e_j} and choosing distinct Taylor degrees 0,..., m-1.

#### Proper blocks retaining both partial rows

If the column set has exactly two of {a, b, c}, a forced matching of the
partial rows leaves a full block, so the determinant is a nonzero monomial
factor times a nonzero full minor. If its size is three and it contains
all of {a, b, c}, its mask determinant is -1, so its top-degree coefficient
is nonzero. The only remaining case has size four and columns a, b, c, d
(or a, b, c, e). A short independent exact proof of that particular minor is
included here; it does not assume the false general complex-offset
four-row conjecture.

Normalize partial offsets to 0,1, factor out the common exponent a from
each row, and write the remaining exponents 0, B, C, D. Thus B, C, D are
nonzero and pairwise distinct. Write the full offsets as p, q, which are
distinct and avoid 0,1. Set z=1/X and

    V_uv(z)=(1+p z)^u(1+q z)^v-(1+p z)^v(1+q z)^u,
    H(z)=V_0D(z)-V_BD(z)-(1+z)^(-C)V_CD(z).

The normalized four-row determinant is (1+z)^C H(z), a unit times H near
z=0. Write h_j=[z^j]H/(q-p). Direct binomial expansion gives successively

    h_1 = B+C-D,
    h_2 |_(D=B+C) = -BC(p+q-1),
    h_3 |_(D=B+C,q=1-p) = BC p(p-1)(B+C+2)/2,
    h_4 |_(D=B+C,q=1-p,C=-2-B) = BC p(p-1)(B+1)/6.

If the determinant vanished identically, these equations would force
D=B+C, p+q=1, C=-2-B, and B=-1. Then C=-1=B, contradicting distinct
exponents. Every canceled factor is nonzero by the stated hypotheses.
The attached own-code checker regenerates these four identities from
binomial products; no repository code was executed.

This completes the gap theorem. Four consecutive gaps each at most 408
give the normalized span bound 1632.


## 8. Explicit compact polynomial definitions

These formulas, also stored as parseable text in `inputs/C7_FORMULAS.json`, define the exact obstruction. No omitted table or remote source is needed. Define N=L² n2+L n1+n0 and Phi=mu N+5(R+2)(L-4R)eta Q:

```text
mu = 2*L**2 + L*(-8*R - 5*Z + 5) + 6*R**2 - 7*R*Z - 8*R + 2*Z**2 - 4*Z - 18

eta = 2*R*(R + 2) + Z**2*(R - 4) - Z*(R + 4)*(2*R + 1)

Q = 2*L**3 + L**2*(-16*R - 3*Z - 9) + L*(38*R**2 + 4*R*Z + 29*R - 3*Z**2 + 36*Z - 53) - 24*R**3 + 32*R**2*Z - 8*R**2 - 14*R*Z**2 + 40*R*Z + 144*R + 2*Z**3 - 18*Z**2 + 10*Z + 126

n2 = -10*R*(R + 2)**2 - 2*Z**2*(R**2 - 11*R - 20) + 5*Z*(R + 2)*(R + 4)*(2*R + 1)

n1 = 15*R*(R + 2)**2*(5*R + 4) - 15*Z**3*(R**2 + 2*R - 4) + Z**2*(43*R**3 + 52*R**2 - 80*R - 180) - 5*Z*(R + 2)*(15*R**3 + 85*R**2 + 101*R + 24)

n0 = -20*R**2*(R + 2)**2*(7*R + 12) + 3*R*Z**4*(R + 4) + R*Z**3*(23*R**2 - 88*R - 304) - R*Z**2*(128*R**3 + 467*R**2 + 170*R - 672) + 10*R*Z*(R + 2)*(14*R**3 + 98*R**2 + 171*R + 50)
```

Expanding L^5 Phi(L, A/L, t+2A/L+1) gives exactly 112 integer terms of coordinate degrees (8,6,6). Engine A contains the complete table in `sources/engine_a.cpp`. The portable verifier derives it from the formulas above, checks every coefficient against that table, and independently generates Engine B's header. `scripts/phi.py` is a handwritten rational factored evaluator independent of either sparse-polynomial implementation.

The 2,432 modular survivors are recorded in `certificates/survivors.tsv`; columns are B, C, D, E, order, L, A, t, M with M=L*mu. `scripts/check.py` checks row count, distinctness, all coordinates, both modular conditions, and every exact nonzero value using both Python integer polynomial evaluation and the rational factored evaluator. In full mode it recompiles the two original independently implemented engines and recomputes the complete survivor set and all per-order counts from scratch. Thus this certificate is not reliance on an inaccessible exhaustive-run log.
