# Recognizing a representation with prescribed common-star groups

2026-10-17. Extension of the pair-sum recognition criterion. Established graphic recognition and matching algorithms are used; no historical novelty or general SAT claim.

## Exact criterion

Input is an explicit binary matrix A with nonzero columns and designated groups of columns. Parallel columns mean identical vectors. Within each group keep one representative of each distinct vector **only for the recognition construction**.

A graph representation of A in which every designated group is incident to one common vertex exists exactly when BOTH conditions hold:

1. The distinct representative vectors within each group are linearly independent.
2. The matrix obtained by appending a_i+a_j for every pair of distinct representatives within every group is graphic.

The criterion itself concerns graph representations. For the polynomial quota solver below, the input groups are globally disjoint, so whichever common host each receives, their local port sets do not overlap. An overlapping group system would need a separate local feasibility theorem; this report does not assume one.

## Proof

Necessity: in a loopless graph, distinct nonparallel edges incident at a single vertex form a star forest, so their incidence vectors are independent. Add an edge between the two outer endpoints of every pair of distinct group edges. These closing edges have precisely the appended sum vectors, giving a graphic representation of the whole extension. Repeated new columns are harmless parallel edges.

Sufficiency: every pair of distinct representative columns and its appended sum is a three-element circuit. In a graph representation of the extension, this circuit is a triangle, so every two group representatives share an endpoint. A pairwise intersecting family of two-element endpoint sets is either a common star or the three edges of a triangle. To see this, choose two sets {u,v},{u,w}; any set not containing u must be {v,w}, after which every other pairwise-intersecting distinct two-set is one of these three. The triangle alternative gives a linear dependency among three distinct group columns, contradicting condition 1. Therefore each representative group has a common endpoint.

An original column parallel to a representative forms a two-element circuit with it and therefore is a parallel edge with the same two endpoints in every graph representation. Restoring all duplicate edges preserves the common host. No original variable or quota multiplicity is removed by this recognition simplification.

The construction appends at most quadratically many columns. Gaussian independence checks and fundamental-circuit normalization are polynomial. Standard binary graphic recognition decides condition 2 and can recover a representation. As in the pair case, affine targets are transported by solving Az=b and using Bz; identical binary kernels prove the equivalence. Added sum columns are recognition-only and are deleted before solving the quota instance.

## Degeneracies and essential negative control

A zero column can be fixed to zero and deleted for an upper-quota problem: this does not change the syndrome and cannot violate an upper bound. Keep the quota value, or cap it at the smaller remaining group size. This argument is specific to upper quotas and must not be transferred to lower bounds or exact-count constraints. The prototype requires zero columns to be preprocessed.

The independence condition is essential. The three columns 1,2,3 represent a triangle. All their pair sums are again 1,2,3, so appending the sums is graphic. Yet the three triangle edges cannot share one host in any graph representation. Their distinct-vector rank is only two, so condition 1 rejects correctly.

Parallel duplicates must NOT be collapsed for solving. In the verified example A=[1,1,2,4] with one quota-two group, recognition uses three directions but the solver retains four selectable edges and counts both parallel copies separately. All eight target syndromes were independently checked.

## Solver and checks

`star_solver.py` constructs the extension and checks the independence condition. Given a proposed graph certificate for the extension, it verifies equality of the binary kernels, verifies actual common hosts, transports the target, and invokes the polynomial blossom-backed quota solver. Returned witnesses are checked against the original matrix and original group counts.

It verifies certificates; it does not implement automatic graphic-representation discovery. The polynomial discovery theorem invokes the existing graph-realization algorithm. Exhaustive small-rank recognition below is validation-only.

`test.py` checks 1,813 rank-three column/group configurations against all 168 invertible binary row maps. Direct common-star existence agrees exactly with the two-condition criterion. It also checks the triangle counterexample and all eight targets of the parallel-duplicate quota example. All tests pass.

Run `python test.py`. Sibling certificate, quota and blossom modules are imported by explicit paths; see the source. Results and hashes are included.

## Prior-art and scope

[Robert E. Bixby and Donald K. Wagner, An Almost Linear-Time Algorithm for Graph Realization (1988)](https://doi.org/10.1287/moor.13.1.99) supplies the underlying graph-realization algorithm after Gaussian normalization. The incident-pair matching case is already a corollary of [Cannon, Ishaque and Tóth, Conflict-free graph orientations with parity constraints (2012)](https://arxiv.org/abs/1203.3256). The present artifact records an elementary recognition reduction and its checked integration, without a novelty assertion.

This enlarges the recognizable presentation class for the local quota solver. It does not say arbitrary binary systems are graphic, arbitrary groups are independent stars, or arbitrary overlapping constraints are tractable. A rejected recognition test rejects this structural certificate, not the satisfiability of the original instance.
