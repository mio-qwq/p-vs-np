# Four-row masked determinants: two auxiliary extensions

Research checkpoint, 18 October 2026. Python 3.10 or later. The primary checkers and boundary controls use only the standard library; the separate tail-gap audit uses SymPy 1.14.0.

- [One-tail-gap and separated-largest-exponent theorems](monic-four-gapped/REPORT.md): every binary 4-by-4 mask with a perfect matching gives a nonzero shifted-power determinant for distinct complex offsets and exponents `(d,d+1,d+2,d+m)` with `d>=0, m>=4`. More generally, exponents `(d,d+p,d+q,d+r)` are covered when `0<p<q<r` and `r>=3(p+q+1)`. The infinite argument uses Hermite interpolation; eight finite symbolic classifications cover the remaining tail cases `m=4,...,11`.
- [One partial row and three full rows](monic-one-partial-row/README.md): any nonempty subset in one row, with all other entries retained, gives a nonzero determinant for all distinct nonnegative integer exponents and distinct real offsets. A complete proof and 38 exact coefficientwise identities cover all 15 nonempty subsets, including the exceptional symmetric exponent pairs.

These are bounded auxiliary determinant results. General gapped four-row masks, arbitrary sizes, the color-conditioned ASNC claim, and P versus NP remain unresolved. No novelty, human peer review, or Lean verification is claimed. The separate audits are AI-assisted; symbolic checks support the stated proof components and do not replace the infinite structural arguments.

The complex-offset theorem starts at `m=4`. The partial-row theorem requires real offsets: an exact cube-root-of-unity counterexample at exponents `(0,1,2,3)` shows why the stronger complex-field extension is false. Both limitations are exercised as negative controls.

## Reproduce

From the repository root:

    python3 -m pip install -r results/requirements-gapped-20261018.txt
    python3 results/verify-gapped-20261018.py
    python3 -O results/verify-gapped-20261018.py

The verifier checks every package-source hash, creates a clean temporary copy, regenerates omitted certificate data, verifies its frozen hash, and runs each exact checker and its negative controls under both ordinary and optimized Python. It also tests manifest corruption. All generated certificate and corruption files stay in temporary storage. The expanded certificate, caches, exploratory scans, and duplicated transient logs are excluded from the source tree and ZIP.

`manifest-gapped-20261018.json` identifies every packaged source file except itself. `verification-gapped-20261018.json` records the successful publication verification. Each result's `PROVENANCE.json` distinguishes original source hashes from publication-edited prose or tooling.

This package only adds new paths. The earlier [consecutive-exponent result and affine-hull obstruction](README-20261018.md) are retained unchanged in the repository; they are not duplicated in this compact extension archive. When reading the extension ZIP alone, that earlier link is intentionally external to its contents. The earlier source checkpoint is [commit e3089e6](https://github.com/mio-qwq/p-vs-np/tree/e3089e62f9cc98ee39dfb2186beccd26c11ac7cf/results).
