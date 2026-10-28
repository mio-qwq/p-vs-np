# Overlapping-pair determinant: reproducible local proof packet

**Result:** the 5×5 masked determinant with partial-row supports `{a,b}`, `{a,c}` and three full rows is nonzero for every five distinct integer exponents and five distinct complex offsets. Negative exponents are interpreted in the rational-function field; shifting the common minimum reduces to the polynomial case.

This is a **computer-assisted result for this mask only**. It is not a P vs NP result, a general circuit lower bound, a theorem for arbitrary masks or noninteger exponents, Lean verification, or independent human peer review. The original mathematical and computational reviews were AI-assisted.

- `PROOF.md`: standalone argument, full 408-gap / 1632-span proof, algebraic low exceptions, μ-undivided C3–C7 obstruction, and explicit compact formulas.
- `sources/`: two byte-for-byte original, independently implemented C++ signed-divisor engines. A merges factorizations of |B| and |C| and precomputes modular tables; B uses a smallest-prime-factor sieve of |2BC| and lazily caches polynomial evaluations.
- `scripts/`: portable exact checker, independent direct-alternant coefficient derivation, independent structural controls, and handwritten factored-Phi evaluator.
- `inputs/`: only the compact C7 formula certificate and original raw coefficient data. These JSON files are data, never imported as Python modules. The prior table includes C8 for byte-preserving provenance; the proof needs and checker uses only C3–C7.
- `certificates/`: all 2,432 final modular survivors and original all-order counts.
- `reviews/`: selected original sealed review documents and receipts, unchanged; see `PORTABILITY.md`.

## Reproduce

Requirements: Python 3.10+ with SymPy 1.14.0, and `g++` supporting C++17. Tested with Python 3.12.14 and g++ 14.2.0. No network is used by the checks. Install the external requirement beforehand if necessary: `python -m pip install -r requirements.txt`.

From the extracted packet directory:

```sh
sha256sum -c SHA256SUMS
python scripts/check.py --quick
python scripts/check.py --full
# Optional additional undefined-behavior/bounds instrumentation:
python scripts/check.py --full --sanitize
# Independent coefficient identities also work under optimized Python:
python -O scripts/check_coefficients.py
```

The scripts resolve input paths relative to their own location and work from any current directory. All compiled executables, generated headers, and engine output files are placed in a temporary directory and removed automatically. No build output, cache, binary, or network fetch is shipped.

**Quick mode** reconstructs all 112 integer P7 terms, checks Engine A's embedded term table and all 30 canonical order labels, compiles both engines, verifies H=40 coverage against direct B,C,D-to-E enumeration, checks the negative-negative divisor omission control, verifies structural identities, and evaluates all 2,432 recorded survivors exactly by two independent expressions. It does not rerun full-height enumeration or derive C3–C7 afresh.

**Full mode** additionally reruns both engines at the mathematically proved height 1632, matches every per-order counter and complete survivor set, and freshly derives C3–C7 by direct power/binomial alternants before comparing the old coefficient table. Sanitizers are optional because the original independent full sanitizer replay is already recorded, but can be rerun here.

No check relies on `assert`, floating-point arithmetic, modular division, an omitted order class, or dividing by μ. Full mode does not trust a precompiled executable. SHA-256 verifies byte integrity, not mathematical truth; the derivations and replays supply the substantive checks.

## Exact full-domain counts

| Stage | Count |
|---|---:|
| B,C pairs | 3,992,688 |
| All distinct C3 tuples, all 30 orders | 19,658,082 |
| L=0 | 3,540 |
| A=0 after L exclusion | 0 |
| K=A+2L=0 after L,A exclusion | 6 |
| L,A,K nonzero | 19,654,536 |
| P7=0 mod101 | 220,631 |
| P7=0 mod101 and mod103 | 2,432 |
| P7 exactly zero | **0** |

The regular domain retains two μ=0 tuples, 37 Z=0 tuples, and 32 R=−4 tuples. Nothing in the proof excludes these by a denominator shortcut. The 13 canonical orders without C3 tuples are included and counted as zero, not omitted a priori.

This packet was prepared locally on 2026-10-27. It is not a publication, pull request, merge, or release. No external state was changed.
