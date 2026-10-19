# Independent adversarial proof audit

19 October 2026. Reviewed PROOF.md Sections 1–6 directly. No defect found.

The raw squared-node Vandermonde factorization, deletion sign, common scalar K, and residue beta_st are correct. Distinct real offsets ensure each individual rational function has only simple pair-sum poles. Equal-sum pairs are disjoint, so the grouped residue equation correctly accounts for collisions. At the smallest pair sum the pair is unique; the stated ordering at a_0+a_j makes the induction valid even when other pair sums collide. This proves the first-coordinate kernel injection, odd-branch mixedness, and even-branch constancy. Distinct exponents make the full alternant nonzero, excluding the constant candidate in the even case.

The explicit functional is also valid: each normalized residue row has entries 1 at indices 0 and j and zero above j. The chosen epsilon gives a strict positive leading contribution that dominates the entire bounded geometric tail. It does not require a positive measure or point-evaluation representation. Common shifts multiply every Laplace term by the same known nonzero factor, so division on the divisible subspace is legitimate.

The sharpness example originated as an exploratory rank lead, but this package now certifies its complete polynomial identity and rank independently. The proof remains scoped to one full column modified against the specified background; it does not permit iteration to arbitrary multi-column masks or imply a complexity-class result.
