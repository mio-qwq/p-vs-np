# Source and audit receipt

19 October 2026 UTC. No remote content was changed.

## Frozen local sources audited

- `constructive-cost-audit-20261019/PROOF.md`: SHA-256 `dcc8c31b8089326410a008bcd40222171654db9e7fbe716be331f1a3e41bf0b1`.
- Its `check.py`: SHA-256 `dcbf1171d6e7e981848177d686233bbb5d3712a0abb92e92d62b8d49f94bb119`.
- `fixed-depth-hull-obstruction-20261018/proof-and-certificate/general-theorem.md`: SHA-256 `a02a5125b5905d9127cc698c64156572b53a20ab32243ffa6238859472fc957b`.

The constructive-cost proof was read in full and independently audited. Its checker was run normally and with Python -O; both passed. This package's newly written generic matching enumerator separately checks the C6 count support and compatible gluing, the 3DM gadget, and the nonzero-signature construction.

## Primary external anchors

1. Richard M. Karp, *Reducibility among Combinatorial Problems* (1972), pp. 85–103, DOI https://doi.org/10.1007/978-1-4684-2001-2_9. The publisher record was opened. The web search index of the original-paper scan at https://www2.seas.gwu.edu/~simhaweb/champalg/tsp/papers/KarpOriginal.pdf supplied the precise definition of problem 17, 3-Dimensional Matching, and problem 18, the exact-sum Knapsack formulation. Direct retrieval of that scan exceeded the web tool's size limit. These standard NP-completeness facts are the imported complexity anchors; the reductions in this package are independently proved.
2. Florian Hörsch, András Imolay, Ryuhei Mizutani, Taihei Oki, and Tamás Schwarcz, *Problems on Group-Labeled Matroid Bases*, ICALP 2024, Theorem 4.2. Opened the official full PDF and checked the theorem's hypotheses: two matroids represented over one field, finite abelian group given by its operation table, and forbidden label set. The stated randomized algorithm is polynomial in that representation. URL: https://drops.dagstuhl.de/storage/00lipics/lipics-vol297-icalp2024/LIPIcs.ICALP.2024.86/LIPIcs.ICALP.2024.86.pdf . The direct Fourier-determinant derivation in PROOF.md separately establishes the parameter dependence needed here.

No conclusion about current complete derandomization status is drawn from a failed literature search. No novelty claim is attached to the reduction or automaton construction. The output is a scoped mathematical audit, not a proof-assistant-verified result.

## Cross-check coordination

The constructive-cost researcher confirmed the exact U-ASNC and bit-cost scope. The structural and adversarial researchers reported only restricted Vandermonde mask results, with no arbitrary-mask or multi-XOR solver. These restrictions are preserved in this report. The root independently derived the layered-DAG path-to-matching construction; its bijection agrees with Section 3. All findings were exchanged with both research pairs before finalization.
