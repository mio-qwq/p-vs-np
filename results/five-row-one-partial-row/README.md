# Five-row one-partial-row nonvanishing theorem

18 October 2026. Exact mathematical proof and reproducible symbolic-algebra checks.

## Theorem

Let `a0,...,a4` be distinct real numbers, `e0,...,e4` distinct nonnegative integers, and `A` a binary 5-by-5 matrix with at least four full rows and a nonempty remaining row. Then

`det[A_ij (x+a_i)^e_j]`

is not identically zero as a polynomial in `x`.

Read the [complete proof](five-row-c12-20261018/PROOF.md) and [independently implemented audit](five-row-c12-audit-20261018/AUDIT.md). The proof covers all five nonempty support sizes and arbitrary exponent gaps within this subclass. The [earlier necessary reduction](five-row-cancellation-20261018/PROOF.md) and [its audit](five-row-cancellation-20261018/AUDIT.md) are included, so no external mathematical dependency is needed.

The key addition is an exact coefficient-12 obstruction. Together with coefficient 10 it eliminates the offset-shape parameter without dividing by a potentially zero coefficient. Uniform sign bounds leave six retained-pair gaps and twelve complementary-triple gaps. Every resulting integer quadratic has a negative or nonsquare discriminant.

## Reproduce

From this directory, with Python 3.10 or newer:

```sh
python -B verify.py
python -B -O verify.py
```

Default mode uses only the standard library. It checks the frozen inventory, eight unchanged original checkers, source provenance, exact polynomial elimination and positivity certificates, every finite discriminant and printed proof-table entry, plus deliberate arithmetic and packaging corruptions. It does **not** reconstruct determinant coefficients; it reports that stage as `NOT_RUN`.

To reconstruct coefficients and rerun every source checker and independent audit, install the pinned dependency in your preferred environment and use full mode:

```sh
python -m pip install -r requirements.txt
python -B verify.py --full
python -B -O verify.py --full
```

Full mode requires installed SymPy and fails clearly if it is missing. Tested with Python 3.12.14 and SymPy 1.14.0. The aggregate runs all original checkers in temporary copies, compares freshly produced receipts, and checks deliberate C9, C12 and complementary-elimination failures. No source checker is patched at runtime. Directly running a source checker also works, but may rewrite its adjacent receipt; use the aggregate to keep this frozen package untouched.

## Contents and provenance

- [Current status and historical context](STATUS.md)
- [Release notes](RELEASE_NOTES.md)
- [Selected-source hashes and editorial record](PROVENANCE.json)
- [Verification contract](verification.json)
- `manifest.json` and `SHA256SUMS`: exact packaged byte inventory
- `five-row-c12-20261018/`: current theorem, primary checker and canonical receipt
- `five-row-c12-audit-20261018/`: independent coefficient method, prior reduction recheck, final table check and receipts
- `five-row-cancellation-20261018/`: complete prerequisite reduction, checker, independent audit and receipts
- `root-review/`: additional independent elimination/sign review and receipt

The original checkers are preserved byte-for-byte. Explorations, caches, nested archives, and redundant normal/optimized logs are omitted. Source reports retain their historical file listings; `manifest.json` is this package's authoritative inventory. Proof-critical sibling references resolve locally; the prior audit's ancillary d=9 example points to the immutable published v0.16.0 commit.

## Scope and trust

This completes the one-partial-row subclass only. Arbitrary five-row binary masks and the general colored problem remain unresolved here. No novelty, complexity, general ASNC, P-versus-NP, human peer-review or proof-assistant-verification claim is made. The two coefficient implementations use different algorithms in the same SymPy system, not separate proof kernels. The proof's logical and real-variable arguments remain mathematical text for review; executable algebra certificates are not formal proof-assistant proofs.

This package adds only `results/five-row-one-partial-row/`. It does not rewrite earlier results or historical claims.
