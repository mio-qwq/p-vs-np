# Bounded prior-art review: translated Vandermonde column kernels

Reviewed 19 October 2026 (UTC). This is a limited literature comparison, not a novelty certification or a proof that a question is open in the literature. It concerns one weighted column with every other column full. No claim about arbitrary graph masks or P versus NP follows.

## Bottom line

1. **The main algebraic ingredients are classical.** Alternant/Schur factorization, Schur positivity, barycentric interpolation, the monomial divided-difference identity, and equal-degree shifted-power independence should be attributed accordingly.
2. **No checked primary source directly states the three complete constant-kernel propositions below.** In particular, the checked sources do not by themselves give the parity theorem's collision-resistant dimension/sign conclusion, the arithmetic-background theorem's full complex independence, or the missing-degree theorem's exact exceptional condition and kernel vector. This is a bounded search outcome, not evidence of historical novelty.
3. **The unrestricted nonnegative one-column statement was not verified as an established theorem.** It must not be presented either as known or as a newly identified open problem on this review's authority. A closely related 2026 preprint makes a broader binary-mask claim, but the previously audited defects prevent using that claim as established subsumption.
4. **A useful baseline is directly classical:** exact background step 1, with a distinct higher distinguished exponent, reduces to independence of equal-degree shifted powers. The local results with step at least 2 require additional arguments.

## Objects and versions compared

For distinct real offsets a_s, distinct nonnegative integer exponents, and distinguished exponent k in column c, define

    T_s(L) = (-1)^(s+c) (L+a_s)^k det[(L+a_t)^(b_j)]_(t != s,j).

The issue is a relation with weights independent of L:

    sum_s u_s T_s(L) = 0 as a polynomial identity.

Pointwise nonsingularity of the unmasked evaluation matrix is a different statement.

The local inputs checked were:

- **Parity background:** arbitrary distinct background exponents b_j of one parity. The asserted kernel is zero for k < h or nonnegative even k-h; for nonnegative odd k-h its dimension is at most one and a nonzero vector satisfies u_0 = -u_1 != 0. Here h = min b_j.
- **Arithmetic background, final version:** b_j = h+mj for j=0,...,n-2, n >= 3, m >= 3, k distinct from the background exponents. The final file asserts full linear independence over C, including k < h. This supersedes the earlier draft's possible half-residue exception.
- **One missing degree:** exponents d,d+1,...,d+n-2,d+n; distinguished exponent d+1. After centering offsets b_s, the kernel is nonzero exactly when every b_s != 0 and f'(0)=0 for f(x)=product_s(x+b_s). In that case it is spanned by h'(b_s)/b_s, with h(t)=product_s(t-b_s), and is mixed-sign.

Input SHA-256 receipts are in INPUTS.sha256. They identify the actual local versions reviewed, rather than every later revision.

## 1. Schur factorization and positivity: direct classical coverage

Harry Tamvakis, *The theory of Schur polynomials revisited*, author manuscript dated 10 December 2011, introduction equations (1) and (3), supplies the bialternant identity and the semistandard-tableau expansion. For a partition lambda of length at most N,

    det[z_i^(lambda_j+N-j)] / det[z_i^(N-j)] = s_lambda(z),

and the tableau expansion has nonnegative integer coefficients. [Author manuscript](https://www.math.umd.edu/~harryt/papers/schurrev.pdf)

**Direct application.** The squared-node factorization in the parity note is an instance of this identity after extracting the minimum exponent. Its positivity at a collision also follows: if at least length(lambda) variables are positive and all others are nonnegative, fill each tableau row with one of those positive-variable labels to obtain a strictly positive monomial. This remains valid when two squared nodes coincide. Thus factorization and positivity are established ingredients, not independent novelty claims.

R. J. Evans and I. M. Isaacs, *Generalized Vandermonde determinants and roots of unity of prime order*, Proc. AMS 58 (1976), 51–54, §2, also proves the nonnegative-coefficient property of the generalized Vandermonde quotient, crediting Mitchell. [Author-hosted paper](https://www.math.ucsd.edu/~revans/Vandermonde.pdf), [DOI](https://doi.org/10.1090/S0002-9939-1976-0412205-0)

**Boundary.** These statements concern the unmasked alternant and its quotient. They do not classify constant linear combinations of individual column-Laplace terms after z_s=(L+a_s)^2. In particular, subtracting or retaining selected signed Laplace terms does not preserve Schur positivity automatically.

## 2. Divided differences and barycentric formulas: direct coverage of identities

Carl de Boor, *Divided Differences*, Surveys in Approximation Theory 1 (2005), 46–69, Example 9/equation (41), gives, for distinct nodes y_s,

    [y_0,...,y_(n-1)] p = sum_s p(y_s)/product_(t != s)(y_s-y_t).

Example 7/equation (27) identifies the divided difference of t^q with the complete homogeneous symmetric polynomial h_(q-n+1) when q >= n-1, and with zero for q < n-1. Section 7 also gives partial-fraction formulations. [Journal PDF](https://surveys-in-approximation-theory.com/papers/2/2.pdf), [arXiv record](https://arxiv.org/abs/math/0502036)

**Direct application.** This is exactly the all-ones rational-sum identity used in the earlier arithmetic-background argument when k-h is a nonnegative multiple of m. It applies over complex nodes away from collisions, and the resulting rational identity extends algebraically. The final arithmetic proof no longer needs that identity, but it remains a valid classical alternative ingredient.

Jean-Paul Berrut and Lloyd N. Trefethen, *Barycentric Lagrange Interpolation*, SIAM Review 46 (2004), 501–517, equations (2.1), (3.2), and (3.3), gives the cardinal polynomials and weights 1/product_(t != s)(b_s-b_t) = 1/h'(b_s). [Author-hosted paper](https://people.maths.ox.ac.uk/trefethen/barycentric.pdf), [DOI](https://doi.org/10.1137/S0036144502417715)

**Direct application and limit.** The starting cardinal term in the missing-degree note is standard Lagrange interpolation. Adding a multiple of the node polynomial to remove one coefficient is an elementary interpolation construction. The cited paper does not state the resulting common-translation kernel classification, the condition f'(0)=0, or the vector h'(b_s)/b_s.

## 3. Missing exponents: the determinant formula is classical

Thomas Ernst, *Generalized Vandermonde determinants*, manuscript received 19 December 2001, Theorem 2.1/equation (13), records the classical identity: deleting degree l from degrees 0,...,n yields the ordinary Vandermonde times the elementary symmetric polynomial e_(n-l). Definition 2/equation (5) is the general Schur quotient. [University-hosted manuscript](https://www.mathe2.uni-bayreuth.de/axel/papers/ernst:generalized_vandermonde_dterminants.pdf)

**Direct application.** With l=n-1, the missing-degree note's full determinant is Delta(b) times sum_s(x+b_s), hence n x Delta(b) after centering. That factorization is fully classical. Ernst also discusses more general missing-exponent formulas, but the checked statements are formulas for alternants, not a classification of the constant kernel of the n individual translated Laplace terms. An explicit determinant formula can enable such a classification without already asserting it.

## 4. Shifted powers and Birkhoff interpolation: relevant, but different objects

Ignacio Garcia-Marco, Pascal Koiran, and Timothee Pecatte, *On the linear independence of shifted powers*, arXiv:1705.03842v2, Proposition 1.1, records that d+1 distinct translates (L+a_s)^d form a basis of degree-at-most-d polynomials in characteristic zero. Theorem 1.4 gives a stronger real-node sufficient condition for unequal-degree shifted powers: with n_j counting degrees below j, require n_1 <= 1 and n_j+n_(j+1) <= j+1. [Versioned paper](https://arxiv.org/pdf/1705.03842v2)

**A directly subsumed baseline.** If background exponents are h,h+1,...,h+n-2 and k >= h is distinct from them, then ell=k-h >= n-1. Dividing T_s by the common nonzero factor product_t(L+a_t)^h leaves a nonzero constant multiple of (L+a_s)^ell. Proposition 1.1 therefore implies full independence. If k<h, the corresponding normalized rational functions have distinct own-node poles, which is an elementary separate argument.

**Why this is not automatic subsumption of the new cases.** For m>=2 or arbitrary same-parity gaps, the cofactor contributes a nonconstant product and possibly a Schur polynomial. T_s is generally not a single shifted power. No reduction to a shifted-power family satisfying those hypotheses was found in this review.

Garcia-Marco and Koiran, *Lower Bounds by Birkhoff Interpolation*, arXiv:1507.02015v1, Theorem 8, recalls the Atkinson–Sharma criterion: an incidence matrix with exactly d+1 prescribed derivative data, satisfying the Pólya condition and having no odd supported sequence, is order regular. [Versioned paper](https://arxiv.org/pdf/1507.02015v1)

Here an odd sequence is a consecutive run of prescribed derivatives at one node, not a statement that all background monomial degrees have the same parity. A correspondence meeting the theorem's derivative-incidence hypotheses would have to be proved before invoking it for the present Laplace-polynomial kernels. None is supplied by the local notes or the checked sources.

## 5. Pair-sum and cyclotomic residues: closest verified mechanisms

The rational representations are barycentric-type sums with moving nodes y_s=(L+a_s)^m. Comparing their residues uses ordinary partial-fraction uniqueness. The additional work is geometric and combinatorial:

- For m=2, collision parameters are real pair midpoints. Different disjoint pairs can collide at one parameter. The local minimum-index argument prevents those collisions from concealing the first active residue; Schur positivity makes that residue nonzero.
- For m>=3 with exact arithmetic background, primitive-root collision parameters have imaginary height proportional to the offset gap. The final proof isolates every primitive pole involving an extreme offset. The endpoint equations then force the asserted constant-vector restrictions.

No checked primary paper was found containing these particular all-offset isolation arguments or their full kernel conclusions.

**A roots-of-unity theorem that does not subsume this.** Evans–Isaacs Theorem 1 concerns a primitive root of *prime* order, a characteristic-zero field F, and n=[F(zeta):F]; any n distinct powers of zeta are an F-basis. Its nodes lie among powers of a fixed root of unity. The present theorem instead has arbitrary real offsets, allows composite m, and uses roots of unity as ratios at isolated complex collisions. The resemblance in terminology is not a match of hypotheses.

## 6. General nonnegative masks and the previously audited preprint

Yuefeng Du, *Bipartite Exact Matching in P*, arXiv:2604.01571v3, §4, defines column-hole cofactors and fixed-support replacement functionals. Proposition 7.1 in §7.2 claims that a binary masked generalized Vandermonde with pairwise-coprime linear bases is nonzero exactly when its support has a perfect matching. [Versioned primary source, §4](https://arxiv.org/html/2604.01571v3#S4), [§7.2](https://arxiv.org/html/2604.01571v3#S7.SS2)

This is relevant prior discussion, but not verified subsumption. The earlier local audit already records that the arbitrary-linear-form statement is false and that its valuation proof fails even for monic bases. This review recovered those issues and treats them as existing baseline, not new findings. The monic one-column conclusions are not refuted by those examples.

Moreover, binary-mask nonvanishing alone would not establish exclusion of every nonzero *real nonnegative* weighting: the two coefficient domains differ, and an additional argument is required. The §4 fixed-support elimination framework also does not replace a theorem about a single fixed distinguished exponent with constant real weights.

## 7. Recommended attribution and permitted conclusion

A suitable concise annotation for the three local notes is:

> The arguments use classical alternant/Schur factorization and positivity, together with Lagrange/barycentric interpolation and residue comparison. A bounded primary-source comparison did not locate a theorem with the same complete constant-kernel conclusions. No historical novelty claim is made. The results are restricted to the stated exponent families and one weighted column.

For the arithmetic note, state the **final full-complex-independence result**, rather than the superseded half-residue exception. For the missing-degree note, separate the classical Delta times e_1 formula from the local exact exceptional-kernel classification.

Do not describe the general arbitrary-exponent nonnegative-column assertion as established, or the general multi-column mask assertion as proved. Conversely, do not call either a literature-wide open problem merely because no suitable theorem was found here.

## Search coverage and limits

The bounded search covered generalized/translated/shifted/lacunary Vandermonde determinants; column cofactors and masks; constant relations; nonnegative column weights; same-parity and arithmetic exponents; pair sums and cyclotomic residues; Schur positivity; barycentric/divided-difference formulas; and shifted-power/Birkhoff interpolation results. Primary documents were checked at the cited theorem/formula locations. Search-result snippets and nonprimary discussions were used only to locate sources.

This was not an exhaustive MathSciNet/zbMATH citation survey, nor a search through every monograph on total positivity or lacunary interpolation. The SIAM full-text endpoint for Demmel–Koev was unavailable in this session; its paper's title/abstract and introductory statement were locatable, but no uninspected theorem from it is used to assert subsumption. The review does not rely on the status of any broad complexity claim.

The companion SOURCES.json records stable identifiers and retrieval dates. Versioned arXiv URLs pin manuscript versions; ordinary university PDF URLs and DOIs are stable references, not cryptographic guarantees of unchanged bytes. No external PDF-byte hashes are claimed, and no external full texts are redistributed in this review bundle.
