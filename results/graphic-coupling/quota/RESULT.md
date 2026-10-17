# Local upper quotas, parity, and an executed matching backend

2026-10-17. Constructive extension and literature clarification. Earlier graphic-coupling artifacts are unchanged. No novelty claim.

## Result

A graph edge subset with prescribed vertex-degree parity and disjoint local upper-quota groups reduces to a polynomial-size perfect-matching instance. The implemented solver uses the independent standard Edmonds backend in `../blossom/blossom.py`, not an exponential matching oracle.

At each vertex v, the incident edges may be partitioned into disjoint groups. A group C has a quota c between zero and |C|; at most c of its edges may be selected. Groups at different endpoints may constrain the same edge independently. Ungrouped edges are unrestricted. This includes all the incident forbidden-pair instances from the preceding report but also permits large groups and arbitrary upper quotas.

## Explicit gadget

Create one port q_(v,e) per incidence. Join the two ports of each original edge by an external edge. For each hosted group C of size k with quota c, add k−c private auxiliary vertices, each adjacent to all ports of C. Let a_v be the total number of auxiliaries at v. Create a clique on all d_v ordinary ports and an optional dummy port δ_v, where

    d_v+a_v+δ_v = b_v modulo 2.

No auxiliary connects to the clique except through its designated group ports.

In any perfect matching, the original edge is selected iff its external edge is used. If s_C ports of a group are externally matched, its k−c auxiliaries require k−c distinct remaining group ports. This is possible iff s_C≤c. Because groups at v are disjoint, their auxiliary matchings do not compete.

After matching all auxiliaries, the remaining local clique has d_v−s_v−a_v+δ_v vertices. It is nonnegative under the quotas, and even exactly when s_v≡b_v. Thus it can be perfectly matched iff the target parity holds. This proves both directions and supplies witness extraction.

Total auxiliary count is at most the total number of incidences. The matching graph has O(|V|+|E|) vertices and O(sum_v d_v^2+|E|) edges. The backend is a standard unweighted general-graph augmenting-path/blossom algorithm with cubic vertex-count time bound. No enumeration of the potentially exponentially many local feasible tuples is used.

## Direct prior art: the pair case is already covered

[Sarah Cannon, Mashhood Ishaque and Csaba D. Tóth, Conflict-free graph orientations with parity constraints, arXiv:1203.3256v2](https://arxiv.org/abs/1203.3256) gives polynomial algorithms for parity-constrained orientations with locally disjoint exact or subset conflicts, and NP-completeness without disjointness. Section 3 reduces its tractable cases to matching; its definition of disjointness is per vertex, allowing an edge to participate in constraints at both endpoints. This is stronger direct prior art than the general delta-matroid references previously located.

Our incident-pair T-join result is a direct corollary, by the following elementary mapping. Subdivide each original edge with a degree-two midpoint requiring even indegree. Its two arcs must either both point toward the midpoint or both away. Interpret the latter as selecting the original edge. The selected status is then the incoming status at both original endpoints. Keep their parity targets and their hosted subset-conflict pairs. This proves equivalence. The direct gadget here is an independently checked matching adaptation, not a newly discovered tractability theorem. The quota extension is likewise not asserted to be historically new.

## Executed implementation and validation

`quota.py` constructs the gadget, calls the polynomial backend, checks the returned matching, extracts selected original edges and independently rechecks every parity and quota.

`test_quota.py` compares this end-to-end solver with exhaustive original-edge search on 700 random instances with 2–8 vertices and at most 10 edges. They contain 303 generated groups larger than two, including nontrivial and zero/full quotas. All comparisons pass. The test oracle is exponential, but it is used only to independently validate the polynomial solver.

The backend is developed and tested separately; this report does not infer maximum-cardinality correctness merely from the feasibility checker. Its independent exhaustive tests are recorded in its own directory. The backend has no external package dependency.

Run `python test_quota.py` from this directory. `results.json` and the package-level `CHECK_OUTPUT.txt` record the checks; the repository manifest freezes their hashes. The bundled sibling blossom directory is resolved relative to this file.

## Exact scope

Arbitrary remote forbidden pairs remain NP-complete by the preceding SAT reduction. Local incidence structure and local group disjointness are essential. This solver does not test general succinct periods, solve arbitrary binary matrices, or provide a general SAT algorithm.

A simple parameterized extension is available: if k forbidden pairs are remote and all others fit the local matching core, branch on one excluded edge from each remote pair. Every feasible solution excludes at least one endpoint of every pair, so one of the 2^k branches retains it. Delete the selected excluded edges, discard constraints already satisfied by deletion, and run the local solver. The resulting bound is 2^k times a polynomial, not a uniform polynomial when k is unbounded.
