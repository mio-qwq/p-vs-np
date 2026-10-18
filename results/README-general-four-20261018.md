# General four-row masked translated-power determinants

Research checkpoint, 18 October 2026. The written argument passed a separate AI-assisted mathematical audit. The original checker verifies 84 exact identities; the independent implementation verifies 168 named checks and all 65,536 labelled masks.

## Statement and scope

For every binary 4-by-4 matrix whose support has a perfect matching, every four distinct real offsets, and every four distinct nonnegative integer exponents, the determinant of the masked entries `(x+a_i)^(e_j)` is not the zero polynomial. The proof classifies the finite support patterns while treating the offsets and exponents symbolically; it does not infer the unbounded statement from sampled exponent sets.

- [Frozen proof](monic-four-general/PROOF.md)
- [Current audit status](monic-four-general/STATUS.json)
- [Independent mathematical audit](monic-four-general/independent/AUDIT.md)
- [Order-at-most-three component argument](monic-four-general/SMALL_ORDER.md)
- [Historical attribution and claim boundaries](monic-four-general/ATTRIBUTION.md)

PROOF.md is preserved byte-for-byte, including its original candidate label. STATUS.json and the independent audit report record the later review status separately. An exact symbolic check supports the written mathematical argument; it is not a formal proof-assistant verification or human peer review.

The offsets must be real. The stronger unrestricted complex-offset statement is false. This is only an auxiliary uncolored order-four determinant result. It makes no arbitrary-order, color-conditioned ASNC, P-versus-NP, or historical novelty claim.

## Reproduction

Python 3.10 or later and SymPy 1.14.0 are required. From the repository root or an extracted extension archive:

    python3 -m pip install -r results/requirements-general-four-20261018.txt
    python3 results/verify-general-four-20261018.py
    python3 -O results/verify-general-four-20261018.py

The compact verifier validates source hashes, checks the frozen proof and audit status, and runs exact checkers and negative controls in clean temporary storage. Ordinary and optimized execution exercise the same explicit checks. Expanded certificates, caches, exploratory tables, temporary output, and large raw transcripts are not distributed.

This additive extension introduces only new paths under results/monic-four-general plus its dated index, dependency pin, manifest, verifier, and verification receipt. The prior [v0.12.0 result](https://github.com/mio-qwq/p-vs-np/releases/tag/v0.12.0) and its files remain unchanged. Earlier statements about what remained unresolved are historical checkpoints; this extension records the later scoped result separately.

The independent audit report and programs are preserved verbatim, with their original compact run and portability receipts. The report describes raw logs in its original audit directory; this source package omits those logs and the regenerated orbit/identity tables. Their hashes are retained in PROVENANCE.json and independent/SHA256.json. The public verifier regenerates and checks the mathematical output in temporary storage. For optional standalone paired audit reproduction, copy the independent directory to a writable temporary directory and run python3 run_audit.py there.

The public verifier runs each positive checker once in the current interpreter mode, rejects the deliberately perturbed C6 identity, reproduces exact counterexamples outside the theorem assumptions, and exercises packaging corruption controls. Run both commands above to check both execution modes. The dated verification receipt is derived output and is excluded from its own source manifest; the local delivery manifest additionally hashes every archive entry.
