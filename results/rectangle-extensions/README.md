# Separated rectangles and one-entry extensions

19 October 2026. Three scoped mathematical results, with complete proofs,
independent AI-assisted audits, exact checkers and reproducible certificates.

## Results

1. [Arbitrary-omission rectangle theorem](general-omission-20261018/PROOF.md).
   A red r-by-(r+q) rectangle, q>=1 and n>=2r+q, has nonzero feasible fibers
   for distinct real row offsets with strict separation of the two row blocks
   and distinct nonnegative integer exponents. An exact first-coefficient
   identity is valid for arbitrary distinct offsets; nonvanishing there is
   conditional on its row factor. The pivot/Schur argument proves that all
   competing smaller Laplace layers lie strictly below the candidate degree.
2. [One disjoint added red entry](single-edge-perturbation-20261019/PROOF.md).
   Nonvanishing extends to that nonrectangular family if n>=2r+q+1, and to the
   tight boundary n=2r+q for r>=2. Exact cofactor linearity and the deleted
   moment-loss inequality provide the proof. The tight r=1 boundary requires
   additional conditions rather than following from this argument alone.
3. [Two one-row boundary tests](single-row-boundary-20261019/PROOF.md).
   For the remaining one-row configuration, the middle fiber has degree D,
   D-1 or D-2 under the successive nonresonance conditions stated in the proof.
   This settles all sizes with a distinguished minimum/maximum exponent or
   consecutive exponent set. A genuine simultaneous-resonance regime for
   n>=5 remains open here; exact examples can lose four highest coefficients
   and still be nonzero. They are not zero-polynomial counterexamples.

The general rectangle proof is stored once. The single-entry proof and result
have only their dependency reference redirected to that canonical copy.
All six original mathematical checker scripts and all other source documents
are byte-preserved. [PROVENANCE.json](PROVENANCE.json) records original and
packaged hashes and the two editorial changes. Source checkpoints and
SOURCE_MANIFEST.json files are historical local records, not a current remote
publication receipt or the bundle inventory.

## Reproduce

From this directory with Python 3.10 or later:

    python -B verify.py
    python -B -O verify.py

Default mode needs only the standard library and reruns four exact checkers:
general q=3 translated-minor certificates and q=1/q=2 regressions, eight
single-edge fixtures, 32 separately implemented deterministic single-edge
cases, and 40 one-row boundary cases. It compares recomputed certificate bytes,
checks provenance and inventory, and rejects deliberate mathematical and
packaging corruptions. It explicitly reports the independent SymPy boundary
audit and stress-certificate reconstruction as NOT_RUN.

For all six original scripts, including that symbolic audit and stress
certificate, install the pinned dependency in your preferred environment:

    python -m pip install -r requirements.txt
    python -B verify.py --full
    python -B -O verify.py --full

Full mode requires SymPy and fails explicitly when it is missing. Tested with
Python 3.12.14 and SymPy 1.14.0. The aggregate runs scripts in temporary copies
so their normal receipt-writing behavior cannot change the frozen package.
Source-level wrong-sign and wrong-variance controls must fail even under -O.
There are no network calls, generated code downloads, or numerical tolerances.

## Scope and trust

These are structured-coloring results, not arbitrary binary masks or all
colorings. Nonseparated offsets with vanishing first row factor and the stated
one-row simultaneous-resonance regime remain outside the proved conclusion.
No general ASNC resolution or counterexample, P-versus-NP result, complexity
claim, historical novelty, human peer review, Lean or other proof-assistant
verification is claimed. Exact computations corroborate mathematical proofs;
they do not enumerate all instances or provide a formal proof kernel.

[STATUS.md](STATUS.md) and [RELEASE_NOTES.md](RELEASE_NOTES.md) summarize the
boundaries. [verification.json](verification.json) describes the verification
contract. manifest.json and SHA256SUMS are the complete packaged byte inventory.
This bundle adds only results/rectangle-extensions/ and replaces no old files.
