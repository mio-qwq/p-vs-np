# Independent audit: common-star groups and laminar quotas

2026-10-17. Verdict: the star-group criterion, target transport, certificate-only integration, and separate laminar matching construction are correct. Prior frozen audits are unchanged. No general SAT or novelty claim.

## 1. Star-group recognition theorem

For nonzero binary columns, collapse equal vectors within each designated group only when building the recognition constraints. Check independence of the distinct directions and append their pairwise sums. The entire extended matrix is graphic iff one graph representation makes every designated group incident to a common vertex, provided the independence checks pass.

Both directions survive audit. In a common star, distinct directions correspond to distinct outer endpoints and are independent. Added sums close the corresponding triangles. Conversely each distinct pair and its sum is a three-element circuit, forcing pairwise incidence in every graph representation of the extension. A pairwise-intersecting family of distinct two-element endpoint sets is either a common star or exactly the three directions of a triangle. The latter is dependent and therefore excluded. Parallel original columns have identical endpoints and may be restored without changing the common host.

The extension is simultaneous: one representation of the full augmented matrix witnesses every group at once. Separate per-group graphicness tests would not establish that. Pairwise sums may coincide with original or other added columns; parallel graph edges make this harmless.

For an explicit list of groups, the number of added columns is at most quadratic in the total group-list length. For disjoint groups it is at most quadratic in the original number of columns. The recognition theorem does not require groups to be disjoint; the current quota-solver integration does.

### Essential negative control

Columns [1,2,3] form a triangle. Appending all three pair sums only duplicates the same columns, so the extension remains graphic. Nevertheless the original three edges cannot share a vertex. Distinct-direction independence rejects this case. The extra rank test cannot be omitted.

## 2. Degeneracies and transport

- Zero columns can be fixed to zero in a pure upper-quota instance: this preserves the syndrome and only decreases selected counts. Remove them, retaining the old capacity or capping it at the new group size. This preprocessing does not apply unchanged to lower/exact counts.
- Parallel variables may remain separate in the solver and must then be counted separately in its quota checks. Recognition-only representative selection does not authorize silently changing the variable list or quota bookkeeping. In fact, within one upper-quota group, a carefully proved parity-based duplicate reduction is possible, but it is unnecessary and not what this implementation does.
- Empty groups are vacuous; singleton groups and groups consisting of one parallel class are automatically local once A is graphic. The implementation skips empty hosted groups.
- A nongraphic or dependent-group rejection means the instance lacks this structural certificate; it is not a SAT-unsatisfiability certificate.
- Same labeled binary circuits determine the kernel. If B is the realizing incidence matrix restricted to original columns, solve Az=b first and use t=Bz. Then Ax=b iff Bx=t; the result is independent of the particular z, even with redundant rows. Added sum columns are not selectable original variables.

## 3. Actual implementation scope

Reviewed star_solver.py and its imported certificate_solver.py. The star solver builds the extension, validates disjoint groups, checks group-direction independence, verifies a supplied graph certificate by binary-kernel equality, finds common hosts, transports the target and calls the blossom-backed quota solver. It rechecks any returned assignment against the original syndrome and original group counts.

The kernel checker constructs a linear map from the A-column span to the B-column span, rejects inconsistent dependencies, then checks injectivity by the images' rank. This is a valid polynomial equality-of-kernels test, without circuit enumeration.

The implementation does not discover a graph certificate. Automatic discovery is supplied at the theorem level by classical constructive graphic-matroid recognition, as documented in the previous pair-sum audit. The exhaustive GL(3,2) searches are validation oracles only. The solver requires zero columns to have been preprocessed and relies on sibling module paths, whose original and packaged hashes are captured in ../SOURCE_PROVENANCE.json.

## Packaging scope

This is an excerpt of the independent audit: sections 1–3 are reproduced above; the separate laminar-quota section is omitted because it is not implemented in this packet. The reviewer additionally ran 700 simultaneous-group configurations in check_simultaneous.py and reran the peer's 1,813 star configurations. The packaged programs are rerun separately; see the top-level verification record.
