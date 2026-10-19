# Consecutive-even background: a one-column nonnegative-kernel theorem

19 October 2026. A structural theorem beyond the one-missing-degree family. No arbitrary-support noncancellation or complexity-class conclusion is claimed. No historical novelty claim is made.

## 1. Theorem

Let n>=2, let a_0,...,a_(n-1) be distinct real offsets, let d>=0 be an integer, and choose a nonnegative integer k outside

    E_even = {0,2,4,...,2n-4}.

Take the n distinct column exponents to be

    {d+j: j in E_even} union {d+k},

in any fixed order. Distinguish the column with exponent d+k. Let T_s(L) be its full signed Laplace term, including the entry in row s.

Then every nonzero nonnegative constant vector u has

    sum_s u_s T_s(L) != 0.

Equivalently, multiplying the distinguished column entries by arbitrary fixed nonnegative weights, not all zero, preserves a nonzero determinant polynomial.

More precisely, after sorting offsets increasingly:

- If k is odd, the constant real kernel of the family (T_s) has dimension at most one. Every nonzero kernel vector has u_0=-u_1!=0, so it has both signs.
- If k is even, then necessarily k>=2n-2, and the T_s are linearly independent.

The conclusions include every nonempty binary retained-row mask in this one column. Other columns remain full; no iterative claim for multi-column masks is made. A common shift d only multiplies all T_s by the same nonzero polynomial and does not affect the kernel.

## 2. Exact rational factorization

Remove the common exponent shift d, sort rows by increasing offset, and sort columns by exponent. Permutations of rows or columns multiply every T_s by the same sign, apart from relabeling rows, so do not affect the assertions. Let c be the sorted position of exponent k. Define

    h(t) = product_s(t-a_s),
    Delta(a) = product_(s<t)(a_t-a_s),
    B(z) = product_(s<t)(z+a_s+a_t),
    R_s(z) = (z+2a_s)^k
             / [h'(a_s) product_(t!=s)(z+a_s+a_t)].

The cofactor after deleting column c has the powers 0,2,...,2n-4 on n-1 nodes. It is an ordinary Vandermonde in the squared nodes:

    det[(L+a_i)^(2j)]_(i!=s, 0<=j<=n-2)
      = Delta(a_without_s)
          product_(i<j, i,j!=s)(2L+a_i+a_j).       (1)

This is a polynomial identity, including shifts at which squared nodes coincide. The Vandermonde deletion sign is

    Delta(a_without_s)/Delta(a)
       = (-1)^(n-1-s)/h'(a_s).

Multiplying by the signed column entry and setting z=2L yields

    T_s(z/2) = K B(z) R_s(z),
    K = (-1)^(n-1+c) Delta(a)/2^k != 0.           (2)

The right side is polynomial despite its displayed rational factors. Since B is a nonzero polynomial, a constant vector u is in the kernel iff

    sum_s u_s R_s(z) = 0                          (3)

as a rational-function identity.

## 3. Residues at pair-sum poles

Each R_s has simple possible poles at `z=-a_s-a_t`, t!=s. At such a point its numerator is `(a_s-a_t)^k`, which is nonzero, including k=0 if it were allowed. Thus these are genuine simple poles of the individual R_s.

For s<t, the residue of R_s at this point is

    beta_st = (-1)^(n-1) (a_s-a_t)^(k+1)
                / [h'(a_s) h'(a_t)] != 0.        (4)

Indeed,

    product_(r!=s,t)(a_r-a_t)
      = (-1)^(n-2) h'(a_t)/(a_t-a_s),

which gives (4) on substitution. Interchanging s,t gives

    Res R_t = (-1)^(k+1) beta_st.                (5)

Several unordered pairs can have the same sum. Their pairs are disjoint: two equal sums with a shared index would imply equal offsets. Therefore the residue condition of (3), for every numerical sum q, is exactly

    sum_(s<t, a_s+a_t=q)
       beta_st [u_s+(-1)^(k+1)u_t] = 0.          (6)

No assumption that all pair sums are distinct is made.

## 4. A triangular pole argument

Because a_0<a_1<...<a_(n-1), the smallest pair sum a_0+a_1 is unique. Equation (6) forces

    u_0+(-1)^(k+1)u_1=0.                        (7)

We also need a simple ordering observation. For any j>=1, every pair with sum a_0+a_j has maximum index at most j. Otherwise its sum is at least a_0+a_(j+1), which is strictly larger. The only such pair containing j is {0,j}; all other coinciding pairs have both indices less than j.

Consequently, a kernel vector with u_0=0 must vanish. Equation (7) gives u_1=0. If j were the smallest nonzero index, apply (6) at q=a_0+a_j. Every competing pair uses only smaller, zero coordinates. The remaining nonzero coefficient beta_0j forces u_j=0, a contradiction.

Thus projection of the kernel to its first coordinate is injective, so the kernel dimension is at most one.

## 5. Odd and even distinguished powers

If k is odd, (7) reads u_0+u_1=0. Every nonzero kernel has u_0!=0 by Section 4, hence its first two entries are nonzero and opposite. No nonzero nonnegative kernel vector exists.

If k is even, (7) gives u_1=u_0. Applying (6) inductively at q=a_0+a_j gives u_j=u_0: all smaller-index competing pairs already have equal coordinates, and their differences vanish. Therefore every putative kernel vector is constant.

But the sum of all column Laplace terms is the full generalized Vandermonde determinant:

    sum_s T_s(L) = det[(L+a_s)^e_j].              (8)

It is nonzero. For sufficiently large positive L, its nodes are positive and strictly increasing; after sorting exponents, it is a positive ordinary Vandermonde times a positive Schur polynomial. Alternatively, its first surviving translated-alternant coefficient is the nonzero product of the offset and exponent Vandermondes divided by positive factorials. Exponent distinctness is essential here; for even k it follows from k>=2n-2. Thus a constant kernel vector must also be zero. This proves independence and completes the theorem.

## 6. An explicit positive functional in the odd branch

This proof can supply a positive functional directly, rather than only obtaining one afterwards from a linear-programming alternative. For j=1,...,n-1, define a functional on polynomials in the variable L by

    ell_j(P) = (1/beta_0j) Res_(z=-a_0-a_j)
                         [P(z/2)/(K B(z))].       (9)

Taking the residue of a fixed rational denominator is a linear functional in the numerator coefficients. Repeated roots of B cause no ambiguity: the residue is the coefficient of `(z+a_0+a_j)^(-1)` in its Laurent expansion. On the particular polynomials T_s, all relevant rational functions have only simple poles by (2).

Let r_(j,s)=ell_j(T_s). The pair-sum ordering from Section 4 gives

    r_(j,0)=r_(j,j)=1,
    r_(j,s)=0 for s>j.

Every other coefficient has index less than j and can have either sign. Set

    M = max(1, max_(j,s) |r_(j,s)|),
    epsilon = 1/(2M+2),
    ell = sum_(j=1)^(n-1) epsilon^(j-1) ell_j.     (10)

Its value on T_0 is the positive geometric sum. For s>=1, its value on T_s is bounded below by

    epsilon^(s-1) - M sum_(j=s+1)^(n-1) epsilon^(j-1)
      >= epsilon^(s-1) [1-M epsilon/(1-epsilon)] > 0.

Thus (10) is an explicit strictly positive functional on all the T_s. For rational offsets all residues, M, epsilon, and the resulting functional are rational. This construction does not assert a positive measure representation or a single-point evaluation; it legitimately combines residue/jet functionals at different pair-sum poles.

For a common exponent shift d, (9)--(10) apply after dividing by the known common polynomial factor. On its divisible subspace this remains a linear functional, sufficient for the claimed family.

## 7. Exact nontrivial odd-power kernel

The focused lead supplied by the adversarial group is genuine:

    n=7,
    a=(0,1,2,3,4,5,6),
    e=(0,1,2,4,6,8,10), distinguished c=1,
    u=(-1,1,1,0,-1,-1,1).

An exact coefficient certificate verifies `sum_s u_s T_s=0`; the coefficient matrix has rank six. Thus the odd branch cannot generally be strengthened to full independence. Its first two coordinates are opposite, exactly as the theorem requires.

This signed dependence is not a counterexample to the nonnegative theorem or a binary support mask. The universal proof is the residue argument; the certificate only verifies a sharpness example.

## 8. Scope and reproducibility

The theorem allows arbitrary distinct real offsets, all n, all common exponent shifts d>=0, and every distinguished nonnegative exponent outside the consecutive-even background. The algorithmic certificate files use integer offsets and exact rational/integer arithmetic.

`check.py` verifies the factorization after clearing denominators, individual pair residues including colliding pair sums, the exact seven-row dependence and rank, and selected odd/even/shifted controls by independent raw signed-permutation expansions and exact arithmetic. Finite controls are not the proof of the theorem.

Run `python check.py` and `python -O check.py`. The earlier cost, one-gap, and boundary packages are unchanged. No remote action or publication was performed.
