# A simple imaginary root excludes all proper powers in the symmetric case

Date: 2026-10-19. Local mathematical research. No remote changes.

## Result and scope

Let X be a nondegenerate symmetric real random variable with a log-concave density. For every even N >= 2, the polynomial

    P_N(z) = E[(z+X)^N]

has a simple root on the positive imaginary axis, and its conjugate is also simple. In particular, P_N is not a proper polynomial power over C, even up to a nonzero scalar.

More generally, normalized even-moment log-concavity alone suffices. No stronger simplex structure is needed for this symmetric conclusion. The elementary coefficient lemma below does not require its coefficients to come from any probability distribution.

Consequently, if n >= 2 and the real offset multiset a_1,...,a_n is nonconstant and symmetric about some center, then

    h_N(L+a_1,...,L+a_n)

is not a proper polynomial power for every positive integer N. Repeated offsets are allowed. For odd N, a separate elementary derivative argument suffices, even without offset symmetry.

This does not settle arbitrary asymmetric offsets in general even degree. It does not assert that all roots of the polynomials in question are simple. No publication novelty is claimed.

## 1. Elementary coefficient lemma

Let m >= 1 and

    A(z) = sum_{j=0}^m c_j z^(2j)/(2j)!,     c_j > 0.

Suppose c_0,...,c_m is log-concave:

    c_j^2 >= c_{j-1} c_{j+1}               (1 <= j < m).

Then A has a simple root i eta with eta > 0. For m >= 2,

    sqrt(2 c_0/c_1) < eta < 2 sqrt(c_0/c_1).             (1)

There is exactly one such root with

    0 < eta <= 2 sqrt(c_0/c_1).

For m=1 the unique positive imaginary root is eta=sqrt(2 c_0/c_1), and it is simple.

### Normalize the coefficients

Set s=sqrt(c_0/c_1) and

    B(z)=A(sz)/c_0=sum_{j=0}^m d_j z^(2j)/(2j)!,
    d_j=c_j c_0^(j-1)/c_1^j.

Thus d_0=d_1=1. Log-concavity is preserved by this positive geometric scaling, so its successive ratios are nonincreasing:

    d_{j+1}/d_j <= d_1/d_0=1.

In particular,

    1=d_0=d_1 >= d_2 >= ... >= d_m > 0.                (2)

Only (2), not the full log-concavity assumption, is used in the rest of the proof.

Put

    F(x)=B(ix)=sum_{j=0}^m (-1)^j d_j x^(2j)/(2j)!.

This is real for real x. The case m=1 is F(x)=1-x^2/2 and is immediate. Hence assume m>=2.

### A negative value at x=2

At x=2 the first three terms give

    1-2+(2/3)d_2 <= -1/3.

Pair every remaining odd-index negative term with the following even-index positive term. For odd j>=3 with j+1<=m,

    -d_j 2^(2j)/(2j)! + d_{j+1} 2^(2j+2)/(2j+2)!
    = -2^(2j)/(2j)! [d_j - 4d_{j+1}/((2j+2)(2j+1))]
    < 0,

because d_{j+1}<=d_j and (2j+2)(2j+1)>4. If the last index is odd, its unpaired term is negative. Therefore

    F(2) <= -1/3 < 0.                                  (3)

### Strict decrease up to x=2

For 0<x<=2,

    F'(x) = -x G(x),

where

    G(x)=1-d_2 x^2/6
          +d_3 x^4/5! - d_4 x^6/7!
          +d_5 x^8/9! - ... .

Pair every positive term indexed by odd j>=3 with the following negative term, whenever both are present. Each such pair is

    d_j x^(2j-2)/(2j-1)! - d_{j+1} x^(2j)/(2j+1)!
    = x^(2j-2)/(2j-1)!
        [d_j - x^2 d_{j+1}/((2j)(2j+1))]
    > 0.

Here (2), x^2<=4, and (2j)(2j+1)>4 justify the strict sign. If the last index is odd, its unpaired term is positive. Thus

    G(x) >= 1-d_2 x^2/6 >= 1-4/6=1/3,

and consequently

    F'(x) <= -x/3 < 0                 (0<x<=2).        (4)

Since F(0)=1 and F(2)<0, there is exactly one zero xi in (0,2). By (4), F'(xi) is nonzero. The identity

    F'(xi)=i B'(i xi)

shows that i xi is a simple complex root of B, so i s xi is a simple root of A.

### The optional lower bound

At x=sqrt(2), the first two terms cancel. Pair every even-index positive term j>=2 with the following odd-index negative term. The ratio of the latter magnitude to the former is at most

    2/((2j+2)(2j+1)) < 1.

Every pair is strictly positive; any unpaired last even term is positive. Since d_2>0, F(sqrt(2))>0. The strict decrease gives sqrt(2)<xi<2, proving (1).

### Why a simple root excludes every proper power

If A=lambda Q^k with lambda!=0 and integer k>=2, every complex root of A has multiplicity divisible by k. A simple root contradicts this. There is no need to assume that Q has real coefficients, to classify its degree, or to consider only square exponents.

## 2. From normalized even moments to the coefficient lemma

Let X be symmetric about zero, with finite moments through N=2m and mu_{2j}=E[X^(2j)]>0. Put mu_0=1. Assume the sequence

    b_j=mu_{2j}/(2j)!                 (0<=j<=m)

is log-concave. Symmetry removes the odd terms, and

    P_N(z)=sum_{j=0}^m binom(N,2j) mu_{N-2j} z^(2j)
          =sum_{j=0}^m c_j z^(2j)/(2j)!,

with

    c_j=N! mu_{N-2j}/(N-2j)!=N! b_{m-j}.               (5)

Reversal and multiplication by a positive constant preserve log-concavity. Thus (5) satisfies the coefficient lemma.

In terms of moments, c_0=mu_N and c_1=N(N-1)mu_{N-2}. For N>=4 its simple positive imaginary root obeys

    sqrt(2 mu_N/[N(N-1)mu_{N-2}])
      < eta
      < 2 sqrt(mu_N/[N(N-1)mu_{N-2}]).                (6)

For N=2, eta=sqrt(mu_2).

This step is an implication from explicitly assumed moment inequalities. It makes no claim that arbitrary positive log-concave sequences are realizable by probability measures.

## 3. Why symmetric log-concave densities meet the hypothesis

If X has a symmetric log-concave density f on R, then |X| has density 2f(t) on [0,infinity), which is log-concave. The Berwald-Borell normalized-moment inequality gives log-concavity of

    k -> E[|X|^k]/k!.

In particular, its even-index subsequence b_j is log-concave. Section 2 now applies. Symmetry about an arbitrary center is handled by translating X and the polynomial variable.

Source checked directly: Bo'az Klartag and Joseph Lehec, "Poisson processes and a log-concave Bernstein theorem," Lemma 2.1, proof, equation (6), printed page 4. The author's manuscript explicitly states the integer normalized-moment inequality used here:

https://www.math.tau.ac.il/~klartagb/papers/log_concave_bernstein.pdf

For the unweighted moments, apply the statement to the log-concave density on [0,infinity) directly, or take the monotone limit of its exponentially tilted versions as the positive tilt parameter decreases to zero. The assumed finite moments justify the resulting inequalities.

## 4. Consequence for symmetric real offsets

Let U be uniform on the standard simplex in R^n and put

    X=sum_i U_i a_i.

The elementary Dirichlet moment identity gives

    E[(L+X)^N] = h_N(L+a_1,...,L+a_n)/binom(n+N-1,N).  (7)

Uniform measure on the simplex is log-concave in its affine span, and its nonconstant one-dimensional linear projection has a log-concave density by marginal log-concavity. For n=2 the projection is a nondegenerate uniform interval distribution. Repeated offsets do not change these facts.

After subtracting the center of a symmetric offset multiset, a permutation of the simplex coordinates sends X to -X and preserves its law. Thus X is symmetric. Nonconstant offsets make X nondegenerate. Compact support supplies every moment.

For every even N>=2, Sections 1-3 exclude a proper power in (7). Scaling by the positive binomial constant and translating L preserve proper-power status up to a nonzero scalar, so the same conclusion holds for the original translated complete homogeneous polynomial.

For completeness, for any nondegenerate real random variable with the requisite moments and any odd N>=1,

    P_N'(L)=N E[(L+X)^(N-1)]>0                       (L real).

For N=1 this is the constant 1. For odd N>=3, strict positivity follows because X is not almost surely a single point. The odd monic polynomial has a real zero, and the derivative makes that zero simple. Therefore odd degrees never give proper powers either, whether or not the offsets are symmetric.

## 5. Exact scope warning: ordinary moment realizability is insufficient

There are genuine symmetric probability distributions whose moment polynomials are squares if normalized even-moment log-concavity is dropped.

For example, let

    P(X=0)=8/9,   P(X=3)=P(X=-3)=1/18.

Then E[X^2]=1 and E[X^4]=9, so

    E[(L+X)^4]=L^4+6L^2+9=(L^2+3)^2.

The normalized even-moment sequence is (1,1/2,3/8), which fails log-concavity because 1/4<3/8. This is a discrete distribution, not a log-concave density and not evidence against the symmetric simplex conclusion.

## 6. Verification and relation to the earlier results

The argument in Section 1 is an exact finite algebraic proof valid in every degree. It does not rely on numerical scans, a finite set of degrees, root approximations, or an unproved realization claim. The small checker verifies the universal pair-denominator identities and normalization constants symbolically, and tests the moment-to-coefficient identities on exact named examples. Those examples are regression checks, not the proof of universality.

Run:

    python check.py
    python -O check.py

This all-degree symmetric result replaces the earlier restriction to power bases of degree at most six for symmetric log-concave moment polynomials. It does not replace the degree-eight theorem for arbitrary asymmetric real offsets, whose hypothesis is genuinely broader in a different direction.

## 7. Precise one-outlier-background consequence

The preceding result closes the symmetric-offset case of the existing one-outlier cofactor problem in every degree.

Assume n>=3, distinct symmetric real offsets a_1,...,a_n, and integers h>=0, d>=1. Fix exactly the n-1 background exponents

    h,h+1,...,h+n-3,h+n-2+d.

For any nonnegative integer k outside this list, form the generalized Vandermonde matrix whose distinguished column has entries (L+a_s)^k and whose other columns have the displayed background exponents. Let T_s be its n signed full-column Laplace terms for the distinguished column. Then T_1,...,T_n are linearly independent over C.

Here is the exact bridge from the previously audited cofactor reduction. Put m=n-1, ell=k-h, and

    H(L)=h_d(L+a_1,...,L+a_n),
    alpha=(ell+1)/(m+d).

The existing proof excludes every ell<0 by a distinct-pole and infinity argument. For ell>=0, a nonzero constant relation between the T_s would give a nonzero polynomial Y satisfying

    H Y' - alpha H'Y = 0,
    0<alpha<1.

The last interval follows from first-nonzero-moment degree comparison and the exclusion of the background exponents; it is not an extra assumption on k. Our all-degree theorem supplies a simple root rho of H. If Y has multiplicity q>=0 at rho, comparison of the first nonzero local coefficients forces q=alpha, impossible for an integer q and 0<alpha<1. This excludes every relation.

The complete independently checked bridge, its lower-dimensional boundary, and its scope warnings are retained in INDEPENDENT_AUDIT_AND_BRIDGE.md, Section 5. Its ODE input is the existing one-outlier proof and audit at:

    /workspace/shared/mixed-column-positivity-20261019/PROOF.md
    /workspace/shared/mixed-background-ode-audit-20261019/AUDIT.md

This consequence is restricted to exactly the displayed background. It is not a result for arbitrary gapped or multirow-hook backgrounds; such other families can have kernels even with symmetric offsets. It gives no multicolumn, sparse-support, complexity-bound, or P-versus-NP conclusion.

## 8. Independent audit receipt

The independent reviewer checked the normalized coefficients, both truncation parities, the derivative's strict sign, the lower bound, the simplex transfer, and the precise one-outlier bridge. Its verdict is approved. The complete receipt is INDEPENDENT_AUDIT_AND_BRIDGE.md.

The full manuscript and checker were additionally read by a separate researcher, who approved the coefficient reversal, exact root bounds, truncation endings, simplex application, and precise one-outlier bridge. The proof in Sections 1-4 is self-contained apart from the explicitly cited normalized-moment and marginal log-concavity inputs.
