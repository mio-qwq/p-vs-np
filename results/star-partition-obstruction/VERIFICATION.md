# Verification record

Local verification date: 2026-10-25. Interpreter: Python 3.12.14. Both included scripts ran successfully with assertions enabled, using exact integers and `fractions.Fraction`; there is no floating-point numerical test or external dependency.

The two checkers are preserved byte-for-byte from the checked source versions:

| File | SHA-256 |
|---|---|
| `verifiedcheckers/check_transversal.py` | `7a8cffc8b1abb0d57f7801a09f02e3305aea703cedeea3b7ff32ca23a235b8b5` |
| `verifiedcheckers/check_multiblock.py` | `aeed521a834b55681f57f99b410e36adb325745e6ea4cac23a6cead8378b2318` |

## Two-block finite certificate

`check_transversal.py` uses the fixed canonical 7+7 coordinate split and parity-check columns 1 through 7 on each block. It checks all 64 product-code cosets, each with 256 centers, and all 64 error pairs.

It exhaustively checks the transversal bijection for every coset. Integer Walsh–Hadamard XOR convolution computes residual sums; a complete direct XOR-sum check at all 16,384 ambient centers cross-checks that convolution, and representative centers are additionally checked by direct threshold evaluations. The expected ambient probability is `21021/65536`, and every matching-block 64-gate family mean is `21021/1024` (raw numerator `336336`, denominator `16384`).

Negative controls verify that deleting the zero translation destroys coset constancy, and that the full 106-gate weight-at-most-two family has a lower bound but not constant means over this fixed code's cosets. Details and exact ranges are retained in `verifiedcheckers/results.json`.

This is not an exhaustive test over all block splits or code labelings. Their universal coverage follows from the proof's syndrome bijection, not from this finite certificate.

## Multiblock finite certificate

`check_multiblock.py` computes exact binomial sums for these ten triples `(n,r,b)`:

```text
(14,2,7), (16,2,7), (16,4,3), (20,4,3), (24,6,3),
(32,8,3), (32,4,7), (40,8,3), (64,8,7), (64,16,3)
```

For each tested positive pair of bundle support sizes, it checks a squared conditional lower bound with constant 2048, avoiding square roots. It also checks the squared global bound with constant 4096 and the shared two-block exact value. These are deliberately conservative numerical assertions; they do **not** test every sharper intermediate constant in PROOF.md. All ten pass, with exact probabilities in `verifiedcheckers/multiblock-results.json`.

Some tested block counts exceed the fourth-root range used in the existential carrier theorem. That is intentional: the ambient lemma applies more broadly. The checker does not construct the existential family, enumerate all configurations, or computationally certify the asymptotic concentration/collision argument. Those are general proofs, not extrapolations from the finite tests.

## Comparing reruns with fixtures

From the package directory, this standard-library command copies the checkers into a temporary directory (so the transversal script's side-effect does not overwrite a fixture), executes them with assertions enabled, and compares parsed JSON outputs:

```sh
python3 - <<'PY'
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

base = Path('verifiedcheckers')
with tempfile.TemporaryDirectory() as tmp:
    for name, fixture in [('check_transversal.py', 'results.json'),
                          ('check_multiblock.py', 'multiblock-results.json')]:
        script = Path(tmp) / name
        shutil.copyfile(base / name, script)
        actual = json.loads(subprocess.check_output([sys.executable, str(script)], text=True))
        expected = json.loads((base / fixture).read_text())
        assert actual == expected, name
        print(name + ': PASS; output matches fixture')
PY
```

The comparison above was run successfully during preparation. Finite checks supplement but do not replace the mathematical proof. No external manuscript theorem, novelty search, efficient carrier-construction claim, or circuit/algorithmic lower-bound claim was verified. The context-only external link is not a proof dependency.
