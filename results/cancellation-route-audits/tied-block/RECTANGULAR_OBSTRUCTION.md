# Rectangular all-red blocks: an exact obstruction and its next coefficient

The nonempty rectangular formulas below assume 1≤r<s; empty red blocks are trivial and treated separately.

18 October 2026. Structural checkpoint, with exact bounded examples. This is not an ASNC counterexample.

## 1. The maximal Laplace coefficient

Let exactly I×J be red, with 1≤r=|I|<s=|J| and r+s≤n. Retain arbitrary distinct real offsets a_i and distinct nonnegative integer exponents e_j. Define H_m=∏_{q=0}^{m−1}q!, E=Σe_j, and use original index order in every Vandermonde. Since r<n/2, the size-r Laplace terms strictly dominate every smaller size. Their common degree is

    D = E−binom(r,2)−binom(n−r,2).

Their combined leading polynomial is

    [λ^D] F(z,λ) = A S (z−1)^r,
    A = (−1)^ΣI Δ(a_I)Δ(a_{Iᶜ})/(H_r H_{n−r}),
    S = Σ_{B⊆J, |B|=r} (−1)^ΣB Δ(e_B)Δ(e_{Bᶜ}).

Unlike a square block, the maximal size has several column choices. The scalar S can vanish although all offsets and exponents are distinct.

## 2. Exact remainder-matrix quotient

Put X=(e_j:j∈J), Y=(e_j:j∈Jᶜ), each in original index order; let m=n−s, p=s−r, q=m−r. Let

    f(Xvar)=∏_{j∈J}(Xvar−e_j),
    g(Xvar)=∏_{j∈Jᶜ}(Xvar−e_j).

Build a (p+q)×(p+q) matrix K with rows h=r,…,n−r−1. Its first p columns are indexed by ℓ=r,…,s−1 and contain

    [Xvar^ℓ](Xvar^h mod f).

Its last q columns are indexed by ℓ=r,…,m−1 and contain

    [Xvar^ℓ](Xvar^h mod g).

Then the exact polynomial identity is

    S = (−1)^(ΣJ+binom(p,2)) Δ(e_J)Δ(e_{Jᶜ}) det K.        (1)

Proof. Form the n×n matrix M whose first r rows are e_j^h 1_{j∈J}, h=0,…,r−1, and whose last n−r rows are e_j^h, h=0,…,n−r−1. Laplace expansion in the first r rows gives S=(−1)^binom(r,2) det M. Order the columns as J,Jᶜ, producing sign (−1)^(ΣJ−binom(s,2)). Subtract the first r rows from the corresponding low-degree rows in the lower block. These lower low-degree rows now have support only on Jᶜ. Right-multiply the two column blocks by their inverse Vandermonde evaluation matrices. The determinant factors removed are Δ(e_J)Δ(e_{Jᶜ}); evaluation of a polynomial followed by this inverse gives its remainder coefficients modulo f or g. Expanding the two low-degree identity blocks leaves K and a sign (−1)^{r(s−r)}. Combining signs gives binom(r,2)+ΣJ−binom(s,2)+r(s−r) ≡ ΣJ+binom(p,2) mod 2, proving (1).

In particular the quotient is a homogeneous polynomial of degree

    (s−r)(n−s−r) = pq.

Its determinant form is preferable to claiming positivity. Neither distinctness nor ordering of the full exponent list forces it to be nonzero for arbitrary J.

### Saturated rectangles are reducible

If r+s=n, then q=0 and K is the identity. Therefore

    S=(−1)^(ΣJ+binom(s−r,2)) Δ(e_J)Δ(e_{Jᶜ}) ≠ 0.

This is also an exact fiber reduction to a square block: each permutation has r edges from the row set I, so its counts in I×J and I×Jᶜ sum to r. Consequently

    F_{I,J}(z,λ)=z^r F_{I,Jᶜ}(z^{-1},λ).

Since |Jᶜ|=r, the right side is an already established square-block family with reversed target count. Thus this corollary should not be advertised as an independent general rectangular theorem.

## 3. The first nonconstant quotient: an explicit cancellation family

Take n=2r+2 and s=r+1, so p=q=1. Writing σ_X=Σ_{j∈J}e_j and σ_Y=Σ_{j∈Jᶜ}e_j, the remainder matrix is simply

    K = [[1,1],[σ_X,σ_Y]].

Therefore

    S = (−1)^ΣJ Δ(e_J)Δ(e_{Jᶜ})(σ_Y−σ_X).             (2)

The candidate degree-D coefficient vanishes exactly when the two exponent sums agree. This is a multirow obstruction when r≥2, not just a one-partial-row example.

### Gapped exponents at n=6

Take r=2, I={0,1}, J={0,2,5}, a_i=i and e=(0,1,2,3,4,6). The selected exponents are {0,2,6}, the others {1,3,4}; both sums are 8. Hence the candidate degree D=9 cancels. The next coefficient is

    [λ^8]F(z,λ)=−6048(z−1)².

Thus target degrees are all 8, with leading coefficients −6048,12096,−6048 at t=0,1,2.

### Source-standard labels at n=8

Take r=3, I={0,1,2}, J={0,1,6,7}, a_i=e_i=i. The selected exponents and their complement both sum to 14. The candidate degree is

    D=28−binom(3,2)−binom(5,2)=15,

but its coefficient is zero. The exact next coefficient is

    [λ^14]F(z,λ)=967680(z−1)³.

Every target t=0,1,2,3 is nonempty and its polynomial is nonzero of exact degree 14. The leading coefficients are

    −967680, 2903040, −2903040, 967680.

This is an exact counterexample to the proposed universal nonvanishing of the maximal-size rectangular Laplace leading sum, under standard ordered labels. It is explicitly not an ASNC counterexample.

## 4. A proof of the next coefficient on the balanced-sum locus

Throughout this section r≥1, as required for the row mean and the r×r minor correction; the empty-block case r=0 is outside this correction formula.

Write e₂(X)=Σ_{u<v in X}uv. In the equal-halves family of Section 3, define

    T = Σ_{B⊆J, |B|=r} (−1)^ΣB Δ(e_B)Δ(e_{Bᶜ}) Σ_{j∈B}e_j.

There is a second exact determinant identity:

    T = (−1)^ΣJ Δ(e_J)Δ(e_{Jᶜ}) [e₂(Y)−e₂(X)].       (3)

For its proof replace the top-row monomial degrees 0,…,r−1 in M by 0,…,r−2,r. Their determinant on columns B is Δ(e_B)Σ_{j∈B}e_j. Repeat the elimination proving (1), now using these same low-degree indices in each column block. The two remaining coefficient columns have degree r−1, and the remaining row degrees are r−1,r+1. The remainder matrix has rows (1,1) and (−e₂(X),−e₂(Y)). The single row interchange needed to place the eliminated degrees first changes its determinant sign, yielding (3). This proof also covers r=1, with the initial degree list empty before the final degree r.

For a full translated minor of size m, with offsets b and exponents f, its first two coefficients are

    det[(λ+b_i)^{f_j}]
      = L λ^d + L (Σ_i b_i)(Σ_j f_j−binom(m,2))/m · λ^{d−1}
        + terms of smaller degree,

where d=Σf−binom(m,2) and L=Δ(b)Δ(f)/H_m. The formula follows from Cauchy–Binet: after the minimal degree list 0,…,m−1, the unique next list is 0,…,m−2,m. The two alternant ratios are Σb and (Σf−binom(m,2))/m. If d=0, the displayed next coefficient is interpreted as zero, consistent with its factor d.

Multiplying this expansion for the selected and complementary minors shows that, whenever S=0,

    [λ^{D−1}]F(z,λ)
      = A (mean(a_I)−mean(a_{Iᶜ})) T (z−1)^r.        (4)

The constant-in-Σe_B pieces sum to multiples of S and vanish. The next lower Laplace size has degree D−3 because n=2r+2, so it cannot interfere with (4).

For the n=8 standard example, A=−1, the row-mean difference is 1−5=−4, Δ(e_J)Δ(e_{Jᶜ})=1260·12=15120, and e₂(Y)−e₂(X)=71−55=16. Formula (4) gives (−1)(−4)(15120)(16)=967680. This proves the observed degree-14 certificate directly. For n=6, A=−1, mean difference −3, the signed Vandermonde product is −288, and e₂ difference 7, giving −6048.

Further cancellation is possible if the row means or these second elementary sums also agree. No general lower-degree nonvanishing claim is made here. This checkpoint stops after the displayed bounded constructions.

## 5. Verification scope

`check.py` compares all bivariate coefficients from direct permutation expansion and raw subset-state Laplace recurrence for fixed examples; it verifies the n=5 and n=7 tied square cases, nonprincipal/gapped square labels, a larger-majority square block, and the stated rectangular examples. `results.json` contains the complete exact coefficients. Checks are ordinary exceptions, not removable assertions. The n=8 example is a single specified coloring, not an all-colorings enumeration. `check_identities.py` separately verifies the quotient and weighted column identities on ten fixed cases through n=12, including unsorted labels. Normal and optimized full-polynomial runs produce the identical `results.json` SHA-256 recorded in `CHECKPOINT.md`. All work is local, uses only standard-library code written for this checkpoint, and makes no remote writes or publication.
