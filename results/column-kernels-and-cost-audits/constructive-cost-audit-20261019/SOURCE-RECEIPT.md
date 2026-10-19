# Source and review receipt

Checked 19 October 2026 (UTC). Version-pinned primary source:

https://arxiv.org/html/2604.01571v3#S2.SS2

Location: Proposition 2.3, proof Steps 2–3. This receipt records a short literal excerpt and the exact mathematical claim under review; it is not a copy of the complete paper.

Literal excerpt from Step 3 (13 words total across these fragments):

“Since matchings decompose along tight cuts”

“A standard knapsack-style DP over the blocks”

Between those fragments the displayed-in-prose mathematical criterion is:

    F_(G,t) nonempty iff there exist t_1+...+t_s=t
    with F_(G_j,t_j) nonempty for each j.

This is unconditioned per-block feasibility, with no selected-cut-edge state. Step 2 identifies G_j as brace blocks and uses their individual ASNC tests. It also states the size inequality sum_j n_j <= n. These are the precise targets of Section 3 of PROOF.md. The counterexample does not dispute the elementary grid interpolation on an input already certified to be a brace.

Additional version-pinned location:

https://arxiv.org/html/2604.01571v3#S3.SS6

In Theorem 3.11's Step 1, the reduction identifies its tight cuts with balanced Hall partitions of defect zero, then invokes independent factorization. PROOF.md Section 3.3 explains why this does not account for the six-cycle's genuine tight cut. The general Hall-block identity in Section 3.2 is not refuted here.

Deduplication: the 18 October limited audit records three separate polytope/masked-minor/valuation issues. Its final scope paragraph expressly excludes review of the tight-cut algorithm and arithmetic cost. Its root review concerns those same earlier certificates. This package adds an independently derived algorithmic-scope audit, without a historical novelty claim.

Verification performed here:

- Read the limited audit, its root review, two-bit status note, general-omission theorem, single-row-boundary theorem, and original P-versus-NP route audit.
- Reopened the version-pinned primary paper and checked Proposition 2.3 and Theorem 3.11.
- Wrote a self-contained exact-arithmetic checker from scratch.
- Ran it in both ordinary Python and optimized Python; both passed 689 small graphs, 11,126 determinant comparisons, 1,643 witness extractions, the C6 certificate, and five SUBSET-SUM gadget samples.

This is not formal verification, human peer review, an ASNC proof, or a general lower bound. File hashes in MANIFEST.json identify this frozen package. No earlier source archive was modified.
