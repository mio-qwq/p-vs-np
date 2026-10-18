# Binary red-block exact-count nonvanishing

Research checkpoint, 18 October 2026.

## Sufficient all-order theorem

Use the complete bipartite graph on n+n labeled vertices. Take pairwise distinct real row offsets a_i and pairwise distinct nonnegative integer column exponents e_j, in their original index orders. Set

    V_ij(lambda) = (lambda+a_i)^e_j,
    E = sum_j e_j,
    P_t(lambda) = [z^t] det[z^rho(i,j) V_ij(lambda)].

Assume all red edges lie in I x J, where |I|=|J|=k<n, and their binary incidence block B is nonsingular. Thus this is a proper square red block in a complete underlying graph; all other edges are present and blue. Put m=n-k. For every integer target 0 <= t <= k,

    deg P_t = E - binom(m,2),

    [lambda^(E-binom(m,2))] P_t
      = (-1)^(sum I + sum J + k - t) binom(k,t) det(B)
        Delta(a_(I complement)) Delta(e_(J complement))
        / product_(q=0,...,m-1) q!.

Complementary sequences retain increasing index order, and Delta(x)=product_(r<s)(x_s-x_r). Every factor in the displayed leading coefficient is nonzero, so every such exact-count polynomial is nonzero. The case k=0 uses the empty determinant and product equal to one. A proper red matching is a special case; the extension permits intersecting red edges and multiple red perfect matchings.

The proof combines a finite Cauchy–Binet leading-term calculation for full translated Vandermonde minors with the determinant-of-a-sum expansion. The unique maximal selected row/column pair has a nonzero incidence determinant and strictly dominates smaller selections in degree. This is an all-order proof under the stated assumptions, rather than an extrapolation from finite checks.

## All-red square-block addendum

A separate sufficient theorem also covers singular all-ones incidence blocks. Keep the same complete graph, real-offset and integer-exponent assumptions. If exactly I x J is red, |I|=|J|=k and 1<=k<=floor(n/2), then for every 0<=t<=k,

    deg P_t = E - binom(k,2) - binom(n-k,2),

    leading coefficient
      = (-1)^(sum I + sum J + k - t) binom(k,t)
        [Delta(a_I) Delta(e_J) / product_(q=0,...,k-1) q!]
        [Delta(a_(I complement)) Delta(e_(J complement))
         / product_(q=0,...,n-k-1) q!].

Both minors are full translated Vandermonde matrices. Selected subsets of size s have degree E-binom(s,2)-binom(n-s,2), strictly increasing through s=k in this range. The unique size-k pair therefore gives the nonzero coefficient. For k>=2 this is a singular binary block, beyond the main theorem's hypothesis. See the [separate addendum](all-red-block/PROOF.md) and its [independent audit](all-red-block/AUDIT.md).

## A nontrivial interior example

For n=6, a_i=e_i=i, and red edges (0,0), (1,1), (2,2), the exact-one fiber has 234 permutations: 117 even and 117 odd. It uses all 36 edges. The nominal coefficients of degrees 15, 14 and 13 cancel, while the coefficient at degree 12 is 6. The report gives the full polynomial and the signed cubic-moment identity. This example cannot be represented as the perfect matchings of a fixed support mask.

If m>=2, two entirely blue rows give a parity-reversing involution, so parity counts balance even though a lower coefficient survives. Full support is a separate statement: for the first k red diagonal edges, the proved interior full-support range is 1<=t<=k-2 under 2<=k<=n-2. At t=k-1, cross-edges between distinct marked vertices are absent.

## Contents

- [Detailed theorem, proof, moments, support boundary and source comparison](binary-fiber/REPORT.md)
- [Independent mathematical audit, including the square-block extension](binary-fiber/AUDIT.md)
- [All-red square-block proof](all-red-block/PROOF.md), [audit](all-red-block/AUDIT.md), [exact checker](all-red-block/check.py), and [certificate](all-red-block/results.json)
- [Separate derivation](independent/PROOF.md) and [second proof review](independent/REVIEW.md)
- [Supplied exact checker](binary-fiber/check.py) and [five-case plus singular-boundary certificate](binary-fiber/results.json)
- [Separate permutation checker](independent/check.py), [five-case certificate](independent/results.json), and [coefficient-by-coefficient raw-Laplace cross-check](binary-fiber/root-crosscheck.json)
- [Source provenance](PROVENANCE.json), [fresh checker verification](verification.json), [file manifest](manifest.json), and [release notes](RELEASE_NOTES.md)

## Reproduction and integrity

Python 3.9 or later; standard library only. No solver, network or additional package is needed. From the repository root or extracted archive:

    python3 results/binary-red-block/verify.py
    python3 -O results/binary-red-block/verify.py

The verifier checks the exact inventory, file sizes, SHA-256 hashes, checker-source preservation, and internal Markdown links. It runs the three original mathematical checkers in temporary copies, reproduces their frozen outputs, and recomputes the independent raw-Laplace comparison of every polynomial coefficient in the separate five-case certificate. It rejects deliberately altered polynomial certificates using fresh arithmetic comparisons independently of manifest hashes, and tests modified-file, missing-file, unexpected-file, and altered-manifest failures. Explicit exceptions remain active under optimized Python. Distributed files remain unchanged.

The supplied checker covers five fixed theorem examples and a singular-block boundary. The separate checker covers five fixed examples including nonprincipal indices, negative offsets, unordered gapped exponents, k=n-1, a triangular block and a block with multiple perfect matchings. The all-red-block checker covers eight exact examples and twenty target fibers, including rational offsets, nonprincipal blocks, k=n/2, k=0 and n=1, with independent permutation and selected-minor coefficient calculations. These are bounded exact checks, not a search over all binary colorings. The two implementations inside the supplied checker use direct permutation expansion and recursive raw bivariate Laplace expansion. All three original check.py files are preserved byte-for-byte. Identical optimized logs and certificate copies are omitted; provenance records their hashes and equality.

The package manifest hashes all payload files except itself and SHA256SUMS; SHA256SUMS hashes the payload and manifest. This finite self-exclusion is deliberate. Hashes detect inconsistent or damaged contents; they are not an authenticity signature and do not replace mathematical review.

## Boundaries and status

Completeness of the underlying graph, distinct real offsets, distinct nonnegative integer exponents, k<n, and det(B) != 0 are the main theorem’s hypotheses. The addendum separately requires a complete all-red square block of size at most floor(n/2). Neither result covers arbitrary missing blue edges or arbitrary red support. The report treats a perfect red matching separately; that does not extend the proper-block formula to all k=n colorings.

Singularity does not imply a zero polynomial. The all-red 2x2 block in K4,4 has exact-one polynomial

    -2 lambda^4 - 12 lambda^3 - 38 lambda^2 - 60 lambda - 24.

Its degree is 4, below the unsupported nonsingular candidate degree 5, and is exactly explained by the later all-red-block addendum. The earlier report and audits are retained as chronological source records. General singular incidence blocks and tied maximal-degree selections remain outside these sufficient results.

This checkpoint has AI-assisted derivations, independent AI-assisted proof reviews and exact arithmetic checks. There is no claim of historical novelty, human peer review, Lean or other proof-assistant verification, a general ASNC theorem or counterexample, or a P-versus-NP solution.

This is an additive local-only package under results/binary-red-block/, with expected repository base 69bf4596e885277fd60a3d597faebbfc0ec945b6. It changes no earlier result or shared index. Remote publication status is separate from local verification; no remote mutation is performed by this package's preparation or verifier.
