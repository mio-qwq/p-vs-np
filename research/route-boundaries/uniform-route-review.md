# Independent audit of the uniform SAT-cover route

Verdict: PASS for the corrected document. This identifies the exact outstanding algorithmic obligation and rejects a projection shortcut; it supplies no new SAT algorithm or separation.

## Correction found and verified

The first version required only a polynomial-time-decodable CNF encoding. That condition alone is insufficient to infer P=NP from polynomial-time decision of the encoded language: exponential padding can make exhaustive assignment search polynomial in padded length, while decoding remains efficient. The designer corrected the premise to a standard polynomial-overhead encoding polynomial-time intertranslatable with ordinary CNF SAT, explicitly including polynomial-time encoding with polynomial output length. I inspected the corrected text and verified its hash below. The issue is closed for that version.

## Main claims

1. The distinction between assignment evaluation and SAT decision is correct. Given one CNF F, a small circuit for a->F(a) and the corresponding cover already exist uniformly. This does not decide whether any satisfying a exists. The length-m SAT target instead takes the formula-encoding bits themselves as its inputs.

2. One polynomial-time generator of explicit polynomial-size pair-state wiring, correct at every input length and every encoded string, gives a polynomial-time SAT decider. The encoding premise then yields P=NP. With k states, each of k rounds evaluates k ANDs and O(k(m+k)) read work; the final read costs O(m+k). The stated O((k^2+1)(m+k+1)) bound safely covers this, including k=0. Pointwise Boolean monotonicity makes the bottom trajectory increasing and stable by k rounds. No SAT membership or subset oracle is required once the explicit flags are supplied.

3. Conversely, a polynomial-time SAT machine can be uniformly unrolled into polynomial-size circuits. Double-railing removes internal negations. OR-only dependencies can be flattened by reachability among input literals, constants and AND-state outputs in polynomial time; distinct selected sources are recorded once, so formula-tree explosion is unnecessary. The resulting acyclic network is within the specified cyclic format and has polynomially many explicit flags. Thus the executable-wiring target is genuinely equivalent to polynomial-time SAT, rather than an independently established shortcut.

4. Nonuniform existence of polynomial-size covers/wiring supplies polynomial-size circuits, hence SAT in P/poly, through the previously audited polynomial unrolling. It does not supply a polynomial-time generator. The converse also follows from circuit-to-cover extraction and double-railing. This distinction is correctly maintained; the finite flags do not become uniformly computable merely because they exist.

5. The subset-test warning is valid. For explicit polynomial-time circuit/CNF predicates on an ordinary Boolean cube, a failed inclusion has a polynomial witness, and inclusion is coNP-hard already for A equal to a CNF's satisfying set and B empty. That coNP classification is for this explicit-predicate setting; arbitrary semantic sets or domains themselves defined using SAT can require additional oracle resources. The document does not assume such tests are efficient and explicitly restricts its hardness conclusion to general succinct inclusion, not every special endpoint family.

6. Naming T_m semantically is not an executable representation of its membership predicate. The corrected route insists on explicit finite wiring, so no efficient SAT membership or semantic subset operation is smuggled into the stated sufficient target. The actual source compiler's classical choices remain an obligation for any proposed uniform construction.

## Exact projection counterexample

Nonemptiness preserves union but not intersection. A={1} and B={0} are nonempty while their intersection is empty. Equivalently, (x) AND (NOT x) is UNSAT although each clause is separately satisfiable. Replacing point-local clause membership with independent nonemptiness bits changes existential quantifier scope and loses consistency of the assignment.

Reran check_projection.py without modification, saving reproduced_projection.json in this review directory. Its output is byte-identical to the supplied result. The enumeration contains all CNFs with at most three distinct non-tautological clauses on one, two, or three variables, including empty clauses/formulas: 3,442 formulas, 26,968 assignment evaluations, and 122 false positive shortcut answers. The direct mathematical counterexample establishes the failure; finite testing is corroboration, not a lower bound.

## Exact source hashes

Reviewed corrected ROUTE_AUDIT.md:
4b23a9fb2f9a531268f8c5905ff336eb8e7b805fd647265f9b1bd8fca6542bfd

check_projection.py:
329ded3bc0da458b4c05c821dd9c522ce47e2d0e561460fceffc396aa6dbce70

projection_results.json:
27fc623465c1634cef5b94e868c70c107583663244db346523a941f32fd5d64a

The initial document, before the encoding correction, had SHA256 7d16ccc1b72a5ca76f085270f9ee0389742e4df5686495419ba7ee66a97be1f6. This review's PASS applies to the corrected version. I did not edit source artifacts or perform external writes.
