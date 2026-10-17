# An unbounded gap between canonical and unrestricted parity covers

2026-10-17. Direct corollary of the exact parity theorem; pending independent review. No historical novelty claim.

Let m>=2 be even, T the odd-parity inputs and V the even-parity inputs. For x in T define the minimal canonical semifilter

    F_x={S subset V : for some coordinate i, {v in V:v_i=x_i} subset S}.

For m>=2 every displayed literal-match set is nonempty, so F_x is upward closed, accepts V and rejects empty. It is an admissible unrestricted witness above x, but the canonical class uses only these minimal witnesses.

Let 0 and 1 denote the all-zero and all-one vectors. Both lie in V because m is even. Put A=V minus {0} and B=V minus {1}. Every odd x has at least one coordinate 1 and at least one coordinate 0: neither constant vector is odd. A therefore contains a true-literal match set from a 1-coordinate; B contains one from a 0-coordinate. Thus A,B belong to F_x.

Every true-literal match set contains one of the two constant vectors. Consequently none is contained in A intersection B=V minus {0,1}, so A intersection B is not in F_x. The single pair (A,B) defeats every canonical F_x. Since this canonical class is nonempty, its cover cost is exactly one.

In contrast, the full unrestricted semifilter cover cost is 2m-3 by EXACT_PROOF.md and model-linkage.md. Hence the ratio of unrestricted to canonical cover cost is 2m-3 for this explicit even-parity family, and is unbounded.

This disproves any universal constant-factor comparison asserting that these particular minimal generator-upset witnesses always approximate unrestricted pair-cover cost. It is a counterexample to that proposed comparison, not a counterexample to a cited published conjecture unless such a conjecture is separately identified. It does not rule out richer canonical families, weighted thresholds, or a restricted theorem for other targets. The definition of canonical used here is explicit and must not be confused with other admissibility classes in the literature.
