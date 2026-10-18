# A symbolic order-four masked-minor theorem

18 October 2026 (UTC). Scope: an auxiliary uncolored masked determinant only.

## Result

**Theorem.** Let η be any binary 4×4 matrix with a perfect matching. Let a₀,a₁,a₂,a₃ be distinct real numbers, and let d be a nonnegative integer. Then

    det[ηᵢⱼ (x+aᵢ)^(d+j)] (j=0,1,2,3)

is a nonzero polynomial.

This establishes the intended monic masked-minor criterion for every order-four mask when the column exponents are consecutive. The existing order-at-most-three theorem permits arbitrary distinct nonnegative exponents. This is a complete exact symbolic classification of the order-four support patterns, not a finite sampling of offset values.

The theorem does **not** establish arbitrary gapped exponent sets in order four or arbitrary orders. It does not imply any P-versus-NP conclusion.

## Reduction to a finite symbolic certificate

1. Factor `(x+aᵢ)^d` out of row i. These are nonzero polynomials, so reduce to exponents 0,1,2,3.
2. Permute rows so their four-bit support codes are nondecreasing. A code r has column j present exactly when bit j of r is 1. A zero row has no perfect matching and may be excluded. This gives all 3,060 multisets of four nonzero row codes from 1 through 15.
3. Put s=a₁−a₀, which is nonzero, and substitute x=s y−a₀. After nonzero column scaling the offsets are `(0,1,b,c)`, where b=(a₂−a₀)/s and c=(a₃−a₀)/s. Their distinctness is precisely

       D(b,c)=b c (b−1)(c−1)(c−b) ≠ 0.

   This normalization preserves realness, rationality, and identically-zero versus nonzero status. It imposes no ordering restriction on b,c.
4. Discard the 1,062 row-code multisets without a perfect matching. For 940 of the remaining 1,998, the determinant of the binary mask is nonzero. This is the coefficient of y⁶ in the polynomial determinant, so nonvanishing is immediate.
5. For the remaining 1,058 singular binary masks, retain only edges that occur in a perfect matching. Other edges contribute to no Leibniz term, and deleting them leaves the determinant unchanged. If this allowed-edge graph is disconnected, its balanced components block-diagonalize the determinant. Each component has at most three rows, so the established order-at-most-three result proves all 851 such cases. Arbitrary subsets of the four exponents are allowed by that smaller-order theorem.
6. This leaves 207 connected allowed-edge classes. Compute their seven polynomial coefficients in y directly from the signed permutation expansion, as exact polynomials in b,c. No parameter values are substituted in this calculation.

## The 207 symbolic checks

The supplied checker uses only integer arithmetic and `fractions.Fraction` from Python's standard library. It recomputes the masks and coefficient polynomials itself; it does not trust the certificate, the exploratory CAS output, floating point, or random tests.

Every coefficient is divided repeatedly by any exact factor from

    b, c, b−1, c−1, c−b.

These factors are nonzero on the domain D≠0. Thus removing them preserves the common-zero condition for the coefficient list, including when different coefficients lose different factors.

- **171 classes:** At least one stripped coefficient is a nonzero rational constant. Hence the determinant cannot vanish identically on D≠0.
- **35 classes:** The highest-degree nonzero stripped coefficient is a linear polynomial L(b,c). A zero determinant would require L=0. Solve it exactly for c as an affine function of b, or for b as a constant if necessary. Substitute this relation into every stripped coefficient. Their exact univariate polynomial gcd is either a nonzero constant or has all its roots among zeros of the substituted D. The latter is verified by repeatedly removing gcd factors shared with D until only a nonzero constant remains. Therefore a common zero would violate distinctness.
- **One class:** Row codes `(6,15,15,15)`. The forced linear relation is c=−b−1. The substituted coefficient gcd is b²+b+1. It is strictly positive for real b because

       b²+b+1=(b+1/2)²+3/4.

  This excludes the last class over the reals.

All 207 coefficient lists and the particular reductions used are recorded in `exact_certificate.json`. The standard-library checker regenerates that file and asserts the complete class counts.

### A human-readable view of the exceptional class

The matrix has first row `(0,x,x²,0)`, and its other three rows are full Vandermonde rows with offsets a,b,c. Direct expansion gives

    det = x (a−b)(a−c)(b−c)
            [ab+ac+bc + x(a+b+c)].

If the four offsets 0,a,b,c are distinct and real, zero determinant would force a+b+c=0 and ab+ac+bc=0. Then

    a²+b²+c²=(a+b+c)²−2(ab+ac+bc)=0,

which forces a=b=c=0, contradicting distinctness.

The field restriction is genuine: over the complex numbers, offsets `(0,1,ω,ω²)` for a primitive cube root of unity give a zero determinant for this mask despite 12 perfect matchings. This is **not** a counterexample for rational or real offsets. The exact classification shows that, up to row permutation and affine normalization, this is the only row-mask class among order-four consecutive exponents with distinct complex exceptional offsets.

## A larger support-graph class

The same argument gives a structural corollary for any matrix order. Delete edges not belonging to a perfect matching and take the balanced connected components of the remaining support graph. If every component either

- has at most three rows, with arbitrary distinct nonnegative column exponents; or
- has four rows, whose four column exponents form a consecutive block,

then the full determinant is nonzero for distinct real offsets whenever the support has a perfect matching. Block decomposition reduces it to the proved factors. This corollary still does not address larger matching-covered components or order-four components with exponent gaps.

## Reproduce and boundaries

Run:

    python check_consecutive_four.py

Expected outcome: `PASS: all 207 remaining row-mask classes proved over the reals.`

The compact source-only package contains this report and the checker. Run the checker first to regenerate `exact_certificate.json`; the generated certificate is intentionally untracked. Its expected SHA-256 and size are recorded in `../GENERATED.json`. Exploratory SymPy files are not needed by the checker. No complexity claim is inferred. The bounded branch stops here: the next open condition is an order-four matching-covered component with genuinely gapped exponents, or a component of larger order.

## Publication editorial note

This is a publication-edited version of the frozen report. A section concerning an external argument and associated references were omitted; the theorem, mathematical proof, reductions, and scope boundaries are unchanged. The original and public hashes are recorded in `../PROVENANCE.json`. Novelty is unverified. The independent audit is AI-assisted and is not human peer review or proof-assistant verification.
