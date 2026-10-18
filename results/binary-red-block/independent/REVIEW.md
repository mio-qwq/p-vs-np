# Root mathematical review

18 October 2026. Reviewed the complete mathematical report in [the full report](../binary-fiber/REPORT.md), independently derived the generalized minor formula and the nonsingular square red-block extension, and independently checked five finite instances using direct permutation expansion.

The proof uses finite Cauchy–Binet and the unique minimum exponent set 0,...,m-1. Distinct offsets and distinct integer exponents make both Vandermonde factors nonzero. For a proper red block, size-k red selections strictly dominate all smaller selections in lambda degree. The sum over size-k red matchings is exactly det B times the fixed cofactor sign; nonsingularity is essential. Extraction of the color coefficient cannot kill this term. These steps are valid for arbitrary order n, not merely the checked examples.

The parity-involution statement requires two rows without red edges. Full support for a proper red matching has the stricter interior range 1<=t<=k-2. At t=k-1, cross-edges between marked vertices are impossible. The final report correctly states this correction. The full-support n=6, k=3, t=1 example has 234 permutations, both parities, and first surviving coefficient 6 at degree 12.

In a separate fresh directory, reran the supplied independent permutation/raw-Laplace checker normally and under python -O. Outputs match exactly: results.json SHA256 d13285963f291d9d7bb446086f9b16c38cb8a51945243bf7b3d5b1ca749993c8. Its singular 2x2 control gives degree 4 instead of the unsupported nonsingular degree 5. My separate checker also covers nonprincipal index sets, negative/distinct offsets, unordered gapped exponents, k=n-1, a triangular red block, and a block with multiple perfect matchings.

This validates the stated sufficient family and explicit certificates. It does not establish historical novelty, general ASNC, general masked minors, P versus NP, or formal Lean verification. No finite experiment is used as an all-order proof. The next actual boundary is cancellation among maximal red selections when their incidence block is singular or their row/column sets differ.
