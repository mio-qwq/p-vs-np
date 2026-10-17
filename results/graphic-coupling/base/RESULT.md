> Historical first-stage report. The current package includes the polynomial blossom backend and direct Cannon–Ishaque–Tóth prior-art attribution; see ../README.md and ../quota/RESULT.md. The old backend-availability paragraph below describes the earlier stage.

# Graphic coupling: exact NP/P boundary for disjoint forbidden edge pairs

2026-10-17. New research artifact; no historical novelty claim. This changes the coupling matrix rather than assuming a semantic period oracle.

## Problem and outcome

Let A be the binary vertex-edge incidence matrix of an explicitly given loopless graph G. Every column has exactly two ones. Given target b, choose an edge subset J with odd-degree set T={v:b_v=1}, while choosing at most one edge from each designated disjoint pair. An unpaired edge is allowed; if the original domain requires every edge to lie in a pair, a forced-zero leaf edge can pad it.

* Arbitrarily located pairs: NP-complete, already for |T|=2 on a simple series-parallel core (optional forced-zero leaf padding preserves treewidth at most two).
* Every forbidden pair shares a vertex: polynomial-time solvable by an explicit polynomial-size reduction to general perfect matching. The proof permits unbounded degrees; it does not enumerate local relations.

Neither conclusion says anything about P versus NP. The positive case is a structural restricted algorithm, and the negative case explains why graph incidence alone is insufficient.

## 1. Arbitrary pairs: self-contained reduction

Given strict 3-CNF G(x), build a chain of variable gadgets followed by a chain of clause gadgets. Successive gadgets share only their articulation endpoints.

Each variable gadget has two internally disjoint paths, corresponding to values 0 and 1. On the value-a branch, reserve a separate edge for each occurrence of that variable whose literal is false at value a. Each clause gadget has three internally disjoint paths, one per literal. Reserve one edge on each literal path and pair it with the corresponding reserved falsification edge in the variable gadget.

Every reserved edge belongs to exactly one pair, so the forbidden pairs are disjoint. All branches are padded to length at least two, with distinct internal vertices, so the underlying graph is simple. Its core is a two-terminal series-parallel graph. Set T={s,t}, the chain endpoints.

A satisfying assignment chooses its variable branches and, for each clause, one true literal branch. No chosen literal edge is paired with a chosen falsification edge, yielding a feasible s-t path and therefore a feasible T-join.

Conversely every T-join contains an s-t path: the component containing s must also contain t, since every component has an even number of odd-degree vertices. Choose a simple path inside it. Taking a subset preserves all at-most-one pair constraints. Articulation structure forces this path to choose exactly one branch in every gadget. The variable choices form an assignment; every chosen clause literal must be true, or its forbidden falsification edge would also be on the path. Hence the formula is satisfiable.

For full edge pairing, attach a fresh leaf edge for each previously unpaired edge and pair the two. Give every new leaf target zero. Its unique edge is forced absent, so this padding imposes no restriction on the old edge and does not change T. These leaves can attach at s with distinct leaf endpoints. The padded graph is still simple and has treewidth at most two. Size is linear in occurrences before padding and remains polynomial afterward. Membership in NP is immediate by checking the selected edge set.

## 2. Incident pairs: explicit matching gadget

For each pair, choose a common endpoint as its host. Let d_v be the original degree and p_v the number of pairs hosted at v. Construct:

1. A port vertex q_(v,e) for each edge e incident at v.
2. For each hosted pair {e,f}, a private auxiliary vertex c joined only to q_(v,e),q_(v,f).
3. A dummy port if needed: choose δ_v in {0,1} so d_v+p_v+δ_v equals b_v modulo two.
4. A clique on all ordinary ports at v plus its optional dummy.
5. For each original edge e=uv, an external matching edge joining q_(u,e) to q_(v,e).

A perfect matching selects original edge e precisely when it uses its external edge. If both edges of a hosted forbidden pair were selected, its auxiliary c would have no unmatched neighbor. Hence at most one is selected.

If s_v original incidences are externally matched, the remaining local gadget has d_v+p_v+δ_v-s_v vertices. A perfect matching requires s_v≡b_v mod2.

Conversely, given a feasible selected subset, every pair has at least one unselected port. Match its private c to one such port; disjointness of hosted pairs makes those choices independent. The remaining vertices are all in the local clique, whose size is

    d_v-s_v-p_v+δ_v.

It is nonnegative and even by the chosen parity, so it has a perfect matching. Together with the external selected edges this matches the entire gadget graph.

The gadget has O(|V|+|E|) vertices and O(|E|+sum_v d_v^2) edges. Any polynomial general-graph maximum-cardinality matching algorithm decides whether a perfect matching exists and returns the original T-join witness. An isolated vertex with b=1 creates an isolated dummy, correctly rejecting; b=0 creates no local vertices. Odd-sized T is also rejected automatically.

The proof actually needs only that the pairs hosted at each individual vertex are disjoint; an original edge may participate in one hosted pair at each endpoint. The implementation in this artifact deliberately checks the original stronger promise of globally disjoint pairs.

This is not a direct use of linear matroid parity: that problem asks for unions of pairs subject to independence, whereas this problem asks for at-most-one choices and an affine incidence target. The explicit matching reduction is the needed bridge.

## 3. Literature checked and precise relevance

- [Edmonds, Paths, Trees, and Flowers (1965)](https://doi.org/10.4153/CJM-1965-045-4) is the foundational general maximum-cardinality matching algorithm. The positive theorem uses polynomial general matching, not bipartite matching or Gaussian elimination.
- [Darmann, Pferschy, Schauer and Woeginger, Paths, trees and matchings under disjunctive constraints (2011)](https://doi.org/10.1016/j.dam.2010.12.016) studies negative pair constraints and forbidden-pair path reductions. Its results depend on the underlying optimization problem, so a tractability result for constrained spanning trees cannot be transferred to T-joins. The self-contained reduction above establishes our precise decision restriction.
- [Kazda, Kolmogorov and Rolínek, Even Delta-Matroids and the Complexity of Planar Boolean CSPs](https://arxiv.org/abs/1602.03124) supplies polynomial edge-CSP algorithms for even delta-matroid constraints represented by tuple lists. Its abstract explicitly warns that succinct matrix representations may encode exponentially many tuples. The incident-pair gadget bypasses this input-size issue by constructing a polynomial-size matching instance directly.
- [Geelen, Iwata and Murota, The linear delta-matroid parity problem](https://www.math.uwaterloo.ca/~jfgeelen/Publications/deltamatroidparity.pdf) gives algorithms for specified linear representations and defines parity objectives distinct from simply choosing at most one paired element. No theorem from it is being applied without a reduction.

These sources establish relevant existing frameworks. They do not establish novelty of the exact gadget, which is not claimed.

## 4. Implemented checks and honest complexity accounting

`graphic.py` implements the matching reduction, witness checking, SAT reduction and independent exact validation oracles. `test.py` ran successfully:

* 600 random incident-pair graph instances: exhaustive original T-join feasibility agrees with perfect-matching feasibility; every extracted witness passes parity and pair checks.
* 4,438 exhaustive local gadget signatures, covering degrees 0 through 8, every possible number of disjoint hosted pairs, both target parities and every externally selected port subset.
* 180 SAT-to-arbitrary-pair path comparisons, with all edges paired by forced-zero padding.
* Nine strict-3CNF controls: the eight sign-pattern clauses on three variables are UNSAT; removing any one clause is SAT. Their reduced instances match these outcomes.
* One direct exhaustive T-join UNSAT control from contradictory unit clauses, in addition to the strict-3CNF path controls.

IMPORTANT: `brute_pm` is an exponential memoized validation oracle, clearly marked as such. The current executable does not implement a polynomial blossom backend. The polynomial-time result is the proved reduction plus the established polynomial matching algorithm. No exponential local enumeration is hidden in the reduction.

Run `python test.py`. Results, logs and hashes are beside this report. No external repository was changed or third party contacted.
