# Results and limits

19 October 2026. Local adversarial mathematical investigation; no remote actions or publication.

## Main structural result

`KERNEL-THEOREM.md` completely classifies constant signed-cofactor dependencies for arbitrary distinct real offsets and exponents `(d,d+1,...,d+n-2,d+n)`, with the distinguished second-smallest exponent and n>=3. Exceptional dependencies are exactly one-dimensional and always mixed-sign. Therefore every nonempty nonnegative retained-row weighting of that one column is nonvanishing, although full linear independence fails in infinitely many sizes.

This is a rigorous scoped theorem, not an all-exponent or arbitrary-graph noncancellation result. Root independently derived the classification, and the constructive researcher independently audited the proof with no defect found (`KERNEL-INDEPENDENT-AUDIT.md`). `check_kernel.py` verifies its exact identity from raw minors on seven cases; a separate defining-polynomial certificate supplies a nonsymmetric algebraic five-row exception. Neither finite check is used as proof of the universal statement.

## Independent audit of the constructive boundary theorem

The proof in the separate `resonant-column-structure-20261019` package was independently audited. Its even-rank, second-smallest-rank Schur-ratio, and diagonal-hole total-positivity arguments pass. They close the prior five-row simultaneous-resonance two-hole boundary. The audit was delivered as that package's `INDEPENDENT_AUDIT.md` and includes its six-row normal form and parity reduction.

The constructive worker also supplied an exact six-row obstruction to extending the same extreme-root test. I independently reproduced both rational ratios by raw minors: for offsets `(0,t,1/3,2/3,1-t,1)`, exponents `(0,1,2,3,4,18)`, and holes `(0,3),(5,3)`, all prior resonances hold. At t=1/20 the positive-node removed-entry/full-determinant ratio exceeds one; at t=1/4 it is below one. Continuity therefore gives an algebraic intermediate t where the extreme-root evaluation is zero. This is a failure of that root test, not a zero full polynomial. The worker preserves the detailed certificate separately.

## Supplemental exact finite search

`search_complete.cpp` enumerates all 2^25 binary colorings of the canonical complete five-by-five bipartite graph via 2^24 global-complement representatives. For each coloring it checks every nonempty exact-red-count fiber for a zero polynomial. No such fiber was found.

The final exact counters are:

- 16,777,216 complement representatives
- 50,208 nonempty fibers whose evaluation at Lambda=1 was zero and therefore required full coefficient checking
- zero full-polynomial failures

Each permutation polynomial is expanded with integer arithmetic and has degree at most 10. A Gray-code edge flip changes the red count of exactly 24 permutations. The program tracks each fiber's exact evaluation at Lambda=1 and its matching count. A zero polynomial must pass that evaluation filter; every surviving candidate is then tested coefficient by coefficient from the independently stored permutation expansions.

All intermediate signed sums fit in 64-bit arithmetic: their absolute values are at most 120*5^10=1,171,875,000, since each nonnegative permutation polynomial's coefficient sum equals its value at 1 and is at most 5^10. Global complementation simply sends target t to 5-t, so the fixed final color bit loses no case. This also tests every uncolored canonical five-row support mask via its zero-red fiber.

Reproduction: compile `search_complete.cpp` with a standard C++17 compiler and optimization, then run it. The saved final output is `search_complete.out`; `search_complete.progress` records progress counters. The executable is intentionally not retained. This is supplemental finite evidence; there has been no second independent exhaustive implementation, and no larger-size or symbolic-offset theorem follows from it.

## Open boundary

The wider no-nonnegative-constant-kernel conjecture remains unresolved for arbitrary exponent sets. No full-polynomial-zero example satisfying the real-offset hypotheses was found. None of these results establishes P=NP, P!=NP, or an unconditional polynomial-time algorithm for the general requested complexity problem.
