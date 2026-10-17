# Initial research direction

Status checked 2026-10-17. P versus NP remains unresolved; this repository currently has no new separation theorem.

## Selected bounded question

Reconstruct the parameter constraints in Chen–Tal–Wang's depth-two threshold-circuit analysis, then determine whether any improvement is possible by parameter optimization alone or requires a new structural lemma. This is a proposed investigation, not a claim that such improvement exists.

Baseline: [ECCC TR26-039](https://eccc.weizmann.ac.il/report/2026/039/), March2026, proves a gate lower bound of n^(2.5−epsilon) against THR∘THR for a function in E^NP, via an acceptance-probability estimation algorithm faster than exhaustive search. The parameter epsilon is fixed: substituting an n-dependent epsilon without uniform control of constants and thresholds is invalid.

A distinct July2026 result of [Ren–Williams](https://arxiv.org/abs/2607.09963) obtains near-maximal general-circuit lower bounds for exponential time with promise-MA queries and one advice bit. The oracle, advice and complexity class cannot be silently removed.

[ECCC TR26-167](https://eccc.weizmann.ac.il/report/2026/167/) reports near-cubic **wire** lower bounds and includes public discussion. Gate count and wire count are different resources. This report requires its own proof/dependency review before being used as a trusted improvement baseline.

## Acceptance criteria

1. State the exact machine/circuit model, uniformity, gates versus wires, and every asymptotic quantifier.
2. Reproduce the original parameter constraints and runtime without numerical extrapolation.
3. If no improvement follows, identify the blocking inequality precisely rather than claim a lower bound on all possible methods.
4. A new lemma must have a complete proof; finite computations are discovery/certification tools only within their stated scope.
5. Check literature and actual formal theorem hypotheses before priority or verification claims.

## Logical boundaries

Proving NP is not contained in P/poly would imply P!=NP, but is stronger than that separation. Lower bounds for a restricted circuit family, or for a much larger complexity class, do not suffice.

Relativization, natural-proofs and algebrization barriers constrain specific methods. The natural-proofs obstruction uses strong pseudorandomness assumptions. None is a proof that P versus NP is unresolvable.

Sources: [Clay](https://www.claymath.org/millennium/p-vs-np/), [Baker–Gill–Solovay](https://doi.org/10.1137/0204037), [Razborov–Rudich](https://eccc.weizmann.ac.il/eccc-reports/1994/TR94-010/index.html), [Aaronson–Wigderson](https://www.scottaaronson.com/papers/alg.pdf).

This plan was prepared with substantial AI assistance. It is a research roadmap, not a mathematical result or a formally verified proof.
