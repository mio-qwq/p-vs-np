# Arbitrary fixed-depth failure of conditioned affine-hull tests

For every fixed integer depth `d≥0`, there is an infinite family of binary-vector-labeled complete bipartite matching instances with **no target-zero perfect matching**, even though the labels of the perfect matchings extending **every partial matching of at most d edges** have full affine hull. Label dimension is `k=O_d(log N)` on `K_(N,N)`.

The self-contained general proof is in [`general-theorem.md`](general-theorem.md), with an exact-file independent audit in [`AUDIT.md`](AUDIT.md). A sufficient parameter choice is

    t = ceil((d+1)/2), L = ceil(log₂(2t)), m ≥ 2L, N = 2^m,
    v_x = (x,x³,…,x^(2t−1)) ∈ GF(N)^t ≅ F₂^(tm).

Give each of the first `2t` columns the corresponding row label `v_x`, and every other column label zero. A Vandermonde argument excludes zero sums on `2t` distinct rows. A disjoint-Frobenius-orbit argument and an elementary Boolean-polynomial support bound show that removing any `2t−1` rows preserves full affine span. A subset-exchange lemma transfers this to exact matching extensions. The audit also gives an optional Weil-bound proof under the slightly sharper sufficient condition `N≥4t²`.

This closes only the proposed completeness route based on a conjunction of all fixed-depth conditioned affine-hull tests. It makes no claim about stronger pruning rules, fixed label dimension, P versus NP, or novelty of the finite-field and coding-theoretic ingredients.

## A small exact depth-five obstruction

Take `t=3`, `m=5`, `N=32`, and

    F = F₂[X]/(X⁵+X²+1),
    v_x = (x,x³,x⁵) ∈ F³ ≅ F₂¹⁵.

Use six special columns, labeled by `v_x`; all other columns have zero labels. All 32² edges are present, and the target is zero.

Field elements use the polynomial-basis integer encoding in which the coefficient of `X^i` is bit `i`. A row label is encoded as

    x | (x³ << 5) | (x⁵ << 10).

The powers are computed in the field. The modulus is integer `37` (`0b100101`). Its irreducibility is checked exactly by trial division by every monic polynomial of degree at most two, which suffices for a degree-five polynomial.

### No accepted perfect matching

Each perfect matching assigns six distinct rows to the six special columns. Their label sum cannot be zero by the general Vandermonde argument. Independently, the checker enumerates all `C(32,6)=906,192` row sets and verifies that none has zero total label. It also checks that all `C(32,3)=4,960` triple sums are distinct, an independent collision certificate against any nonempty zero even subset of size at most six.

### Robust full affine span

For all masks `a∈F₂¹⁵` and constants `c∈F₂`, enumerate the 65,536 ambient affine functionals `v↦a·v+c`. Their exact weight histogram on the 32 row labels is:

| Weight | Count |
| ---: | ---: |
| 0 | 1 |
| 8 | 620 |
| 12 | 13,888 |
| 16 | 36,518 |
| 20 | 13,888 |
| 24 | 620 |
| 32 | 1 |

The unique zero-weight functional is the ambient zero functional. Every nonzero affine functional is supported on at least eight rows. Consequently, removing any at most seven rows leaves full affine span `F₂¹⁵`: otherwise a nonzero ambient affine functional vanishing on all survivors would have support at most seven.

### Every partial matching through depth five passes

Fix a partial matching `P` of `h≤5` edges, of which `s` lie in special columns. Let `D` be its used rows and `b` its fixed label sum. Then exactly `r=6−s` special columns remain, and the exact attainable label set of perfect extensions is

    { b + Σ_(x∈R) v_x : R⊆F\D, |R|=r }.

Both inclusions hold: every perfect extension chooses such rows, and every such choice extends because all edges are present. There are `32−h≥27` surviving rows and `1≤r≤6`, so `r` is strictly smaller than the number of surviving rows.

The surviving labels have full affine span by the weight certificate. For each pair of surviving rows `i,j`, choose `r−1` other rows. The two valid `r`-subsets obtained by adding `i` or `j` have sum difference `v_i+v_j`. These differences span the whole ambient space, so the `r`-subset sums, and their translate by `b`, have full affine hull. In particular, every conditioned hull contains target zero even though no perfect matching attains it.

The finite example is deliberately below the sufficient general threshold (`m≥6` for `t=3`). Exact enumeration certifies its stronger behavior; it is not inferred from an inapplicable asymptotic bound.

## Negative controls and exact boundaries

The checker also verifies:

- The alternate modulus `X⁵+X+1` is reducible and is rejected.
- Dropping the fifth-power coordinate creates a zero six-subset on rows `{0,1,2,6,16,21}`.
- Illegal repeated choices `{0,0,1,1,2,2}` have zero label sum; distinctness is essential.
- Fixing rows `0,…,5` to all six special columns gives singleton conditioned hull `{27233}`, which rejects zero. Thus the claimed matching-conditioning boundary is five, even though row-deletion robustness extends to seven.
- The affine functional with mask `1176` and constant `1` is supported on `{0,5,8,13,16,21,24,29}`. Removing those eight rows drops affine rank to 14. The seven-deletion guarantee is sharp.
- Over `GF(16)` using `X⁴+X+1`, `Tr(x⁵)` vanishes on every row and `(x,x³,x⁵)` has affine rank 10 rather than 12. Field-size hypotheses really matter.

## Reproduce

Run ordinary Python 3.10 or later, without `-O`:

    python3 check_depth_five.py

The checker uses only the standard library and deterministic exact arithmetic. It regenerates the row labels, field checks, subset sums, affine-functional histogram, and negative controls. No perfect matchings are enumerated. `certificate.json` is the saved output; the script does not trust it as input.

The only externally sourced analytic fact is the optional Weil bound in `AUDIT.md`. The main theorem and finite verification do not require it.

## Publication status

This is an auxiliary obstruction to one fixed-depth relaxation, not a solution of P versus NP. Novelty has not been established. The independent audit was AI-assisted and is not human peer review or proof-assistant verification. The general derivation and both checkers are preserved byte-for-byte; the audit has only editorial provenance/path changes. See `PROVENANCE.json`. The derivation is a historical frozen note; the subsequent audit supplies its verification status.

A second independent finite implementation is `independent_check.py`; run it with ordinary Python without `-O`. Its output is `independent_output.json`.
