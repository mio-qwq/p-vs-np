# P versus NP research

**Neither P=NP nor P≠NP is proved here.** Two exploratory directions are developed with cross-checking: exact SAT algorithm candidates and lower-bound formulations.

## Verified scoped checkpoints

- [Affine residual branching](results/affine-residual/README.md): an exact XOR-aware SAT candidate and an explicit family refuting its proposed polynomial state bound. The family defeats this specified algorithm, not all SAT algorithms; elementary preprocessing repairs this family.
- [Pair-state unrolling](results/pair-state-unrolling/README.md): a checked reproduction/application of the known quadratic fusion bound to a pinned public compiler, with k-round convergence, at most k² AND gates, and a precise nonuniform circuit lower-bound target. No required superpolynomial lower bound is proved.

Both checkpoints have written proofs, separate AI-assisted reviews, executable checks and negative tests where applicable. No human peer review, formal verification of these new statements, or historical-priority claim is made.

[The initial research plan](RESEARCH_PLAN.md) records the earlier threshold-circuit route. Its parameter analysis remains preliminary and is not a new lower-bound result. The present dual-direction checkpoint supersedes a one-route interpretation of that plan.

## Further scoped checkpoints

- [Connected nonpure ARB-PC obstruction](results/affine-residual-pc/README.md): a superpolynomial-state family survives the specified purity/component repair but not stronger SCC or arbitrary-isomorphism methods.
- [Radial witness obstruction](results/radial-witness-obstruction/README.md): exact parity3 cover certificates and an infinite-family proof that radial threshold witnesses cannot give large cover lower bounds on power-of-two parity dimensions. This refutes a proposed strategy, not an existing public conjecture.

[Exact parity4 benchmark](results/parity4-cover/README.md): unrestricted semifilter pair-cover cost is exactly 5, certified by an explicit upper construction and three exact lower-bound checks. This is a finite result, with historical novelty unverified, not a scalable circuit lower bound.

## Reproduction and recovery

Use Python 3, standard library only. Each result directory states its commands and limitations. SHA256.json hashes all tracked checkpoint files except itself. Checks may regenerate their adjacent result logs; timing fields are environment-dependent.

The unpublished first working environment was lost. Current algorithm code was reconstructed from retained specifications and tested afresh; this repository does not pretend to recover old uncommitted bytes or reuse old tests as new runs.

AI systems contributed substantially to derivation, implementation, review and documentation. Releases freeze scoped research records, not a Millennium-problem solution.

## Cyclic parity recurrence

[Audited proof and tests](results/parity-recurrence/README.md): an odd-arity strengthened gate-elimination recurrence, yielding a linear lower bound for cyclic supplied-literal AND complexity and exact five-bit cost7. Historical novelty remains unverified; this is not a P-versus-NP separation.

## Exact parity cost for all arities

[Full proof and independent audit](results/parity-exact/README.md): cyclic supplied-literal AND cost and unrestricted semifilter pair-cover cost of m-bit parity are exactly 2m-3 for m>=2. This strengthens the preceding odd-arity recurrence. Historical novelty remains unverified; parity is a linear-size-circuit problem, not a P-versus-NP separation.

## Route boundaries

[Audited next-step limitations](research/route-boundaries/README.md): an unbounded gap for the explicit minimal canonical witness class, and the uniformity/quantifier obligations for a genuine SAT-cover algorithm. No such algorithm is supplied.

## Residual certificate verification and proof-model comparison

- [Executable UNSAT certificate generator/checker](results/residual-certificates/README.md), with independent finite semantics and malformed-input tests.
- [Polynomial SF/EF upper-simulation construction](results/affine-proof-simulation/README.md), independently reviewed at proof-template level; no proof emitter is claimed.
- [Hidden-Tseitin route obstruction](results/tseitin-cache-obstruction/RESULT.md): low polynomial-calculus degree and a cache-conflict reuse counterexample; no asymptotic solver lower bound or new SAT algorithm.

## Syndrome-period route checkpoint

[Exact quotient and occurrence-clause obstruction](results/syndrome-period-obstruction/README.md): local translation periods can be quotiented soundly, but the quotient is trivial for strict single-clause occurrence blocks whose variables all repeat. Exact interface enumeration can still be exponential. This bounded research checkpoint records a route limitation, not a general SAT algorithm or a lower bound against every algorithm.

## Graphic-coupling research checkpoint

[Local quotas, graph certificates and representation criteria](results/graphic-coupling/README.md) package a blossom-backed restricted solver, exact pair-sum/common-star criteria and sharp locality boundaries. The incident-pair case is credited as a direct corollary of Cannon–Ishaque–Tóth (2012). Code verifies supplied graph certificates; automatic general recognition remains a classical theorem-level dependency. This does not solve general SAT or P versus NP.

## Sharp permutation-polynomial support radius

[Field-uniform proof and independent audit](results/sharp-permutation-radius/README.md) establish the exact radius min(n,2d+1) for degree-d functions on all permutation matrices, with constant/trivial-group exceptions. This sharpens Derksen's stated sufficient 3d bound; historical novelty remains unverified. The complete-bipartite parity-search consequence is XP (polynomial for each fixed k), with no general SAT or P versus NP conclusion.
