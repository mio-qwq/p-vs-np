# Constructive cross-check and consolidation record

19 October 2026. Verdict: **PASS** for the canonical `PROOF.md` endpoint-pole theorem. The constructive structural researcher independently checked the root's original complex-pole argument and both partner strengthenings, then consolidated the final text. This is therefore a cross-check/consolidation record, not an assertion that the final prose author is an independent reviewer of that same prose. The separate adversarial audit and raw-cofactor checks provide additional review.

## Independently rederived ingredients

1. The exact arithmetic background minor is a Vandermonde after factoring the common powers. With columns sorted increasingly, the common sign is `(-1)^(n-1+c)`. The rational factorization is valid even when `ell=k-h` is negative.
2. For `x_i=zeta*x_j`, direct solution gives `L=-(a_i+a_j)/2-i(a_i-a_j)cot(arg(zeta)/2)/2`. For `i<j` and primitive positive angle `2*pi/m`, this is in the upper half-plane.
3. The collision is simple, and no third denominator factor vanishes at a nonreal collision: equality of powers implies equality of moduli, which has at most two real shifts on the translated horizontal line.
4. The two endpoint residues have ratio `-zeta^(-ell)`. Both residues are nonzero, including negative ell. Its extra own-node poles are real and cannot interfere.
5. A primitive upper pole of a pair containing a global extreme offset is isolated. A second pair at the same pole would share its center and need at least its gap, because the primitive angle maximizes the positive cotangent. It would extend beyond the global extreme unless it were the identical pair.
6. The star from the minimum endpoint forces `u_j=r*u_0` for every `j>0`, with `r=zeta^ell`. The edge from index 1 to the maximum forces `u_max=r*u_1`. For `n>=3`, these make the vector zero when `r!=1`, and constant when `r=1`. The nonzero full generalized Vandermonde excludes the nonzero constant case.

Thus full complex linear independence holds. No restriction on the residue class of ell or on its sign remains. This is stronger than the valid original root draft, which retained an unnecessary possible real mixed-sign kernel class.

## Independent alternate strengthening

Before checking the endpoint-star proof, this reviewer also checked the algorithm auditor's two-root route: the smallest pair sum `a_0+a_1` is unique, so both the primitive-root and squared-primitive-root poles are isolated. Since `m>=3`, both roots are nontrivial. Their two residue equations force either zero first coordinates or `m|ell`. A minimum-index pole induction then finishes together with the appropriate constant-sum or extreme-root argument. In the m=4 squared-root case the pole is real, but no own-node pole can occur at the midpoint of adjacent offsets. The endpoint-star proof avoids this extra case handling and is preferred.

## Scope

No step uses a generic-offset assumption, numerical rank, or leading-coefficient noncancellation. The exact staircase is essential to the presented proof because it removes any potentially vanishing complex Schur factor. The result applies to one weighted column, with all other columns unmasked. It gives no claim about arbitrary mixed-background gaps, arbitrary sparse support, or P versus NP.
