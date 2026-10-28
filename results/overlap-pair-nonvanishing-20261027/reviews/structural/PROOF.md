# Structural finite-height reduction by polynomial Wronskians

2026-10-27. Scope: the 5 by 5 masked determinant with partial supports
`{a,b}` and `{a,c}` and three full rows. The five column exponents are
pairwise distinct nonnegative integers and the five offsets are pairwise
 distinct. This proof allows complex offsets; the intended real model is a
special case. No claim of a zero determinant, complete nonvanishing, a new
order-type exclusion, or a general circuit lower bound is made.

## Result

If this determinant is identically zero, every consecutive gap between the
five sorted exponents is at most **408**. Consequently, after subtracting
the least exponent, all exponents belong to **{0,...,1632}**.

Subtracting the common minimum multiplies the determinant by a nonzero
polynomial factor, so preserves identity-zero. Thus this is a uniform,
unconditional finite exponent-height reduction, not a finite exponent scan
or an assumption on low Taylor coefficients. The proof is independent of
C6/C7/C8 elimination.

## 1. Equal-degree S-unit circuit lemma (proved here)

Let f_1,...,f_k be a minimally linearly dependent set over C of distinct
nonzero monomials in s distinct linear factors X-rho_1,...,X-rho_s, all of
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

At rho_l some g_j has valuation zero, because gcd(g_1,...,g_k)=1. Use the
Wronskian omitting that j. Writing v_i,l=ord_(rho_l)(g_i), every determinant
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

## 2. Apply the circuit lemma to the 18 determinant terms

There are precisely 18 permitted permutations: the partial rows have the
three distinct-column choices (a,c), (b,a), (b,c), and the three full rows
have 3! completions. Their monic polynomial terms are pairwise distinct:
different permutations assign different exponents to at least one of the
five distinct linear factors. All terms have the same total degree.

Every minimal linear circuit of these terms has k<=18 and s<=5. Hence any
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

## 3. One pattern has a nonzero block-factor determinant

One of L,H contains at least two of {a,b,c}; call that side S. Put both
partial rows and any |S|-2 full rows on side S. All remaining rows are full
and are put on the other side. There is a perfect matching in each block:
any two distinct columns from {a,b,c} match the two partial supports.

The signed sum of terms in precisely this assignment pattern is, up to an
overall sign, the product of the determinants of the two square blocks.
Their sizes are |S| and 5-|S|, both between 1 and 4. The second block is
full. The first has the two inherited partial rows, together with full
rows. Every such proper block is nonzero, as established next. Thus the
pattern sum is nonzero, contradicting the direct-sum conclusion from an
identity-zero full determinant.

### Full blocks

For distinct exponents e_j and offsets r_i, the leading nonzero coefficient
at infinity of a full m by m generalized Vandermonde is the product of the
offset Vandermonde and exponent Vandermonde divided by
0!1!... (m-1)!, up to the chosen ordering sign. In particular the full
block determinant is not identically zero, also over C. This follows by
expanding (1+r_i z)^{e_j} and choosing distinct Taylor degrees 0,...,m-1.

### Proper blocks retaining both partial rows

If the column set has exactly two of {a,b,c}, a forced matching of the
partial rows leaves a full block, so the determinant is a nonzero monomial
factor times a nonzero full minor. If its size is three and it contains
all of {a,b,c}, its mask determinant is -1, so its top-degree coefficient
is nonzero. The only remaining case has size four and columns a,b,c,d
(or a,b,c,e). A short independent exact proof of that particular minor is
included here; it does not assume the false general complex-offset
four-row conjecture.

Normalize partial offsets to 0,1, factor out the common exponent a from
each row, and write the remaining exponents 0,B,C,D. Thus B,C,D are
nonzero and pairwise distinct. Write the full offsets as p,q, which are
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

## Boundary and immediate utility

- This is an integer/polynomial structural reduction; it does not assert
  the same finite-height bound for arbitrary real exponents.
- It covers all exponent-order types, but excludes no additional complete
  order type by itself. The existing 24/30 classification is unchanged.
- It leaves a large finite family of exponent shapes and a continuous
  distinct-offset feasibility problem. No finite search of that family
  has been claimed or started here.
- A candidate still requires full determinant identity and distinct real
  offsets; cancellation of a finite truncation is not enough.
- This proof is elementary and self-contained. No external theorem,
  priority claim, or literature attribution is needed or made.
