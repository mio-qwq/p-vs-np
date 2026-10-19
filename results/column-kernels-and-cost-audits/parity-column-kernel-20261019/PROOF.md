# Nonnegative column kernels when the other exponents share a parity

19 October 2026. This is a full-polynomial structural result for one-column masks. The nondistinguished exponent gaps may be arbitrary. It does not cover arbitrary exponent lists or multiple independently masked columns.

## 1. Theorem

Let a_0<...<a_(n-1) be distinct real offsets, with n>=3. Let the n column exponents be distinct nonnegative integers. First sort the columns by increasing exponent; this multiplies every T_s by the same fixed permutation sign and does not change any constant kernel. Distinguish one exponent k in its sorted column c, and suppose the other n-1 exponents b_j, listed increasingly, all have the same parity. Let

    T_s(L)=(-1)^(s+c)(L+a_s)^k
                   det[(L+a_t)^(b_j)]_(t!=s,j).

These are the signed full-column Laplace polynomials. For constant real weights u_s, replacing the distinguished entry in row s by u_s times itself changes the determinant to sum_s u_s T_s.

Put h=min_j b_j. Then:

1. If k<h, the polynomials T_s are linearly independent.
2. If k>=h and k-h is even, they are linearly independent.
3. If k>=h and k-h is odd, their constant kernel has dimension at most one, and every nonzero kernel vector satisfies u_0=-u_1!=0. In particular it has both signs.

Consequently every nonempty nonnegative one-column weighting gives a nonzero polynomial determinant. This includes every nonempty binary retained-row mask, with no requirement that an extreme row be retained or deleted.

The theorem includes common exponent shifts automatically, and arbitrary gaps among the nondistinguished exponents. The distinguished exponent need not be second-smallest.

## 2. Rational factorization in squared nodes

Write

    x_s=L+a_s, y_s=x_s^2,
    ell=k-h,
    g_j=(b_j-h)/2.

The g_j are distinct nonnegative integers and include zero. Let lambda be their (n-1)-variable alternant partition. Its last part is zero, so its length is at most n-2. Put

    G(L)=product_s x_s^h,
    Delta(y)=product_(r<s)(y_s-y_r).

Neither G nor Delta(y) is the zero polynomial. The ordinary alternant/Schur factorization in the squared nodes gives the rational identity

    T_s(L)=(-1)^(n-1+c) G(L) Delta(y) R_s(L),

    R_s(L)= x_s^ell s_lambda(y_t:t!=s)
                    /product_(t!=s)(y_s-y_t).       (1)

This identity is in the rational function field; negative ell causes no difficulty because the original T_s are polynomials. Since the common factor is nonzero, a constant relation among the T_s is equivalent to the same relation among the R_s.

Each R_s can have finite poles only at

    tau_st=-(a_s+a_t)/2, t!=s,

and, when ell<0, at the additional own-node point L=-a_s. The pair poles of a single R_s are distinct and simple.

## 3. Pair residues are nonzero and have a parity relation

At L=tau_st, put

    d=(a_s-a_t)/2 !=0.

Then x_s=d, x_t=-d, and y_s=y_t=d^2>0. All other squared nodes are nonnegative, and at most one of them is zero. In the Schur numerator for R_s there are n-1 variables, at least n-2 of which are positive. Because lambda has length at most n-2, its value is strictly positive. The same Schur value occurs for R_t: their retained multisets differ only by exchanging the equal variables y_s=y_t.

No other denominator factor y_s-y_r vanishes: for real nodes, equality of their squares would imply x_r=x_s or x_r=-x_s, hence a_r=a_s or a_r=a_t, both excluded. Also

    derivative_L(y_s-y_t)=4d.

Therefore, if S_st is the common positive Schur value and

    D_st=product_(r not in {s,t})(d^2-x_r(tau_st)^2),

then

    res_(L=tau_st) R_s = d^(ell-1) S_st/(4D_st) !=0,
    res_(L=tau_st) R_t
       =(-1)^(ell+1) res_(L=tau_st) R_s.           (2)

Different pairs may have the same sum a_s+a_t. Equation (2) remains valid; all colliding pairs are disjoint, because offsets are distinct. The argument below explicitly handles these collisions.

## 4. The minimum-index pole lemma

**Lemma.** Suppose w_0=w_1=0, and the rational function sum_s w_s R_s has no pole at any tau_0r for r>=2. Then w=0.

Otherwise let r>=2 be its smallest nonzero index. At tau_0r, the term w_r R_r has a nonzero simple-pole residue by (2), while w_0 R_0 vanishes. Any other pair (s,t) with

    a_s+a_t=a_0+a_r

has both indices strictly less than r: if either index is at least r, strict ordering forces the other index to be 0 and that index to be exactly r, giving the original pair. Thus all other colliding-pair terms have zero weights by minimality.

If ell<0, an additional own-node pole at this same point would require

    a_j=(a_0+a_r)/2.

Such an index also lies strictly between 0 and r, so its weight is zero. No other active term can cancel the nonzero residue of w_r R_r. This contradicts the no-pole hypothesis and proves the lemma.

The smallest pair sum a_0+a_1 is unique. There is no offset at its midpoint, since a_0,a_1 are adjacent. Hence any constant kernel relation gives, from its residue there,

    u_0+(-1)^(ell+1)u_1=0.                         (3)

## 5. Completion of the three cases

### Case k<h

At the extreme point L=-a_0, T_0 has exactly order k: its cofactor is a generalized Vandermonde on the positive distinct nodes a_t-a_0, t>0, so it is nonzero. Every other T_s is divisible by (L+a_0)^h, because its cofactor contains row 0 and every nondistinguished exponent is at least h.

A kernel relation therefore forces u_0=0 by its lowest-order term. Equation (3) gives u_1=0, and the minimum-index pole lemma forces all remaining coordinates to vanish. This proves case 1, even though the rational functions may have additional own-node poles.

### Case ell>=0 odd

Equation (3) gives u_0+u_1=0. If u_0=0, both coordinates vanish and the minimum-index pole lemma forces u=0. Thus the projection of the kernel to u_0 is injective; its dimension is at most one, and every nonzero kernel has u_0=-u_1!=0. This proves case 3.

### Case ell>=0 even

Equation (3) gives u_0=u_1. In this case the all-ones sum

    R_all=sum_s R_s

has no finite poles. There are no own-node poles because ell>=0. At every pair pole, the two partner residues cancel by (2). If several pairs collide, each pair cancels separately. All poles are simple, so zero residues remove them. Thus R_all is a polynomial.

For a kernel vector u, put w=u-u_0*1. Then w_0=w_1=0, and

    sum_s w_s R_s=-u_0 R_all

has no finite poles. The minimum-index pole lemma gives w=0, so every kernel vector is constant. But

    sum_s T_s=det[(L+a_s)^(e_j)]

is nonzero: for sufficiently large positive L it is a positive generalized Vandermonde, up to the fixed column-order sign. Therefore the only constant kernel vector is zero. This proves case 2 and the theorem.

## 6. Consequences and boundary

The proof uses positivity only at the real pair-collision points, where the squared-node Schur factor has nonnegative arguments and enough positive variables. It does not assume the signed Laplace polynomials have positive coefficients, full linear independence in the odd case, or that individual point evaluations form a common positive functional.

The result supplies a structural proof of nonnegative-kernel exclusion for this whole parity class. It also proves full linear independence whenever all exponents have the same parity, or when the distinguished exponent is smaller than all the others in this class.

For arbitrary mixed-parity nondistinguished exponent lists the squared-node Schur factorization is unavailable. No extension to that case, to arbitrary sparse graphs, or to P=NP/P!=NP is claimed. A future extension needs another real collision or positivity mechanism; finite searches alone do not prove the missing universal statement.
