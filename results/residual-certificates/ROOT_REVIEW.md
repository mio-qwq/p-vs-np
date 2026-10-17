# Additional source review and reproduction

Root independently inspected the generator and verifier, including terminal-root handling, component short circuit, shared local-coordinate references, strict rank rejection, exact bool-versus-int checks, sparse-label preprocessing and replay of every FALSE token. No soundness gap was found relative to the frozen normalizer specification. The normalizer itself is shared code, as prominently disclosed.

The complete finite semantic test suite, malformed CLI tests, generation of the shared example, and checks of shared/component/terminal certificates were rerun from the packaged relative layout. All final commands passed. One initial CLI command used the nonexistent name shared.cert.json and was rejected; rerunning with shared.certificate.json / regenerated output passed. This was a filename error, not an accepted invalid certificate.

Independent truth-table tests and corruptions are evidence about the implementation, not a machine-checked universal soundness proof. The mathematical rank induction and normalization arguments remain separate.

## Transparent CLI fixup before release

After the initial main commit, root acceptance found that a valid contradictory CNF using a5000-digit sparse variable label hit Python's default4300-digit decimal conversion cap before dense preprocessing. No invalid certificate was accepted. The follow-up commit explicitly configures arbitrary-precision decimal conversion only in the CLI before parsing/serialization; library import does not modify its caller's setting. New subprocess regressions accept the valid sparse-label input and reject a5000-digit supplied certificate dimension before normalization. Both the original suites and new regressions were rerun successfully. This does not allocate coefficient vectors by original label magnitude.
