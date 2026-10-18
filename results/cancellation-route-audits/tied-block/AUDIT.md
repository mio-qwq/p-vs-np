# Independent audit: tied squares and rectangular cancellation

18 October 2026. Read-only review of `PROOF.md`, `RECTANGULAR_OBSTRUCTION.md`, and the prior square-block addendum. The proof files were not modified. All checks below were written independently for this audit; no existing checkpoint code was executed or imported. No remote writes or publication.

## Verdict

The substantive claims reviewed are correct under the stated distinct-label hypotheses. In particular:

- The exact square-complement identity settles the tied majority-square boundary and extends the earlier small-square theorem to every square block.
- The remainder-matrix quotient has the stated sign, `(-1)^(sum J + binom(s-r,2))`.
- The weighted column identity has the stated difference `e₂(Y)−e₂(X)`, with no missing minus sign.
- For the specified standard `n=8`, `I={0,1,2}`, `J={0,1,6,7}` example, the candidate degree-15 coefficient vanishes, and the exact degree-14 coefficient is `967680(z−1)^3`.
- Every target `t=0,1,2,3` is feasible and has a nonzero polynomial of exact degree 14. This is a counterexample to a universal *maximal-size rectangular leading-sum nonvanishing* assertion. It is not an ASNC counterexample and does not establish general ASNC.

One small domain clarification is advisable: state `r≥1` where row means and the first-correction formula are used, and `m≥1` in the two-coefficient minor lemma. Empty blocks are trivial separate cases. The main examples and all substantive conclusions already satisfy these restrictions.

## 1. Square-block proof

For an arbitrary weighted complete bipartite matrix, let `t` count permutation edges in `I×J` and `b` count those in `Iᶜ×Jᶜ`. The four block counts give

    t−b = |I|+|J|−n.

Thus for `|I|=|J|=k>n/2`, the identity

    F_{I,J}(z,λ) = z^(2k−n) F_{Iᶜ,Jᶜ}(z,λ)

is exact term by term, including permutation signs and all edge weights. The complementary block has size `n−k<n/2`, so the prior small-square theorem applies without a tied-leading-term issue. The parity of the complementary cofactor sign is unchanged. This verifies the unified formula in `PROOF.md`, including its feasible target interval. The endpoint cases `k=0,n` use the empty determinant convention and are consistent.

The separate interpolation proof also checks out. If `α` is the number of indices of `I` below `p`, the ratio of the summand in (★) to its right-hand side has sign

    (-1)^p (-1)^(k−1−p+α) / (-1)^(k−1−α) = 1.

Its unsigned algebraic ratio is `U(x_p)/Q′(x_p)`. Since `U` is monic of degree `k−1`, Lagrange interpolation makes the sum equal to one. This argument uses original index order and does not require the values themselves to be increasing. The factorization of the tied row and column sums, and hence `A_{k−1}=C`, is valid.

The generalized-minor degree formula has no hidden negative-degree problem: any set of `m` distinct nonnegative integer exponents has sum at least `binom(m,2)`. Distinct real offsets suffice for the nonzero Vandermonde factors. No positivity assumption is used.

## 2. Remainder quotient: determinant and sign

Write `s=|J|`, `m=n−s`, `p=s−r`, `q=m−r`. The hypotheses `r<s` and `r+s≤n` imply `p>0` and `q≥0`. The matrix `K` is square: both its number of rows and its number of columns are `n−2r=p+q`.

For the displayed matrix `M`, Laplace expansion in its first `r` rows gives

    S = (-1)^binom(r,2) det M.

Moving columns into the order `J,Jᶜ` contributes `(-1)^(sum J−binom(s,2))`. Right multiplication by the two inverse evaluation Vandermondes divides the determinant by `Δ(X)Δ(Y)`, and correctly converts evaluated polynomials into remainder coefficients. After subtracting the supported top rows from the corresponding lower rows, the two eliminated identity blocks have column degrees `0,…,r−1` on their respective sides.

Moving the second identity block past the first block's `p` remaining columns contributes `(-1)^(rp)`. Therefore the total exponent is

    binom(r,2) + sum J − binom(s,2) + r(s−r)
      ≡ sum J + binom(p,2)  (mod 2).

This establishes equation (1) with exactly its stated sign. All inverses used in this proof exist because the exponent labels are distinct. Multiplying through gives a polynomial identity, so the proof does not rely on ordering or positivity of the labels.

Each entry of `K` in row degree `h` and column degree `ℓ` is homogeneous of degree `h−ℓ` in the roots, with a zero entry when that degree is negative. Every nonzero determinant term therefore has total degree

    sum(h) − sum(ℓ) = pq.

The homogeneous-degree assertion is correct. If `q=0`, all relevant powers have degree below `s`, and `K` is literally the identity. The saturated-rectangle formula and the target-reversal reduction to a square both follow as stated.

## 3. Weighted column identity

For `n=2r+2`, `s=m=r+1`, replace the supported row degrees by

    L = {0,…,r−2,r}.

The corresponding alternant on a selected `r`-set is `Δ(e_B) sum(e_B)`, so its determinant produces the weighted sum `T`.

To repeat the elimination, move the lower degree-`r` row before degree `r−1`. This is one row interchange. Within each of the two column blocks, moving degree `r` before degree `r−1` produces two column interchanges in total, whose signs cancel. Moving the second eliminated identity block across the one remaining first-block column contributes the same `(-1)^r` as in the unweighted calculation.

The remaining columns both have degree `r−1`; the remaining row degrees are `r−1,r+1`. Their matrix is

    [[1, 1], [−e₂(X), −e₂(Y)]].

Its determinant is `e₂(X)−e₂(Y)`. The extra row interchange reverses this, giving

    T = (-1)^sum J Δ(X)Δ(Y) [e₂(Y)−e₂(X)].

Thus equation (3) is correct. It holds without imposing equal first sums. The argument covers `r=1`, where `L={1}` and the same single interchange occurs.

## 4. First correction after leading cancellation

For a nonempty translated minor of size `m`, Cauchy–Binet gives the minimal degree list `0,…,m−1` and the unique next list `0,…,m−2,m`. The offset alternant ratio for the latter is `sum b`. The binomial-coefficient alternant ratio is

    (sum f − binom(m,2))/m.

One way to check its constant is to eliminate all lower rows from `binom(f,m)`: its two surviving highest coefficients are those of `(f^m−binom(m,2) f^(m−1))/m!`, while the original last-row scale is `1/(m−1)!`. This supplies the factor `1/m` and the subtraction `binom(m,2)`.

Consequently the displayed first-correction lemma is correct for arbitrary distinct nonnegative integer exponents, including unsorted or gapped exponent lists. If the minor degree is zero, its putative next coefficient is zero because the multiplying degree factor is zero.

For a fixed selected column set `B`, the product of the two minor expansions has correction factor

    mean(a_I) [sum(e_B)−binom(r,2)]
      + mean(a_Iᶜ) [E−sum(e_B)−binom(n−r,2)].

Summing against the signed exponent Vandermondes makes the constant part a multiple of `S` and leaves `(mean(a_I)−mean(a_Iᶜ))T` when `S=0`. In the equal-halves family, the next smaller Laplace size has degree `D−3`, so it cannot contribute at `D−1`. This proves equation (4), including its sign.

For standard `n=8`:

    sum X = sum Y = 14,
    Δ(X)Δ(Y) = 1260·12 = 15120,
    e₂(Y)−e₂(X) = 71−55 = 16,
    T = 241920,
    A = −1,
    mean(a_I)−mean(a_Iᶜ) = 1−5 = −4.

Hence the coefficient is `967680(z−1)^3`, with target coefficients

    −967680, 2903040, −2903040, 967680.

For the specified gapped `n=6` example, the signed Vandermonde product is `−288`, the second-elementary difference is `7`, `A=−1`, and the mean difference is `−3`. These give `−6048(z−1)^2`, as claimed.

## 5. Independent exact verification

The new standalone `audit_exact_checks.py` uses only Python's standard library and exact rational arithmetic. It does not import or execute the existing checker.

It passed:

- 125 independently generated fixed-seed quotient-identity cases through `n=12`, including unsorted exponents and saturated rectangles.
- 55 weighted-identity cases, including `r=1` and unsorted labels.
- 15 translated-minor checks of both degree and the first two coefficients, through minor size 5, with unsorted rational offsets and unsorted nonnegative integer exponents.
- A full independent reconstruction of the standard `n=8` bivariate determinant using exact numeric determinant evaluation and polynomial interpolation, a method different from both signed-permutation enumeration and a subset Laplace recurrence.

The last check evaluates at `λ=0,…,28` and `z=0,…,3`. The raw determinant has degree at most 28 in `λ` because every permutation uses all exponents, and at most 3 in `z` because only three rows contain red edges. These degree bounds make the interpolation complete, rather than a sample-based inference. It recovers exact degree 14 in all four target fibers. All 58 nonzero bivariate coefficients independently recovered this way also agree with the recorded `results.json`.

Normal Python and `python -O` produce identical audit output. The check uses explicit exception-raising conditions, not removable assertions.

Files:

- `audit_exact_checks.py`: independent checker.
- `audit-results.json`: complete recovered standard `n=8` fibers and check counts.
- `audit-results-optimized.json`: identical optimized-run output.

The two result files have SHA-256:

    0fcfdb2ed1f01cc30a1b9c274e2693d84713a01d108ce6fc1840bc87bc601f35

## 6. Scope boundaries

The hypotheses are essential to the claims being made: distinct offsets and exponents, nonnegative integer exponents for polynomial degree statements, the complete underlying bipartite graph, and the specified all-red rectangular support. The audit does not extend them to general red incidence patterns.

For a rectangle satisfying `r+s≤n`, all target counts `0,…,r` are combinatorially feasible. In the examples their exact-count polynomials have explicitly nonzero next coefficients. The canceled degree-`D` term therefore cannot be reported as an identically zero fiber. Additional cancellation when row means or second elementary sums agree remains outside the proved nonvanishing conclusion. No historical novelty, general rectangular nonvanishing theorem, general ASNC proof or counterexample, or complexity consequence is established by this checkpoint.
