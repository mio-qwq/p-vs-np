# Deterministic colorful parity matching

This checkpoint implements and audits deterministic fixed-parameter algorithms for parity-labeled matching on specified dense domains. It does not solve general SAT or P versus NP, and no historical novelty is claimed.

## Algorithms and exact scope

- PROOF.md and solver.py: complete bipartite perfect matching with k-bit GF(2) labels and a target. An explicit deterministic color family, colorful path/cycle dynamic programming and disjoint-color cycle packing give FPT in k, with large parameter constants.
- COVER_EXTENSION.md and cover_solver.py: bipartite allowed-edge matching with a supplied, directly verified cover of the forbidden-edge graph, size q. The algorithm is FPT in k+q. Covered vertices may be on either side.
- GENERAL_MATCHING.md and general_solver.py: undirected simple-graph perfect matching via baseline-pair ports, again using a supplied verified forbidden-edge cover. **The frozen implementation retains its valid changed-pair bound 4(k+q)+1. It has not been optimized to the newer direct bound 2(k+q)+1.** A minimum forbidden-edge cover in a general graph is NP-hard; no polynomial optimizer is claimed or implemented.

The empty/trivial inputs and validity checks are described in the proofs and code. The complete undirected case has q=0. Arbitrary forbidden-edge patterns with unbounded supplied cover size do not give a uniform polynomial algorithm.

## Prior art and dependency

The support-radius dependency is the previously released [sharp permutation theorem](../sharp-permutation-radius/README.md). Crucially, the same standard color-coding route already gives FPT using Derksen's older sufficient 3k support bound. FPT itself must not be presented as requiring the sharper theorem or as a new tractability discovery. The sharper radius improves a parameter bound within this construction; historical novelty remains unverified. Primary comparison: [Derksen (2013), Lemmas 2.7–2.9](https://sites.lsa.umich.edu/hderksen/wp-content/uploads/sites/614/2018/05/A.I.a.38.pdf).

Separate [direct matching radius theorems](../matching-polynomial-radius/README.md) and the [permutation transposition-distance addendum](../permutation-cayley-radius/README.md) accompany this checkpoint. They do not silently modify the frozen implementations.

## Reproduce all three result directories

Python 3, standard library only, from this directory:

    python run_checks.py

The runner executes 13 commands, including all root algorithm tests and independent audit checkers. Each script's adjacent .log is actual captured output. The original solver/proof files are unchanged; only independent checker paths and report path references were adapted. SOURCE_PROVENANCE.json records source and packaged hashes across all three directories. See VERIFICATION.md for the completed run.

Independent reviews are AI-assisted. Finite tests corroborate the proofs and implementations; no human peer review, Lean/formal verification, or practical-performance guarantee is claimed. Ring, graphic-recognition and Yang–Mills investigations are excluded.

## Composition boundary

GADGET_PARAMETER_BOUNDARY.md checks the previously published local NAND gadget: its m private pair auxiliaries have no edges between them, so their forbidden-edge graph contains K_m and every forbidden-edge cover has q>=m-1. Consequently this composition does not yield FPT solely in additional parity bits. This elementary source-checked note is not a separate independent audit or a lower bound for every algorithm.
