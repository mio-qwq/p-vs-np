# Fresh independent review: transposition-distance radius

Verdict: **PASS, conditional only on the stated support-radius dependency.** No mathematical defect found. The exact radius is min(n−1, 2d) for integer n≥2,d≥1 over every field. Radius zero is correct for d=0 and n≤1. This is an independent mathematical review with exact finite controls, not formal verification, a literature novelty determination, or a P versus NP conclusion.

## Frozen inputs

- Addendum: `../transposition_radius_addendum.md`, SHA256 `6d7cc48014adcc493cdf121c2365e02042a582e59f9f331aa984d318ae220f43`.
- Dependency: `../../sharp-permutation-radius/PROOF.md`, SHA256 `d46686373a10634f6976fa7c97cbdecf47b4876409ad7111829a821beab41f79`.

Both hashes were independently recomputed and matched. Neither source was changed. The existing checker was not read or reused.

## Logical review

The quantifier is over polynomial functions on the entire symmetric group that admit a degree-at-most-d representative, and are nonzero somewhere on that group. It is not over nonzero formal polynomials regardless of their evaluations. The target ball is centered at identity and uses arbitrary transpositions. One lower witness for each n,d over each field is enough to disprove every smaller radius. The constructed integer polynomials reduce to such witnesses over all fields because their exhibited nonzero values are units ±1.

### Upper bound

The supplied dependency gives a witness with support m≤2d+1. A nonidentity witness with c nontrivial cycles has distance m−c≤2d. Identity has distance zero. Independently every permutation has distance ≤n−1. Taking the same witness gives both bounds simultaneously.

### Rank argument, including characteristic two

For the adopted row convention or its transpose, PPᵀ=I, and expansion gives (P−I)(I+Pᵀ)=P−Pᵀ exactly. Consequently rank(P−Pᵀ)≤rank(P−I). The kernel equations of P−I identify coordinates around each cycle; there is one free coordinate per cycle over any field, with no division by cycle lengths. Thus rank(P−I)=n−number of cycles, including when the characteristic divides cycle lengths.

A nonzero Pfaffian of a principal 2d-submatrix implies its determinant is nonzero by the integer polynomial identity det=Pf². The matrix is alternating in characteristic two as well: its diagonal is zero. An invertible submatrix forces rank of the full matrix at least 2d. All rank inequalities therefore remain valid in characteristic two.

### Lower bound regimes and boundaries

- n≥2d+1: the 2d-index Pfaffian has degree d and forces distance ≥2d. A cycle on those indices and one extra index leaves an even path after deleting the extra vertex. The path has exactly one perfect matching, whose weight is ±1.
- Odd n≤2d+1: degree (n−1)/2≤d and the same argument forces distance n−1. Equality n=2d+1 is covered consistently by both constructions.
- Even n≤2d, n≥4: the additional factor has degree one and the remaining Pfaffian degree (n−2)/2, giving total degree n/2≤d. These inequalities explicitly include the important boundary n=2d. Together with the previous regimes they exhaust all n,d.
- In the even construction, nonzero x_ab−x_ba means exactly one directed adjacency holds. Both adjacencies would constitute a 2-cycle and give 1−1=0 in every characteristic. Thus a,b belong to one cycle of length ≥3. Any other cycle C is entirely within S; its nonzero indicator vector is annihilated by the principal alternating matrix because both the incoming and outgoing cycle edges remain inside C. This applies equally to fixed points and 2-cycles. The matrix would be singular, contradicting the nonzero Pfaffian. Hence the permutation must be a single n-cycle.
- An n-cycle with a,b consecutive leaves an even path on n−2 vertices after deleting them; its Pfaffian and the first factor are each ±1. Thus the even construction is genuinely nonzero over every field.
- n=2 requires and receives the separate x_12 witness. Its only nonzero evaluation is the transposition. Using the antisymmetric factor there would be wrong; the text explicitly avoids it.
- n=0 (if S_0 is included) and n=1 have only identity, and d=0 gives a nonzero constant. Radius zero is exact in each case.

No hidden characteristic assumption, missing even-n regime, or degree/quantifier mismatch was found.

## Independent exact controls

`check.py` computes transposition distance by breadth-first search using the generating transpositions, rather than using the cycle-count identity from the proof. It independently evaluates the Pfaffians by signed perfect-matching expansion.

All permutations for n=0,...,8 were enumerated. For every n≥2 the extremal polynomial has values only 0,±1, has a nonempty nonzero set, and every nonzero evaluation has BFS distance n−1. The nonzero counts for n=2,...,8 are 1,2,4,24,48,720,1440. Every feasible principal 2d-Pfaffian was also checked against distance ≥2d (120,960 such checks at n=8).

A separate control directly tests the universal-radius definition using evaluation-space ranks over F_2 and F_3. All degree≤d monomials on permutation matrices reduce to zero or indicators of partial injective maps with at most d edges. The script enumerates these indicators as columns and permutations as rows. A ball detects every nonzero function exactly when its evaluation rows span the same row space as the whole group. It computes exact modular ranks after each BFS radius and finds the first full-rank radius.

The direct universal test covers all n=0,...,5 and d=0,...,n over F_2; all n=0,...,4 and d=0,...,n over F_3, plus n=5,d=0,1,2 over F_3. In every case the first full-rank radius is the claimed min(n−1,2d), with the stated trivial exceptions. Testing d through n is sufficient for all larger degrees in these small n, because functions on permutation matrices already have partial-injection representatives of degree at most n.

Raw exact ranks and counts are saved in `results.json`. These controls corroborate, rather than replace, the all-field proof.
