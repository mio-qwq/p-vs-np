# Canonical brace cancellation and row-support-transfer audit

Public research-source archive, 20 October 2026 UTC. This directory adds three frozen source checkpoints to the earlier [canonical binary cancellation archive](../canonical-binary-counterexample-20261019/README.md). The earlier archive contains the disconnected 83-edge seed; the new 224-edge brace certificate and all-k construction are successor results, not claims already established by that seed alone.

The preserved materials contain written proofs, exact integer/rational Python checkers, separately reconstructed AI-assisted audits, certificates, provenance, and negative controls. They do not resolve P versus NP or the complexity of Exact Matching. No historical-novelty, priority, human-peer-review, or independent Lean-verification claim is made.

## 1. Standard brace counterexample and the endpoint caveat

The first archive constructs a connected bipartite graph with 73 vertices on each side and 224 binary-colored edges. Its actual numerical row offsets and column exponents remain exactly 0 through 72. It is 2-extendable: every two-edge matching extends to a perfect matching. Both exact implementations check all 24,508 disjoint edge pairs; the written proof also establishes the necessary Hall expansion.

Its entire target-three-red-edge fiber consists of eight perfect matchings. After removing a common nonzero factor of degree 2582, all 47 coefficients of the signed sum of degree-46 terms vanish exactly. Thus the full signed sum of degree-2628 translated-power terms is identically zero, despite the nonempty fiber. This is an entire-fiber identity, not a selected cancelling subsum. The 141 added red edges do not enter any target-three matching: every perfect matching using a new edge has at least 34 red edges.

This contradicts the nonvanishing assertion of Theorem 1.2 in Yuefeng Du's [Bipartite Exact Matching in P, arXiv:2604.01571v3](https://arxiv.org/html/2604.01571v3#S1.SS2), under its expressly intended standard brace/2-extendability interpretation. The manuscript's Definition 3.1 also has a literal Hall-plus-two endpoint defect: imposing |N(S)| >= |S|+2 at |S|=n-1 would require n+1 distinct columns in an n-column graph. The construction is not a counterexample to that impossible literal condition. Its applicable standard Hall-plus-two range is 1 <= |S| <= n-2, with matching and connectedness conditions. This distinction is essential whenever comparing the certificate to the paper.

Read the first archive's construction/PROOF.md, independent_audit/AUDIT.md, review/SOURCE_COMPARISON.md, and review/VERIFICATION_GUIDE.md. The embedded prior_five_cycle documents retain the earlier disconnected seed's narrower scope.

## 2. Exact failure of row/layer-support transfer

The second archive isolates e=(42,8). Removing e leaves a 223-edge standard brace H, with all 24,291 disjoint edge pairs extendable. The original eight-term target fiber splits into two nonzero four-term branches with opposite polynomials: matchings avoiding e and matchings using e.

The actual minimal cofactor circuit is T={(42,1),(30,0)}, while the matching-induced support is S={(42,1),(30,1)}. On columns 8 and 10 the circuit minor is zero, but the matching-induced minor is nonzero. The cofactor restriction annihilates the active columns on T; moving to S loses the required annihilation. This is a failure of the transfer between different row/layer supports. It is not a counterexample to the existence of a nonzero matching-induced minor, nor a failure of an invertible pivot change on one fixed survivor space.

Here the lower packet is empty and there are 146 literal Schur survivors, not two. T is an additional circuit restriction. Restricting to T also does not preserve every graph-column pairing; the explicit column-9 check demonstrates this distinction. These facts prevent an incorrect identification of the two-row circuit with the full survivor space.

The separate 4-by-4 doubled-state example concerns repeated bases and disjoint color support only. It is not a graph-perfect-matching witness or an ASNC counterexample. It has its own exact supplemental checker and is outside the main independent packet audit's scope.

Read construction/PROOF.md and independent_audit/AUDIT.md in the second archive. The comparison concerns the pinned [v3 packet argument](https://arxiv.org/html/2604.01571v3#S7.Thmtheorem21).

## 3. Arbitrary extendability, with growing graph size

For every integer k >= 1, set n=max(73,3k+6) and m=n-5. Append blue singleton pairs to the canonical seed, retain all existing labels and colors, and add missing red shifts 1 through k in a consecutive-component matched-pair ordering. The resulting binary-colored bipartite graph is connected and k-extendable, with actual canonical row offsets and column exponents 0 through n-1.

Every perfect matching containing an added edge has at least ceil(m/k) >= 4 red edges. Consequently the entire target-three fiber remains exactly the same eight padded matchings and its signed polynomial remains identically zero. Complete balanced base components and the strict inequality m>3k are essential; the archive includes negative controls for the strict-threshold and component-completeness hypotheses. The extension argument uses |N(S)| >= min(n,|S|+k), so it respects the Hall endpoint.

The all-k theorem is established by the written proof, not extrapolated from finite testing. The checker fully enumerates the target fiber for k=1,2,3,4; checks construction and seed data at k=22,23,50,100; and runs 81,858 cyclic-expansion and 107,777 component-step checks. Graph size grows with k. This is not a fixed-order all-k result or a result covering every dense support or every relabeling.

Read audit/AUDIT.md in the third archive. root/PROPOSITION.md is the preserved earlier mathematical proposal; the audit is its subsequent completed review.

The uncolored cyclic shift-0-through-k backbone is classical. It is isomorphic to the consecutive cyclic-neighborhood bipartite constructions in Zan-Bo Zhang, Xiaoyan Zhang, Dingjun Lou, and Xuelian Wen, [Minimum size of n-factor-critical graphs and k-extendable graphs](https://arxiv.org/pdf/1707.07288), Theorems 2.4–2.5, Graphs and Combinatorics 28 (2012), 433–448. Those theorems already establish the backbone's k-extendability; no novelty is claimed for it here. The present construction combines that backbone with binary low-target-fiber preservation and the specified canonical cancellation certificate. This attribution does not establish novelty of that combination.

## Frozen archives and reproducibility

- [Brace certificate](archives/research-checkpoint-20261019-1501.zip): 205667 bytes; SHA-256 db6e7f3e4e96ddcc9b98f0a5639723070e937067da1f0f6545ad83e6ee324b3b
- [Packet-transfer supplement](archives/pnp-packet-transfer-supplement.zip): 191979 bytes; SHA-256 42d61bc45800fdbaa93071d62d4244cae77baaaa7a792b8795f43dff27b5095a
- [Arbitrary-extendability construction](archives/pnp-arbitrary-extendability-private.zip): 23388 bytes; SHA-256 688a59ecd010c1802f5afeb34a0b8bbc7904fcd86e1441df88e83dd79c12e9f1

All three ZIPs are preserved byte-for-byte. Their historical private-status wording, original local source-path provenance, and pre-audit wording describe preparation at the time of freezing. They do not describe the later public status of this directory. REPLAY_PLAN.json is executable replay configuration. No prior archive or old file is replaced by this addition.

Python 3.10 or newer and the standard library suffice. Extract each archive into its own empty directory. In the first archive's extracted root run:

```sh
python -B verify_bundle.py
python -O -B verify_bundle.py
```

In the second archive's extracted root run the same two commands. In the third archive's extracted root run:

```sh
python -B replay.py --receipt ../replay-receipt.json
```

The third harness itself runs normal and optimized checkers and fault controls. The first two also validate their full frozen inventories, reconstruct the exact certificates in temporary directories, compare expected outputs, and reject specified mutations. Use receipts outside the frozen extracted directories. See [VERIFICATION.json](VERIFICATION.json) and [verification/](verification/) for fresh pre-publication replay results. Hashes attest byte identity, not mathematical correctness.

## Source attribution and verification limits

The second ZIP includes an unchanged HTML snapshot of Yuefeng Du, Bipartite Exact Matching in P, arXiv:2604.01571v3 (9 April 2026), [source](https://arxiv.org/html/2604.01571v3). Its retained banner identifies CC BY 4.0; that third-party snapshot remains subject to [that license](https://creativecommons.org/licenses/by/4.0/), not a newly asserted repository license. Original author attribution and license notice are preserved. Its SHA-256 is c04bd735efa1cd7dfb5201b58dd1d34d1b1199fe2e8e3bb54c486065d479959c.

A bounded source-scope check on 19 October 2026 at 22:54 UTC found the arXiv record still at v3 and the relevant claims unchanged. It did not establish comprehensive prior-art coverage, novelty, or absence of all possible corrections. The manuscript's linked anonymous Lean repository returned an expired-repository notice. Its source, theorem signatures, changes, and build remain unverified; no independent Lean audit is claimed here. The manuscript describes partial Lean verification with eight hypotheses.

These results concern the stated canonical nonvanishing claim and the identified proof transfer. They do not prove P=NP, P!=NP, P-versus-RP separation, impossibility of deterministic Exact Matching, or failure of all Exact Matching algorithms. Further independent mathematical review remains appropriate.
