# Executable affine residual UNSAT certificates

This implements the residual certificate specified in ../affine-proof-simulation/MODEL_TRANSLATION.md, for the exact frozen arb_pc.py whose SHA-256 is:

`32ba57a17c8af1fc1045314fd89b849743bd6ba810fdfdb96f3a4ac9cde577c5`

The original solver is neither edited nor instrumented. Its source is hash-checked and executed in an isolated module namespace without writing bytecode beside it. All deliverables and generated examples are in this directory. Python standard library only.

## Commands

The default source location is `Path(__file__).resolve().parents[1] / 'affine-residual-pc/design/arb_pc.py'`, suitable for installation at `results/residual-certificates/`. Set `ARB_PC_SOURCE` to override that path during development. Overrides must still pass the mandatory frozen SHA-256 check before execution.

The packaged repository layout needs no environment override.

From this directory:

```
python test_certificate.py
python test_cli.py
python residual_certificate.py generate shared.input.json > shared.regenerated.json
python residual_certificate.py check shared.input.json shared.regenerated.json
python residual_certificate.py check component.input.json component.certificate.json
python residual_certificate.py check terminal.input.json terminal.certificate.json
sha256sum residual_certificate.py test_certificate.py *.input.json *.certificate.json
```

Input JSON is `{"clauses": [[1, -2], ...], "n": optional_integer}`. The n field must cover input labels but does not determine mask dimensions. Labels are densely renamed before any coefficient-mask construction or 3-CNF expansion. Huge sparse labels therefore cost their input encoding length, not their numeric magnitude.

Generate prints a JSON certificate and exits 0 for UNSAT; prints `null` and exits 2 for SAT. Check exits 0 for acceptance and 1 for rejection. Malformed top-level input JSON and file-access errors receive a clean rejection; internal programming exceptions are not suppressed. The programmatic checker raises InvalidCertificate on invalid certificates. Generation is exhaustive and may be exponential; this does not claim an efficient UNSAT search algorithm.

## Certificate format and replay

Top-level fields: version (integer 1), solver_sha256, root, nodes. A reference is either an exact nonnegative integer index into nodes, or JSON null for FALSE. Booleans are never accepted as integers. There is no node claiming FALSE without normalization replay. A terminal-root UNSAT certificate has null root and an empty node list.

Each node has dimension, clauses and kind. Affine literals [mask, constant] mean parity(mask) XOR constant, with constant encoded as integer 0 or 1. Branch records also have query and children. The children, in order, set query's affine value to 0 and 1; equivalently, the Gaussian equation right sides are constant and constant XOR 1. Component records have index and child. The component index refers to the frozen splitter's canonical order.

Keys use local coordinates. Multiple edges may refer to the same node, including both branch children. This does not assert a single fixed global affine query at a shared node.

The checker:

1. Recomputes dense relabeling, long-clause conversion and initial parity extraction from the original CNF; let D be the expanded variable count.
2. Checks every supplied node's exact encoding, dimension in [0,D], and masks by bit_length before dimension-indexed work. Checks reference types/bounds and strict dimension decrease on every nonterminal edge before normalizing or splitting any supplied key. It rejects unreachable extra nodes too.
3. Recomputes the root normalization and checks exact agreement. FALSE is allowed only with null; TRUE never establishes UNSAT.
4. Re-normalizes each supplied key and requires it to be unchanged. Recomputes components, enforces decomposition whenever prescribed, or checks the prescribed first affine query and replays both branch values. Each residual must match its reference exactly, including justified FALSE leaves.

Cycles cannot satisfy strict dimension descent, independently of list order. The checker does not rely on node ordering, stored semantic judgments, trusted preprocessing traces or generator bookkeeping. Its work is polynomial in input plus certificate size, given the stated frozen normalization routines; this is not a claim of polynomial certificate size in the CNF alone.

The generator is a separate iterative replay of the frozen search schedule with key memoization. For branches it retains both UNSAT children; for decomposition it retains the executed UNSAT component. It prunes irrelevant nodes, recording each retained local-coordinate key once. It supports nonterminal and terminal roots without recursive Python search calls.

## Scope and evidence

The checker deliberately shares the frozen normalizer and splitter as its specification. It is not an independent verification of every implementation detail of those routines, nor a machine-checked proof of their soundness. Tests independently evaluate original CNFs using dictionaries and truth tables and affine formulas using bit-coordinate truth tables; these are finite semantic cross-checks, not a universal correctness proof.

Tests cover:

- Every subset of all nine non-tautological clauses on two variables, including the empty clause: 512 formulas.
- Every combination of up to three nonempty width-at-most-two clauses on three variables: 988 formulas.
- 1,600 seeded random formulas, including repeated literals, tautologies and long clauses, on up to seven variables.
- Explicit shared-cache, component, sparse-label, terminal-root, parity, long-clause and safe-purity cases.
- 1,202 independent affine semantic checks, including explicit singleton/multi-coordinate purity hazards.
- Malformed dimensions, masks, constants, references and root; bool-vs-int; negative masks; huge dimensions/masks; self/two-node cycles; invalid FALSE leaves; altered query; noncanonical key; invalid components; extra/unreachable nodes; invalid input literals.
- Six malformed CLI input shapes tested for clean rejection without traceback.
- Instrumentation that makes normalization raise if invoked before structural rejection of huge dimensions, huge masks and cyclic references.

The shared example has two certificate nodes, with root children [0,0], and the unchanged solver records one cache hit. Its local shared-node query has different original-variable meanings on the two paths.

No EF, substitution-Frege, Res(⊕) or symmetry-rule proof emitter is implemented. No proof-system equivalence, simulation, separation, polynomially bounded proof size, or P-versus-NP conclusion is claimed.

The separate mathematical upper-simulation proof is in ../affine-proof-simulation/. This verifier checks residual certificates only; it does not check the generated proof-system derivation described there.
