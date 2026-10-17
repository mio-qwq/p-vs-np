# Independent audit: local conflict-free T-joins reduce to perfect matching

## Problem and precise scope

Input is a finite loopless undirected multigraph G=(V,E), a parity target b_v in {0,1} for each vertex, and at each v a family P_v of disjoint pairs of edges incident at v. Choose X subset E such that |X intersect delta(v)|=b_v modulo two and X never contains both edges of any local pair.

Disjointness is only required **within each P_v**. An edge may belong to a pair at each of its two endpoints. Parallel edges are allowed and receive distinct ports. Loops are excluded from this statement to avoid ambiguity about incidence multiplicity and labeled parallel gadget edges; the tested reduction does not silently simplify loops.

## Construction

At vertex v of degree d_v, create one port p_{v,e} for every incident edge. For every original edge e=vw, join its two ports with an external edge.

For each pair {e,f} in P_v, create an auxiliary vertex adjacent to exactly p_{v,e} and p_{v,f}. No other edges touch that auxiliary vertex. Put all ports at v in a clique. Write p_v=|P_v| and c_v=d_v-p_v. If delta_v=(c_v-b_v) mod2 equals one, add one dummy vertex to that clique. The dummy has no neighbors outside that clique. There are no auxiliary–auxiliary edges.

## Correctness, both directions

Let M be a perfect matching of the gadget, and let X be the original edges whose external edges belong to M. A pair auxiliary has to match one of its two ports. Therefore those ports cannot both be occupied by selected external edges: X respects every conflict pair.

At v, exactly s_v=|X intersect delta(v)| ports are consumed by external edges. The p_v auxiliary vertices consume exactly p_v more ports. Every other port and the optional dummy must be matched inside the clique. Their number is

    d_v-s_v-p_v+delta_v=c_v-s_v+delta_v,

which is even. By the chosen delta_v this is equivalent to s_v=b_v modulo two.

Conversely, start with a conflict-free edge set X satisfying all parity targets and select its external edges. For every local conflict pair, at least one of its ports remains available. Because local pairs are disjoint, choose and match one such port to each auxiliary independently. The remaining clique has the displayed even number of vertices, hence admits a perfect matching, including the empty case. These local matchings and the external edges together form a perfect matching of the entire gadget.

At an isolated original vertex, b_v=0 gives an empty local gadget, while b_v=1 gives one isolated dummy and correctly prevents a perfect matching. Degree-one and paired degree-two cases are covered without exceptions.

## Size, algorithm, and qualifications

There are O(|V|+|E|) gadget vertices and O(|E|+sum_v d_v^2) edges. Construction and a general-graph perfect-matching algorithm yield a polynomial-time decision and witness procedure. The |V| term should be retained when counting explicit isolated vertices.

The classical matching algorithm is established by [Jack Edmonds, Paths, Trees, and Flowers, Canadian Journal of Mathematics 17 (1965), 449–467](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/paths-trees-and-flowers/08B492B72322C4130AE800C0610E0E21). The constructive reduction here is treated as an audited application of standard matching machinery, with no novelty claim.

For edge-weighted optimization, put each original weight on its external edge and zero on all other gadget edges. Every matching's weight then equals the weight of its selected original edge set, giving a minimum-weight matching formulation as well. This reduction is not counting-preserving: one valid edge set can have multiple internal matching extensions.

## Independent checks

check_matching_gadget.py uses an exact memoized matching search, not the construction proof as an oracle. It compares perfect-matching existence with exhaustive original-edge subset search, extracts each matching witness and rechecks its original parity and conflict constraints.

Passed:
- 155 exhaustive graph/local-pair/parity instances on at most three vertices, including the empty graph.
- 2,000 seeded random instances with at most six vertices and eleven edges.
- Parallel-edge instances with pairs allowed at both endpoints.

The test search is exponential and serves only as a small-instance verifier. The polynomial-time result uses general matching algorithms.

## Immediate structural extension: local partition capacities

Replace disjoint conflict pairs by disjoint groups G_j of incident ports, each permitting at most u_j selected external edges, where 0<=u_j<=|G_j|. For group G_j, create |G_j|-u_j auxiliary vertices, all adjacent to every port in G_j, and to nothing else. All of these auxiliaries can be matched precisely when at least |G_j|-u_j group ports remain unused by external edges, equivalently when selected count is at most u_j. Disjointness of groups makes simultaneous local auxiliary matching independent.

Keep the port clique and use

    c_v=d_v-sum_j(|G_j|-u_j),
    delta_v=(c_v-b_v) mod2.

The identical leftover-parity argument proves the reduction. The pair gadget is the case |G_j|=2,u_j=1. This expands the matching-solvable presentation to local partition upper-capacity constraints plus graphic parity, but does not cover overlapping local groups or arbitrary conflicts between remote edges. The extension is proved by the construction; the current script specifically tests the pair case.

## Direct prior art; no new tractability claim

[Sarah Cannon, Mashhood Ishaque and Csaba D. Tóth, Conflict-free graph orientations with parity constraints (2012)](https://arxiv.org/pdf/1203.3256) gives polynomial algorithms for parity-constrained orientations with locally disjoint subset conflicts, and NP-completeness when such conflicts may overlap. Their disjointness definition is local to the host vertex. The T-join problem above maps directly to their formulation: subdivide each edge, require even indegree at its new midpoint, and call the edge selected when that midpoint has indegree zero. Then both original endpoints receive one incoming edge exactly when it is selected. Original parity and hosted subset conflicts transfer unchanged. Consequently the local-pair tractability statement is an adaptation/implementation of an established subclass, not a new theorem of tractability. The capacity and laminar formulations below also carry no novelty claim.
