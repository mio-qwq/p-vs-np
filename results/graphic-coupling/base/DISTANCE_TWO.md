# Distance-one versus distance-two pair locality

2026-10-17. Extension of RESULT.md, using the parent-proposed guarded connector construction. No novelty claim.

## Exact statement

Incident forbidden pairs (line-graph distance one) admit the matching reduction in RESULT.md. Allowing line-graph distance at most two makes the same decision problem NP-complete for arbitrary parity target T, even on simple graphs with disjoint pairs and with every edge paired.

This extension does NOT retain |T|=2, because the connector guards introduce additional odd-target vertices. It does NOT claim that the transformed graph stays series-parallel.

## Reduction from arbitrary disjoint pairs

Start from any loopless simple graph, disjoint forbidden edge pairs and target b. Subdivide every original edge e once, using a private midpoint u_e of target zero. Mark one of its two halves, which is incident at u_e. The midpoint equation forces both halves to have the same selection value, preserving original edge selection.

For each original forbidden pair {e,f}:

1. Retain a forbidden pair between the marked half of e and the marked half of f.
2. Add a connector c=u_e u_f.
3. Add a pendant edge d=u_e l to a fresh leaf l. Set the leaf target to one and toggle the midpoint target at u_e from zero to one.
4. Add forbidden pair {c,d}.

The new leaf forces d=1. Its pair then forces c=0. The midpoint equation at u_e is

    first_half XOR second_half XOR c XOR d = 1,

which reduces to equality of the two halves. At u_f it is the same equality because c=0. All original vertex equations are unchanged. Thus the transformed feasible subsets correspond exactly to the original ones, after adding the forced guard edges and duplicating each selected edge onto both halves.

The marked halves are at line-graph distance at most two via c, even though c is forced absent in every feasible solution. The guard pair {c,d} is incident. Each edge is in at most one forbidden pair, since the original pairs were disjoint and all new edges are private. Every new edge has distinct endpoints, and no two edges coincide, so the graph remains simple.

If full pairing is required, pair each still-unpaired edge g with a new pendant edge attached to an endpoint of g and ending at a fresh target-zero leaf. That edge is forced zero; the new pair is incident and does not change feasibility. This includes every unmarked subdivision half. Graph size is linear in the original graph size.

Therefore the NP-hard family from RESULT.md reduces to a distance-two instance, and membership in NP is unchanged.

## Exact validation

`distance_two.py` implements the transformation and witness lifting. `test_distance_two.py` independently compares exhaustive original and transformed T-join feasibility on 80 small instances, with transformed graphs up to 16 edges. All pass. It also verifies:

* every graph is simple;
* every edge belongs to exactly one pair;
* every pair has line-graph distance at most two;
* 24 original feasible witnesses lift correctly;
* extracted transformed witnesses have forced guard values, equal subdivision halves and valid recovered original witnesses.

Results: `distance_two_results.json`.

## Interpretation

The local-matching algorithm depends on conflicts being enforceable at one vertex. A connector that is present in the input graph but forced absent in solutions can make a remote conflict look distance-two local without providing that enforcement property. Consequently graph-distance locality alone stops being sufficient at distance two. The construction is a self-contained threshold proof, not an assertion that this threshold is new in the literature.
