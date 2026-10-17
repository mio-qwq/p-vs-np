# Round 3: safe purity, component decomposition, and connected padding

Status: verified candidate-specific obstruction, not a P versus NP result. No historical novelty or priority claim is made. Round 2 remains frozen; this directory contains a separate solver version and newly executed experiments.

## Reproduce

Python 3 standard library only:

    python run_experiments.py
    echo '{"n":2,"clauses":[[1,2],[-1,2],[1,-2],[-1,-2]]}' | python arb_pc.py

`solve(cnf,n=None)` returns a Boolean answer and statistics. Literals are signed nonzero integers. Sparse variable labels are densified before bit-vector allocation. A state-budget exception is never interpreted as a SAT answer. The explicit DFS stack handles both branching and component conjunction without a fixed recursion-depth limit.

Frozen solver SHA256:

    32ba57a17c8af1fc1045314fd89b849743bd6ba810fdfdb96f3a4ac9cde577c5

Files: `arb_pc.py` is the solver; `families.py` contains generators; `run_experiments.py` reproduces `growth_results.json` and `repair_controls.json`; `PROOF.md` states the exact boundary and proof.

## Exact repair

The solver retains round 2's initial complete parity-block extraction, Gaussian substitution, affine-unit propagation, syntactic subsumption, deterministic shortest-clause branching, and dense-coordinate syntactic memoization. It adds:

1. Safe pure-coordinate elimination. A free coordinate is eligible only when every occurrence is a singleton affine literal with the same polarity. Any occurrence inside a multi-coordinate affine form disqualifies it. Eligible coordinates are assigned their satisfying value; normalization repeats.
2. Component decomposition. After normalization, all coordinates appearing anywhere in the same clause are joined. Disjoint coordinate-support components are solved independently and their answers combined by AND. Components are ordered by dimension, clause count and canonical key.

SCC implication-equivalence detection, arbitrary variable-isomorphism canonicalization and recursive parity-block re-extraction are not included. The purity rule is existentially satisfiability preserving, not pointwise equivalence on discarded pure variables.

## Connected, nonpure family

The independently proposed checker construction adds selector implication cycles and marker implication cycles to a fixed PHP(4,3) contradiction. Marker cycles share one core variable h. A selector controls whether a binary marker clause is retained, but every marker variable remains present in either branch. Before core branching, all residuals are connected and every variable occurs with both polarities. Thus the two new preprocessing rules cannot remove the selector search tree.

For parameter k, the family has 12+5k variables, 22+7k clauses, and 48+15k literal occurrences. The proof establishes at least 2^k distinct reached nonterminal keys for the exact implemented cache. Its explicit binary-index input length is Theta(k log k), so this is superpolynomial, equivalently at least 2^{Omega(L/log L)} along the family. It is not asserted to be 2^{Omega(L)} in bit length.

Fresh runs k=0..12 returned UNSAT with zero parity-block extractions and zero component splits. State counts were:

    3, 5, 9, 17, 33, 65, 129, 257, 513, 1025, 2049, 4097, 8193.

The observed identity `2**(k+1)+1` is not needed by the proof. At k=12 the input has 72 variables and 106 clauses.

## Repairs and stopping point

The old selector-star family now collapses to three nonterminal states for every tested k. Conversely, the new family's directed implication cycles force explicit variable equalities. Substituting those equalities and applying purity also collapses it to the same three-state core. `collapse_family_cycles` in the experiment script is a documented family-specific identity substitution, not a claimed general SCC implementation.

This closes the requested test of pure-literal elimination plus component decomposition. The obstruction still exploits a missing standard simplification. Continuing to add standard preprocessors and design padding against each would not by itself provide a credible route to a general polynomial-time SAT algorithm. This incremental route stops here pending a genuinely new structural invariant or a separate precisely stated research target.

The result does not establish hardness for all XOR-aware solvers, semantic caches, arbitrary-isomorphism caches, or SAT algorithms.
