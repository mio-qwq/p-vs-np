# Degree-two flip radius in characteristic three

Exact finite certificates, with a uniform consequence. No novelty claim.

Let B be a fixed perfect matching on 2n vertices. Let R_2(n;K) be the
least r such that every polynomial of degree at most two in edge indicators
which vanishes on the flip-distance-r ball around B vanishes on all perfect
matchings. For a field K of characteristic three,

- R_2(n;K)=0 for n<=1;
- R_2(n;K)=min(n-1,3) for 2<=n<=4 and for n>=7;
- R_2(5;K)=R_2(6;K)=4.

Thus the exceptional radius-four behavior in characteristic three is confined
to n=5,6. The radius is not monotone in n.

## Exact certificates and their semantics

The baseline is {(0,1),(2,3),...,(2n-2,2n-1)}. Each edge is an unordered
vertex pair, and each matching is a list of such edges.

witness_n5.json and witness_n6.json describe polynomials over F_3. Each term
has an integer coefficient and a list of monomials; the term means its
coefficient times the SUM of those monomials. A monomial is a list of edges,
interpreted as the product of their indicators. The empty monomial is 1.
These are explicit polynomials of degree at most two, with 116 and 521 listed
monomials respectively. They vanish on EVERY matching at flip distance <=3,
and take value 1 on the listed target of distance four. The n=6 witness has
no edge outside vertices 0,...,9, but this does not make it valid at larger n:
extension_failure.json gives a radius-three n=8 matching with nonzero value.

certificate_mod3_n7.json describes the evaluation-functional identity

  ev_target = sum_terms coefficient * sum_matchings ev_matching   (mod 3).

There are 49 terms and 1,273 listed matching evaluations. Every matching on
the right is at distance <=3. The target is the five-baseline-pair alternating
cycle with edges {2i+1,2(i+1 mod 5)} for i=0,...,4, together with baseline
edges (10,11),(12,13). The identity holds on EVERY degree-at-most-two
polynomial over every characteristic-three field.

## Independent verification

Run python check_certificates.py using only the Python standard library.
It does not import discovery scripts or use linear algebra or group orbits.
It constructs exact flip balls by breadth-first search with both possible
two-edge switches. The radius-three balls have cardinalities 561, 2171,
6623 for n=5,6,7. It evaluates each lower polynomial on every point of its
ball, checks target value 1 and target distance exactly four, then verifies
the upper identity on all monomials that occur in its evaluations. All other
monomials have zero evaluation in every term. It rejects a deliberately
corrupted coefficient. Repeated-edge monomials reduce to x_e; products of
distinct incident edges vanish, so this covers every degree-two polynomial.
The integer arithmetic is reduced modulo three only in final equality tests.

## Uniform upper bound and finite exceptions

Use the previously independently audited matching-support theorem: a
nonzero degree-d polynomial function has a nonzero witness changing at most
2d+1 baseline pairs. At d=2 this is at most five, over every field.
For a matching whose nontrivial alternating components use m baseline pairs
and number c, its flip distance is m-c. Thus every witness changing <=4
pairs has distance <=3; every witness changing <=5 has distance <=4.
This already proves the required upper four at n=5,6.

Suppose n>=7 and a witness changes five pairs. Unless these form one
five-pair alternating cycle, its distance is <=3. In the five-cycle case,
choose two untouched baseline pairs. Restrict the polynomial to these seven
pairs by fixing all other baseline edges. This does not increase degree.
Relabel baseline pairs and their endpoints to map the witness to the target
of certificate_mod3_n7.json. The identity forces a nonzero evaluation at
radius <=3. Restoring the fixed outside edges preserves this distance.
This proves the uniform upper three for n>=7. No division by 3 is used.
For n<=4 the matching-graph diameter n-1 gives the upper bound directly.

## Remaining lower bounds

For n>=4 use (x_{0,2}-x_{1,3})(x_{4,6}-x_{5,7}). It vanishes at distance
<=2 and is -1 at the distance-three matching with edges
{0,2},{3,4},{5,7},{6,1}, all other baseline edges retained. A nonzero first
factor requires its two indicated baseline pairs in a component of size
at least three; likewise the second factor. The possible distance<=2
component patterns (2), (3), (2+2) cannot satisfy both requirements.
For n=3, x_{1,2}x_{3,4} vanishes at distance<=1 and is 1 on the unique
matching containing those edges, a three-pair cycle. For n=2, x_{0,2}
separates baseline from a one-flip matching. n<=1 is immediate.

## Discovery and limitations

The discovery scripts use modular linear algebra and symmetry; they are not
needed to check the certificates. The target stabilizer used at n=7 has
order 80 (D5 acting on the five-cycle, independently permuting and swapping
the two extra baseline pairs). Its order is invertible modulo three, so
averaging preserves an evaluation certificate or witness. The smaller D5
symmetry has order 10, also invertible modulo three. An unsuccessful
internal-edge-only search at n=8 is exploratory and is not needed for the
proof. This result is an exact local polynomial-testing theorem, not a
runtime lower bound or a P versus NP result.
