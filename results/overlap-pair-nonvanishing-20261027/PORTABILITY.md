# Portability, provenance, and preserved reviews

The original research workspace is not required to run this packet. Active scripts resolve every input relative to their own file. Both C++ sources are byte-for-byte original; Engine B's required `polynomials.hpp` is regenerated in a temporary directory from `inputs/C7_FORMULAS.json`, not copied from an old build. No prior C8 experiment, resultant computation, six-order-only engine, compiled binary, or cache is needed.

`PROVENANCE.json` records relative source labels and destination paths and source SHA-256 values for copied material. Source paths there are historical provenance, not runtime dependencies. No repository or private account metadata is needed by the verifier.

## Editorial and packaging changes

- The original integrated `FULL_MODEL_PROOF_DRAFT.md` is preserved byte-for-byte in `reviews/root/`.
- Its integrated argument is reproduced in `PROOF.md` with the two requested editorial corrections: “pre-filter offset” → “pre-filter exponent value”, and the old “expressions of0654” reference → `inputs/C7_FORMULAS.json`.
- English spacing in the integrated proof was polished without changing mathematical content; the original spacing remains in the sealed review copy. Links and checker references in the portable proof point to packet-local files. Standalone appendices supply the exact normalization, entire structural proof, full compact formulas, and explicit all-integer common-shift corollary. The reviewed root file itself was not altered.
- `scripts/phi.py` copies the independent review's handwritten function verbatim, adding only a module docstring and its standard-library import.
- `scripts/check_structure.py`, both C++ engine sources, input JSON files, survivor TSV, original counts, and selected original review documents were copied without editing. `scripts/check.py` and `scripts/check_coefficients.py` are new portable verification adapters; they do not change the theorem or enumeration algorithms.

## What a preserved review means

Files in `reviews/` are sealed historical records, not rewritten to appear contemporaneous with this packaging. Some mention old filenames, earlier partial statuses, or checks beyond this packet's minimal C7 route. These strings are historical references only. For example, the original structural proof correctly stated that a height reduction alone was not yet complete nonvanishing; the later all-order exhaustion completes that implication.

Original review receipts refer to source hashes in the original workspace. Those references are not rewritten to name the edited standalone proof. `PROVENANCE.json` and the current `SHA256SUMS` provide the explicit bridge. Included original review files retain their original bytes; omitted old files are not represented as included. A selected review is evidence of that review's stated scope, not a substitute for the current portable replay.

`certificates/survivors.tsv` is the independent engine's ordering of all 2,432 survivors. Its SHA-256 is `b10b59f7c09d9c074d41d86ea5e86cf7023be87345eabb5f41edde93dbbdb817`. The root's different 7-column ordering has historical SHA-256 `b008f2a7ec55b6156c355ff6d2c83b11cf4580a42b6046ba1a823e7757dc83c5`; full replay checks their reconstructed tuple sets coincide and checks output row counts to detect truncation.

## Integrity

`SHA256SUMS` covers all packet files except itself. The sibling ZIP checksum covers the complete archive, including that manifest. Neither file is a digital signature or an independent proof review. The ZIP uses sorted paths and a fixed timestamp, and contains no absolute paths or symlinks.
