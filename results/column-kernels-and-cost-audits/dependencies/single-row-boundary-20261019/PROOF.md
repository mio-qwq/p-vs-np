# The one-row boundary: two explicit nonvanishing tests

19 October 2026. Local continuation of `../single-edge-perturbation-20261019/PROOF.md`, Section 4. This closes two broad subcases of that remaining boundary; it does **not** prove every residual case or give a zero-polynomial counterexample.

## 1. Setup and result

Let n=q+2≥3, let a_0,…,a_(n−1) be distinct real offsets, and let e_0,…,e_(n−1) be distinct nonnegative integers. Fix distinct row indices i,p and a column c. Assume a_i is strictly smaller than every other offset, or strictly larger than every other offset. Color row i red in every column except c, and also color entry (p,c) red; every other entry is blue. Put

    V_sj=(Λ+a_s)^(e_j),
    F(z,Λ)=det[z^(red(s,j)) V_sj],
    P_t(Λ)=[z^t]F(z,Λ).

Only t=0,1,2 are feasible. Write

    k=e_c, m=n−1,
    S=Σ_j e_j,
    d=S−k−binom(m,2), D=k+d,
    A=Σ_s a_s,
    R=∏_(s≠i,p) (a_s−a_i)/(a_s−a_p),
    L_i=(−1)^(i+c) Δ(a without a_i) Δ(e without e_c)/H_m,
    H_m=∏_(h=0)^(m−1) h!.

The Vandermonde lists retain the original index order. In particular L_i≠0. Let b_0<⋯<b_(m−1) be the increasing list of exponents other than k, and define the nonnegative rational number

    v = [Σ_h b_h² − (Σ_h b_h)²/m − m(m²−1)/12]
        /[m(m²−1)].                                  (1)

The following are exact degree conclusions:

1. If R≠1, then deg P_1=D and

       [Λ^D]P_1 = L_i(R−1).                          (2)

2. If R=1 and nk≠D, then deg P_1=D−1 and

       [Λ^(D−1)]P_1 = −L_i(a_i−a_p)(k−d/m).         (3)

3. If R=1, nk=D, n≥4, and A≠n(a_i+a_p)/2, then v>0, deg P_1=D−2, and

       [Λ^(D−2)]P_1
         = −L_i v(a_i−a_p)[A−n(a_i+a_p)/2].         (4)

The outer fibers P_0 and P_2 are always nonzero of degree D. Thus each displayed sufficient condition proves nonvanishing of every feasible fiber. For n=3, R=1 is impossible, so item 1 settles that size.

### Immediate all-size corollaries

The middle fiber is nonzero for every n≥3 when k=e_c is the minimum or maximum exponent. If k is the minimum, distinct integrality gives S≥nk+binom(n,2), hence D≥nk+n−1. If k is the maximum, S≤nk−binom(n,2), hence D≤nk−(n−1)². Either way nk≠D, so cases 1–2 apply.

It is also nonzero for every n≥3 when the exponent set is consecutive, {h,h+1,…,h+n−1}, in any column order. Here D=nh+n−1 is not divisible by n, so nk=D is impossible. These corollaries concern the complete polynomial, including offsets at the leading-cancellation locus.

These conclusions do not need separation except where separation is part of the surrounding theorem. The proof works for arbitrary distinct real offsets whenever its stated numerical conditions hold.

## 2. Exact reduction to a column mask

Define the column-c Laplace term

    T_s(Λ)=(−1)^(s+c)(Λ+a_s)^k det V[rows≠s, columns≠c].

In any determinant permutation, assigning column c to row i gives exactly zero red edges; assigning it to row p gives exactly two; assigning it to any other row gives exactly one. Consequently

    P_0=T_i,  P_2=T_p,
    P_1=Σ_(s≠i,p) T_s = det V−T_i−T_p.             (5)

Equivalently, P_1 is det V after replacing just entries (i,c),(p,c) by zero. This is an identity of full polynomials, not a leading-term assertion.

The usual binomial/Cauchy–Binet expansion of a shifted alternant gives

    deg det V = S−binom(n,2) = D−m,
    deg T_s=D,
    [Λ^D]T_s=L_s
      =(−1)^(s+c) Δ(a without a_s) Δ(e without e_c)/H_m.  (6)

All displayed leading constants are nonzero. Indeed, for an l×l alternant with distinct exponents f_j, the first nonzero Taylor-index set is {0,…,l−1}; its coefficient is Δ(offsets)Δ(f)/H_l. Distinct nonnegative exponents ensure the resulting degree is nonnegative.

The Vandermonde deletion identity gives

    L_p/L_i = −R.                                   (7)

Equations (5)–(7) prove (2) and the outer-fiber assertions.

## 3. The first two normalized corrections of a cofactor

Let λ_h=b_(m−h)−(m−h), for h=1,…,m. This is a nonnegative partition of size d. The alternant formula yields

    T_s/L_s = (Λ+a_s)^k
              s_λ(Λ+a_t : t≠s)/s_λ(1,…,1).         (8)

In particular, the coefficient of Λ^(D−1) in T_s/L_s is

    β_s = (d/m)(A−a_s)+k a_s.                       (9)

This follows from symmetry and homogeneity: all first partial derivatives of s_λ at 1 agree and their sum is d s_λ(1).

Suppose now that nk=D, equivalently d=mk. Define

    α = (∂_1²s_λ)(1)/(2s_λ(1)),
    β = (∂_1∂_2s_λ)(1)/s_λ(1).

A direct computation below gives

    2α=k(k−1)+(m−1)v,
    β=k²−v.                                        (10)

Let Q_s=[Λ^(D−2)]T_s/L_s. Expanding (8) to second order,

    Q_s = binom(k,2)a_s²
          + k² a_s(A−a_s)
          + α Σ_(t≠s)a_t²
          + β Σ_(u<t;u,t≠s)a_u a_t.

Terms independent of s cancel on subtraction. Substituting (10) leaves the particularly simple identity

    Q_i−Q_p = v(a_i−a_p)[A−n(a_i+a_p)/2].            (11)

When R=1, equation (5) gives P_1=det V−L_i[(T_i/L_i)−(T_p/L_p)]. Since deg det V=D−m, its degree is below D−1 for n≥3, and below D−2 for n≥4. Equations (9) and (11) now prove (3) and (4).

## 4. Derivation and strict positivity of v at resonance

Here is a direct calculation, including the sign of (1), with no assumed positivity of signed moment weights. Put B_1=Σb_h, B_2=Σb_h², and f(T)=∏_h(T−b_h). The confluent alternant at m−1 nodes equal to 1 gives

    s_λ(x,1,…,1)/s_λ(1,…,1)
      = (m−1)!/(x−1)^(m−1) Σ_h x^(b_h)/f′(b_h).   (12)

The apparent singularity at x=1 is removable. Expanding x=1+h and using Lagrange interpolation,

    Σ b_h^(m−1)/f′(b_h)=1,
    Σ b_h^m/f′(b_h)=B_1,
    Σ b_h^(m+1)/f′(b_h)=(B_1²+B_2)/2,

shows that the coefficient of h is d/m. The coefficient α of h² is

    α = [(B_1²+B_2)/2 − m(m+1)B_1/2 + E_2]
        /[m(m+1)],

    E_2 = [(m(m+1)/2)² − m(m+1)(2m+1)/6]/2.

Elementary simplification gives

    2α + d/m − (d/m)² = (m−1)v.                    (13)

At d/m=k this is the first part of (10). Homogeneity at 1 yields

    m(2α)+m(m−1)β = d(d−1),

which gives the second part of (10).

Finally,

    B_2−B_1²/m = (1/m)Σ_(u<t)(b_t−b_u)²
                ≥ (1/m)Σ_(u<t)(t−u)²
                = m(m²−1)/12.                    (14)

The inequality uses distinct integer exponents b_t−b_u≥t−u. Equality holds precisely when b_h=h+b_0 for all h. At resonance, this would give d=mb_0=mk, hence b_0=k, contradicting the fact that k=e_c is absent from the b-list. Thus v>0 whenever nk=D.

## 5. Exact residual example and honest remaining scope

The three simultaneous conditions

    R=1,
    S=n e_c+binom(n−1,2),
    Σa=n(a_i+a_p)/2                                (15)

can all hold with separated, distinct integer offsets. For example choose

    n=5, a=(0,2,4,14,15), i=0,p=3,
    e=(0,1,2,3,5), c=1.

Here R=(2·4·15)/((2−14)(4−14)(15−14))=1, S=11=5·1+6, Σa=35=5·14/2, and D=5. Exact signed permutation expansion gives

    P_1(Λ)=−480480(49Λ²+446Λ−1680).                  (16)

Thus the degrees D,D−1,D−2 all vanish but the full middle fiber remains nonzero, with exact degree 2. This example is a finite certificate of deeper cancellation, not a strict counterexample to nonvanishing and not a universal residual proof.

The n=4 example with a=(0,1,2,3), e=(0,1,2,4), i=0,p=3,c=1 similarly has D=4 and

    P_1(Λ)=12(2Λ+3).

The general n≥5 simultaneous-resonance regime (15) remains unresolved by this argument. A useful next step must either control a genuinely later coefficient in that regime, give a full-polynomial structural proof, or exhibit an exact zero-polynomial certificate. More isolated nonzero examples do not close the gap.

### A further stress test, not an additional theorem

Keeping the same offsets (0,2,4,14,15) and rows i=0,p=3, but taking e=(0,7,10,17,22), c=2, gives D=50. The exact middle fiber has degree 46 and leading coefficient 542602700640000; hence all four coefficients at degrees 50,49,48,47 vanish. The full polynomial is recorded in `checker/results.json`. Both the signed-permutation checker and the independent audit verify it. This prevents replacing the unresolved regime with an unsupported assertion that the third correction must always survive.

## 6. Reproduction

Run `python checker/check.py` and `python -O checker/check.py`. The checker uses exact integer polynomial arithmetic and signed permutations. It verifies the original binary coloring, full fiber/cofactor identities, every cofactor's first two normalized corrections, the exact degree tests above, row/column reordering and reflected-offset cases, and the residual full-polynomial certificates. Its 40 cases are finite corroboration; the proof is in Sections 1–4.
