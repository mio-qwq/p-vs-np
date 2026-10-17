# Independent audit of the supported matching finite-test lemma

Verdict: correct, with no mathematical gap found, under the usual flip metric and the natural baseline-extension convention.

## Precise scope

Let B_S be a fixed matching of m distinguished pairs on a labeled vertex set V(S). All ambient baselines extend B_S by disjoint auxiliary pairs. A flip replaces two distinct matching edges on four vertices by either alternative perfect matching of those vertices. A radius-r ball means distance at most r. The function is one fixed function of the indicators of edges with both endpoints in V(S), evaluated by the same rule in every ambient space. Under these conventions, universal vanishing is equivalent to vanishing in one standard extension by r auxiliary pairs.

It would improve the statement to spell out those conventions. In particular, the conclusion is not being asserted for an alternative move called a “flip” that replaces an arbitrarily long alternating cycle in one step, or for ambient baselines that change the distinguished baseline pairs.

## Proof checks

1. The union with the baseline is a disjoint union of alternating cycles, with a common edge treated as a one-pair component. A component with k baseline pairs contributes k-1 to ordinary flip distance. The upper bound follows by splitting off one baseline edge per flip; the lower bound follows because a single flip increases the number of components in the union with the baseline by at most one. Thus the stated distance is exact.
2. An outside-only component has no vertex in V(S). Replacing it by baseline edges leaves every internal indicator unchanged and reduces its distance contribution to zero.
3. Each surviving mixed component contains a distinguished baseline pair count a >= 1 and an auxiliary count b >= 1. Its distance contribution a+b-1 is at least b. Summing over the disjoint mixed components bounds their total auxiliary pair count by r, even when components entirely in S also consume distance.
4. Choose an injection from the auxiliary pairs in mixed components to the r standard auxiliary pairs. Choose any bijection on the two endpoints of each pair and keep every distinguished vertex fixed. This preserves baseline edges, component sizes, and all matching edges internal to S. Unused standard auxiliary pairs are left as common edges. There is no collision between mapped components.
5. This construction realizes every ambient radius-r internal-indicator pattern in the standard m+r model. Therefore any function of that pattern has the same value in both realizations. The argument works over any coefficient field or ring, or without algebraic structure at all.
6. Necessity follows because the m+r model itself is an allowed ambient model. Smaller ambient models also embed by padding with common baseline edges. The padding claim is consistent, although the direct compression construction already covers them.

## Edge cases

- r=0: only the baseline is allowed; no auxiliary pair is needed.
- m=0: the function depends on no indicators and is constant; all components can be removed. The empty matching at m=r=0 causes no problem.
- Ambient size m, less than m+r, equal to m+r, or greater than m+r: all are covered.
- Common edges, components wholly inside S, and wholly outside S: each receives the correct treatment and distance contribution.
- Constants, repeated monomials, non-multilinear polynomials, arbitrary characteristic, and arbitrary functions of internal indicators: all are covered because the proof preserves the complete indicator vector.
- The statement uses a ball, not an exact-distance sphere; deleting components need not preserve exact distance.

## Independent exhaustive check

`check.py` uses only Python's standard library. It enumerates all perfect matchings on 0 through 7 baseline pairs (135135 matchings at 7 pairs). It computes the minimum distance realizing each complete internal-indicator signature. For every m=0,...,4 and r=0,...,3, all ambient models with m through 7 pairs have radius-r projection sets contained in the m+r model's projection set; equality holds whenever the ambient model has at least m+r pairs. Every check passed.

Separately, breadth-first search over actual two-edge-flip neighbors verifies the cycle-distance formula for every matching on 0 through 5 pairs. Every check passed. Machine-readable counts and outcomes are in `results.json`.

The five-pair, radius-three consequence follows conditionally from the lemma. This audit supplies no evidence that a particular characteristic-three polynomial passes the required eight-pair test.
