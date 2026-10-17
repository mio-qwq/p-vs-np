# Single-clause obstruction to the syndrome-period quotient

Research note, 2026-10-17; no novelty or P-versus-NP claim.

Let a non-tautological clause on k distinct variables forbid precisely a in F_2^k. Let A:F_2^k -> F_2^r be linear and S=A(F_2^k\{a}).

If rank(A)<k, each nonempty fiber has at least two elements. Deleting a cannot empty its fiber, so S=im(A). Its translation stabilizer is im(A).

If rank(A)=k, A is injective and S=im(A)\{Aa}. For k>=2, a translation stabilizing S lies in im(A) because S is nonempty and translating any member to another gives their difference. Within im(A), the complement of S has one element, so a stabilizing translation fixes that element and is zero. This also holds for k=1 (S singleton).

Thus for an ordinary 3-clause with injective occurrence-copy coupling, the period quotient has no effect. With a lost local direction the clause's feasible image is already the complete linear image. This is an exact limitation of that representation, not a limitation of all possible algorithms or grouped encodings.

For general finite feasible images S_i in a common binary vector space, H_i={h:S_i+h=S_i} and H=sum_i H_i, the sumset T=sum_i S_i is H-invariant. Consequently b in T iff its image mod H belongs to the sum of the projected S_i. This is a sound quotient but its efficiency depends on constructing local sets and the width after quotienting. The clause dichotomy blocks a generic shortcut on fully coupled single-clause instances.
