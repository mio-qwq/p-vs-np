# Status and dependency boundary

The current result is the nonvanishing theorem for binary 5-by-5 masks with four full rows and a nonempty remaining row. The [current proof](five-row-c12-20261018/PROOF.md) and [final independent audit](five-row-c12-audit-20261018/AUDIT.md) include the complete exclusion.

The prerequisite files in `five-row-cancellation-20261018/` are historical source documents from the earlier necessary-condition stage. Their statements that the subclass remained open, that the proof initially lacked independent review, and that an explicit d=9 candidate was still unresolved describe that earlier stage. They are preserved for provenance. The later audit checked those necessary conditions, and the current proof resolves every remaining case in this subclass. Neither statement changes the status of arbitrary five-row masks.

The theorem requires distinct real offsets, distinct nonnegative integer exponents, and a nonempty remaining row. Signed exponents occur only after a justified rational normalization. The coefficient convention is `C_k=[z^k]det[A_ij(1+a_i z)^e_j]` with `z=1/x`, and is stated in the current proof. The determinant's identity-zero property is invariant under the row/column permutations and common exponent normalization used there.

The full previous C6-C10 derivation, parity argument and independent audit are included and rerun. The prior audit also describes an ancillary d=9 example; its immutable external reference is supplied for historical context and is not a theorem prerequisite or executable dependency.

Both source reconstruction algorithms and the additional review use SymPy 1.14.0. Independent implementation means different coefficient algorithms, not human peer review or independent proof kernels. The default verifier checks exact certificate algebra and finite arithmetic only; full mode additionally reconstructs determinant coefficients and reruns all included source checks.
