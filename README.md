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

## Reproduction and recovery

Use Python 3, standard library only. Each result directory states its commands and limitations. SHA256.json hashes all tracked checkpoint files except itself. Checks may regenerate their adjacent result logs; timing fields are environment-dependent.

The unpublished first working environment was lost. Current algorithm code was reconstructed from retained specifications and tested afresh; this repository does not pretend to recover old uncommitted bytes or reuse old tests as new runs.

AI systems contributed substantially to derivation, implementation, review and documentation. Releases freeze scoped research records, not a Millennium-problem solution.
