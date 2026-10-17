# Round 2: reproducible affine-residual branching and a state-count obstruction

**Status:** candidate-specific reproduction and falsification. This is not a proof of P=NP or P!=NP. No novelty or priority claim is made for the algorithm or the counterexample method.

**Recovery status:** `arb.py` was newly reconstructed from the retained round-1 prose specification after the cloud workspace reset. This is not byte-exact recovery of an earlier implementation. All numerical results in this directory were newly executed in round 2. Round-1 numerical claims are not being reused as fresh tests.

## Files and reproduction

Python 3 standard library only. From this directory:

    python run_growth.py
    python run_controls.py
    echo '{"n":2,"clauses":[[1,2],[-1,2],[1,-2],[-1,-2]]}' | python arb.py

`solve(cnf,n=None)` returns `(answer, Stats)`. Input clauses are signed nonzero integer literals. The optional `n` must cover the maximum variable name. Input variable names are relabelled densely before bit vectors are created, so sparse enormous names do not imply enormous arithmetic words. `max_states` is experimental instrumentation: hitting it raises an exception, never a SAT/UNSAT conclusion. An explicit DFS stack avoids Python's fixed recursion-depth limit.

Files:
- `arb.py`: exact reference algorithm, frozen SHA256 `f949e6d749959a88e73f5516fd9dc0cca61fb17d55140265cb624538eaa4f941`
- `families.py`: selector-star, pigeonhole, raw Tseitin and hidden-clause generators
- `run_growth.py`, `growth_results.json`: freshly executed state-growth experiment
- `run_controls.py`, `parity_controls.json`, `repair_controls.json`: positive parity controls and an elementary repair diagnostic
- `PROOF.md`: all-input correctness/accounting and the precise asymptotic counterfamily

Independent correctness and state-census tests are supplied by the separate checker, not substituted by these demonstration scripts.

## Algorithm, exactly

1. Densify original variable names; normalize ordinary clauses. Convert long clauses into equisatisfiable 3-CNF with fresh chain variables. Empty clauses and empty formulas retain their ordinary semantics.
2. Group clauses by their exact support of at most three variables. In lexicographic support order and then parity order 0,1, extract any complete set of clauses forbidding the wrong-parity local assignments. Replace each such block by its XOR equation, retaining other clauses. This extraction happens **once**, initially.
3. Compute deterministic reduced row-echelon form over GF(2), smallest column first. Substitute equations into each literal, represented as a coefficient bit vector plus constant whose value must equal one. Reject inconsistent equations.
4. Repeatedly remove constant-false literals, satisfied/tautological clauses, duplicate literals/clauses, and syntactically subsumed clauses. Move affine unit clauses into the equation system and repeat substitution until saturated.
5. Drop unused free coordinates and densely relabel the remaining ones in inherited order. Use the sorted remaining affine clauses as the exact syntactic cache key. A consistent equation system need not be stored in the key after substitution: the free coordinates parametrize all its solutions.
6. Select the first affine form of the first shortest clause, with coefficient-mask integer order followed by constant bit as tie rules. Branch on form=0 first, then form=1 if necessary. Memoize the Boolean result. Every branch fixes a nonconstant affine form and reduces the free dimension.

Refinements made explicit in this implementation are initial sparse-name densification, removal of unused free coordinates, and an explicit DFS stack. None uses semantic equivalence, a SAT oracle, unbounded-precision unit-cost arithmetic, advice, or uncharged preprocessing. Pure-literal elimination and component decomposition are **not** part of this frozen candidate.

## Results

On selector-star parameter k=0..10, every instance is UNSAT and zero parity blocks are extracted. The measured distinct nonterminal states are:

    k:       0   1   2   3   4    5    6    7     8     9    10
    states:  5  11  23  47  95  191  383  767  1535  3071  6143

These finite results fit `6*2**k - 1`; the theorem in `PROOF.md` only needs, and proves, the lower bound `2**k`. At k=10 the input has 97 variables, 87 clauses and 233 literal occurrences. The asymptotic input length is Theta(k^2 log k) under ordinary explicit binary-index encoding, so `2**k` is superpolynomial in the input length.

Raw even- and odd-charge K4 Tseitin controls both extract four parity blocks and finish in a single normalization call, correctly returning SAT and UNSAT respectively. Hiding each cubic clause behind a fresh auxiliary variable disables extraction and introduces branching; these are small correctness controls, not an asymptotic theorem for hidden Tseitin with renaming-aware caching.

The star counterfamily is deliberately easy for a different algorithm. Pure-literal preprocessing removes all selector/marker gadgets; all k=0..10 repair controls then use exactly five nonterminal ARB states on the fixed PHP(4,3) core. Component decomposition also isolates the fixed contradiction. Thus the result identifies an exact deficiency of the specified candidate, not an inherent failure of XOR methods or memoization.

## What is established and what is not

Established: the reference mathematical algorithm decides every finite CNF exactly; per-state work and state encoding are polynomial; its claimed all-input polynomial number of states is false, with an explicit asymptotic family robust to the implemented coordinate-renaming cache. Fresh independent tests check the implementation separately from the proof.

Not established: a polynomial upper bound for an improved candidate, a general lower bound for SAT algorithms, or a general resolution simulation of the renaming-aware cache. In particular, a known lower bound for ordinary resolution cannot simply be transferred through cached isomorphic subproblems without a proof-reuse argument.

The narrow next experiment, if another round is authorized, would add pure-literal elimination and component decomposition as a new version, then seek a connected, non-pure adversarial family. The present proof does not apply automatically to that version.

## Independent final verification

The separate checker tested the frozen solver SHA above and reported no correctness discrepancy:

- 23,376 original-CNF checks against direct assignment enumeration
- 556 pointwise parity-extractor inputs
- 2,800 affine-normalization tests
- 180 long-clause conversions, including 6,720 pointwise existential-projection checks
- Three deliberately incorrect implementation mutants detected
- Sparse 201-bit variable labels; explicit search depth 80 under Python recursion limit 50; 300 cache-toggle comparisons; and state-budget exception behavior checked
- An independently written marker generator confirmed exactly `2**k` selector-complete keys and `6*2**k-1` total states for k=0..10

These are regression and falsification tests of the implementation. The all-input correctness argument and asymptotic state-count obstruction are the separate proofs above; the finite tests alone establish neither.
