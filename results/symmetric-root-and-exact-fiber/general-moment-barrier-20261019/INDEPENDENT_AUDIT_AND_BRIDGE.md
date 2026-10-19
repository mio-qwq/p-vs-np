# Independent audit: all-degree symmetric simple-root obstruction

19 October 2026. Local research and audit. No remote writes.

## Verdict

Approved: for every nondegenerate symmetric real random variable X with a log-concave density and every even N>=2, the polynomial

    P_N(z)=E[(z+X)^N]

has a pair of simple purely imaginary roots. In particular it is not a proper polynomial power over C, even up to a nonzero scalar. The argument is degree-uniform. It does not show that every root is simple or imaginary.

The corresponding statement applies to translated complete homogeneous polynomials with nonconstant symmetric real offset multisets, including repeated offsets. The one-outlier cofactor consequence below still assumes distinct offsets, as does its existing ODE reduction.

## 1. Normalization checked directly

Write N=2m, M_k=E[|X|^k], and

    b_j=P_N^(2j)(0)=N! M_(N-2j)/(N-2j)!,  0<=j<=m.

Every b_j is positive. The density of |X| is 2f(x) on x>=0, hence log-concave. The Berwald–Borell normalized-moment inequality says k -> M_k/k! is log-concave. Its reversed even subsequence is log-concave, so b_j^2>=b_(j-1)b_(j+1).

Put

    sigma=sqrt(P_N(0)/P_N''(0)),
    d_j=b_j sigma^(2j)/b_0.

Then d_0=d_1=1; positive geometric rescaling preserves log-concavity. Consequently d_(j+1)/d_j is nonincreasing and at most d_1/d_0=1. Thus

    1=d_0=d_1>=d_2>=...>=d_m>0.

The exact normalized real polynomial is

    F(x)=P_N(i sigma x)/P_N(0)
        =sum_(j=0)^m (-1)^j d_j x^(2j)/(2j)!.

## 2. Endpoint 2 and derivative: all truncation parities checked

For 0<x<=2,

    F'(x)=-x [1-d_2 x^2/3!+d_3 x^4/5!-d_4 x^6/7!+...],

where missing terms are omitted. The bracket's first two terms are at least 1-4/6=1/3. Each later positive term (odd j>=3) paired with its following negative term (even j+1) is positive: the latter's magnitude divided by the former's is at most

    x^2/[(2j)(2j+1)] <= 4/(6*7)<1.

If the final term is unpaired, it is positive. If m=1, the bracket is 1. Therefore F'(x)<=-x/3<0 throughout 0<x<=2.

At x=2, the first three terms give

    1-2+(2/3)d_2 <= -1/3.

All remaining terms pair as a negative odd-j term followed by a positive even-(j+1) term; each pair is negative because the ratio is at most

    4/[(2j+1)(2j+2)] <=4/(7*8)<1.

An unpaired final term is negative. For m=1, F(2)=-1 directly. Therefore F(2)<0 in every degree.

Since F(0)=1, there is exactly one zero x_* in (0,2), and F'(x_*)!=0. The complex chain rule gives

    F'(x_*)=i sigma P_N'(i sigma x_*)/P_N(0),

so i sigma x_* is a simple root of P_N; conjugation gives the negative partner.

## 3. Lower bound checked

At x=sqrt(2), the j=0,1 terms cancel. The remaining terms pair as positive even-j terms followed by negative odd-(j+1) terms. Their ratios are at most

    2/[(2j+1)(2j+2)] <=2/(5*6)<1,  j>=2.

Each complete pair is strictly positive, as is any unpaired last term. Thus F(sqrt(2))>0 for m>=2. Combined with strict monotonicity, the root is i eta with

    sqrt(2P_N(0)/P_N''(0)) < eta < 2sqrt(P_N(0)/P_N''(0))

for N>=4. For N=2 the lower endpoint is attained exactly.

This is a bound for the first positive zero on the imaginary axis. No assertion about all other complex roots, or the globally smallest root modulus, is needed.

## 4. Application to symmetric offsets

Let a_1,...,a_n be nonconstant and symmetric about c. For uniform simplex coordinates U, put X=sum U_i(a_i-c). The simplex law is log-concave in its affine hull; its nonconstant one-dimensional linear projection has a log-concave density. A permutation reversing the offset multiset gives X and -X the same distribution. The standard moment identity is

    h_N(L+a_1,...,L+a_n)
       =binom(n+N-1,N) E[(L+c+X)^N].

Therefore for even N the translated complete homogeneous polynomial has simple roots on Re L=-c. Its proper-power status is unchanged by the nonzero scalar and translation. For odd N, its derivative is a positive multiple of E[(L+c+X)^(N-1)] and is strictly positive on R, so its unique real zero is simple. Consequently every degree N>=1 has a simple root and no proper-power representation for every such symmetric offset multiset.

## 5. Precise one-outlier-background corollary

Assume n>=3, distinct symmetric real offsets, h>=0, d>=1, and nondistinguished exponents

    h,h+1,...,h+n-3,h+n-2+d.

Let k>=0 be any other exponent, and let T_s be the signed full-column Laplace polynomials for the distinguished exponent k. Then the T_s are linearly independent over C.

To verify the bridge, use the existing cofactor identity from the one-outlier theorem. Put m=n-1 and ell=k-h. Cases ell<0 are already excluded by that proof's distinct-pole and infinity argument. For ell>=0, any nonzero constant kernel would produce a nonzero polynomial Y and

    H Y'-alpha H'Y=0,
    H=h_d(L+a_1,...,L+a_n),
    alpha=(ell+1)/(m+d),   0<alpha<1.

The last interval follows from the first-nonzero-moment and degree comparison in that proof, with the excluded background exponent removing alpha=1. Our theorem supplies a simple root rho of H. If Y has multiplicity q>=0 at rho, the leading local term of the ODE is a nonzero constant times q-alpha. Hence q=alpha, contradicting q integral and 0<alpha<1. No shifted-power-span check is needed after this contradiction.

This corollary concerns exactly the displayed background. It must not be confused with the different hook background whose cofactor partition has more than one row; that family can have signed kernels even for symmetric offsets.

For n=2 the analogous background has one exponent. The two full-column Laplace terms are independent for any distinct exponents because their ratio is a nonzero scalar times ((L+a_1)/(L+a_2)) to a nonzero integer power, hence is nonconstant. This elementary case does not use the ODE theorem.

## 6. Scope and sources

The arbitrary asymmetric real-offset proper-power problem remains open here. No arbitrary-background, multicolumn, sparse-support, polynomial-time implicit-oracle, or P-versus-NP conclusion follows. No claim of historical novelty is made.

Primary analytic source verified on 19 October 2026: Bo'az Klartag and Joseph Lehec, “Poisson processes and a log-concave Bernstein theorem,” Lemma 2.1, equation (6), author manuscript page 4. It explicitly gives the normalized integer-moment log-concavity used above:

https://www.math.tau.ac.il/~klartagb/papers/log_concave_bernstein.pdf

The ODE input is the local one-outlier mixed-background proof, Sections 2–6. The simplex marginal log-concavity and simplex moment formula are the same standard inputs as in the earlier symmetric low-base result. The new root argument itself is elementary and exact; no numerical root, sample of degrees, or computer-assisted positivity claim is used for the universal theorem.
