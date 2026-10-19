# Minimum-centering does not restore normalized even-moment log-concavity

19 October 2026. Exact local counterexample to one proposed extension route. This is separate from the all-degree symmetric theorem.

## Refuted lemma

A plausible extension would assert: for every real-knot simplex projection A and even N, translate A so that z -> E[(z+A)^N] is minimized at z=0; then its normalized even-moment sequence is log-concave, allowing the symmetric coefficient argument to continue.

That assertion is false even for N=6 and distinct real knots. This note does not supply a proper-power counterexample. Degree six is already covered by the existing no-proper-power theorem.

## Exact real-knot instance

Take exactly 100 distinct real knots

    a_j=j/1000,  0<=j<=98,   and a_99=100.

Thus there are 99 small knots, including zero, plus one final knot at 100. Let U be uniform on the 100-coordinate probability simplex, and let A=sum_j U_j a_j. This is a nondegenerate compactly supported log-concave real random variable.

Define its raw moments and translated moments by

    mu_k=E[A^k]=k! h_k(a)/(100)_k,
    M_k(c)=E[(A-c)^k]
          =sum_(j=0)^k binom(k,j) mu_j (-c)^(k-j).

All these coefficients are rational. Let c_* be the unique real zero of

    q(c)=-M_5(c).

Because q'(c)=5M_4(c)>0 for every real c, and q is monic of odd degree five, this root exists and is unique. Moreover

    d/dc M_6(c)=6q(c),

so c_* is the unique global minimizer of E[(A-c)^6]. Equivalently, E[(L+A)^6] is minimized at L=-c_*.

Exact rational endpoint evaluation gives

    q(2173/1000)<0<q(2174/1000),

so

    2173/1000<c_*<2174/1000.                         (1)

No approximate root is used in the proof.

## Strict failure of the needed inequality

Put

    H(c)=5M_4(c)^2-2M_2(c)M_6(c).

The normalized even-moment log-concavity difference at index four is exactly

    (M_4(c)/4!)^2-(M_2(c)/2!)(M_6(c)/6!)=H(c)/2880. (2)

Let l=2173/1000, u=2174/1000 and expand the exact degree-eight polynomial

    H(l+(u-l)t)=v_0+v_1 t+...+v_8 t^8.

The accompanying certificate records all nine rational coefficients and verifies

    v_0<0,       v_j>0 for 1<=j<=8,
    sum_(j=0)^8 v_j=H(u)<0.                          (3)

For 0<=t<=1, nonnegative powers are at most one, so

    H(l+(u-l)t)<=sum_(j=0)^8 v_j=H(u)<0.

Together with (1), this gives H(c_*)<0. Equation (2) proves the strict inequality

    (E[(A-c_*)^4]/4!)^2
      < (E[(A-c_*)^2]/2!) (E[(A-c_*)^6]/6!).        (4)

Thus even centering at the moment polynomial's own global minimum does not provide the normalized even-moment log-concavity required by the symmetric proof.

## Verification and recovery conditions

`check_asymmetric_barrier.py` reconstructs h_k in two independent exact ways: Newton's power-sum recurrence and direct truncated multiplication of all 100 geometric generating factors. It verifies (1), (2), every sign in (3), the derivative identities, and independently counts real roots of q and H on the rational interval. All checks use rational arithmetic and explicit exceptions, so they remain active under optimized Python.

Run:

    python check_asymmetric_barrier.py
    python -O check_asymmetric_barrier.py

The output file `asymmetric_barrier_certificate.json` contains the complete rational data. Numerical values are unnecessary to the certificate.

The symmetric theorem remains valid: actual symmetry provides a log-concave density for |X| and removes all odd polynomial terms. A nonsymmetric extension needs an additional hypothesis guaranteeing an adequate coefficient bound, a separate treatment of odd terms, or a different real-knot invariant. Merely translating until the linear polynomial coefficient vanishes is insufficient. No claim about arbitrary proper powers, kernel counterexamples, novelty, or P versus NP follows from this failed route.

## Quantitative recovery condition via a coefficient tail

A restricted nonsymmetric extension remains possible under an explicit coefficient bound. Let P be a real even-degree moment polynomial, center its unique real minimum at zero, and put

    sigma^2=P(0)/P''(0),
    B(z)=P(sigma z)/P(0)=sum_(k=0)^N beta_k z^k/k!.

Then beta_0=beta_2=1 and beta_1=0. A sufficient condition for a simple conjugate root pair is

    sum_(k=3)^N |beta_k| 2^k/k! < 1.                (5)

Indeed, on |z|=2, |1+z^2/2|>=1. Condition (5) makes the remaining tail strictly smaller than the quadratic there. Rouché's theorem gives exactly two roots inside |z|<2, counted with multiplicity. Since P is strictly positive on R, neither is real. Real coefficients force conjugation, so the two roots are distinct and each is simple.

A convenient stronger set of assumptions is

    0<beta_(2j)<=1,  2<=j<=N/2,
    sum_(odd k>=3) |beta_k| 2^k/k! < 3/13.          (6)

To see this, the even tail is at most sum_(j=2)^infinity 4^j/(2j)!. Its first term is 2/3 and successive ratios are at most 2/15, so it is at most 10/13. The odd-tail bound in (6) then implies (5).

These are degree-uniform sufficient conditions, not inequalities asserted for arbitrary real-knot projections. The strict conditions also give a quantitative route for sufficiently small asymmetric perturbations of a symmetric instance. In the counterexample above, beta_4=2M_2(c_*)M_6(c_*)/[5M_4(c_*)^2]>1 by (4), so minimum-centering by itself cannot establish the even coefficient hypothesis; a separate odd-tail estimate would be necessary as well. This recovery observation does not alter the frozen symmetric theorem or establish the unrestricted asymmetric conjecture.
