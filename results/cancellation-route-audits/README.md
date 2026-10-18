# Cancellation-route audits

18 October 2026. A compact, additive research checkpoint for `mio-qwq/p-vs-np`, prepared against expected base `b4841433f732c0b11bf6fdff5a74ec8e251cb87b`.

## What this establishes

- **Square-block reductions:** the tied majority-square case has top coefficient `C z(z−1)^(k−1)`. Exact complement identities reduce larger square blocks to smaller ones, completing the square-block family when combined with the included prior small-square result.
- **Rectangular route obstruction:** for standard ordered labels at `n=8`, red block `I={0,1,2}`, `J={0,1,6,7}`, the candidate degree-15 coefficient cancels. The next coefficient is exactly `967680(z−1)^3` at degree 14. All four feasible target polynomials remain nonzero. This disproves universal nonvanishing of the maximal-size rectangular Laplace leading sum, not ASNC.
- **Five-row necessary conditions:** with four full rows and one partial row, identically zero would force two or three retained columns, symmetric noncentral offsets `±u,±v`, explicit exponent equations and a strict real-offset ratio constraint. These conditions are not sufficient and do not complete the subclass.
- **Exact failed candidates:** the engineered `(0,3,5,8,9)` three-retained-column construction has a nonzero coefficient after its deliberately canceled leading term. The later `(0,5,9,12,14)` two-retained-column candidate also fails exactly at moment 12, giving degree 28. The audit additionally exhausts the justified `d=7` arithmetic branch within this subclass.

This is route-obstruction and necessary-condition research. It exhibits no identically zero ASNC fiber polynomial, proves neither general ASNC nor a full five-row theorem, and has no P-versus-NP consequence. It makes no historical-novelty, human-peer-review, or proof-assistant-verification claim.

## Read in this order

1. [Current status and historical wording](STATUS.md).
2. [Square complement and tied-sum proof](tied-block/PROOF.md), with the [prior small-square background](tied-block/SMALL_SQUARE_BACKGROUND.md).
3. [Rectangular quotient and next-coefficient proof](tied-block/RECTANGULAR_OBSTRUCTION.md), [independent audit](tied-block/AUDIT.md), and [root review](tied-block/ROOT_REVIEW.md).
4. [Five-row necessary-condition derivation](five-row/PROOF.md) and [independent symbolic audit](five-row/AUDIT.md).
5. [Exact exclusion of the next candidate](next-candidate/RESULT.md).

The rectangular preface explicitly assumes `1≤r<s`. Row means and the next-coefficient minor lemma concern nonempty blocks/minors; empty cases are separate trivial cases. The source already incorporated the reviewer’s `r≥1` clarification before freezing. The added preface is an editorial reminder, not a formula change.

## Reproduce

From this directory:

```text
python -B verify.py
python -B -O verify.py
python -B verify.py --full
python -B -O verify.py --full
```

Default mode uses only the Python standard library. It reruns the ten complete bivariate determinant examples, ten structural identity examples, the independent 125 quotient/55 weighted/15 minor checks, all 58 nonzero standard `n=8` coefficients by interpolation, and both concrete five-row candidates by exact permutation/binomial arithmetic. It validates the fixed inventory, source-checker hashes, relative links, and rejection controls. **It does not rerun the general symbolic five-row identities.** Its output explicitly reports those checks `NOT_RUN`; their frozen receipts receive integrity checks only.

Full mode additionally requires installed **SymPy** and reruns all 31 supplied symbolic checks, the 18-check independent quotient-ring/direct-determinant audit, and the independent direct determinant for the later candidate. A missing dependency fails clearly instead of silently skipping work. The source checkers use different algorithms within the same SymPy system; they are not independent proof kernels. The recorded source runs used Python 3.12.14 and SymPy 1.14.0. The aggregate reports the actual runtime versions.

The checker uses explicit exception checks that remain active under `python -O`. Both modes deliberately modify mathematical certificates independently of the inventory hashes. Full mode also exercises the original symbolic `--negative-control`, which changes the `c9` identity and must fail with residual `−1`. Inventory controls separately reject a modified file, missing file, unexpected file, and altered manifest.

All subprocess output and test corruption stay in fresh temporary copies. Running the aggregate leaves the frozen package unchanged. Running an individual original checker directly may rewrite its own result/receipt files; use a disposable copy for those commands. Python 3.10 or later is required. No network, downloaded code, vendored binaries, or browser is used.

## Compact package and provenance

[PROVENANCE.json](PROVENANCE.json) records every copied source hash, packaged hash, and editorial change. All seven original mathematical checkers are byte-preserved. The source five-row proof remains byte-preserved so its reviewed hash and independent receipt agree.

[manifest.json](manifest.json) and [SHA256SUMS](SHA256SUMS) define the canonical payload. [verification.json](verification.json) distinguishes source receipts and the validation protocol. The outer staging `MANIFEST.json` records actual normal/optimized runs, fresh ZIP extraction, archive hashes, and the fixed additive tree mapping.

Exploration artifacts, duplicate normal/optimized logs, duplicate certificates, caches, and nested archives are omitted. Historical file listings inside source reports describe their original research folders; the manifest is the authoritative packaged inventory. No existing repository file is changed by this package. A publisher must independently recheck the remote base and path absence before an additive operation; this preparation makes no remote calls.
