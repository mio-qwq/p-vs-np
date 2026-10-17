# Independent audit: syndrome route excerpts

Selected verbatim sections of the independent AI-assisted audit dated 17 October 2026. The unrelated parity/proof-model and selector/Tseitin-family sections are omitted. The stabilizer refinement was reviewed mathematically and at source level; its executable tests were not independently rerun by that reviewer. The packaged tests were separately rerun during publication preparation.

## 3. Affine block-syndrome candidate

Suppose variables are partitioned into ordered blocks, each local CNF uses only its block, and the remaining cross-block constraints are Ax=b over GF(2). Let U_i be the span of columns in the processed blocks and V_i that of the unprocessed columns. The exact reachable prefix syndrome set can be pruned to

    S_i ⊆ U_i ∩ (b+V_i).

If nonempty, this intersection is an affine coset of U_i∩V_i, hence has at most 2^w elements for w=max_i dim(U_i∩V_i). Enumeration of at most 2^t assignments in the next block, where t is maximum block size, gives O(k·2^(w+t)·poly(L)) time. Pruning is necessary-only feasibility against the suffix linear equations; local future CNF feasibility is recovered by subsequent transitions, so this does not claim Gaussian elimination solves those clauses. Empty initial intersection correctly rejects b outside the full column span. The final suffix span is zero, enforcing syndrome b.

For arbitrary CNF encoded with one copy per occurrence and equality-star equations between copies of each original variable, each variable's d columns are

    e_1, ..., e_(d−1), e_1+...+e_(d−1).

These form a single binary matroid circuit (including the zero-column d=1 case separately). Any proper subset is independent and the full rank is d−1. A cut splitting the copies has intersection dimension 1 by the rank identity; an unsplit group contributes 0. Different original variables have disjoint row supports, so dimensions add. Consequently w is EXACTLY the number of original variables appearing on both sides of the block cut. This is a rigorous obstruction to claiming that the occurrence-copy encoding always has logarithmic width. It does not prove that no better encoding or ordering can exist.

Independently enumerated every partition of d columns for d=1,...,10: 2,046 checks, all agree with the identity.

### Stabilizer quotient

Read the worker's `stabilizer_dp.py`. Normalize each explicit local syndrome set S_i by a representative s_i, obtaining T_i containing zero, and replace b by b+Σs_i. The translation stabilizer H_i={h:T_i+h=T_i} is a vector subspace. Since 0∈T_i, every period lies in T_i and exhaustive membership checks over that set find it exactly. Quotient by H=ΣH_i. Any original solution projects to a quotient solution. Conversely a quotient solution has error h∈H; write h=Σh_i and shift the i-th local choice by h_i. Every shifted choice remains in T_i and the total error cancels. Thus quotienting by the sum of local stabilizers is sound even though an individual H_j need not stabilize every other T_i. Tracking set representatives and linear decomposition coefficients supports witness reconstruction.

This is an exact strengthening of the bounded-width algorithm, with cost polynomial in the explicit local sets before the remaining potentially exponential syndrome DP. A three-element set has trivial stabilizer because a nonzero translation pairs its members; odd cardinality forbids that. The worker's repeated independent sets {0,e_(2i),e_(2i+1)} therefore survive quotienting and have 3^k distinct feasible middle sums under the duplicated ordering. Pair-adjacent ordering/decomposition avoids this barrier; it is not a universal algorithmic lower bound.

## 6. Single-clause stabilizer dichotomy

Reviewed the root note `stabilizer_clause_obstruction.md`. For a clause on k≥1 distinct variables, deleting its sole falsifying assignment from a noninjective linear map domain leaves every nonempty fiber inhabited, so its feasible image is the full linear image. For an injective map, the image has precisely one missing point. Any period belongs to the image subspace (difference of two feasible elements), and must fix its singleton complement, hence is zero. This includes k=1. An empty clause k=0 should be rejected as an empty feasible set before applying this nonempty-set argument.

For equality-star occurrence encoding, a clause whose distinct variables all have at least two occurrences has injective local coupling: its columns are nonzero and lie in disjoint original-variable row blocks. Thus the quotient does nothing to those single-clause feasible sets. If a variable occurs just once, its zero equality column creates a lost local direction; deleting one falsifying assignment then leaves the full image, in accord with ordinary pure-variable satisfiability elimination. This verifies the claimed representation-specific dichotomy without extending it to arbitrary block grouping or preprocessing.
