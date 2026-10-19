# Symmetric log-concave moment polynomials cannot have power bases of degree at most six

Date: 2026-10-19. Local theorem supplement; no remote changes.

## Theorem

Let X be a nondegenerate symmetric real random variable with a log-concave density and finite moments through an even degree N. Set

    P_N(L)=E[(L+X)^N].

If P_N is a proper polynomial power Q(L)^s over C, with Q monic and s>=2, then deg Q>=8.

In particular, this applies to the monic normalization of h_N(L+a_1,...,L+a_n), for any nonconstant real offset multiset symmetric about its mean, after translating that mean to zero. Repeated offsets are allowed. Therefore all symmetric-offset degree-eight and degree-twelve cases are excluded.

This theorem does not exclude bases of degree at least eight, and it does not apply to arbitrary asymmetric offsets.

## Proof

The polynomial P_N is real, even, monic, and strictly positive on R. If P_N=Q^s with Q monic, uniqueness of the monic s-th root shows that Q is real. It has no real roots and therefore has even degree. Because Q(-L) is also monic and its s-th power is P_N, uniqueness likewise makes Q even. Its leading coefficient is positive and it has no real zeros, so Q is strictly positive on R.

Write the bottom of Q as

    Q(L)=c+b L^2+a L^4+O(L^6).

Here c>0. Let A=[L^4]P_N, B=[L^2]P_N and C=P_N(0). The L^2 coefficient of P_N is positive, so B=s c^(s-1)b>0 and hence b>0.

The density of |X| on [0,infinity) is log-concave. The Berwald–Borell normalized-moment inequality says that k -> E[|X|^k]/k! is log-concave. Applying it at N-4,N-2,N (all nonnegative because N>=4) gives

    (E[X^(N-2)]/(N-2)!)^2
       >= E[X^(N-4)]/(N-4)! * E[X^N]/N!.

The three quantities on the two sides are respectively 2B/N!, 24A/N!, and C/N!. Thus

    B^2 >= 6AC.                                        (1)

Meanwhile expansion of Q^s gives

    C=c^s,
    B=s c^(s-1)b,
    A=s c^(s-1)a + s(s-1)c^(s-2)b^2/2.

Substitution into (1), followed by division by the positive factor s c^(2s-2), gives

    (3-2s)b^2 >= 6ca.                                  (2)

Since s>=2 and b,c>0, equation (2) forces a<0.

If deg Q=2, then a=0. If deg Q=4, monicity gives a=1. Both contradict a<0.

If deg Q=6, then Q=L^6+a L^4+b L^2+c. Comparing the next-to-leading coefficient in P_N=Q^s gives

    s a = binom(N,2) E[X^2] > 0.

Again this contradicts a<0. Hence deg Q>=8.

## Why simplex projections satisfy the hypotheses

Uniform measure on the simplex is log-concave in its affine span. Its nonconstant linear projection X=sum_i U_i a_i has a one-dimensional log-concave density by marginal log-concavity; for n=2 it is a nondegenerate uniform density. A permutation reversing a symmetric offset multiset sends X to -X and preserves uniform measure, proving symmetry. Compact support gives every moment.

## Degree corollaries

If every proper positive divisor of N/2 is at most 3, then all possible proper-power bases have degree 2, 4, or 6 and are excluded, so P_N is not a proper power. This includes N/2 prime, and N/2=4,6,9 (thus N=8,12,18), as well as N=2 trivially. No larger-degree conclusion is asserted without checking the possible base degrees.

## Source

Bo'az Klartag and Joseph Lehec, “Poisson processes and a log-concave Bernstein theorem,” Lemma 2.1, proof, equation (6), page 4 in the author manuscript, explicitly states the normalized-moment log-concavity used above:

https://www.math.tau.ac.il/~klartagb/papers/log_concave_bernstein.pdf

The proof uses established marginal log-concavity and Berwald–Borell theorems. No novelty claim is made.
