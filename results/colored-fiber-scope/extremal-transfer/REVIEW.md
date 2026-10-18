# Review scope and transfer boundary

18 October 2026. AI-assisted mathematical cross-review.

The [support-mask report](../support-mask/REPORT.md) establishes equivalent support-union, potential, alternating-cycle, and face criteria. Its diagonal-red K3,3 example has a nonempty target-one fiber, a fractional vertex of the sliced polytope, and a private-edge certificate for proper-support minimality. The eight-edge global support minimum concerns arbitrary graphs; it is not a connected-brace minimum. Direct expansion gives P1(x) = -3x^3 - 9x^2 - 9x - 2.

The source's Theorem 2.7(iii) asserts the sliced-polytope vertex identity contradicted by this example. Adding nonemptiness or the intended brace assumption does not repair that identity. The example does not refute ASNC.

The [extremal-transfer proof](RESULT.md) uses assignment duality and block factorization. Its finite checker verifies 31,380 exact minimum/maximum fiber-to-mask equalities through order three; these checks supplement the general duality proof.

The package verifier reproduces the current support certificate and all three supplied checkers in clean temporary storage. Fresh normal and optimized receipts are in `../verification.json`. The final frozen support checker additionally examines all 512 binary 3-by-3 masks and obtains determinant values {-2,-1,0,1,2}; this corroborates the leading-coefficient obstruction to accidental equality with P1. Its final normal and optimized reruns both produce results SHA256 `6037ae9402f627e9163f96850f5fb476edf28b15830975bced112f97a335b1b1`. This current certificate supersedes the earlier review's pre-extension digest.

The transfer remains restricted to support-representable fibers. Extending it to nonrepresentable interior fibers requires an additional argument controlling signed cancellation. The uncolored determinant theorem does not settle this missing colored step. This cross-review is not human peer review, Lean verification, or another proof-assistant certification.
