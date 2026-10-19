# Extreme-root tests for the two-zero column mask

19 October 2026. This is a separate continuation of the frozen `single-row-boundary-20261019` package. No prior package is changed. The results here are full-polynomial nonvanishing theorems, not numerical evidence from additional examples.

## 1. Setup and statements

Let

    P(L) = det M(L),
    M_sj(L) = (L+a_s)^(e_j), except M_ic=M_pc=0.

The offsets are distinct real numbers, the exponents are distinct nonnegative integers, and a_i is an extreme offset. Nonvanishing is unchanged by sorting rows and columns, or by reflecting all offsets and replacing L by -L. Accordingly, assume

    a_0 < a_1 < ... < a_(n-1),  i=0,
    e_0 < e_1 < ... < e_(n-1).

All ranks below are zero-based in these orders. Put h=e_0 and

    R = product over s not in {0,p} of (a_s-a_0)/(a_s-a_p).

We prove the following tests on the prior leading-cancellation locus R=1:

1. If c is even and c>0, then P is nonzero.
2. If c=1 and the tail e_1,...,e_(n-1) is not consecutive, then P is nonzero.
3. If c=p, then P is nonzero.

In each case the root L=-a_0 has exactly multiplicity h. In particular, when h=0, direct evaluation there is nonzero.

The remaining prior exponent resonance is

    sum_j e_j = n e_c + binom(n-1,2).                (1)

At c=1, a consecutive tail would make (1) imply e_0=e_1, a contradiction. Therefore test 2 always applies to c=1 in the resonant regime. Tests 1--3 do not require the prior centroid condition.

**All-five-row corollary.** Every simultaneous-resonance case with n=5 has P nonzero. Thus the unresolved part of the previous n>=5 boundary is reduced to n>=6, with odd c>=3, c!=p, c not the maximum exponent rank, in addition to the prior three resonance conditions.

No theorem about arbitrary sparse graphs, arbitrary colorings, deterministic Exact Matching, P=NP, or P!=NP follows from these results.

## 2. Root reduction and row parity

Factoring (L+a_s)^h out of each row, including its zero entry, gives the polynomial identity

    P(L) = [product_s (L+a_s)^h] P_tilde(L),

where P_tilde has exponents e_j-h. Since c>0, row 0 of P_tilde at L=-a_0 has exactly one nonzero entry: the entry 1 in column 0. Expanding along that row leaves the (n-1)-square matrix on positive distinct nodes

    x_s = a_s-a_0 > 0,  s=1,...,n-1,

and exponents e_j-h, j=1,...,n-1, with just the (p-1,c-1) entry zeroed. Let A be this same matrix before zeroing the entry.

Every square minor of A is positive. Indeed, sorting is already retained, and each minor is a generalized Vandermonde alternant at positive increasing nodes and increasing nonnegative integer exponents. The alternant is its positive Vandermonde times a Schur polynomial with nonnegative coefficients and a positive value. Thus A is strictly totally positive.

Every numerator factor in R is positive. Its denominator has exactly p-1 negative factors. Hence R=1 forces p odd. Moreover p=1 would make every ratio in R strictly greater than 1, so p>=3.

For even c>0, the removed Laplace term in det A has sign

    (-1)^((p-1)+(c-1)) = (-1)^(p+c) = -1.

Its entry and minor are positive. Therefore the zeroed determinant is det A plus a strictly positive number, and is nonzero. This proves test 1.

Since the other factors (L+a_s)^h are nonzero at L=-a_0, nonzero P_tilde(-a_0) gives exact root multiplicity h, as asserted.

## 3. The second-smallest exponent: a strict Schur ratio

Now let c=1. Factor the positive quantity x_s^(e_1-h) from each row of A. The resulting unmasked matrix B has the increasing exponent list

    r = (0, e_2-e_1, ..., e_(n-1)-e_1),

of length m=n-1. Its distinguished column is its constant column. Let q=p-1 be the distinguished row in B. Define the partition of length m

    mu_j = r_(m-j) - (m-j),  j=1,...,m.

It has mu_m=0. Write X=(x_1,...,x_(n-1)) and Y=X with x_p removed, both in their inherited increasing order. The alternant formula gives

    det B = Delta(X) s_mu(X).

On deleting B's constant column and its row q, the exponents are r_1,...,r_(m-1). Their associated partition is

    (mu_1+1,...,mu_(m-1)+1).

Consequently this minor equals

    Delta(Y) [product_(y in Y) y] s_mu(Y),

where evaluating s_mu on m-1 variables is legitimate because mu_m=0. The entire signed deleted Laplace contribution C therefore satisfies

    C / det B
      = [product_(y in Y) y/(y-x_p)] s_mu(Y)/s_mu(X)
      = R s_mu(Y)/s_mu(X).                         (2)

All signs are included in the product denominator. For example the denominator has p-1 negative factors, exactly matching the row cofactor sign.

If mu is nonempty, then

    0 < s_mu(Y) < s_mu(Y,x_p)=s_mu(X).               (3)

The first inequality follows from positive variables and length(mu)<=m-1. For strictness, the Schur branching identity

    s_mu(Y,z) = sum_(nu interlaces mu)
                    s_nu(Y) z^(|mu|-|nu|)

has the term nu=mu, equal to s_mu(Y), and at least one further positive term: remove a removable corner of the nonempty partition mu. This produces an interlacing partition nu with |nu|=|mu|-1 and length(nu)<=m-1. Its coefficient and z=x_p are positive. This proves (3).

Under R=1, equations (2)--(3) give 0<C/det B<1. Hence

    det(B with B_q0=0) = det B-C > 0.

Restoring the positive row factors proves test 2.

The partition mu is empty exactly when r=(0,1,...,m-1), equivalently when e_j=e_1+j-1 for every j>=1. In that case

    sum_j e_j = e_0 + (n-1)e_1 + binom(n-1,2).

For c=1, resonance (1) would require e_0=e_1, contradicting distinct exponents. This proves the resonant c=1 conclusion.

## 4. A diagonal hole in a strictly totally positive matrix

We need a general elementary fact.

**Lemma.** If B is a strictly totally positive square matrix of size m>=2, then

    B_qq det B[not q,not q] > det B,

and therefore det(B with B_qq=0)<0.

For a set S of indices, let D(S) be the corresponding principal minor and let D(empty)=1. For i,j not in S, the Desnanot--Jacobi identity gives

    D(S+i)D(S+j) - D(S)D(S+i+j)
      = det B[S+i,S+j] det B[S+j,S+i] > 0.          (4)

All row and column sets are sorted. Strict total positivity makes every displayed minor positive. Dividing gives

    D(S+i)/D(S) > D(S+i+j)/D(S+j).                  (5)

Starting with S empty and adding the other m-1 indices one at a time, (5) implies

    B_ii > det B / D(all indices except i).

This proves the lemma. Equivalently B_ii(B^{-1})_ii>1.

When c=p, the hole in the positive-node matrix A of Section 2 is diagonal. Applying the lemma directly to A proves test 3. Notice that this argument needs neither exponent resonance nor centroid resonance.

## 5. Why n=5 is now complete within the boundary

Under R=1, Section 2 forces p odd and p>=3. With five rows this means p=3. The prior degree tests already exclude c=0 and c=4 from exponent resonance. Of the remaining ranks:

- c=1 is handled by the strict Schur ratio;
- c=2 is even and is handled by the cofactor sign;
- c=3 equals p and is handled by the diagonal-hole lemma.

This exhausts every resonant five-row case. The proof works for arbitrary distinct real offsets with a_0 extreme; centroid resonance is unnecessary for this five-row corollary.

## 6. A false stronger lemma: the Laplace polynomials need not be independent

Let T_s denote the full column-c Laplace term of the unmasked determinant. One tempting approach would be to prove all T_s linearly independent. That lemma is false.

For offsets (-3,-1,1,3), exponents (0,1,2,4), and c=1, direct exact expansion yields

    T_0 = -128 L^4 + 896 L^2 + 768 L,
    T_1 =  384 L^4 -1152 L^2 + 768 L,
    T_2 = -384 L^4 +1152 L^2 + 768 L,
    T_3 =  128 L^4 - 896 L^2 + 768 L.

Thus T_0-T_1-T_2+T_3=0. The coefficient matrix has the one-dimensional kernel spanned by (1,-1,-1,1).

This is a signed linear-dependence certificate, not a zero-polynomial two-hole certificate. In particular T_1+T_2=1536 L is nonzero.

A potentially useful stronger target, explicitly still unproved, is that every nonzero constant kernel vector of the family (T_s) has both positive and negative coordinates. It would exclude every nonempty nonnegative one-column mask, including the present mask. The signed certificate above does not refute that weaker statement.

## 7. Remaining scope and resume condition

For the original simultaneous-resonance problem, the unclosed cases now have n>=6, p odd with p>=3, and odd distinguished exponent rank c>=3 satisfying c!=p and c<n-1. They must still satisfy R=1, equation (1), and the centroid condition sum a=n(a_0+a_p)/2.

### The first unresolved size has a symmetric normal form

At n=6 the remaining rank restrictions force p=5 and c=3. Translate and scale the endpoint offsets to a_0=-1 and a_5=1. The centroid condition makes the four interior offsets have sum zero. Their monic root polynomial Q therefore has no cubic coefficient. The condition R=1 is Q(-1)=Q(1); with the cubic coefficient already zero, this forces the linear coefficient to be zero as well. Hence Q is even. Its four distinct real interior roots occur in opposite pairs, and the normalized offsets are exactly

    (-1,-v,-u,u,v,1),  0<u<v<1.

The exponent condition is sum e=6e_3+10, an even integer. Replacing L by -L multiplies each column by (-1)^e_j and reverses the six rows, while preserving the endpoint-hole mask. The column factor is 1 and the row-reversal sign is (-1)^15=-1. Consequently the centered P satisfies P(-L)=-P(L). This is a normal-form reduction and a parity constraint, not a proof that P is nonzero.

Resume with a structural argument for the remaining off-diagonal odd-rank holes, a proof/refutation of the stated nonnegative-kernel target, or an exact zero-polynomial certificate satisfying all hypotheses. At n=6 the symmetric two-parameter offset form above is sufficient and necessary. Additional isolated nonzero examples do not settle this remaining scope.
