# A general obstruction to quadratic-base powers

19 October 2026. Local research; no remote changes.

## Theorem

Let n >= 2, let a_1,...,a_n be real numbers that are not all equal, and let s >= 2. Then

    h_(2s)(L+a_1,...,L+a_n)

cannot be the s-th power of a quadratic polynomial, up to a nonzero scalar.
Consequently, if d/2 is prime, the translated complete homogeneous polynomial of even degree d is not a proper polynomial power at all. Together with the elementary degree-2 case, this gives a uniform infinite degree family, rather than separate degree-8/10 coefficient calculations.

The theorem does NOT exclude proper powers with base degree 4 or more. It does NOT imply squarefreeness: individual repeated nonreal roots can occur.

## 1. Normalize and recover the knot moments

Translate the offsets to arrange sum_i a_i = 0 and write

    p_k = sum_i a_i^k.

Let U be uniform on the probability simplex and A=sum_i U_i a_i. The monic normalization of H_(2s) is

    P(L)=E[(L+A)^(2s)],
    E[A^k] = k! h_k(a)/(n)_k,

where (n)_k is rising factorial. Since the offsets are not all equal, p_2>0 and P is strictly positive on the real line.

If P is an s-th power of a monic quadratic over C, the monic quadratic has real coefficients by conjugation and uniqueness. It has no real roots. The coefficient of L^(2s-1) in P vanishes, so its linear coefficient vanishes. Thus

    P(L)=(L^2+c)^s,       c>0.                         (1)

Comparing coefficients in (1) gives, for 0<=j<=s,

    h_(2j)(a) = c^j (n)_(2j) binom(s,j)/(2s)_[2j],     (2)
    h_(2j+1)(a)=0       whenever 2j+1 <= 2s-1.

Here (2s)_[2j] is the falling factorial. In particular

    c=(2s-1)p_2/[n(n+1)]>0.

The generating identity

    G(t)=sum_(k>=0) h_k(a)t^k
        =product_i (1-a_i t)^(-1),
    log G(t)=sum_(k>=1) p_k t^k/k                       (3)

shows that every odd p_k with k<=2s-1 also vanishes.

## 2. The finite hypergeometric identity

Put b_j=h_(2j)(a), and choose any formal series B(z) whose coefficients through z^s are b_0,...,b_s. Equation (2) gives

    b_j/b_(j-1)
      =c(n+2j-2)(n+2j-1)/[2j(2s-2j+1)]
      =-c(n/2+j-1)((n+1)/2+j-1)/[j(1/2-s+j-1)] .      (4)

Thus through degree s these are the coefficients of

    _2F_1(n/2,(n+1)/2;1/2-s;-c z).

No analytic convergence or infinite-series identity is needed. Equivalently, the coefficient recurrence (4) directly gives, modulo z^s,

    z(1+c z) B''
      +[1/2-s+c(n+3/2)z] B'
      +c n(n+1)B/4 = 0.                              (5)

Define R=zB'/B. By (3) and the vanishing odd coefficients,

    R(z)=sum_(j=1)^s r_j z^j + O(z^(s+1)),
    r_j=p_(2j)/2 >0.                                  (6)

Multiplying (5) by z/B and substituting R gives, modulo z^(s+1),

    zR' + R^2 -(s+1/2)R
       +c z[zR'+R^2+(n+1/2)R+n(n+1)/4]=0.             (7)

Hence for 1<=j<=s,

    (s+1/2-j) r_j
      = sum_(i=1)^(j-1) r_i r_(j-i)
        +c[(j-1+n+1/2)r_(j-1)
            +sum_(i=1)^(j-2) r_i r_(j-1-i)
            +n(n+1)/4 * 1_(j=1)],                    (8)

with r_0=0 and empty sums zero. This is the structural recurrence; it holds for every s.

## 3. The last coefficient contradicts real knots

At j=s, the left coefficient of r_s in (8) is 1/2. Every displayed summand is nonnegative, and the term c(n+s-1/2)r_(s-1) is strictly positive.

If s=2, equation (8) therefore gives

    r_2 > 2r_1^2,
    p_4 > p_2^2.

If s>=3, the i=1 and i=s-1 summands are distinct, so it gives

    r_s > 4r_1 r_(s-1),
    p_(2s) > 2p_2 p_(2s-2).

Both contradict the elementary real-knot bound

    p_(2s)=sum_i a_i^(2s)
      <= (sum_i a_i^2)(sum_i a_i^(2s-2))
      =p_2 p_(2s-2),                                 (9)

which follows from a_i^2<=p_2. This proves the theorem.

## 4. Prime half-degrees and the ODE kernel reduction

For even degree d, the translated polynomial is positive on R. If its monic normalization is Q^q with q>1, uniqueness makes Q real, and Q has no real roots. Its degree is therefore even. Hence q divides d/2.

If d=2s and s is prime, the only possible q is s, so Q would be quadratic and the theorem excludes it. Thus there is no proper power for any d=2s with s prime, with no restriction on n beyond nonconstant real knots.

In the one-outlier-background ODE reduction, a kernel needs such a proper power plus the specified shifted-power span condition. Therefore absence of the proper power proves full complex linear independence for this infinite degree family, subject to the background assumptions in that reduction. No span membership or sign assertion follows for the remaining composite half-degrees.

## 5. Status

Independent audit completed: the root researcher independently derived the same finite coefficient recurrence, and the power-to-kernel auditor read this exact proof and approved equations (5)--(8), their truncation orders, both strict inequalities, and the prime-half-degree corollary. The separate audit is in `/workspace/shared/power-kernel-bridge-audit-20261019/AUDIT.md`; the independent root derivation is in `/workspace/shared/quadratic-power-root-20261019/DERIVATION.md`.

`check.py` passes both normal Python and `python -O`. It verifies the recurrence symbolically in n for s=2,...,12 (homogeneity reduces c to 1), exactly for positive rational c and s through 30, and checks the translation formula on representative real knots. The universal proof is (4)--(9), not finite testing.

The essential extra structure is (3), the generating function from real knots. General compactly supported positive moment distributions can have proper-power moment polynomials; no general-distribution claim is made.
