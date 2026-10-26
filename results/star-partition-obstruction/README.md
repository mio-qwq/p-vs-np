# Star-partition residual-population obstruction

A self-contained, restricted mathematical result about the **unsigned expected number of nonzero two-bundle anchored mixed differences** of translated majority gates.

* **Explicit two-block family:** one family of all weight-at-most-two translates works for every balanced two-block Hamming partition, labeling, and common coset. A matching-block transversal subfamily has an exact coset-independent mean.
* **Existential growing-block family:** for every sufficiently large even dimension, a polynomial-size set of distinct translates works simultaneously for all specified configurations with even block count at most the fourth root of the dimension. No efficient explicit construction is claimed.

Read [PROOF.md](PROOF.md) for definitions, quantifier order, complete elementary proofs, and limitations. Read [VERIFICATION.md](VERIFICATION.md) for reproducibility and the strictly finite scope of the checks.

## Reproduce

Python 3.10 or later is recommended; only its standard library is used. From this directory, run without Python's `-O` option (the checks use assertions):

```sh
python3 verifiedcheckers/check_transversal.py
python3 verifiedcheckers/check_multiblock.py
```

Both print JSON with `"status": "PASS"` if their assertions succeed. The first also rewrites `verifiedcheckers/results.json` beside the script. The second only prints its result; its expected output is `verifiedcheckers/multiblock-results.json`. These are the sole retained result fixtures, not independent evidence of a successful run on another machine. No network, external package, or downloaded executable is needed.

## Context and attribution

The [public Nag record](https://zenodo.org/records/22774131) is cited only as the source of the partition/residual context motivating this restricted question. The mathematical model needed here is stated in full in PROOF.md. No theorem from that record is assumed, and this package does not certify or refute the entire manuscript.

**Substantial AI assistance** was used in the mathematical derivation, proof checking, code preparation, and exposition. No novelty or priority claim is made. This package establishes no circuit lower bound, CAPP running-time lower bound, or P-versus-NP conclusion. Its represented wire count is not minimum circuit complexity. Signed cancellation, top-gate simplification, gate-specific partitions, masks, and downstream computational cost are outside the claim.
