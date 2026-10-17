# Verification and scope record

On 17 October 2026 all four commands in README.md were run from this portable result directory and exited zero. The accompanying four JSON files are their actual output. They cover 1,800 random local-CNF/XOR tests, 500 clause-copy checks, 3,500 exact syndrome-set quotient tests, all 4,096 3-by-3 binary-map/deleted-point combinations, candidate-specific exponential controls, and the five-anchor truth table.

Both prototypes and all four test programs are byte-identical to their supplied source artifacts. No external workspace paths or imports needed changing. RESULT.md and README.md are also copied unchanged. CLAUSE_OBSTRUCTION.md is the independently reviewed root proof. INDEPENDENT_AUDIT.md explicitly excerpts only the relevant sections of a broader audit, without changing their mathematical text.

The additional anchor truth table is a small negative control explaining an easy repair of a frozen-heuristic example. No selector/Tseitin lower-bound packet is included or newly claimed here. The result is the sound syndrome-period quotient and its precise single-clause occurrence-encoding obstruction. Alternative grouping, preprocessing, ordering and representations remain outside that obstruction. The quotient implementation returns a decision, not a reconstructed witness.

Review was AI-assisted; no human peer review, Lean/formal proof, novelty claim or resolution of P versus NP is asserted. Finite regressions support the implementation; the general claims rely on the written proofs.
