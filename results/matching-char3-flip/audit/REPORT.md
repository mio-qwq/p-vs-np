# Independent raw audit: characteristic-three quadratic flip radius

Verdict: PASS. The three frozen principal certificates check exactly. Together with the previously audited changed-pair support upper bound, the uniform conclusion is valid: over every characteristic-three field, the degree-two flip testing radius is 4 for n=5,6, is min(n-1,3) for n>=2 otherwise, and is 0 for n<=1.

## Independence and scope

`check_raw.py` was written from the definition of perfect matchings and two-edge flips. It imports no discovery code, group-action code, modular solver, or discoverer's checker. It parses the raw JSON, validates every edge and matching, and uses actual flip-neighbor BFS to establish distances. Group labels play no mathematical role: listed terms are simply expanded sums. Copies of the audited inputs are retained here. No source proof or source artifact was edited.

The existing general support<=2d+1 upper theorem is an explicit dependency of the all-n conclusion. This audit checks its application at d=2, rather than claiming a new independent proof of that earlier theorem.

## Frozen hashes

- certificate_mod3_n7.json: 73d6ede1a9f04599455a4ba2095a9cccfdd70309030e9e3fe68b328e6b16eb6d
- witness_n5.json: 70560d38922036a0e97bd6843d18effaeb0b56adcba6e2e69aee39f4fa62fdfd
- witness_n6.json: 0443b02cef2841e8b754f956c64b50f7246336638bc7e2e064d0227a02f77be6

These agree with the discoverer's frozen hashes, obtained separately after this audit computed its own copies.

## Upper certificate

There are 49 coefficient groups containing 1,273 distinct matching evaluations. The BFS radius-three ball at n=7 has 6,623 points. Every listed right-hand matching belongs to this ball; their distance histogram is 1, 37, 230, 1005 at distances 0,1,2,3 respectively. The target has BFS distance exactly four.

The identity was checked against ALL 4,278 formal monomials of degree at most two in the 91 undirected edge variables: one constant, 91 linear monomials, and 4,186 quadratic monomials with repetition. Thus squares and products of incident edges were explicitly included, not merely presumed irrelevant. Every equality holds modulo three. This proves the evaluation-functional identity for every polynomial of degree at most two over F3, and hence by scalar extension over every characteristic-three field. A single-coefficient corruption fails the constant-monomial equality.

## Lower certificates

The n=5 polynomial has 15 groups and 116 distinct listed monomials. The audit evaluates it on all 945 perfect matchings, not just its small ball. Every one of the 561 points of distance <=3 has value zero. Its target has distance four and value one. All 384 distance-four matchings are nonzero.

The n=6 polynomial has 64 groups and 521 distinct listed monomials. The audit evaluates it on all 10,395 perfect matchings. Every one of the 2,171 points of distance <=3 has value zero. Its target has distance four and value one. It is nonzero at 2,304 distance-four points and nowhere else.

Each raw monomial is validated to have degree at most two. No inference from solver ranks, orbit invariance, or presumed symmetry is used.

The extension_failure.json matching also checks directly: the n=6 witness evaluates to one at the stated n=8 matching. Three disjoint two-edge flips produce that matching; its three nontrivial two-pair components require three flips. Therefore support on the first five baseline pairs does not make this lower witness universally radius-three-vanishing.

## All-n argument

Apply the earlier support theorem to any nonzero quadratic matching function: it has a nonzero witness changing at most five baseline pairs. A changed component has at least two pairs, and distance is the sum of component sizes minus one. Consequently this witness has distance at most four. If its distance is four, its changed pairs are exactly five and form one alternating cycle. This proves the upper bound four at n=5,6.

For n>=7, such a five-pair cycle leaves at least two baseline pairs untouched. Choose two of them. Fix every edge outside these seven pairs to the outside baseline matching: outside baseline variables become one, all other outside variables and edges crossing the boundary become zero, and the variables within the seven-pair set remain free. This gives a degree-at-most-two polynomial with the original nonzero target value. Relabeling the five-cycle's pairs and their endpoints maps it to the certificate's target; the two spare pairs map to its final two baseline pairs. Every alternating five-cycle admits such a baseline-preserving relabeling.

The verified certificate forces a nonzero value at one of its radius-three right-hand matchings. Restoring the fixed outside baseline edges preserves the flip distance. This proves the uniform upper bound three. There is no assumption that the original polynomial was supported on five or seven pairs, and no claim that the n=6 lower witness extends. The constant and linear monomial checks ensure that substituting outside variables is fully covered.

## Remaining sharp lower bounds

For n>=4 the quadratic (x_02-x_13)(x_46-x_57) vanishes on the radius-two ball. A nonzero first factor requires the component containing baseline pairs {0,1} and {2,3} to have at least three pairs: in a two-pair component the indicated opposite edges occur together. The analogous statement holds for the other factor. The distance-at-most-two possibilities, one two-pair component, one three-pair component, or two two-pair components, cannot make both factors nonzero. The displayed four-pair cycle in the source proof gives value -1 at distance three. This reasoning survives arbitrary extra untouched or changed pairs and any characteristic-three field.

For n=3, x_12 x_34 vanishes at distance <=1 and equals one on the three-pair cycle. For n=2, x_02 separates the baseline from a one-flip matching. For n<=1 there is only one matching. The audit independently BFS-checks the lower templates at n=2,3,4,7. Diameter n-1 supplies the small-n upper bounds.

## Reproduction

From the workspace root run `python char3-independent-review/check_raw.py`. Full machine-readable outcomes are in results.json, and the captured output is in check.log. These are exact integer/modular checks, with no floating-point arithmetic.
