# Independent round-3 verification: ARB-PC

## Verdict
The frozen candidate passes the independent semantic checks below. The connected/nonpure cycle-marker family defeats its proposed universal polynomial state-count bound despite pure-literal elimination and component decomposition. The proof applies to this specified algorithm and its order-preserving dense cache. It is not a lower bound for arbitrary SAT solvers or arbitrary isomorphism-based caches and does not resolve P versus NP.

Audited source: `../positive-design/arb_pc.py`.
SHA-256: `32ba57a17c8af1fc1045314fd89b849743bd6ba810fdfdb96f3a4ac9cde577c5`.

## Semantic checks
`check_arb_pc.py` uses an independent original-CNF assignment enumerator, never the candidate's brute-force routine. All checks passed:

- 21,376 canonical CNFs: all formulas over at most two variables and all three-variable formulas with at most four distinct nontautological clauses.
- 2,000 seeded random original CNFs, including repeated literals, tautologies, empty clauses, and clauses wider than three.
- 556 extraction inputs, checked pointwise over all original assignments.
- 2,800 random affine-clause/equation inputs, checked for satisfiability preservation under normalization.
- 180 wide-CNF conversions checked by existential auxiliary-variable enumeration for 6,720 original assignments.
- Three invalid input cases rejected.
- Three implementation mutants detected: incorrect chain sign, extracted parity RHS, and Gaussian constant substitution.

`check_repairs.py` adds 3,000 nonunit affine-input tests and 500 deliberately disjoint affine-input tests. Component conjunction agrees with direct truth-table satisfiability. Explicit SAT/SAT, SAT/UNSAT and UNSAT/UNSAT component cases exercise the actual solver's AND control flow.

Two additional real mutation controls were detected:

1. Allowing a coordinate inside a multibit affine form to be treated as an ordinary pure literal changes a satisfiable five-coordinate test into UNSAT. The recorded witness forces x XOR y and y true while requiring x OR q; safe purity may set q, but must not independently force x or y.
2. Combining independent components by OR instead of AND incorrectly declares a satisfiable implication cycle conjoined with PHP(4,3) satisfiable.

Purity is tested for existential satisfiability preservation, not pointwise preservation of eliminated coordinate values. No finite test count is presented as an all-input correctness proof. The new rules' semantic justifications were also reviewed directly: eligible pure coordinates affect no other affine forms, and component supports include every coordinate in every affine literal after equation substitution.

## Independent counterfamily
`connected_family.py` was independently written before the designer adopted the construction. Let H be fixed PHP(4,3), and let h be its least-index variable. For each i add selector cycle x_i -> u_i -> v_i -> x_i, marker cycle h -> a_i -> b_i -> h, and clause (x_i OR a_i OR b_i). An implication p -> q is encoded as (NOT p OR q).

Indices are ordered: all x_i, then u_i/v_i, then H's variables, then a_i/b_i. Counts are 12+5k variables, 22+7k clauses, and 48+15k literal occurrences. Binary-index input length is Theta(k log k). Every formula is UNSAT because H is a conjunct.

No complete initial parity block occurs. The support graph is connected, every variable occurs with both polarities, and there are no units or syntactic subsumptions.

After the first d selectors have been assigned, the exact normalized residual has unchanged H, all marker cycles, remaining selector cycles/gates, and optional (a_i OR b_i) exactly for processed selectors assigned false. Selector-cycle unit propagation deletes the same three variables independently of the chosen value. All marker coordinates remain. There are still no pure coordinates or component splits.

The prescribed clause/coordinate ordering branches on the next selector. At the same depth, the surviving coordinate list is identical across paths; distinct optional-clause subsets therefore give distinct exact dense syntactic keys. At different depths the number of ternary clauses is 4+k-d, distinguishing the stages. This establishes distinct prefixes, not merely distinct hypothetical leaves.

After all selectors, the first subsequent branch touches a core variable, possibly h through a marker clause. It shrinks or removes one of H's four positive ternary clauses. Descendants have at most three ternary clauses: all affine masks here remain ordinary singleton masks, and branching, unit substitution, purity and decomposition never add clauses or increase their lengths. Such descendants cannot collide with any selector-stage key, all of which have at least four ternary clauses. No earlier cache hit can suppress a new selector prefix.

Consequently the complete selector tree is reached: at least 2^k distinct selector-complete nonterminal keys, in fact at least 2^(k+1)-1 selector-prefix keys. Since input size is Theta(k log k), this is a superpolynomial state lower bound for this fixed candidate. It follows from the structural invariant and cache argument, not curve fitting.

## Independent execution evidence
`check_family_invariants.py` independently applies ordinary restriction and unit propagation, without calling ARB-PC. For k=0 through 8 it checked 1,013 selector prefixes: all are connected, nonpure, retain all marker variables, have the predicted optional clauses and ternary count, and have distinct dense keys. Removing one marker-cycle edge serves as a negative control and exposes a pure variable as expected.

`check_growth.py` separately instruments the frozen repaired solver. For k=0 through 10 it verifies exactly 2^k selector-complete keys and 2^(k+1)-1 selector-prefix keys. Every observed selector-stage normalization performs zero pure assignments and has one support component. All runs return UNSAT with zero extracted parity blocks. Total observed states are 2^(k+1)+1 in this finite range; this stronger exact formula is not needed or claimed as a general theorem.

At k=10, input has 62 variables, 92 clauses, and 198 literal occurrences; 1,024 selector-complete keys are visited. The maximum literal count remains bounded by input literal count. This is state proliferation, rather than a hidden exponential per-state representation.

## Essential boundary
The markers are symmetric. An arbitrary variable-isomorphism canonicalizer can merge equal-cardinality subsets; the lower bound is specifically for the implemented order-preserving dense renaming.

Implication-SCC preprocessing also defeats this family: the selector cycles imply x_i=u_i=v_i and marker cycles imply h=a_i=b_i. Identifying those variables collapses gates to (x_i OR h); purity removes them, leaving fixed H. This construction does not survive that stronger preprocessing. It provides a precisely scoped candidate refutation, not an obstruction to all affine methods or all SAT algorithms.

The designer's `PROOF.md` was independently read and agrees with these qualifications and the frozen implementation. All files here are local verification artifacts; no publication or repository changes were performed.
