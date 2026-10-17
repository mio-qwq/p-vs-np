# Sharp permutation-polynomial testing radius

For every field K, n >= 2 and integer d >= 1, the optimal support radius for detecting every nonzero degree-at-most-d polynomial function on permutation matrices is

    R = min(n, 2d+1).

For d=0 or n<=1, radius zero is optimal. “Nonzero” means nonzero as a function on the full symmetric group. We use the **row-image convention P_sigma[i,sigma(i)] = 1**. The frozen PROOF.md is byte-identical to the independently reviewed proof.

## Theorem and historical comparison

The upper bound minimizes moved points and then nontrivial cycles, using a Boolean cube of disjoint row swaps. Pfaffian and monomial examples establish sharpness uniformly over all fields, including characteristic two. See PROOF.md and REVIEW.md.

Derksen, [The Graph Isomorphism Problem and approximate categories, Journal of Symbolic Computation 59 (2013), Lemmas 2.7–2.9](https://sites.lsa.umich.edu/hderksen/wp-content/uploads/sites/614/2018/05/A.I.a.38.pdf), supplies the established sufficient radius 3d. The independent reviewer checked the primary paper, including Lemma 2.8. This packet sharpens that stated sufficient bound to the exact radius (equal at d=1, potentially smaller for d>=2, and capped by n). Historical novelty remains unverified; no priority claim is made.

## Executable consequence and limits

solver.py searches complete bipartite perfect matchings with k-bit GF(2) parity labels and a requested parity target. A degree-k indicator polynomial yields a witness moving at most min(n,2k+1) points when one exists. The deterministic search is XP, polynomial for each fixed k; no FPT or uniform polynomial bound is claimed. The sharp support radius is not a running-time lower bound.

The theorem is about all permutation matrices. Missing-edge matching domains need not contain the row-swap cube, so no extension to arbitrary allowed-edge graphs is asserted. This does not resolve P versus NP. Ongoing Cayley and graphic-recognition investigations are excluded.

## Reproduce

Python 3, standard library only, from this directory:

    python check_lower.py
    python test_solver.py
    python check.py
    python rank_check.py

All four commands were actually rerun successfully from this portable package. Their corresponding .log files record stdout. The tests include exact integer Pfaffians, finite-difference and descent checks, complete solver comparisons, and GF(2) evaluation ranks. They corroborate rather than replace the all-field mathematical proof. See VERIFICATION.md and SOURCE_PROVENANCE.json. Reviews are AI-assisted; neither human peer review nor Lean/formal verification is claimed.
