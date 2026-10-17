# Unweighted Edmonds matching backend

Independent implementation of the standard augmenting-path and blossom-contraction method attributed to Jack Edmonds, “Paths, Trees, and Flowers,” Canadian Journal of Mathematics 17 (1965), 449–467. This implementation is not claimed as new research. No third-party code, dependency, or downloaded implementation was used.

## Interface

`maximum_matching(n, edges)` returns a tuple of n partner indices, using -1 for unmatched vertices. `maximum_matching_edges(n, edges)` returns canonical matching edge pairs. `verify_matching(n, edges, matching, require_perfect=False)` checks feasibility (and optionally perfection), **not optimality**. Use maximum_matching to obtain maximum cardinality. The empty graph has an empty perfect matching.

Input is an iterable of undirected integer endpoint pairs on vertices 0 through n-1. Duplicate/reversed edges are deduplicated. Loops, invalid endpoint types/ranges, invalid n, and malformed edge shapes raise ValueError. Boolean values are rejected as integers. Candidate matching malformations return False. These functions do not provide weighted matching, multiedge identity, or matching with additional constraints directly.

## Algorithm and complexity

An alternating BFS starts at each currently exposed root. Outer-to-outer edges identify odd alternating cycles. The least common alternating ancestor is the blossom base; both arms are marked, the base labels are contracted, and parent links retain the information required for expansion when an augmenting path is reversed. Each augmentation adds one edge. Edmonds' blossom preservation theorem and the augmenting-path characterization of maximum matchings establish the standard method's correctness; the tests below are evidence about this particular implementation, not a new proof of those theorems.

For a simple undirected graph with n vertices and m edges, total time is O(n^3) and auxiliary/graph storage O(n+m), under unit-cost vertex-index and integer operations. Each alternating BFS scans each adjacency list at most once; at most O(n) proper contractions cost O(n) each, giving O(m+n^2) per search. There are at most n searches. Input deduplication and sorting add their own processing cost: for L supplied edge occurrences, O(L + sum_v degree(v) log degree(v)) expected time with Python hash sets. Thus O(n^3) describes the simple graph algorithm, not arbitrarily many duplicate input occurrences. Python object overhead and input encoding bit costs are not included in this RAM bound.

## Reproduce

Python 3.12.14; standard library only. From this directory:

    python3 -m py_compile blossom.py
    python3 test_blossom.py
    python3 test_nested.py
    python3 test_integration.py
    sha256sum blossom.py test_blossom.py test_nested.py test_integration.py README.md

`test_blossom.py`: all 1,100 labeled graphs for 0 <= n <= 5, 2,600 seeded random graphs for 0 <= n <= 12, and 600 structured/relabelled cases. Maximum cardinality is compared with an independent exhaustive subset-DP oracle. Includes odd cycles, linked cycles, alternating stems, isolated vertices, empty graphs, complete graphs, perfect/nonperfect outcomes, 28 malformed-input checks, and 10 invalid-matching checks. Seed 20261017.

`test_nested.py`: runtime tracing independently confirms a contracted nontrivial blossom is included in a later contraction (nested blossom). It tests relabelings of a fixed nine-vertex graph, seed 715. Observed 19 contractions, including one nested contraction, across eleven relabelings; feasible matching cardinality four attains the trivial floor(n/2) upper bound.

`test_integration.py`: imports but does not modify `../base/graphic.py`; 1,200 seeded incident-forbidden-pair T-join cases, up to 12 original edges and 34 gadget vertices. Perfect matching decisions agree with both exhaustive original T-join enumeration and the independently implemented exhaustive gadget perfect-matching oracle. All 395 feasible solutions reconstruct valid original witnesses. Seed 8641027. Original module SHA256: bab4f190d75f0d0068529b944ba08a5947d931882922679e0cec878fc84451e8.

Integration scope is exactly the gadget's supported incident, pairwise-disjoint forbidden-edge pairs. This backend does not establish correctness of the reduction beyond tested instances and the separate mathematical argument. No P versus NP conclusion follows from implementing a known polynomial general-graph matching algorithm.
