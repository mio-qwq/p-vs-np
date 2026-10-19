# Column closure and one-outlier mixed backgrounds

Source-only research checkpoint, 19 October 2026. These restricted exact results do not settle P versus NP or arbitrary sparse binary noncancellation. No novelty, human peer-review, or proof-assistant verification claim is made.

## Contents and scope

- `column-certificate-closure-20261019/PROOF.md`: complete three-row consecutive-exponent nonnegative-relation cone, minimal weighted two-column closure obstruction, and a limited closure theorem when the constant column stays full. The weighted obstruction is not a binary-mask counterexample.
- `weighted-column-counterexample-20261019/CLOSURE_AUDIT.md`: separate independent review of that classification. Its reference to the reviewer's separate checker is historical; that unbundled checker is not needed to run this package.
- `column-closure-adversarial-20261019/PROOF.md`: independent deletion-closure audit, a four-row failure of a particular functional, and the stronger three-row positive-kernel obstruction. Its checker imports the included `search.py` helper.
- `two-column-root-audit-20261019/DERIVATION.md`: separate supporting derivation of the weighted cancellation classification.
- `mixed-column-positivity-20261019/PROOF.md`: one weighted column with all other columns full; background exponents h,...,h+n-3,h+n-2+d. Full complex linear independence is proved for odd d, d=2,4,6, even d with gcd(d/2,n-1)=1, or a distinguished exponent outside the background range. The remaining cases have an exact proper-power-plus-span criterion; arbitrary backgrounds remain open here.
- `mixed-background-ode-audit-20261019/AUDIT.md`: independent audit of normalization, exceptional exponents, the ODE, the power-and-span criterion, and moment exclusions. Author and reviewer checks are retained separately rather than counted as separate mathematical results.
- `mixed-background-root-moments-20261019/DERIVATION.md`: supporting proper-power exclusions for d=2,4,6.

All 14 input files are copied byte-for-byte. Original local absolute paths and local-work status statements inside them are historical provenance, not portable execution instructions. The corresponding included files are found by their directory suffixes above. No old published archive is changed.

## Reproduce

Use Python 3.12 or a compatible Python 3 with the standard library. The independent ODE checker additionally requires SymPy; verification used SymPy 1.14.0. From this directory, run:

    python column-certificate-closure-20261019/check.py
    python -O column-certificate-closure-20261019/check.py
    python column-closure-adversarial-20261019/check.py
    python -O column-closure-adversarial-20261019/check.py
    python mixed-column-positivity-20261019/check.py
    python -O mixed-column-positivity-20261019/check.py
    python mixed-background-ode-audit-20261019/check.py
    python -O mixed-background-ode-audit-20261019/check.py

The first and last checkers rewrite their adjacent JSON results. Run on an extracted copy if keeping this frozen source untouched. All checkers use explicit failures, so optimized mode does not remove their tests. Finite exact computations verify identities and representative cases; universal statements rely on the written mathematical arguments.

`REPRODUCTION.json` records clean-extraction verification. `SHA256.json` covers every other bundle file, including original proof, checker, and result bytes. There are no binaries, dependency caches, large execution logs, or archive files inside the source tree.
