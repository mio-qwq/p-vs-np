# Independent audit: unrestricted parity4 pair-cover number is 5

Verdict: PASS as a finite computer-assisted result for the precise unrestricted semifilter pair-cover definition. No historical novelty, public conjecture refutation, asymptotic lower bound, or complexity-class separation is asserted.

## Definition and witness validation

The carrier is U={0,1}^4; the target is odd parity; V=[0,3,5,6,9,10,12,15] is its complement. Inputs include both polarities of each of the four coordinates. A semifilter is an upward-closed collection of subsets of V accepting V and rejecting the empty set. To be above a positive x it must accept the four restricted literal sets agreeing with x. A pair (A,B) defeats a filter precisely when it accepts A and B but rejects A intersect B. These are the source definitions checked in previous audits at complexitylib2 commit ffc377b51c1faac475b8cb5376d658fec457e70a.

The independent verifier takes the 120 explicit filter masks as candidate witnesses but trusts none of their asserted properties. It checks mask bounds, distinctness, top/bottom, upward closure on every Hasse edge of the eight-element powerset, and the original above-target condition. Hasse-edge closure implies all upward closure by transitivity. All 120 pass. One filter can be associated with any positive point for which the above condition holds; its pair-defeat predicate depends only on the filter, so collapsing duplicate point/filter witnesses is legitimate.

The weight assignment is 24 to each first eight filters, 15 to each next 32, 10 to each next 24, and zero to the remaining 56, scaled by denominator 240. The total is 912. Regardless of how these witnesses were discovered, the verifier recomputes every one of the 32,896 unordered pairs A<=B and verifies that each defeats scaled weight at most 240. Unordered enumeration is complete because the defeat condition is symmetric, and includes A=B and all endpoint sets.

## Pruning proof

Suppose four pairs cover all 120 witnesses. In particular they cover the 912 weighted mass.

- Each selected column must have weight at least 912-3*240=192.
- The union of any two selected columns must have weight at least 912-2*240=432.
- Their intersection has weight at most 240+240-432=48, by inclusion-exclusion.

All weights are nonnegative, so the union bounds are necessary even with overlap or unused zero-weight witnesses. At most three columns cannot cover the total weighted mass, since 3*240<912. Repeating a pair or a duplicate coverage column cannot improve its union, hence any four-cover can be represented by four distinct coverage columns. Deduplicating columns by their entire 120-bit coverage vectors is therefore exact.

The independent implementation reconstructs 2,503 eligible pairs and 587 distinct eligible coverage columns. Its compatibility relation uses union weight at least 432 and independently checks that intersection weight is then at most 48. No valid four-cover is removed by these filters.

## Independent exhaustive search

The design artifact uses increasing-column DFS. The independent verifier instead branches on an uncovered witness having the fewest currently allowed covering columns. Each branch selects one such column and restricts future columns to those compatible with it. Earlier alternatives for the same witness are removed from later branches, partitioning possible solutions by their first selected covering alternative. A genuine four-cover must contain one of these alternatives and must satisfy all retained pairwise constraints, so the recursion is complete. The remaining weighted-capacity prune is necessary because each future column contributes at most 240. The search has no timeout and finished after 184 calls with no four-cover.

The finite conclusion follows already from this witness subset: an unrestricted cover would have to cover these 120 valid witnesses. Thus the unrestricted cover number is at least 5. No floating-point optimization, MILP infeasibility declaration, or closure-generation heuristic is used as a premise.

## Upper bound

Independently evaluated the explicit five-AND monotone supplied-literal circuit on all sixteen assignments. Its first four ANDs compute XOR and XNOR of the first two and last two bits. The fifth AND computes (u OR v) AND (NOT u OR NOT v), using the previously computed complementary rails. Its truth table is odd parity.

The five extracted negative-carrier pairs are (190,125), (215,235), (252,63), (207,243), (60,195), in eight-bit subset encoding. For each of the eight target points, an independent set-based closure starts with its matching-literal sets and V, closes upward, and closes under these five pair implications. It derives the empty set every time. Therefore any semifilter above that point must violate at least one pair: otherwise it would accept every derived set, including the forbidden empty set. This establishes the upper bound for every semifilter, not merely the 120 lower-bound witnesses. Combined with the lower bound, the exact unrestricted pair-cover number is 5.

## Reproducibility and frozen inputs

Run independent_verify.py in this directory. Output: independent_result.json. The verifier checks that source artifact hashes remain unchanged during its run.

- exact_four_search.py: f9a5b4d4e5a47146e817a5a0c40e87f1aa838a27a1d857a9bf6eac6a89e8b887
- exact_four_search_result.json: 28b54f818e224cdfa568464f7d9a9f508bf506074abea4f303cd6c012a482d87
- verify_upper5.py: fec2ac56e37f9ef763a497d8858d0b007272d8309940bcfb67d770d384cd1de9

The parent's separately implemented four-clique enumerator is additional corroboration, not a premise of this independent review. No source artifact was modified.
