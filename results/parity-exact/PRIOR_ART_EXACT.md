# Targeted prior-art addendum: exact parity AND cost 2n−3

17 October 2026. This addresses the stronger candidate under review: rho_n=2n−3 for n>=2, using a universal +2 recurrence and a monotone-extension OR-minor obstruction. It is not a proof audit. The earlier PRIOR_ART.md remains a separate record of the weaker candidate's search.

## Finding

No inspected primary source in this bounded follow-up states the exact 2n−3 parity bound for binary AND cost with free OR, negations restricted to supplied input literals, and least-fixed-point cycles. I also did not establish a published exact acyclic 2n−3 theorem in that cost model. Both historical questions remain unresolved; neither negative search result establishes novelty.

There is substantial, concrete prior art for the proof architecture: repeated literal occurrences permit elimination, while limited occurrences force a bottleneck that conflicts with parity's sensitivity under every restriction. This should be described as a gate-elimination argument or adaptation unless a fuller historical comparison supports something more specific.

## Important newly inspected primary source

Ingo Wegener, *The complexity of the parity function in unbounded fan-in, unbounded depth circuits*, Theoretical Computer Science 85 (1991), 155–170. DOI [10.1016/0304-3975(91)90052-4](https://doi.org/10.1016/0304-3975(91)90052-4). [Full primary paper hosted at Caltech](https://www.paradise.caltech.edu/ist4/lectures/AON%20circuit%20for%20parity%20Wegener%201991.pdf).

Section 4, Theorem 4.1, printed pp. 160–161, proves a 2n−1 gate lower bound for parity in the unbounded-fanin AND-type basis with negation wires free. Its induction eliminates at least two gates. The proof splits between repeated positive/negative occurrences and the situation where every variable has fan-out two. In the latter case, a first gate and the other successor of an input are analyzed using parity's continued dependence on that input after restrictions. Section 2 reviews the classical fan-in-two bounds.

This is not the candidate's cost model: Wegener's AND-type gates subsume AND and OR using internal negations, and both operations cost gates. His proof explicitly selects a first gate. It therefore does not supply a stated cyclic least-fixed-point extension or an AND-only lower bound with OR free. The occurrence/bottleneck architecture is nevertheless clearly relevant prior art.

## Useful pointer, verified against the original

Emil Jeřábek's [2014 answer](https://cstheory.stackexchange.com/questions/26026/what-is-the-minimum-size-of-a-circuit-that-computes-parity) gives a short two-gate-elimination parity argument in the same unbounded-fanin, free-negation-wire model and later credits Wegener. It assumes each literal has at most one parent after handling repetition, then uses a bottom-level gate and parity sensitivity to eliminate another gate. This answer was used to locate Wegener's original paper, not as proof of the candidate result. The thread explicitly discusses the distinction between internal negations and variable-only negations.

## Why no automatic cyclic extension has been verified

The following are methodological checks, not historical claims:

1. Acyclic proofs may select a first/bottom gate. A cyclic charged-state graph need not have one. Replacing that step by initial-activation or bottleneck reasoning is a real proof obligation.
2. Acyclic substitution preserves ordinary evaluation. In a cyclic setting, each rewrite must preserve the least fixed point, not merely the set of simultaneous solutions.
3. Counting two removed gates does not establish two removed AND states when OR is free. A translated proof must track the charged operations explicitly.
4. Dualizing gates or moving internal negations may preserve total gate count while changing AND count. That conversion cannot be silently used.
5. Treating literal rails as independent tokens extends the semantic domain beyond consistent assignments. Monotonicity may constrain this extension, but the exact OR-minor/bottleneck assertion needs its own proof. It is not supplied by the historical sources checked here.

Accordingly, I cannot say either that the classical proof automatically extends to cycles or that the extension is historically new. The independent mathematical audit should identify exactly which of these steps are newly proved in the candidate write-up.

## Other sources and unchanged historical gaps

- Cavalar–Oliveira, [published paper](https://wrap.warwick.ac.uk/id/eprint/191062/1/3718746.pdf), Theorem 30, is the existing exact bridge from cyclic AND cost to fusion-cover complexity. It is not a new ingredient. The introduction's Golovnev 2018 private-communication citation remains an especially important unresolved source for AND-cost gate elimination above n.
- Carmosino–Dang–Jackman, [arXiv:2602.17942v1](https://arxiv.org/html/2602.17942v1), treats acyclic total-binary-gate complexity and reworks Schnorr's 3(n−1) parity result. It supports a careful comparison with classical elimination and simplification, not identification of the 2n−3 theorem.
- Nakayama–Maruoka (1995), DOI [10.1006/inco.1995.1083](https://doi.org/10.1006/inco.1995.1083), remains incompletely inspected because the full article was not retrieved.
- Searches additionally surfaced negation-limited parity papers and multiplicative-complexity material. Those charge different resources; no claimed equivalence to this model was found.

## Scope and recommended wording

Searches included exact variants of “2n−3,” “2n-3,” “2n − 3,” parity AND complexity, AND-count, number of AND gates, free OR, input-only negations, monotone extension, and cyclic/loop circuits. These returned much irrelevant material. No exhaustive archival search or author correspondence was performed; no external writes occurred.

Suggested description, conditional on the audit succeeding: “We give a gate-elimination proof of the exact value 2n−3 for parity in the explicitly defined cyclic supplied-literal AND-cost model. The fusion characterization is due to Cavalar–Oliveira. The historical status of the parity bound and of its cyclic extension has not been established.”
