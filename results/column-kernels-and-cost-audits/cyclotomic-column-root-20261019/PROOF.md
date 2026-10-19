# Full column independence for arithmetic-staircase backgrounds

19 October 2026. This is a full-polynomial theorem for one weighted column. The proof uses isolated nonreal collision poles, not coefficient truncation or a finite search.

## 1. Theorem

Let n>=3 and m>=3. Let a_0<...<a_(n-1) be distinct real offsets. Suppose the n-1 nondistinguished column exponents form the exact arithmetic staircase

    h, h+m, ..., h+m(n-2),       h>=0,

and the distinguished exponent k is a nonnegative integer distinct from every background exponent. Sort all columns by increasing exponent, and let c be the distinguished column index. Set

    T_s(L)=(-1)^(s+c)(L+a_s)^k
                  det[(L+a_t)^(h+mj)]_(t!=s, 0<=j<=n-2).

Then the n polynomials T_s are linearly independent over the complex numbers.

Consequently every nonzero constant complex weighting of this one column gives a nonzero determinant polynomial. In particular every nonempty nonnegative or binary retained-row weighting does. There is no restriction on which rows are retained. This conclusion concerns one weighted column with all the other columns full.

## 2. Exact rational factorization

Write

    x_s=L+a_s, y_s=x_s^m, ell=k-h,
    G(L)=product_s x_s^h,
    Delta(y)=product_(r<s)(y_s-y_r).

The background minor, after factoring x_t^h from each retained row, is the ordinary Vandermonde in its retained y variables. Thus

    T_s(L)=(-1)^(n-1+c) G(L) Delta(y) R_s(L),
    R_s(L)=x_s^ell/product_(t!=s)(y_s-y_t).       (1)

All factors and rational identities are over C(L). The common factor is not the zero polynomial. Each y_s-y_t is a nonzero polynomial because a_s!=a_t. Hence a constant relation among the T_s is equivalent to the same relation among the R_s.

Negative ell is permitted in (1). It creates possible own-node poles L=-a_s, all on the real axis. The proof below uses only nonreal poles and needs no separate negative-ell case.

## 3. Collision locations and residue phase

Put zeta=exp(2 pi i/m) and C=cot(pi/m)>0. For i<j, define

    tau_ij=-(a_i+a_j)/2 + i (a_j-a_i) C/2.       (2)

This lies in the upper half-plane and satisfies x_i=zeta*x_j. In general, a pair collision x_r=eta*x_s, with eta=exp(2 pi i l/m)!=1, occurs at

    L=-(a_r+a_s)/2 - i(a_r-a_s)cot(pi l/m)/2.    (3)

Its absolute imaginary part is at most |a_r-a_s| C/2, since

    |cot(pi l/m)| <= cot(pi/m),    1<=l<=m-1.

At any nonreal collision y_i=y_j, no third y_t can equal that common value. Indeed equality of mth powers implies equality of moduli. For fixed nonreal L, the real shifts a satisfying |L+a| equal a given value have at most two solutions. Thus only the two original offsets can occur.

Moreover x_j is nonzero, and

    derivative_L(y_i-y_j)
        =m*x_j^(m-1)*(zeta^(-1)-1) !=0.

Therefore each endpoint rational function has a simple pole with nonzero residue at tau_ij. Their other denominator factors have the same values, whereas the exchanged factor reverses derivative sign. Consequently

    Res_(tau_ij) R_j = -zeta^(-ell) Res_(tau_ij) R_i.  (4)

The identity is valid for every integer ell.

## 4. Every primitive pole involving an extreme offset is isolated

**Lemma.** If i=0 or j=n-1, then tau_ij is not a collision pole of any other unordered pair.

Suppose another pair r<s has a collision at tau_ij. Equation (3) forces the same real center,

    a_r+a_s=a_i+a_j.

The bound on absolute cotangent and equation (2) force its gap to satisfy

    a_s-a_r >= a_j-a_i.

A pair with this center and at least this gap contains the interval [a_i,a_j]. If i=0, this would imply a_r<=a_0, hence a_r=a_0 and equality of the gaps; then a_s=a_j. If j=n-1, it similarly implies a_s>=a_(n-1), hence equality and a_r=a_i. In either case it is the original pair.

This proves the lemma. Possible own-node poles from negative ell are real and cannot coincide with tau_ij. Thus the residue of any rational linear combination at this pole involves exactly its two endpoint terms.

## 5. Endpoint equations force independence

Let u be a constant complex kernel vector, so sum_s u_s R_s=0. Write r=zeta^ell, which is nonzero. At every pole tau_0j, j>0, the isolation lemma and (4) give

    u_j=r u_0.                                  (5)

Because n>=3, the pair (1,n-1) has distinct endpoints and contains the other extreme offset. Its isolated pole similarly gives

    u_(n-1)=r u_1.                              (6)

Combining (5) and (6),

    r u_0=r^2 u_0.

If r!=1, this forces u_0=0, and (5) makes every coordinate zero. If r=1, equation (5) says u is constant. But

    sum_s T_s=det[(L+a_s)^(e_j)]

is a nonzero polynomial: evaluate at any sufficiently large positive L, when its nodes are distinct and positive and its exponents are distinct nonnegative integers. A positive-node generalized Vandermonde is nonsingular. One elementary verification is that a nonzero linear combination of n distinct monomials has at most n-1 distinct positive zeros, by induction using division by its lowest power followed by Rolle's theorem. Therefore a nonzero constant kernel vector is also impossible.

This proves full complex linear independence for all k, including k<h, and finishes the theorem.

## 6. Provenance and exact boundary

The root researcher proposed the arithmetic-staircase rational factorization and a maximal-active-gap complex-pole argument. That argument correctly established nonnegative-kernel exclusion but retained an unnecessary possible half-residue dependence case. Its unchanged draft is preserved as `SUPERSEDED_ROOT_DRAFT.md` for provenance.

The constructive algorithm auditor independently removed that exception using two distinct roots of unity at the globally smallest pair midpoint, followed by a minimum-index pole induction. The adversarial researcher independently found the stronger endpoint-pole isolation lemma above, which gives a shorter full-complex-independence proof and also eliminates the negative-ell and polynomial-subtraction case splits. The constructive structural researcher checked both routes and consolidated this final endpoint proof. These are collaborative derivations of one theorem, not independent discoveries to be counted separately.

The exact arithmetic staircase is important. With arbitrary gaps in a residue class modulo m, the cofactor acquires a nonconstant Schur factor evaluated at complex nodes; it could vanish at a collision, so the present nonzero-residue argument does not automatically extend. The separate m=2 parity-background theorem uses real squared-node Schur positivity and does allow arbitrary gaps, but only concludes nonnegative-kernel exclusion in its odd-difference case. Neither result covers arbitrary independently masked columns or settles either direction of P versus NP.
