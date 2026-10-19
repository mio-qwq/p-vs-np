# General multiplicity and moment-span obstructions

19 October 2026. Local mathematical note. No remote changes or publication.

## 1. Scope and notation

Let n>=3, let a_0,...,a_(n-1) be distinct real numbers, put m=n-1, and let d>=1. Write

    g(z)=product_s(z-a_s),
    H(L)=h_d(L+a_0,...,L+a_(n-1)),
    N=m+d.

The standard divided-difference identity is

    H(L)=sum_s (L+a_s)^N / g'(a_s).                 (1)

The one-gap cofactor theorem already proved elsewhere reduces a nonzero kernel to

    H Y' - alpha H'Y = 0,
    alpha=t/(m+d)=r/m in (0,1),
    Y=sum_s w_s(L+a_s)^t,
    1<=r<=m-1,

with t an integer >=m. In lowest terms alpha=p/q, every root multiplicity of H must be divisible by q, and q divides m. For even d, positivity on R additionally gives q divides d/2. Those existing statements are inputs here, not new results.

## 2. A general multiplicity theorem

**Theorem.** Every complex root of H has multiplicity strictly less than m=n-1.

Suppose H has a root zeta of multiplicity at least m. Differentiating (1) j=0,...,m-1 times, and dividing by nonzero falling factorial constants, gives

    sum_s (zeta+a_s)^(N-j) / g'(a_s)=0.

Set x_s=zeta+a_s and v_s=x_s^(d+1)/g'(a_s). The preceding identities say that v annihilates every polynomial of degree at most m-1 evaluated at the distinct x_s. This m-by-(m+1) Vandermonde matrix has a one-dimensional nullspace. Its standard null vector is (1/g'(a_s))_s, since translation preserves the pairwise differences. Therefore

    (zeta+a_s)^(d+1)=C                            (2)

for every s and a common constant C. If C=0, every zeta+a_s vanishes, contradicting distinctness. If C!=0, (2) says that the m+1>=3 distinct points zeta+a_s lie on one circle centered at zero. They also lie on a single horizontal line, which intersects that circle in at most two points. Contradiction.

The proof applies to real as well as nonreal zeta. Distinct real offsets and n>=3 are essential assumptions in this argument. It does not prove that H is squarefree when n>=4, and it does not generally exclude all proper powers.

### Kernel corollaries

A kernel denominator q=m is impossible, because every root multiplicity of H would then be at least m. Consequently:

- Every first-moment index r coprime to m is excluded, since its reduced denominator is q=m.
- If n-1 is prime, the whole one-gap family has complex linear independence for every d and every allowed distinguished exponent.
- For the remaining even-d candidates, the denominator must be a proper divisor q of m with q>1 and q dividing d/2.

The prime-(n-1) statement is a kernel theorem. For n>=4 it is not a theorem that H itself has no proper power of arbitrary exponent: a power denominator not dividing m is irrelevant to this kernel reduction.

The parent researcher and both constructive partners independently checked the nullspace argument and the prime-(n-1) corollary.

## 3. A stronger multiplicity bound for nonreal roots

**Theorem.** If zeta is nonreal, then mult_H(zeta)<=floor(n/2).

Let k=mult_H(zeta). By Section 2, k<m, so v=m-k>=1. The same derivative argument, now with k rows, says that

    (zeta+a_s)^D=P(a_s),
    D=N-k+1=v+d+1,
    deg P<=v,                                    (3)

for a complex polynomial P. Indeed vectors P(a_s)/g'(a_s), deg P<=m-k, form exactly the nullspace of evaluation of polynomials of degree <=k-1: they annihilate those polynomials by the divided-difference identity and have the required dimension n-k.

Write zeta=b+ic with c!=0, set Q(x)=(x+b)^2+c^2, and R(x)=P(x) conjugate(P(x)) for real x. The rational function

    f(x)=R(x)/Q(x)^D

is real and smooth on R, and (3) gives f(a_s)=1 at n distinct points. Rolle's theorem forces f' to have at least n-1=m distinct real zeros. But

    f'(x)=[Q(x)R'(x)-D Q'(x)R(x)]/Q(x)^(D+1).

Its numerator is a nonzero polynomial of degree at most 2v+1. To see nonzeroness, if e=deg P<=v, its leading coefficient is 2(e-D) times the positive leading coefficient of R; D>v>=e. Hence

    m<=2v+1=2(m-k)+1,
    k<=floor((m+1)/2)=floor(n/2).

The parent researcher and translated-root partner independently approved this proof. This strengthens the root-multiplicity estimate, but does not improve the denominator corollary by itself: every proper divisor of m is already at most m/2. It must not be counted as an additional independence family.

## 4. Exact general moment-span criterion

This records an additional, independent condition when proper-power exclusion is unavailable. It is an exact test, not a claim that the test always fails.

Suppose a candidate alpha=r/m=p/q is fixed, let t=alpha(m+d), s=alpha d=t-r, and let V=m-r. Suppose H has the necessary power structure and let Y_0 be its monic polynomial alpha-th power. Write

    Y_0(L)=sum_(j=0)^s y_j L^(s-j),   y_0=1,
    F_j=y_j (r+1)(r+2)...(r+j) / [s(s-1)...(s-j+1)]
        for 0<=j<=s,
    F_0=1,
    G(z)=product_s(1-a_s z).

Then Y_0 belongs to span{(L+a_s)^t} if and only if

    [z^j] G(z) sum_(i=0)^s F_i z^i = 0
    for V<j<=s.                                  (4)

Proof: put beta_j=sum_s w_s a_s^j. Because deg Y_0=s=t-r, beta_0,...,beta_(r-1) vanish. The vectors satisfying those r moment conditions are exactly

    w_s=P(a_s)/g'(a_s),   deg P<=V.

After dividing by the nonzero beta_r, write

    P(a)=sum_(i=0)^V c_i a^(V-i),   c_0=1.

The divided-difference identity gives

    beta_(r+j)/beta_r=sum_(i=0)^min(V,j) c_i h_(j-i)(a).

On the other hand, the binomial expansion of Y_0 gives this same ratio as F_j for 0<=j<=s. Since sum h_j(a)z^j=1/G(z), coefficient matching is equivalent to (4), with c_0,...,c_V read from the first V+1 coefficients of G(z)F(z). These coefficients determine the weights uniquely. A constant factor restores the monic normalization: beta_r=1/binom(t,r).

The condition is translation-invariant, although its coefficient presentation uses a chosen origin. It is valid for complex coefficients and distinct real offsets; the proof of this algebraic span equivalence actually only requires distinct complex offsets.

When t=m, one has s=V and (4) contains no equations: all polynomials of degree <=m are in the shifted-power span. Therefore a purely universal span-exclusion argument cannot avoid analyzing the proper-power issue in those parameter ranges. This is a quantifier boundary, not a counterexample.

## 5. A redundant near-top index check

For r=m-1, centering sum a_s=0 and comparing the coefficient immediately below the top degree of Y_0 forces P(a)=a up to scale. Hence a possible real kernel vector u_s=g'(a_s)w_s is proportional to a_s and has both signs. Comparing the next coefficient gives

    d(m-2)=2m.

This supplies a span obstruction, but Section 2 already excludes r=m-1 because gcd(m-1,m)=1. It is not a separate newly proved family and is recorded only as a consistency check.

## 6. Boundaries

These results apply to the one-gap background from the existing cofactor/ODE reduction. They do not prove arbitrary-background independence, a nonnegative-kernel statement beyond the proven family, ASNC, a sparse-support separation oracle, or a P-versus-NP conclusion. They supply no remote merge or release authorization.
