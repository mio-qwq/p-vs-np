# Independent audit: a complete square red block

18 October 2026. Local proof audit and exact, standard-library checks. The earlier matching/nonsingular-block package was read but not modified.

## Verdict

**The proposed extension is correct**, including its sign, degree, and the full range `0 ≤ k ≤ floor(n/2)` and `0 ≤ t ≤ k`. The endpoint `2k=n` is included: its last degree gap is one, not zero. The statement resolves the all-red `2×2` block example left at the boundary of the earlier note. It does not resolve arbitrary singular red-incidence blocks.

Eight independent exact examples, covering twenty target fibers, agree coefficient-by-coefficient between direct permutation expansion and the generalized Laplace expansion. Every predicted degree and leading coefficient agrees. Both ordinary and `python -O` runs pass, with byte-identical outputs.

## Precise statement

Let `n ≥ 1`. Index the rows and columns by `0,…,n−1`, always retaining their original increasing index order within selected sets. Let the real offsets `a_i` be pairwise distinct, and let the exponents `e_j` be pairwise distinct nonnegative integers. Set

    V_ij(λ) = (λ+a_i)^{e_j},       E = Σ_j e_j.

Fix row and column sets `I,J` of the same cardinality `k`, where `0 ≤ k ≤ floor(n/2)`. Color **exactly all** entries in `I×J` red and all other entries blue. Put `R_ij=V_ij` on that block and `R_ij=0` elsewhere, and define

    P_t(λ) = [z^t] det(V(λ)+(z−1)R(λ)).

For a sequence `b` in its specified order, write `Δ(b)=∏_{r<s}(b_s−b_r)`. Empty determinants, Vandermonde products, and products of factorials are one. Complements are taken in the full index set. For every `t=0,…,k`,

    deg P_t = D = E − binom(k,2) − binom(n−k,2),

    [λ^D]P_t = (−1)^{ΣI+ΣJ+k−t} binom(k,t)
                 × Δ(a_I)Δ(e_J) / ∏_{r=0}^{k−1}r!
                 × Δ(a_Iᶜ)Δ(e_Jᶜ) / ∏_{r=0}^{n−k−1}r!.

The coefficient is nonzero. In particular, all the stated exact-count fibers are nonempty.

For `k≥2`, the binary red-incidence block is the singular all-ones matrix. This does **not** make its weighted polynomial block `V[I,J]` singular: its determinant has the nonzero translated-Vandermonde leading coefficient used below. This distinction is the mechanism that repairs the earlier nominal-leading-coefficient cancellation.

## Proof audit

### 1. Full translated-minor degree and sign

For any `m` distinct offsets `b_r` and distinct nonnegative integer exponents `f_s`, the full minor

    Q(λ)=det[(λ+b_r)^{f_s}]

has exact degree `Σf_s−binom(m,2)` and leading coefficient

    Δ(b)Δ(f) / ∏_{q=0}^{m−1}q!.

Indeed, factor `λ^{f_s}` from each column and put `u=1/λ`. Cauchy–Binet applied to the finite expansions `(1+b_ru)^{f_s}` has its first possible power at the unique increasing index list `0,1,…,m−1`. Its coefficient is the product of the usual Vandermonde determinant in `b` and the determinant with entries `binom(f_s,q)`. The latter is `Δ(f)/∏q!`: row `q` is a polynomial of degree `q` and leading coefficient `1/q!`. Both Vandermonde factors are nonzero.

No increasing numerical order of the labels themselves is assumed. Keeping the original row and column index orders in the Vandermonde factors is what preserves the correct sign. The case `m=0` follows by the empty-product convention.

### 2. The generalized Laplace identity

For any square matrices `A,B`, multilinearity gives

    det(A+xB)
      = Σ_{S,T: |S|=|T|=s, 0≤s≤n}
          x^s (−1)^{ΣS+ΣT} det B[S,T] det A[Sᶜ,Tᶜ].

There is no extra factorial or binomial factor here. One can derive it by choosing the rows that use `B`, then expanding the chosen-row matrix along those rows. With `A=V`, `B=R`, and `x=z−1`, any nonzero selected minor must have `S⊆I` and `T⊆J`. If a selected row or column falls outside these sets, that minor has a zero row or column. In particular every `s>k` contribution is zero.

For `S⊆I` and `T⊆J`, the complete-block hypothesis gives exactly

    R[S,T]=V[S,T].

Both this selected minor and its complementary minor are full translated generalized Vandermonde matrices. Their polynomial degrees therefore add to

    d_s = (Σ_{j∈T}e_j−binom(s,2))
          +(Σ_{j∉T}e_j−binom(n−s,2))
        = E−binom(s,2)−binom(n−s,2).

Each such summand has that **exact** degree. This exactness need not hold after summing all pairs at a fixed smaller size, but no such assertion is needed.

### 3. Strict dominance and uniqueness

For every `s=0,…,k−1`,

    d_{s+1}−d_s = n−2s−1 ≥ n−2k+1 ≥ 1.

Thus size `k` has strictly larger degree than every smaller size. At size `k`, there is precisely one allowed pair, `S=I,T=J`. Its signed leading coefficient is

    (−1)^{ΣI+ΣJ}
      Δ(a_I)Δ(e_J) / ∏_{r<k}r!
      Δ(a_Iᶜ)Δ(e_Jᶜ) / ∏_{r<n−k}r!.

It is nonzero. Since `[z^t](z−1)^k=(−1)^{k−t}binom(k,t)`, every `t=0,…,k` receives a nonzero contribution at this degree, with no smaller-size term able to cancel it. This proves the statement.

### 4. Indexing and boundary checks

- Switching from zero-based to one-based row and column indices changes `ΣI+ΣJ` by `2k`, so the sign is unchanged.
- `k=0` is the uncolored full determinant, with `t=0` only.
- `n=2,k=1` is valid; the formula has degree `E` and opposite leading signs at targets zero and one.
- When `n=2k`, the last gap is `d_k−d_{k−1}=1`. The balanced-block boundary is fully covered.
- The range cannot simply be enlarged by this proof. When `n=2m+1` and `k=m+1`, `d_m=d_{m+1}`; when `n=2m` and `k>m`, the sequence decreases after `s=m`. Moreover, for `k>n/2`, every permutation uses at least `2k−n` red entries, so claiming nonzero polynomials for all `t=0,…,k` would already be false.
- The square block and complete underlying graph are essential to this precise argument. Missing red entries destroy the selected full-minor calculation; missing blue entries destroy the complementary full-minor calculation.

## Consequences within the proved scope

For nominal coefficient moments

    T_r(π)=[u^r]∏_i(1+a_i u)^{e_{π(i)}},

the first nonzero signed moment occurs at

    δ = binom(k,2)+binom(n−k,2).

All earlier signed moments vanish; the moment at `δ` equals the displayed leading coefficient. This follows directly from the exact degree, without any extra combinatorial assumption.

If `n−k≥2`, swapping the assigned columns of two rows outside `I` preserves the red count and reverses permutation parity. Thus each fiber is parity-balanced despite its nonzero polynomial. This includes every admissible positive `k` once `n≥3`.

For standard labels `a_i=e_i=i` and the leading principal red block `I=J={0,…,k−1}`, the formula simplifies to

    deg P_t = k(n−k),

    [λ^{k(n−k)}]P_t
      = (−1)^{k−t}binom(k,t)
        (∏_{q=0}^{k−1}q!)(∏_{q=0}^{n−k−1}q!).

## Exact examples and independent checker

[check.py](check.py) was written fresh for this audit and uses only the Python standard library. It computes every coefficient twice:

1. Directly enumerate all permutations, classify each by its red count, multiply the entry polynomials, and sum with its permutation sign.
2. Independently compute all relevant full minors by recursive row-Laplace expansion, then assemble the generalized selected-set expansion and extract the powers of `z`.

All computations use exact rational arithmetic. The checker verifies every individual summand degree, every target polynomial equality, the theorem's exact degree and leading coefficient, and parity balance whenever at least two unmarked rows are available. Its failures raise explicit exceptions, so optimization cannot erase checks.

| Example | `n,k` | Exact degree | Leading coefficients in target order |
|---|---:|---:|---|
| Standard leading principal `2×2` block | `4,2` | `4` | `1, −2, 1` |
| Odd order, nonprincipal block, reordered labels and exponent gaps | `5,2` | `11` | `2268, −4536, 2268` |
| Standard leading principal `3×3` block | `6,3` | `9` | `−4, 12, −12, 4` |
| Even order, nonprincipal block strictly below half-size | `6,2` | `15` | `−2822400, 5644800, −2822400` |
| Rational offsets, nonprincipal block, reordered exponents | `4,2` | `7` | `−275/12, 275/6, −275/12` |
| Empty red block with exponent gaps | `4,0` | `2` | `2400` |
| Single red edge, nonprincipal | `2,1` | `5` | `1, −1` |
| Order one, empty red block | `1,0` | `2` | `1` |

Exact labels, counts of even/odd permutations, full target coefficient lists, and all selected-set summand degrees appear in [results.json](results.json).

In particular, the first example reproduces precisely

    P_1(λ)=−2λ⁴−12λ³−38λ²−60λ−24.

Here `E=6`, `D=6−1−1=4`, both Vandermonde/factorial ratios are one, and `ΣI+ΣJ=2`. The coefficient is therefore `(−1)^{2+2−1}binom(2,1)=−2`.

Reproduction commands from this directory:

    python check.py results.json > normal.log
    python -O check.py optimized-results.json > optimized.log
    cmp results.json optimized-results.json
    cmp normal.log optimized.log

Both runs passed: eight cases, twenty target fibers. This is an exact check of examples, not an exhaustive classification of red colorings. The proof supplies the arbitrary-order result.

## Provenance and limits

The frozen source report was [the earlier report](../binary-fiber/REPORT.md), SHA-256 `7a7caa58432f1be58fe655e19dd17c319011f34b7660dd2dfb584de853a570f1`. Its existing `SHA256SUMS` verification passed after the audit checks. All audit files were written to this separate directory. No remote state was changed.

This audit validates a specific sufficient family. It makes no claim about arbitrary singular incidence blocks, arbitrary absent edges, general ASNC, P versus NP, or historical novelty. No external literature search was needed for the stated algebraic audit, and none was performed.
