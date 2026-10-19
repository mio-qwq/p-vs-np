# Equal-halves rectangular moment hierarchy

18 October 2026. An additive mathematical checkpoint for `mio-qwq/p-vs-np`.

## What is proved

Let `n=2r+2`, `r≥1`, and color exactly `I×J` red, where `|I|=r` and `|J|=r+1`. Row offsets are distinct real numbers and exponents are distinct nonnegative integers. Let `k` be the first differing positive power sum between the two equally sized exponent classes. Then `1≤k≤r+1`.

Writing `D=Σe−binom(r,2)−binom(r+2,2)`, all coefficients above degree `D−k+1` vanish. The coefficient at that degree is

    A K (Δp_k/k) q_(k−1) (z−1)^r,

with the signed Vandermonde factors `A,K` and offset factor `q` defined in [the proof](PROOF.md). If `q_(k−1)≠0`, every feasible fiber `t=0,…,r` has exact degree `D−k+1`, with the corresponding signed binomial leading coefficient.

The offset factor is always nonzero when the selected and complementary row-offset blocks are strictly separated. For standard rows `a_i=i`, `I={0,…,r−1}`, it has the closed form `q_l=(r+1)^l/l!`. Thus this family, including source-standard row labels, has nonzero fibers for every distinct exponent labeling. The proof includes a rank argument excluding all interfering smaller Laplace layers.

For arbitrary distinct offsets, `q` can vanish. Fully checked real and integer examples drop further in degree while their fibers remain nonzero. This result does not resolve arbitrary binary colorings, general ASNC, or P versus NP. No historical-novelty, human-peer-review, or proof-assistant-verification claim is made.

## Read

1. [Status and scope](STATUS.md)
2. [Complete theorem and proof](PROOF.md)
3. [Independent mathematical audit](audit/AUDIT.md)
4. [Frozen producer checkpoint](CHECKPOINT.md)
5. [Release notes](RELEASE_NOTES.md) and [provenance](PROVENANCE.json)

The proof is byte-preserved at its independently audited SHA-256, `f796d745708ca05d4f69e3c55949cc053ab8b6c8561dc07cc090c5838556183f`. All five original checkers are byte-preserved. Audit means a separate AI-assisted derivation/review and independent exact algorithms, not a formal proof kernel or human peer review.

## Reproduce everything

From this directory, using Python 3.10 or later:

```text
python -B verify.py
python -B -O verify.py
```

Both commands rerun all included exact checks using only the Python standard library:

- Seven producer Cauchy–Binet examples through `n=16`, including first-differing moment `k=5` and smaller-layer cancellation checks.
- The complete irrational-offset cancellation polynomial by all 720 signed permutations over `Q(√2)`.
- Fifteen independently reconstructed complete bivariate determinants through `n=10`, `k=5`, using integer Bareiss elimination and exact interpolation; every coefficient and the sharpened bound in each Laplace layer are checked.
- Ninety affine row families through `r=30`, checking every `0≤l≤r` in the closed form.
- Two source-level negative controls: a reversed candidate sign and a wrong third-order factorial must be rejected, including under `python -O`.
- Altered numerical certificates, a modified file, a missing file, an unexpected file, and a changed manifest must each be rejected.

The aggregate verifies the fixed file inventory, hashes, provenance, internal links, and equality to fresh recomputation. It invokes each original checker in a temporary copy, so the frozen package remains unchanged. Running original checkers directly rewrites their result files; use a disposable copy for those commands. No network access, SymPy, numerical tolerance, random sampling, downloaded code, or vendored binaries are needed.

Finite tests corroborate the general algebraic proof; they are not an enumeration of all colorings. [verification.json](verification.json) records the protocol. The outer publication-stage manifest and receipts record actual normal/optimized runs from both the stage and fresh ZIP extractions.

## Inventory and publication

[manifest.json](manifest.json) and [SHA256SUMS](SHA256SUMS) are the canonical packaged inventory. [PROVENANCE.json](PROVENANCE.json) records source hashes and the limited editorial changes. [audit/SOURCE_MANIFEST.json](audit/SOURCE_MANIFEST.json) preserves the original audit inventory, including intentionally omitted duplicate logs; its historical source paths are provenance metadata, not dependencies.

The compact deterministic ZIP contains exactly the additive tree under `results/rectangular-moment-hierarchy/`. No existing repository file is part of the proposed change. This package was prepared locally without remote writes. Publication requires a fresh remote base and destination-absence check, after the preceding five-row release. The staging manifest records that precondition without pinning a stale base commit.
