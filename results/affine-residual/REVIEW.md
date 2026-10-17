# Round 2: Independent ARB audit

## Result and exact scope
The specified affine-residual branching (ARB) algorithm passed the independent finite correctness checks below. A direct selector/star-marker family gives at least 2^k distinct normalized states on inputs of polynomial size in k, refuting a universal polynomial running-time claim for this exact branching, normalization and caching procedure. This is a candidate-specific result. It establishes neither P = NP nor P != NP.

Pure-literal elimination or independently solving connected components defeats this particular family. These operations are absent from the audited candidate; adding them creates a new candidate requiring a new analysis.

## Frozen candidate
Audited source: `../positive-design/arb.py`.
SHA-256: `f949e6d749959a88e73f5516fd9dc0cca61fb17d55140265cb624538eaa4f941`.

All final test runs were repeated after the designer froze the version containing sparse-input-label densification and explicit-stack DFS. No changes to the candidate were made by this verifier.

The algorithm converts CNF to equisatisfiable 3CNF, initially extracts complete same-support parity blocks, substitutes Gaussian equations, saturates affine units, removes syntactic tautologies/subsumed clauses, and branches on the lexicographically first form of the first shortest clause (false first). It caches canonical syntactic residual keys after dropping unused coordinates and densely renumbering remaining coordinates. Parity-block extraction occurs only initially, not at every branch.

## Independent correctness and negative controls
`exact_oracle.py` evaluates the original CNF directly over all Boolean assignments. It does not call the candidate's brute-force function, normalization, Gaussian elimination, or extraction.

Final results in `correctness_results.json`:
- 21,376 canonical original-CNF cases: every CNF on at most two variables; every three-variable CNF with at most four distinct nontautological clauses. Empty clauses and formulas included.
- 2,000 seeded random original-CNF cases with 1–8 variables, repeated literals, tautologies, empty clauses, and clauses wider than three.
- 556 extraction inputs checked pointwise over every original assignment, including all 256 subsets of the eight full-support three-variable clauses and 300 overlapping-support random formulas.
- 2,800 random affine clause/equation inputs checked against direct affine truth-table semantics. Normalization is tested for satisfiability preservation, not model-count preservation, since unused coordinates are intentionally discarded.
- 180 random wide-CNF conversions checked by existentially enumerating all auxiliary assignments for each of 6,720 original assignments.
- Three invalid input cases correctly rejected.
- Three real source-code mutations detected by failing semantic tests: wrong sign in the final 3CNF-chain clause, reversed extracted parity RHS, and omitted Gaussian constant substitution. Exact inputs and expected/incorrect answers are recorded.

`resource_edge_results.json` additionally verifies:
- Four inputs using a 201-bit sparse variable label are solved with at most one expanded variable, avoiding numeric-label-sized bit vectors.
- 300 cases give identical answers with caching enabled and disabled.
- Explicit DFS reaches depth 80 while Python's recursion limit is set to 50.
- A state budget exhaustion raises an exception and is never presented as SAT or UNSAT.

These finite tests do not constitute a proof of correctness on all inputs. The local transformations have separate elementary semantic justifications; no failure was found in the tested implementation.

## Direct selector/star lower bound
Let H be the standard fixed pigeonhole CNF PHP(4,3): 12 variables, four positive three-literal clauses, and 18 negative two-literal collision clauses. H is unsatisfiable.

For each i = 1,...,k introduce selector x_i, partner t_i, star center a_i, and i leaves b_(i,1),...,b_(i,i). Add

- (x_i OR t_i)
- (x_i OR a_i OR b_(i,j)), for j = 1,...,i.

Order variables as all x_i first, then all t_i, then H's variables, then the star variables. This is exactly the ordering in the independent generator `marker_family(k)` in `check_marker_family.py`.

There are 12 + 2k + sum_(i=1)^k (i+1) variables and 22 + k + sum_(i=1)^k i clauses. Literal occurrences and ordinary binary encoding length are polynomial in k.

### Why preprocessing does not remove the family
Every clause support occurs only once, so no parity block is extracted. There are no initial units, tautologies, or subsumptions. All affine masks are singleton variable masks and remain singleton throughout ordinary branching/unit substitution. No pure-literal elimination or connected-component decomposition is performed.

### Why all selector combinations are reached
The shortest binary clause containing each next selector has a smaller first variable than every remaining core/marker clause. Thus all selectors are processed in index order before H.

Setting x_i true deletes its gadget. Setting x_i false forces t_i true and leaves the positive binary star {(a_i OR b_(i,j)): j=1,...,i}. These stars have no units or subsumptions and are not simplified away.

At a fixed selector depth, different zero-subsets yield different multisets of all-positive binary-only connected components: star i has exactly i+1 vertices. The remaining selector components contain ternary clauses; H contains negative clauses. These features distinguish marker components even under arbitrary variable renaming, and therefore under the candidate's more restrictive dense renaming. Consequently two different selector prefixes at the same depth cannot share a key.

Across selector depths, the number of ternary clauses is 4 + sum of sizes of unprocessed stars, which strictly decreases at each selector step. Such keys cannot coincide either. Thus memoization cannot prune away distinct selector-prefix paths.

### Why selector-complete leaf keys are distinct and cannot be pre-cached later
After every selector has been set, exactly the four ternary clauses of H remain, together with a freely selected subset of the distinct-sized marker stars. There are 2^k distinct keys by the component-size argument.

Once branching enters H, at least one of its four ternary clauses disappears or shrinks, so the ternary count becomes less than four and never increases. Every nonterminal residual of H must retain a negative binary clause: otherwise it would consist only of positive clauses and would be satisfiable. Its lower variable indices therefore keep the search inside H before touching any marker star. Every leaf remains UNSAT because H is unchanged and the marker components are independent.

These observations also exclude hits against cached keys from previously explored core branches. Hence at least 2^k distinct nonterminal states are actually visited. Since input length is polynomial in k, this is a superpolynomial lower bound for this specified algorithm. The theorem relies on the structural argument, not extrapolation from the finite measurements.

## Independent measurements
`marker_results.json` records k=0,...,10. Every answer was UNSAT; every run extracted zero parity blocks. The number of selector-complete keys was exactly 2^k. Total distinct nonterminal states empirically followed 6*2^k - 1 over this tested range; the proof above only needs the lower bound 2^k.

For k=10:
- Input: 97 variables, 87 clauses, 233 literal occurrences
- Distinct nonterminal states: 6,143
- Selector-complete keys: 1,024
- Normalization calls: 12,287; cache hits: 2,048
- Maximum intermediate literal occurrences: 233
- Maximum mask bit length: 97

Thus the measured growth comes from the number of states, rather than growing per-state formulas or hidden arbitrary-precision vectors. Timing is recorded for reproducibility and is machine-dependent.

The per-state representation remains polynomial: there are at most the initial number of clauses/forms, affine masks have at most the expanded variable count in bits, Gaussian elimination and syntactic subset checks use polynomial work, and each unit-saturation pass removes a nonzero coordinate direction. Total cache storage must still count all visited keys. Even `cache=False` retains a seen-key set for instrumentation, so that implementation mode must not be described as polynomial-space.

## Hidden parity and the proof-system caveat
`hidden_parity_results.json` checks raw and hidden parity examples. Replacing each (a OR b OR c) by (a OR b OR y_C) AND (NOT y_C OR c), with fresh y_C, preserves existential satisfiability but hides all initial same-support parity blocks. The contradictory pair of XOR3 equations changes from two extracted blocks and zero branch states to zero extracted blocks and two branch states. The K4 Tseitin examples also give correct SAT/UNSAT outcomes.

This blind spot alone does not establish a running-time lower bound. In particular, dense coordinate renumbering allows memoized proof reuse under different original variable identities. One must not automatically identify cached ARB with an ordinary-resolution DAG. The selector/star argument avoids that unsupported transfer and directly distinguishes the actual cache keys.

## Reproduction
Run with Python 3 standard library:

- `python check_arb.py`
- `python check_marker_family.py`
- `python check_resource_edges.py`

The scripts use the fixed task-root candidate path shown above. No external repositories, packages, services, or publication steps are used.
