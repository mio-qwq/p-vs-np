# An infinite one-tail-gap masked-minor theorem

18 October 2026 (UTC). Scope: an auxiliary uncolored masked polynomial determinant.

## Results

**Theorem A (one tail gap).** Let η be any binary 4×4 matrix with a perfect matching. For any four distinct complex numbers a₀,a₁,a₂,a₃, any nonnegative integer d, and any integer m≥4,

    det[ηᵢⱼ (x+aᵢ)^eⱼ],  (e₀,e₁,e₂,e₃)=(d,d+1,d+2,d+m),

is a nonzero polynomial. Together with the previously proved real-offset consecutive case m=3, this proves the entire family m≥3 over distinct real offsets.

**Theorem B (separated largest exponent).** Under the same mask and offset conditions, let the exponents be (d,d+p,d+q,d+r), where d≥0 and 0<p<q<r are integers. The determinant is nonzero if

    r ≥ 3(p+q+1).

Both theorems permit distinct complex offsets. Theorem B is a direct structural proof. Theorem A combines that proof for m≥12 with eight complete finite symbolic classifications for m=4,…,11. These classifications range over support patterns and symbolic offsets; they do not sample offset values or infer an unbounded exponent claim from testing.

Neither theorem proves all gapped exponent sets in order four. Neither establishes the color-conditioned ASNC claim, repairs the disputed local valuation assertion, or yields a P-versus-NP conclusion.

## Structural lemma: separated translates cannot cancel

Let F be a characteristic-zero field, let a₁,…,aₙ∈F be distinct, and let E,m be nonnegative integers. If

    m ≥ (n−1)(E+1),

then the n(E+1) polynomials

    (x+aᵢ)^(m+j),   1≤i≤n, 0≤j≤E,

are linearly independent over F. Equivalently, an identity

    Σᵢ Pᵢ(x)(x+aᵢ)^m = 0,  deg Pᵢ≤E,

forces every Pᵢ to be zero.

### Proof

Put N=m+E and K=n(E+1). The threshold is precisely N≥K−1. For each i and each derivative order s=0,…,E,

    ∂ₐ^s (x+a)^N |ₐ₌ₐᵢ = (N)ₛ (x+aᵢ)^(N−s),

where (N)ₛ=N(N−1)…(N−s+1) is nonzero. These derivative polynomials differ from the displayed powers only by nonzero scalar factors and reversing the order within each group.

Consider their coefficients of x^(N−k), for k=0,…,K−1. The coefficient in column (i,s) is exactly

    binom(N,k) · [∂ₐ^s a^k]ₐ₌ₐᵢ.

Thus the K×K coefficient matrix is a nonzero diagonal scaling of the Hermite evaluation matrix H with entries Hₖ,(ᵢ,ₛ)=(∂ₐ^s a^k)|ₐ₌ₐᵢ. To prove H invertible, suppose a polynomial Q(a) of degree below K lies in the kernel of its transpose. Then Q and its first E derivatives vanish at every aᵢ, so

    ∏ᵢ (a−aᵢ)^(E+1) divides Q(a).

The divisor has degree K, forcing Q=0. Consequently H is invertible, the top K coefficient vectors are independent, and the original polynomials are independent. Finally, expanding Pᵢ(x) in the basis 1,(x+aᵢ),…,(x+aᵢ)^E gives the equivalent formulation. This proof uses exact polynomial identities and divisibility, without a positivity or realness assumption.

### Application to masked determinants

Factor (x+aᵢ)^d from every row, reducing the exponents in Theorem B to (0,p,q,r). Expand the determinant along its last column:

    D(x)=Σᵢ ηᵢ₃ Cᵢ(x)(x+aᵢ)^r,

where Cᵢ is the signed masked 3×3 cofactor and deg Cᵢ≤E=p+q. A perfect matching contains at least one last-column edge (i,3); deleting that edge's row and column leaves a 3×3 support with a perfect matching. The order-at-most-three lemma below shows that this Cᵢ is nonzero over F. Therefore the coefficient polynomials ηᵢ₃Cᵢ are not all zero. The structural lemma, with n=4, rules out D≡0 when r≥3(E+1). This proves Theorem B and the part m≥12 of Theorem A.

## The order-at-most-three lemma also holds over complex offsets

For distinct nonnegative integer exponents and distinct offsets in any characteristic-zero field, every binary masked determinant of order at most three with a perfect matching is nonzero. Here is the complete argument needed by both the structural proof and the finite reductions.

- Order one is immediate.
- A support with an odd number of perfect matchings has a nonzero top coefficient: every supported product is monic of the same total degree, and an odd sum of signs cannot be zero.
- With exactly two matchings, their signs either agree, giving a nonzero top coefficient, or disagree. In the latter case the two monic products cannot be identical, because the multiplicities at the distinct roots −aᵢ are the assigned exponents, which differ between distinct permutations. This covers order two and two-matching order-three cases over any characteristic-zero field.
- The 512 binary 3×3 masks have numbers of perfect matchings 0,1,2,3,4,6 with respective frequencies 265,150,69,18,9,1. Every four-matching mask is the full mask with exactly one entry removed. `check_negative_controls.py` independently enumerates all 512 masks and verifies these assertions.
- For a full k×k determinant, k=2 or 3, write S=Σeⱼ and expand at infinity. Its coefficient at degree S−k(k−1)/2 is

      det[aᵢ^ℓ]ᵢ,ℓ₌₀^(k−1) · det[binom(eⱼ,ℓ)]ℓ,ⱼ₌₀^(k−1)
      = ∏ᵢ<ⱼ(aⱼ−aᵢ) · ∏ᵢ<ⱼ(eⱼ−eᵢ) / ∏ℓ₌₀^(k−1)ℓ!.

  Every higher-degree coefficient vanishes: its expansion uses k nonnegative row powers with sum below 0+1+…+(k−1), so at least two are equal and the associated offset-power determinant is zero. The displayed coefficient is nonzero in characteristic zero. Thus the full order-three determinant has degree S−3, and a full order-two cofactor has degree equal to its exponent sum minus one.
- Deleting one entry from a full 3×3 matrix subtracts that entry times its signed full 2×2 cofactor. This subtracted polynomial has degree S−1 and nonzero leading coefficient, while the full determinant has degree S−3. Cancellation is impossible.

This proof contains no order, positivity, or conjugation argument. It therefore justifies the complex-field use, rather than inheriting a real-only statement without verification.

## Finite symbolic bridge: m=4,…,11

The supplied `check_tail_gap.py` uses only Python's standard library and exact integers/Fraction arithmetic. For each of these eight exponents it performs the following reductions.

1. Factor the common exponent d out of the rows.
2. Sort the four nonzero row-support codes. There are 3,060 row-code multisets. Rows of zero support cannot belong to a perfect-matching mask.
3. Set s=a₁−a₀ and substitute x=s y−a₀. Divide each column by its nonzero scale s^eⱼ. The offsets become (0,1,b,c) with

       D(b,c)=b c (b−1)(c−1)(c−b) ≠ 0.

   This invertible normalization works over the complex numbers too. No ordering assumption on offsets is imposed.
4. Exclude the 1,062 supports without a perfect matching. For 940 of the remaining 1,998, the binary mask determinant is nonzero. It is exactly the top coefficient of the polynomial determinant.
5. Delete edges belonging to no perfect matching. They contribute to no determinant term. If the remaining allowed-edge graph is disconnected, it block-diagonalizes into balanced blocks of order at most three. The complex-field smaller-order lemma proves all 851 such singular cases.
6. The remaining 207 connected singular classes are expanded by all signed supported permutations, yielding exact bivariate coefficient polynomials in b,c. This enumerates finite support patterns, not parameter values.
7. From each coefficient repeatedly remove any exact factor among b,c,b−1,c−1,c−b. These factors are nonzero throughout the distinct-offset domain, so the common-zero condition is preserved.
8. If a stripped coefficient is a nonzero rational constant, the determinant is nonzero. Otherwise the highest nonzero stripped coefficient is verified to be an affine linear polynomial L. Parametrize the entire line L=0, substitute into every stripped coefficient, and compute their exact univariate gcd g. Remove every factor of g shared with the substituted D. In all cases the residue is a nonzero constant. Thus no simultaneous zero is possible at distinct offsets, even over an algebraic closure.

The complete counts are:

    m=4:      171 direct obstructions + 36 line-reduction obstructions = 207
    m=5,…,11: 173 direct obstructions + 34 line-reduction obstructions = 207 each

No positive-quadratic or other real-only argument is needed. The eight cases give 1,656 completed symbolic checks. Together with the structural lemma for every m≥12, they prove Theorem A for the whole infinite family m≥4.

## Verification and boundaries

Run:

    python3 ../verify-gapped-20261018.py

The release verifier generates the certificate in a temporary directory, verifies
its size and SHA-256 from `GENERATED.json`, and runs the producer, independent
audit, and negative controls with ordinary Python and `python -O`. The expanded
certificate is deliberately absent from the source tree and archive. To generate
one explicitly for separate inspection, use:

    python3 check_tail_gap.py --write /tmp/tail-gap-certificate.json
    python3 check_tail_gap.py --check /tmp/tail-gap-certificate.json

The checker recomputes all polynomials and decisions; the saved certificate is not trusted. Default invocation recomputes the proof without reading or writing the certificate. `--write PATH` optionally regenerates its compact exact witnesses. All validation checks remain active under `python -O`. The algebraic arithmetic is adapted from the previously independently audited consecutive-exponent checker, but the new checker imports no files from that package and reconstructs the new cases itself.

Negative/boundary controls:

- Feeding m=3 into the complex-field finite proof is rejected at row codes (6,15,15,15), with remaining gcd t²+t+1.
- The exact zero determinant at offsets (0,1,t,−1−t), modulo t²+t+1, is reproduced for this mask and exponents (0,1,2,3). The distinctness polynomial is coprime to t²+t+1, so these really are distinct complex offsets.
- Allowing repeated offsets produces a zero full determinant for offsets (0,1,0,2) and exponents (0,1,2,4), correctly outside D≠0.
- Altering one stored coefficient in a physical certificate copy causes the normal verifier to fail with a nonzero exit status and `certificate mismatch`.

This is an exact elementary proof plus a finite symbolic certificate, not a formal proof-assistant development. The separate AI-assisted audit is recorded in `AUDIT.md`. No novelty, human peer review, or Lean verification is claimed. This package preserves the mathematical proof and producer; publication edits only clarify reproduction, relative paths, and review status.

## Stopping and restoration conditions

This bounded branch stops after obtaining the infinite tail-gap theorem and the general separated-largest-exponent criterion. Further unstructured exponent/offset sampling would not close the remaining problem.

A useful restoration condition is a structural argument for the interior-gap regime (0,p,q,r), outside p=1,q=2 and below r=3(p+q+1), or a genuinely exact counterexample there. A smaller separation threshold could also be useful if proved structurally. Any larger-order statement needs a separately justified nonzero cofactor or an appropriate lower-order theorem; the translate lemma alone does not prove arbitrary-order masked nonvanishing.
