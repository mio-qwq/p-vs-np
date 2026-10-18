# The first tied all-red-block boundary

18 October 2026. Local proof and exact checks. This is a sufficient binary-fiber family, not a proof of general ASNC or an ASNC counterexample. No novelty claim is made.

## Result

Let n = 2k−1, with k ≥ 2. Rows and columns retain their original order 0,…,n−1. Let a_i be arbitrary distinct real offsets and e_j arbitrary distinct nonnegative integer exponents. Put

    V_ij(λ) = (λ+a_i)^{e_j},       E = Σ_j e_j.

Color exactly I×J red, where |I| = |J| = k. Let

    F_{I,J}(z,λ) = det[z^{1_{i∈I,j∈J}} V_ij(λ)],
    P_t(λ) = [z^t] F_{I,J}(z,λ),
    H_r = ∏_{q=0}^{r−1} q!,
    Δ(x_S) = ∏_{p<q; p,q∈S}(x_q−x_p).

Define

    D = E−(k−1)²,
    C = (−1)^(ΣI+ΣJ)
        Δ(a_I) Δ(a_{Iᶜ}) Δ(e_J) Δ(e_{Jᶜ}) / (H_k H_{k−1}).

Then the exact combined leading coefficient, as a polynomial in z, is

    [λ^D] F_{I,J}(z,λ) = C z(z−1)^{k−1}.

There are no higher powers of λ. Therefore P_0 = 0, and every feasible target t = 1,…,k has exact degree D and leading coefficient

    [λ^D] P_t = C (−1)^{k−t} binom(k−1,t−1) ≠ 0.

The targets 1,…,k are feasible independently: choose t pairings within I×J, k−t pairings from I to Jᶜ, k−t pairings from Iᶜ to J, and t−1 pairings within Iᶜ×Jᶜ. These exhaust both parts with the required sizes. Thus this result does not mistake the impossible t=0 count for a cancellation counterexample.

## 1. Why precisely two Laplace sizes tie

Write R = V restricted to I×J and zero elsewhere. Generalized Laplace expansion gives

    F_{I,J} = Σ_{s=0}^k (z−1)^s
      Σ_{A⊆I,B⊆J; |A|=|B|=s}
        (−1)^(ΣA+ΣB) det V[A,B] det V[Aᶜ,Bᶜ].

The full translated generalized-Vandermonde minor identity gives each nonzero summand degree

    d_s = E−binom(s,2)−binom(n−s,2).

Here d_{s+1}−d_s = 2(k−s−1). Hence d_{k−1} = d_k = D and all s ≤ k−2 have strictly lower degree. The unique size-k term has leading coefficient C. If A_{k−1} denotes the full leading coefficient sum at size k−1, then

    [λ^D] F_{I,J} = A_{k−1}(z−1)^{k−1} + C(z−1)^k.

The issue is exactly to evaluate A_{k−1}, rather than to assume it is separately sign-coherent.

## 2. A structural identity for the tied sum

For any n=2k−1 distinct real numbers x_0,…,x_{n−1} and any k-element index set I,

    Σ_{p∈I} (−1)^(Σ(I\{p}))
      Δ(x_{I\{p}}) Δ(x_{Iᶜ∪{p}})
      = (−1)^ΣI Δ(x_I) Δ(x_{Iᶜ}).                 (★)

All subsets in this formula are ordered by original indices. To prove it, set

    Q(X) = ∏_{r∈I}(X−x_r),
    U(X) = ∏_{q∈Iᶜ}(X−x_q).

After dividing the summand by the right side of (★), the signs from the original index order cancel, and its value is U(x_p)/Q′(x_p). The polynomial U is monic of degree k−1. Lagrange interpolation of U at the k roots of Q, followed by comparison of the X^{k−1} coefficients, gives

    Σ_{p∈I} U(x_p)/Q′(x_p) = 1.

This proves (★). It does not require the x_i to be increasing, positive, or equally spaced.

The tied leading sum factorizes into one such row sum and one column sum:

    A_{k−1} = 1/(H_{k−1} H_k)
      × [Σ_{p∈I} (−1)^(Σ(I\{p}))
           Δ(a_{I\{p}}) Δ(a_{Iᶜ∪{p}})]
      × [Σ_{q∈J} (−1)^(Σ(J\{q}))
           Δ(e_{J\{q}}) Δ(e_{Jᶜ∪{q}})].

Applying (★) twice gives A_{k−1} = C exactly. Thus

    A_{k−1}(z−1)^{k−1} + C(z−1)^k
      = C z(z−1)^{k−1},

proving the claimed nonzero coefficient for every feasible target.

Individual terms in either sum can have opposite signs, even with increasing labels. For n=5, k=3, I={0,1,2}, x_i=i, the three signed row terms are −12, +12, −2. Their sum is −2, exactly (−1)^ΣI Δ(x_I)Δ(x_{Iᶜ}). The conclusion follows from interpolation, not termwise positivity.

## 3. A second proof and an exact fiber equivalence

Let r(π) count π's edges in I×J and b(π) count its edges in Iᶜ×Jᶜ. Counting the rows of I and the columns of J gives

    r(π)−b(π) = |I|+|J|−n = 1.

Consequently the identity holds coefficientwise for every matrix of edge weights:

    F_{I,J}(z,λ) = z F_{Iᶜ,Jᶜ}(z,λ).

This directly relates the tied boundary to the complementary (k−1)×(k−1) block. Applying the [established small-block result](SMALL_SQUARE_BACKGROUND.md) to that complementary block gives the same degree D and coefficient C z(z−1)^{k−1}. The cofactor sign is unchanged because

    (ΣIᶜ+ΣJᶜ)−(ΣI+ΣJ) = 2Σ_{i=0}^{n−1} i−2(ΣI+ΣJ)

is even.

Alternatively, without using the complementary-block theorem, F_{I,J}(0,λ)=0 is immediate because no permutation can avoid I×J. At degree D this says

    0 = (−1)^{k−1} A_{k−1} + (−1)^k C,

so A_{k−1}=C. This is the shortest tied-sum proof; identity (★) explains its Vandermonde structure directly.

## 4. Standard ordered labels

For a_i=e_i=i and I=J={0,…,k−1},

    E = (2k−1)(k−1),       D = k(k−1),
    C = H_k H_{k−1}.

Thus

    [λ^{k(k−1)}] P_t
      = (−1)^{k−t} binom(k−1,t−1) H_k H_{k−1}.

For n=5,k=3, the combined top polynomial is

    [λ^6] F(z,λ) = 2z(z−1)² = 2z−4z²+2z³.

The feasible target leading coefficients are 2, −4, 2. For n=7,k=4 they are −24, 72, −72, 24 at degree 12.

If only the labels are standard but I,J are arbitrary k-element subsets, the general formula above still applies; H_k H_{k−1} is the simplification only for the first-k principal block (or a corresponding consecutive block with the same internal Vandermonde products and sign).

## 5. The larger square-block family also follows

The same exact counting identity for any |I|=|J|=k gives

    r(π)−b(π) = 2k−n.

When k>n/2 this yields F_{I,J}=z^{2k−n} F_{Iᶜ,Jᶜ}. Thus every square all-red block reduces to the smaller of the block and its complement. Combining this identity with the established small-block theorem proves the following unified formula for every 0≤k≤n:

    m = n−k,
    D = E−binom(k,2)−binom(m,2),
    C = (−1)^(ΣI+ΣJ) Δ(a_I)Δ(a_{Iᶜ})Δ(e_J)Δ(e_{Jᶜ})/(H_kH_m),
    [λ^D] F_{I,J} = C z^{max(0,2k−n)}(z−1)^{min(k,m)}.

Every feasible target max(0,2k−n)≤t≤k has a nonzero leading coefficient. Empty products are 1. At k=0 and k=n this includes the full uncolored determinant and its z^n multiple.

This is a structural reduction of the previously unresolved tied majority-block boundary, not an enumeration of colorings or a new proof of the already established small-block case. General singular red incidence patterns remain outside this result.

## 6. Exact verification and limits

`check.py` uses only the Python standard library and exact rational arithmetic. It constructs the raw bivariate determinant in two independent ways: a signed permutation expansion and subset-state Laplace recurrence. It compares all coefficients, verifies the exact complementary-block shift, tests the predicted degrees and leading coefficients, and directly checks the interpolation sum (★). Fixed examples include n=5 standard labels, nonprincipal sets with unsorted rational offsets and gapped exponents, and n=7 standard labels. A majority block beyond the first tie is also checked.

`results.json` records exact outputs, including the complete standard n=5 fiber polynomials. Checks raise explicit errors and remain active under `python -O`. No remote writes, publication, network lookups, or downloaded code were used.

The proof settles this entire first tied all-red-square-block family. In particular there is no zero top coefficient for a feasible target under its hypotheses; P_0=0 is forced infeasibility. No statement is made about all binary colorings, general ASNC, or complexity consequences.
