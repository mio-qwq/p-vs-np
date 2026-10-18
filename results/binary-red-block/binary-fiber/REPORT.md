# A first nonzero signed moment for binary exact-count fibers

18 October 2026. Local derivation and exact checks. This is a sufficient all-order family, not a proof of general ASNC, a P-versus-NP result, or a historical novelty claim.

## Result

For the complete bipartite graph, color exactly a proper matching of `k<n` edges red. Every target `0≤t≤k` has a nonzero exact-count Vandermonde polynomial. More precisely, its exact degree and first nonzero coefficient are explicit for arbitrary distinct real row offsets and distinct nonnegative integer column exponents.

This includes genuinely interior binary fibers with both permutation parities. When there are at least two rows incident to no red edge, even and odd permutations occur equally often. Nevertheless a precisely identified lower signed coefficient-moment is nonzero. The theorem is proved by a determinant update and an unmasked generalized Vandermonde leading term, without transferring the fiber to a support mask.

A useful example is `n=6`, red edges `(0,0),(1,1),(2,2)`, target `t=1`. Its 234 permutations split as 117 even and 117 odd, and their union contains every edge of `K₆,₆`. The nominal coefficients at degrees 15, 14, and 13 all vanish, but

    [λ^12] P₁(λ) = 6.

Thus neither parity imbalance nor an extremal/support-mask argument proves this example. The same mechanism extends to any nonsingular square red incidence block strictly smaller than the full graph.

## 1. Exact polynomial and general theorem

Let rows and columns be indexed by `0,…,n−1`, retaining their original order. Fix distinct real offsets `a_i` and distinct nonnegative integer exponents `e_j`. Write

    V_ij(λ) = (λ+a_i)^{e_j},
    E = Σ_j e_j,
    P_t(λ) = [z^t] det[z^{ρ(i,j)} V_ij(λ)].

Equivalently,

    P_t(λ) = Σ_{π: Σ_i ρ(i,π(i))=t} sgn(π) ∏_i (λ+a_i)^{e_{π(i)}}.

Suppose the red edges form a matching `M` of size `k<n`. Let `I,J` be its row and column sets, let `m=n−k`, and take all complements in original increasing index order. Let `ε(M)` be the sign of the permutation obtained by using the red matching on `I→J` and pairing the remaining rows with the remaining columns in increasing order. Define

    Δ(b₁,…,b_m) = ∏_{r<s}(b_s−b_r).

For every `0≤t≤k`,

    deg P_t = E − binom(m,2),

    [λ^{E−binom(m,2)}] P_t
      = (−1)^{k−t} binom(k,t) ε(M)
        Δ(a_{Iᶜ}) Δ(e_{Jᶜ}) / ∏_{q=0}^{m−1} q!.

Every factor on the right is nonzero. All these targets are therefore nonempty as well. The case `k=0` is the full uncolored generalized Vandermonde determinant.

The sign may also be written `ε(M)=(−1)^{ΣI+ΣJ} sgn(τ)`, where `τ` describes the red matching between the sorted row set `I` and sorted column set `J`.

## 2. Generalized translated-minor lemma

For `m` distinct offsets `b_r` and distinct nonnegative integer exponents `f_s`,

    Q(λ)=det[(λ+b_r)^{f_s}]

has exact degree `Σ_s f_s−binom(m,2)` and leading coefficient

    Δ(b) Δ(f) / ∏_{q=0}^{m−1} q!.

Proof. Set `u=1/λ` and factor `λ^{f_s}` from column `s`. Expand

    (1+b_r u)^{f_s} = Σ_{q≥0} b_r^q binom(f_s,q) u^q.

The expansions are finite. Cauchy–Binet expresses the remaining determinant as a sum over increasing lists `q₁<⋯<q_m` of nonnegative integers. The least possible sum of these integers is `binom(m,2)`, attained uniquely by `0,1,…,m−1`. Its coefficient is

    det[b_r^q]_{r,q=0,…,m−1} det[binom(f_s,q)]_{q,s=0,…,m−1}
      = Δ(b) Δ(f) / ∏_{q=0}^{m−1} q!.

The binomial-polynomial determinant identity follows from `deg binom(x,q)=q` and leading coefficient `1/q!`. The coefficient is nonzero by distinctness. This proves the lemma. In particular the leading-degree statement concerns an ordinary unmasked minor; it makes no assertion about the values of cofactors at individual roots.

## 3. Proper-matching proof

Let `R_ij=V_ij` on red edges and zero elsewhere. The colored matrix is

    V + (z−1)R.

Expand the determinant by the subset `S⊆M` of red entries chosen from the second summand. For `s=|S|`, its contribution is

    (z−1)^s × signed product of its s selected entries
                 × det V[unused rows, unused columns].

The selected factors are monic and their column exponents complement those in the minor. The preceding lemma therefore gives this term exact degree

    d_s = E − binom(n−s,2).

For `s<k<n`,

    d_{s+1}−d_s = n−s−1 > 0.

There is exactly one size-`k` subset, namely all red edges. It strictly dominates every smaller subset. Its leading coefficient is `ε(M)` times the complementary minor's leading coefficient. Finally, extracting `[z^t](z−1)^k` supplies `(−1)^{k−t}binom(k,t)`. This proves the formula, with no possible cancellation at the stated degree.

For `k=n`, the final two subset sizes have equal degree, so this strict-degree proof stops. That boundary does not itself give a counterexample. If all red edges form a perfect matching `σ`, their nominal leading coefficient is given separately by

    [z^t] det[J+(z−1)P_σ]
      = sgn(σ) [z^t](z−1)^{n−1}(z+n−1).

It is nonzero for every nonempty target (`t=n−1` is the sole impossible count). This elementary boundary is not needed for the lower-moment family.

## 4. Signed-moment formulation and explicit fully supported family

Every permutation product has nominal degree `E`. Define its coefficient-moments by

    T_r(π) = [u^r] ∏_i (1+a_i u)^{e_{π(i)}}
           = Σ_{h₀+⋯+h_{n−1}=r} ∏_i binom(e_{π(i)},h_i) a_i^{h_i}.

For `δ=binom(n−k,2)`, the theorem says

    Σ_{π∈F_t} sgn(π) T_r(π) = 0       for 0≤r<δ,

and the same sum at `r=δ` equals the explicit nonzero coefficient in Section 1. This is an exact signed-moment certificate, including arbitrarily long strings of canceled top coefficients as `n−k` grows.

For standard labels `a_i=e_i=i` and the first `k` diagonal edges red, the coefficient simplifies to

    (−1)^{k−t} binom(k,t) ∏_{q=0}^{n−k−1} q!.

### Parity balance

If `n−k≥2`, choose two rows with no red edge and swap their assigned columns. This is a fixed-point-free sign-reversing involution of every exact-count fiber. It preserves red count because all entries in both rows are blue. Thus both parities occur equally often whenever the fiber is nonempty. In particular the nominal leading coefficient `r=0` vanishes, as the formula also shows.

### Exact support and failure of mask representation

Assume `2≤k≤n−2` and `1≤t≤k−1`, with the first `k` diagonal positions red. Let `A={0,…,k−1}`.

- Every designated diagonal edge occurs: fix exactly `t` elements of `A` including the requested one, and put the remaining vertices into one cycle.
- Every other diagonal edge occurs: fix exactly `t` elements of `A` and the requested unmarked vertex, and put the remaining vertices into one cycle. There are at least two remaining vertices.
- For an off-diagonal edge `a→b`, the exact feasibility condition is `t≤k−|{a,b}∩A|`. Necessity holds because neither endpoint can then be a designated fixed point. For sufficiency, fix any `t` designated points avoiding the endpoints, then make one cycle through the remaining points with consecutive arc `a→b`.

Consequently the fiber's edge union is all `Kₙ,ₙ` for `1≤t≤k−2`. At the upper interior target `t=k−1`, it omits exactly the off-diagonal edges whose two endpoints are designated. The full-support condition must not be extended to that boundary.

Every interior fiber in this range fails support-mask representation, including the boundary. Its union contains every diagonal edge, hence contains the identity permutation at red count `k≠t`. Any mask admitting all fiber members would admit that identity as well. The extremal-face transfer is therefore unavailable. All targets `0,…,k` are feasible, so these really are interior targets.

### The cubic-moment example

For `n=6,k=3,t=1`, `E=15` and `δ=3`. Inclusion-exclusion counts the fiber as

    binom(3,1)(5!−2·4!+3!) = 234 = 117+117.

It has full 36-edge support. Write `S_ℓ(π)=Σ_i i^ℓ π(i)`. Then

    T₀=1,
    T₁=S₁,
    T₂=(S₁²−S₂)/2,
    T₃=(S₁³−3S₁S₂+2S₃)/6.

The first three signed sums are zero and the signed sum of `T₃` is `6`. Equivalently,

    Σ_{π∈F₁} sgn(π)(S₁³−3S₁S₂+2S₃) = 36.

The full polynomial, independently checked from the raw matrix, is

    P₁(λ) = 6λ^12 + 246λ^11 + 4566λ^10 + 47886λ^9
            + 308466λ^8 + 1267482λ^7 + 3344370λ^6
            + 5522298λ^5 + 5316288λ^4 + 2620392λ^3
            + 792384λ^2 + 670656λ + 357120.

## 5. Nonsingular square red-block extension

Suppose all red edges lie in `I×J`, where `|I|=|J|=k<n`, and the binary incidence block `B=(ρ(i,j))_{i∈I,j∈J}` is nonsingular. There may be intersecting red edges and multiple red perfect matchings. Then for every `0≤t≤k`,

    deg P_t = E−binom(n−k,2),

    [λ^{E−binom(n−k,2)}]P_t
      = (−1)^{ΣI+ΣJ+k−t} binom(k,t) det(B)
        Δ(a_{Iᶜ}) Δ(e_{Jᶜ}) / ∏_{q=0}^{n−k−1}q!.

Proof. The generalized Laplace expansion of `det(V+(z−1)R)` sums over equally sized selected row and column sets `I′,J′`:

    (z−1)^s (−1)^{ΣI′+ΣJ′} det R[I′,J′] det V[I′ᶜ,J′ᶜ].

Only sets inside `I,J` can contribute. For size `s<k`, each such term has degree at most `E−binom(n−s,2)`, strictly less than the proposed degree. At size `k`, the only selected pair is `(I,J)`. The leading coefficient of `det R[I,J]` at degree `Σ_{j∈J}e_j` is `det B`, since each entry is monic at its column's degree. This is nonzero by hypothesis. Apply the minor lemma to the complementary factor and extract `[z^t](z−1)^k`.

For example, take `n=6`, standard labels, and red block on rows/columns `0,1,2`

    B = [[1,1,0],
         [1,0,1],
         [0,1,1]],    det B = −2.

At `t=1`, the exact degree is 12 and leading coefficient is `−12`. The exact checker verifies this example independently. If `n−k≥2`, the same unmarked-row involution still proves parity balance.

## 6. Checks, source overlap, and stopping boundary

[check.py](check.py) is a self-contained Python-standard-library certificate for five fixed theorem examples and one singular-block boundary. It compares all polynomial coefficients from two implementations: direct permutation expansion and a raw bivariate recursive Laplace determinant. It verifies signs, generalized offsets and exponent gaps, a nonprincipal red matching, the single-unmarked-row boundary, the full-support correction, and the overlapping-edge block extension. These are checks of explicit examples, not an exhaustive search over colorings. Normal and `python -O` runs give identical [results.json](results.json); checks use explicit exceptions rather than removable assertions.

The same raw-matrix implementation also matched every coefficient of a separately generated five-case certificate; [root-crosscheck.json](root-crosscheck.json) records that comparison and its source hash.

[AUDIT.md](AUDIT.md) contains an independent proof audit. The reviewer independently checked the degree proof, parity involution, exact support scope, cofactor signs, and the nonsingular-block extension.

The primary definition is Yuefeng Du, [arXiv:2604.01571v3, Definitions 2.1–2.2](https://arxiv.org/html/2604.01571v3#S2.SS2). A bounded overlap check used the locally preserved source text, including Section 2.4 and Section 4.2. Remark 2.6 already discusses the perfect-red-matching feasible counts; Theorem 2.10 covers all nonempty subsets only through order four; the manuscript's general ASNC claim would include the present standard-label family. This note supplies a self-contained sufficient-family proof and explicit first-nonzero coefficient. The inspected source passages do not supply this exact proper-matching/block formula. This is not a comprehensive literature search or any assertion of novelty, and the proof does not rely on the source's disputed global arguments.

The complete underlying graph is essential to the proof: the complementary minors are full generalized Vandermonde matrices. Arbitrary absent blue edges would replace them with masked minors and invalidate the stated degree calculation.

The next clear condition is a singular square red incidence block, or red support that cannot be confined to one proper nonsingular square block. In the singular-block case the displayed top coefficient cancels. One would need to compare the lower degree of the full red-block determinant against all smaller selected row/column terms, and then control any tied leading sums. Singularity does not imply a zero exact-count polynomial. For example, an all-red `2×2` block in `K₄,₄` has its `t=1` polynomial `−2λ⁴−12λ³−38λ²−60λ−24`, of degree 4 with leading coefficient `−2`, rather than the nonsingular-block degree 5. No general resolution of that next condition is claimed here.

All work was local. No remote edits, publication, or downloaded executable code were used. The requested well-scoped candidate succeeded, and this investigation stops at the stated boundary.
