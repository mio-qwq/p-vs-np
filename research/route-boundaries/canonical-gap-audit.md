# Independent audit of the minimal-canonical cover gap

Date: 2026-10-17.

Reviewed CANONICAL_GAP.md at SHA-256:

    b93140190d78d1d8438a606f09a4a49f81d690eb0187fe7a61fb81cc6d53b6ee

Verdict: **PASS.** Definition, construction, boundary case, ratio, and stated scope are sound. No source changes requested.

For even m>=2, each literal-match generator M_i(x)={v in V:v_i=x_i} contains the constant vector with every coordinate equal to x_i, because both constant vectors have even parity. Thus these generators are nonempty, and the family of sets containing at least one generator is a proper upward-closed semifilter accepting every required generator. It is exactly the minimal such upward-closed family, so it is an admissible unrestricted witness under the explicit definitions in model-linkage.md.

Every positive input x has both a zero coordinate and a one coordinate. For a one coordinate, its generator avoids the all-zero vector and hence is contained in A. For a zero coordinate, its generator avoids the all-one vector and hence is contained in B. Therefore F_x accepts A and B. Every generator contains one of those two constants, so none lies inside A intersection B, and F_x rejects the intersection. The single pair defeats every stated canonical witness.

The canonical class is nonempty, since there are positive inputs and each displayed family is a proper admissible semifilter. A zero-pair family defeats no witness. Thus canonical cover cost is exactly one, rather than merely at most one.

At m=2, V={00,11}, A={11}, B={00}, and each canonical F_x is the family of nonempty subsets of V. It accepts the two endpoints and rejects their empty intersection. Both canonical and unrestricted costs are one; this boundary is consistent with 2m-3. A strict gap is not asserted at m=2.

Using the independently audited circuit theorem and the separately audited exact model linkage, unrestricted cost is 2m-3. Dividing by the positive canonical cost gives ratio 2m-3, unbounded along the even positive integers. Hence no universal finite multiplicative constant can bound unrestricted cost by the cover cost of this specific minimal generator-upset class. This conclusion does not concern richer canonical classes, alternate admissibility requirements, weighted variants, or an unidentified published conjecture.

I independently evaluated the explicit generators and pair for all positive inputs at m=2,4,6,8,10 (2,8,32,128,512 witnesses respectively). All passed. These finite checks are supplementary; the argument above proves the entire even family.

No historical novelty or P-versus-NP implication is endorsed by this audit. The result is a precise obstruction to this explicitly defined restricted-witness approximation route.
