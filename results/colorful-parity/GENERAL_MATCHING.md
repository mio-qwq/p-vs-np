# Undirected matching extension

Research proof; novelty unverified. This is independent of any claim about
general P versus NP. Covers are supplied and directly checked, not optimized.

Input: an undirected simple graph on 2n vertices, k-bit labels on its allowed
edges, a target, and a vertex cover C of its forbidden-edge graph, |C|=q.
The complete-graph special case has q=0. Arbitrary labels can be assigned to
forbidden edges because accepted matchings never use them.

## A small changed-pair witness

Fix the baseline matching {(0,1),(2,3),...}. It need not be allowed. For a
permutation matrix P of order 2n define, for u<v,

    E_uv(P)=sum_i [P_(2i,u) P_(2i+1,v)+P_(2i,v) P_(2i+1,u)].

On every permutation this is exactly the zero/one indicator that the image
of the baseline matching contains {u,v}. Every perfect matching is an image
of the baseline under some permutation. Each E_uv has degree two over GF(2).

The product of the k target-parity factors and the q covered-vertex allowed
incident-edge sums detects exactly the allowed target matchings. On an image
matching, each covered vertex has only one incident selected edge, so its
allowed-edge sum is exactly zero or one. The cover property excludes every
forbidden selected edge. This polynomial has degree at most 2(k+q).

If a valid target matching exists, the support theorem gives a realizing
permutation sigma moving at most 4(k+q)+1 vertices. Write S for its support
and partner(S) for baseline partners of its elements. S is invariant under
sigma; elements outside S are fixed. Hence S union partner(S) is invariant.
Every baseline pair outside this union is fixed pointwise. Thus the resulting
matching differs from the baseline on at most |S| baseline pairs, and has an
alternating-cycle decomposition using at most t=min(n,4(k+q)+1) pairs.

An elementary baseline-to-matching symmetric difference consists of even
alternating cycles. A nontrivial cycle visits each of its baseline pairs once,
and uses at least two pairs. Shared baseline edges are simply omitted.

## Two-port colorful cycles

Treat each baseline pair as a vertex with ports zero and one. Color-code the
pairs, not the individual original vertices, with the explicit family from
PROOF.md. A directed traversal enters one port and exits the opposite port.
It then chooses an allowed edge to either port of a fresh-colored pair.

The state records the used pair colors, start pair and start entry port,
last pair and last entry port, and accumulated delta. A transition from pair
i to pair j contributes the label of the new edge plus the baseline label
of pair i. Closing a path back to the start entry port contributes the same
delta for the last pair. Thus each baseline label is removed exactly once.
Paths closed after at least two pairs yield legitimate alternating cycles.

For each color-set/delta state retain one concrete oriented cycle. Pack cycles
with disjoint pair-color sets. Pair-color disjointness prevents reuse of either
port of a pair, and the traversal uses each of the two ports once. The resulting
new edges form a matching on all selected pairs; keep baseline edges elsewhere.

For forbidden baseline edges, mark their pairs mandatory. They number at most q,
because the baseline edges are disjoint and each needs a cover vertex. Reserve
their pair colors for those exact pairs and require all reserved colors in the
packed union, as in COVER_EXTENSION.md. Reject colliding mandatory colors.
Only allowed transition and closing edges are admitted. Every unselected
baseline edge is then allowed too.

Soundness follows from the port accounting and delta identity. Completeness
follows by taking a small changed-pair witness and a coloring injective on its
changed pairs; reservation preserves it and the two dynamic programs recover
its delta and mandatory coverage. Exhaustion is an exact NO certificate by
the proof, not a randomized failure report.

The extra port bit multiplies state and transition counts only by constants.
The same explicit-family bound therefore proves deterministic FPT in k+q,
with very large parameter constants in this prototype. The complete case is
deterministic FPT in k. The older sufficient permutation radius 3d also gives
FPT with a weaker changed-pair parameter, so novelty does not follow from the
sharp support theorem.

## Cover acquisition and scope

Unlike the bipartite forbidden-edge graph in the earlier extension, a general
forbidden-edge graph need not have polynomial-time minimum vertex cover.
No such claim or implementation is made here. A supplied cover is sufficient.
Endpoints of any maximal matching in that forbidden-edge graph form a cover
of size at most twice optimum, if a separately verified approximation is desired;
the prototype does not perform this preprocessing.

The code general_solver.py reconstructs and directly checks the final matching,
edge legality and parity. It rejects odd vertex count, asymmetric matrices,
invalid label ranges, and invalid covers. Empty inputs and already-valid
baseline matchings are handled directly. Tests use exhaustive perfect-matching
enumeration as an independent decision oracle.
