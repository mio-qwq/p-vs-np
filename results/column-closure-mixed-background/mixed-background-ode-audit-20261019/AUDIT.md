# Independent audit: one-outlier mixed-background column kernels

2026-10-19 UTC. Scope: the theorem in `/workspace/shared/mixed-column-positivity-20261019/PROOF.md`, its ODE reduction, and the proposed even-degree moment extensions. This is local mathematical verification, not a claim about arbitrary backgrounds or multiple weighted columns.

## Verdict

The proposed odd-d full-complex-linear-independence theorem is correct. The all-d conclusions for k<h, k above the largest background exponent, and kernel dimension at most one are also correct. The even-d power-and-span criterion is exact. The exclusions of every proper power for d=2,4,6 are valid; together they give full independence for those three even d as well.

Two presentation clarifications were sent to the author and are resolved in the reviewed final version:

1. State explicitly that k is a nonnegative **integer**.
2. The displayed common sign assumes the background columns are ordered increasingly. An arbitrary other background order contributes its fixed permutation sign, which has no effect on a kernel.

No substantive flaw or unhandled singular case was found.

## Setup and exact normalization

Let n>=3, h>=0, d>=1 be integers; let a_0<...<a_(n-1) be real and distinct. The n-1 background exponents, in increasing order, are

    h,h+1,...,h+n-3,h+n-2+d.

Let k be a nonnegative integer outside this list. Put

    x_s=L+a_s,       ell=k-h,       N=n+d-1,
    D_s=product_(t!=s)(a_s-a_t),
    Delta=product_(r<s)(a_s-a_r),
    G=product_s x_s^h,
    H=h_d(x_0,...,x_(n-1)),       B=h_(d-1)(x_0,...,x_(n-1)).

All D_s and Delta are nonzero constants. G is a nonzero polynomial; it is not required to be nonzero at every evaluation point.

If the distinguished column has index c and the other columns remain increasingly ordered, its signed Laplace term is exactly

    T_s=(-1)^(n-1+c) G Delta x_s^ell h_d(X without x_s)/D_s.

The equality is in C(L), and therefore is legitimate also when ell<0. Multiplication by the common nonzero factor is injective in C(L). There is no cancellation issue at individual zeros of G because no pointwise division is being claimed.

For a proposed relation sum_s u_s T_s=0, define v_s=u_s/D_s and M_j=sum_s v_s x_s^j. The generating-function identities give

    h_d(X without x_s)=H-x_s B,
    H'=N B.

Thus the relation is equivalent to

    H M_ell-B M_(ell+1)=0.                          (A)

For ell!=-1, Y=M_(ell+1) gives the undivided polynomial/rational ODE

    H Y' - alpha H'Y=0,       alpha=(ell+1)/N.      (B)

This formulation remains valid at zeros of H and Y. The shorthand Y'/Y=alpha H'/H is only an identity in the rational-function field when Y!=0; it is not the starting point of the proof.

## Negative exponents, including the exceptional value

If ell<-1, a nonzero v gives a nonzero rational Y: each active summand has a pole at its own distinct point -a_s and every other summand is regular there. Write t=deg_infinity Y. Its expansion at infinity gives t<=ell+1<0. Comparing leading terms of (B) gives

    t=d(ell+1)/N>ell+1,

since d<N. This contradiction proves independence for ell<-1 for every d. This argument is valid for complex weights, complex cancellations of leading moments, and arbitrary real offset signs.

For ell=-1, one must not infer anything from Y'=0. Set U=M_0. At infinity,

    M_(-1)=U/L+O(L^-2),
    H=C L^d+O(L^(d-1)),
    B=(d/N)C L^(d-1)+O(L^(d-2)),
    C=binom(N,d)>0.

The coefficient of L^(d-1) in (A) is C(1-d/N)U. It forces U=0. Equation (A) then forces M_(-1)=0 as a rational function, and the residue at each distinct -a_s forces v_s=0. This completes every case k<h without a logarithm or root argument.

## Why the moment-degree bound has exactly the required range

If ell>=0, distinctness from the consecutive background exponents forces ell>=n-2. Hence M=ell+1>=n-1. For v!=0 let r be its first nonzero ordinary moment index:

    r=min{j>=0: sum_s v_s a_s^j!=0}.

The n-by-n Vandermonde is invertible, so 0<=r<=n-1. Because M>=n-1, none of the relevant binomial coefficients vanish, and

    Y=sum_s v_s(L+a_s)^M !=0,
    deg Y=M-r.

This step would be false without the exclusion of the low background exponents: n translates of a polynomial of degree smaller than n-1 cannot be independent.

Comparing leading terms in (B) now yields

    deg Y=d alpha,
    r=(n-1)alpha.

Consequently 0<alpha<=1. Equality alpha=1 gives k=h+n+d-2, exactly the largest background exponent and therefore forbidden. Any nonzero kernel requires

    0<alpha<1,
    (n-1)alpha in {1,...,n-2}.

This also excludes all distinguished exponents above the largest background exponent, for every d.

## Odd d: one simple real root is sufficient

For V uniform on the (n-1)-simplex and A=sum_s V_s a_s, direct simplex integration gives

    E[(L+A)^j]=h_j(L+a_0,...,L+a_(n-1))/binom(n+j-1,j).

For even j>0 this is strictly positive for every real L. The affine random variable A is nonconstant because the offsets are distinct. For j=0 it equals 1. Therefore odd d gives H'=N B>0 everywhere on R, including d=1. Its positive leading coefficient and odd degree give exactly one real root rho, and this root is simple.

At a simple root rho of H, let t>=0 be the multiplicity of the nonzero polynomial Y, allowing complex coefficients. The first nonzero coefficient in (B) is a nonzero factor times t-alpha. Thus t=alpha. This contradicts 0<alpha<1. The argument does not require Y to be real or H to have only real roots.

This proves full C-linear independence for every allowed k when d is odd.

## Exact even-d obstruction and an arithmetic strengthening

For a potential kernel in the remaining exponent range write alpha=p/q in lowest terms, 0<p<q. Comparing valuations of (B) at each complex root of H shows that its multiplicity must be divisible by q. Conversely, if

    H=C Q^q,

then Q^p solves (B), and all polynomial solutions are its scalar multiples. The original relation exists exactly when Q^p also belongs to

    span_C{(L+a_s)^(ell+1): 0<=s<n}.

The map from v into this span is injective. Thus the kernel has dimension at most one. A proper power alone is not sufficient for a relation, and even a relation need not have nonnegative weights.

There is a useful additional arithmetic obstruction. Integrality of M=alpha N and r=alpha(n-1) implies

    q | gcd(d,n-1).

For even d, H is positive on R. Divide H by its positive leading coefficient and take its unique monic q-th root Q. This Q is real: conjugation preserves the monic root, which is unique. Q has no real roots, so its degree d/q is even. Therefore

    q | gcd(d/2,n-1).

In particular, for even d satisfying gcd(d/2,n-1)=1, full independence follows for all allowed k. This arithmetic condition is sufficient, not necessary.

## Independent audit of d=2,4,6

Translate the offsets so that p_1=sum_s a_s=0 and put p_j=sum_s a_s^j. This does not affect whether H is a proper power. Write mu_j=E[A^j]. Since the offsets are distinct, p_2>0 and mu_2>0. With (n)_j=n(n+1)...(n+j-1), the required moment identities are

    mu_2=p_2/(n)_2,
    mu_3=2p_3/(n)_3,
    mu_4=(6p_4+3p_2^2)/(n)_4,
    mu_6=(120p_6+90p_2p_4+40p_3^2+15p_2^3)/(n)_6.

These follow directly from the complete-homogeneous generating series. The monic normalization of H is E[(L+A)^d].

### d=2

A positive real quadratic cannot be a nontrivial polynomial power: the only candidate is a square of a real linear polynomial, which would have a real root. Thus no proper power exists.

### d=4

A proper power has a real monic root of even degree; the only possibility is a square of a quadratic. Its cubic coefficient and centering force the quadratic to be L^2+c. Comparing with

    E[(L+A)^4]=L^4+6mu_2 L^2+4mu_3 L+mu_4

gives c=3mu_2 and mu_4=9mu_2^2. But p_4<=p_2^2 gives

    mu_4/mu_2^2
      =3n(n+1)(1+2p_4/p_2^2)/((n+2)(n+3))
      <=9n(n+1)/((n+2)(n+3))<9.

Contradiction.

### d=6

Only a cube of a real quadratic is possible. A square of a cubic or a sixth power of a linear polynomial would have a real root. Centering again forces the quadratic to be L^2+c. Comparing coefficients gives

    c=5mu_2,
    mu_3=mu_5=0,
    mu_4=5mu_2^2,
    mu_6=125mu_2^3.

In particular p_3=0. Let r_4=p_4/p_2^2 and r_6=p_6/p_2^3. Substitution into the moment identities gives

    r_4=(n^2+11n+15)/(3n(n+1)),
    r_6=(2n^4+34n^3+202n^2+470n+375)/(3n^2(n+1)^2).

Consequently

    r_6-r_4=(n^4+22n^3+176n^2+455n+375)
              /(3n^2(n+1)^2)>0.

But p_6<=p_2 p_4, simply because the product contains every a_s^6 plus nonnegative cross terms. Hence r_6<=r_4, contradiction. The displayed formulas and their difference were independently verified with exact symbolic arithmetic.

Thus d in {2,4,6} admits no proper power at all, and the original family is fully independent for these d.

## Low cases and limitations

- n=3 is included; the first-moment range is still valid and nonempty. n=1 is not covered, and the stated background notation is not intended for n<3.
- d=1 is included; B=h_0=1 and H'=n>0.
- h=0 simply removes the negative-ell cases.
- Offset zero, negative offsets, a real root of H coinciding with -a_s, and zeros of the removed common factor do not create exceptions: the argument is in C(L), and the only local root argument is used when Y is polynomial.
- Distinctness of the exponents is essential. In particular alpha=1 corresponds exactly to a duplicate background exponent and cannot be silently included.
- The result says nothing about two independently weighted columns, arbitrary Schur partitions, general sparse matching fibers, or complexity-class separation.

## Reproduction

`check.py` independently constructs the original signed Laplace polynomials, checks each cofactor normalization, checks H'=N B and the undivided ODE, and computes exact coefficient-matrix ranks on representative data. The initial run passed all 81 cases, including negative ell and ell=-1. Exact finite checks support the implementation; the universal conclusions follow from the arguments above.

## Final integration review

The author’s final unified theorem was reread after integration of all four sufficient cases. Its normalization, integer quantifier, proper-power-plus-span condition, real-root parity argument, and d=2,4,6 moment algebra are consistent with this audit. The added six-node hook obstruction has generator (80,-30,48,48,-30,80), equal to g'(a_s)/a_s for the listed centered offsets, and its coordinate sum is 196 as stated.
