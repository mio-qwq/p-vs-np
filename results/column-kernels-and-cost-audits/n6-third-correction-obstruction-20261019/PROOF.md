# The universal six-row third correction and an exact vanishing certificate

19 October 2026. This package derives the first possible odd correction in the symmetric six-row residual regime and refutes the claim that it must always survive. It does not exhibit an identically zero masked polynomial, and does not extend the preceding theorem's scope.

## 1. Setup

Normalize the offsets and ranks as

    a=(-1,-v,-u,u,v,1), 0<u<v<1,
    i=0, p=5, c=3, k=e_3,
    sum e=6k+10.

Let b_0<...<b_4 be the five exponents other than k. Then

    sum b=5k+10, mean b=k+2.

Let lambda be their usual five-variable alternant partition, of size 5k. Define

    H(L)=(L-1)^k s_lambda(L-v,L-u,L+u,L+v,L+1)
                    /s_lambda(1,1,1,1,1),
    Q=u^2+v^2,
    C2=sum_j (b_j-(k+2))^2,
    C3=sum_j (b_j-(k+2))^3,
    nu=(C2-10)/120 > 0.

Thus H is the normalized endpoint Laplace polynomial, with leading coefficient 1 and degree D=6k. The strict positivity of nu follows from distinct integral exponents and the absence of k, as in the prior variance argument.

The universal third correction is

    [L^(6k-3)] H
      =nu(Q-2)+(C3/1260)(2-5Q).                   (1)

## 2. Confluent derivation of the third centered moment

The normalized single-variable Schur specialization

    S(t)=s_lambda(exp(t),1,1,1,1)/s_lambda(1,1,1,1,1)

is the exponential generating function of a nonnegative integer-valued weight W: the coefficients of s_lambda(x,1,1,1,1) are nonnegative, and normalization makes their sum 1. Its mean is k by symmetry and homogeneity.

Let f(z)=product_j(z-b_j). The confluent alternant identity is

    S(t)=24/(exp(t)-1)^4 sum_j exp(b_j t)/f'(b_j).

Set

    A(t)=24 t^(-4) sum_j exp(b_j t)/f'(b_j).

Lagrange interpolation gives sum b_j^(4+r)/f'(b_j)=h_r(b), so the apparent singularity is removable and

    A(t)=sum_(r>=0) [24 h_r(b)/(r+4)!] t^r.

Moreover

    S(t)=exp(-2t) [t/(2 sinh(t/2))]^4 A(t).         (2)

The logarithm of the bracketed factor is even. Thus its third cumulant is zero, while exp(-2t) only changes the first cumulant. Writing B_j=sum b_i^j and using

    h_1=B_1,
    h_2=(B_1^2+B_2)/2,
    h_3=(B_1^3+3B_1 B_2+2B_3)/6

in A(t) yields by direct expansion of log A

    kappa_3(A)=2 sum_j(b_j-B_1/5)^3/(5*6*7)=C3/105.

Likewise kappa_2(A)=C2/30, while the bracket in (2) contributes -1/3 to the variance. Consequently

    E(W-k)^2 = (C2-10)/30 =4nu,
    tau:=E(W-k)^3 = C3/105.                       (3)

This derivation uses an exact formal-series identity; no signed moment weights are treated as probabilities.

## 3. Recovering all mixed cubic derivatives by homogeneity

Write the normalized Taylor coefficients of s_lambda near (1,...,1) as

    alpha  = partial_1^2 s/(2s),
    beta   = partial_1 partial_2 s/s,
    alpha3 = partial_1^3 s/(6s),
    beta21 = partial_1^2 partial_2 s/(2s),
    gamma  = partial_1 partial_2 partial_3 s/s,

all evaluated at the all-ones vector. The known second moments and (3) give

    alpha=(k(k-1)+4nu)/2,
    beta=k^2-nu,
    alpha3=binom(k,3)+2(k-1)nu+tau/6.              (4)

Euler homogeneity, differentiated twice, gives

    3alpha3+4beta21=(5k-2)alpha,
    4beta21+3gamma=(5k-2)beta.                     (5)

For the five offsets A=(-v,-u,u,v,1), the power sums are

    p1=1, p2=1+2Q, p3=1,

so the normalized cubic Taylor coefficient of s_lambda(L+A) is

    alpha3 + (2beta21-gamma)Q.

The quadratic coefficient is

    binom(k,2)-kQ+nu(2+5Q),

and its linear coefficient is k. Multiplying by (L-1)^k and using (4)--(5) gives

    [L^(6k-3)]H = (tau/6)(1-5Q/2)+nu(Q-2).

Substituting tau=C3/105 proves (1).

## 4. Exact admissible vanishing of the third correction

Choose

    e=(0,8,9,10,21,22), k=10,
    b=(0,8,9,21,22), mean b=12,
    u^2=60/67, v^2=62/67.

These are distinct nonnegative integer exponents, and

    sum e=70=6*10+10.

The chosen offsets satisfy 0<u<v<1 and are distinct. Their symmetry gives both the product and centroid resonance conditions exactly.

The centered exponent list is (-12,-4,-3,9,10), hence

    C2=350, C3=-90, nu=17/6, tau=-6/7.

Formula (1) becomes

    [L^57]H=(67Q-122)/21.

At Q=122/67 it vanishes exactly.

The two masked-endpoint Laplace terms have opposite leading constants and are related by L -> -L. Their sum retains only odd powers. The degree-59 coefficient vanishes by exponent resonance, and the degree-57 coefficient now vanishes by the explicit certificate. The degree-60,58,56 coefficients vanish by parity. The complete unmasked determinant has degree

    sum e-binom(6,2)=70-15=55.

Thus the masked polynomial has degree at most 55. We do not claim it is zero, nor determine its actual degree here. This certificate refutes the universal assertion that the D-3 correction always survives in the first residual size.

## 5. Scope and stopping condition

Three proposed shortcuts have now been falsified separately: full linear independence of column Laplace polynomials, universal nonzero extreme-root evaluation, and universal nonzero D-3 correction. The first two failures are in separate packages. None is a zero-polynomial counterexample to the original two-hole nonvanishing problem.

Further continuation should use a new structural positive-functional/kernel argument, a complete-polynomial invariant, or an exact full zero certificate. This package stops the escalation through successive coefficients; another isolated deeper cancellation would not resolve the remaining question.
