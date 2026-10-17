# Degree-two flip testing outside characteristics two and three

Research result pending independent review. No novelty claim.

For a field K of characteristic other than 2 or 3, the exact flip-distance
radius for degree-at-most-two polynomial functions on perfect matchings of
K_(2n), relative to any fixed baseline matching, is min(n-1,3) for n>=2.
It is zero for n<=1. This differs from the characteristic-two radius
min(n-1,4) established separately. No general characteristic-three claim
is made here.

## Exact finite certificate

orbit_certificate.json contains an integer evaluation identity on ten vertices:

  48 ev_target = sum_M c_M ev_M.

The target is a single alternating cycle on five baseline pairs. Every matching
on the right is at flip distance at most three from the baseline. The identity
holds on every degree-at-most-two polynomial function.

The standard-library checker reconstructs the full flip graph by BFS (945
matchings), checks every right-hand matching and distance, then verifies the
identity on all 676 potentially nonzero squarefree monomials of degrees zero,
one and two. Repeated edges reduce by x_e^2=x_e; products of distinct incident
edges vanish on every matching, so these tests cover all such polynomials.
The checker rejects a deliberately corrupted coefficient. It uses neither
Gaussian elimination nor the orbit reduction used to discover the certificate.

The discovery script uses exact SymPy rational elimination on stabilizer orbits.
It is not needed to verify the result. The certificate has 49 orbit terms,
expanding to 346 weighted matchings, with common integer multiplier 48.

## Uniform upper bound for every n

The independently audited direct matching support theorem with d=2 gives a
nonzero witness changing at most five baseline pairs. If at most four pairs
change, its flip distance m-c is at most three. If exactly five change, their
alternating-cycle type is either 3+2 (already distance three) or one five-cycle.

Every five-cycle witness is obtained from the certificate target by permuting
baseline pairs and swapping their two ports. Restrict the polynomial by fixing
all outside baseline edges; its degree remains at most two. Relabel the
certificate accordingly. Since 48 is nonzero in K, a nonzero target evaluation
forces at least one nonzero right-hand evaluation, at distance at most three.
For n<5, the diameter bound n-1 gives the stated upper bound directly.

## Matching lower bounds

For n>=4 use the degree-two polynomial

  (x_{0,2}-x_{1,3}) (x_{4,6}-x_{5,7}).

A nonzero first factor puts baseline pairs (0,1) and (2,3) in an alternating
component of length at least three: a two-pair component either contains both
listed edges or neither, giving zero. The same holds for pairs (4,5),(6,7).
At distance at most two, the only possible nontrivial component patterns are
one two-pair cycle, one three-pair cycle, or two two-pair cycles. None can make
both factors nonzero. On the matching with edges

  {0,2}, {3,4}, {5,7}, {6,1}

and all other baseline edges retained, the value is -1 and the flip distance
is three. Thus radius two fails over every field.

For n=3, the product x_{1,2} x_{3,4} forces the third edge {0,5}; this unique
matching is a three-pair cycle and has distance two. For n=2, x_{0,2} forces
an alternative matching at distance one. The trivial cases are immediate.

Together these prove the exact formula over the stated fields. The integer
upper identity also works over rings in which multiplication by 48 is
injective, but no ring generalization is needed for this statement.

## Scope

This is an exact polynomial-testing radius, not a runtime lower bound or a
P versus NP result. The certificate does not invert 48 in characteristics
2 or 3, so no upper bound in those characteristics follows from it. Finite
modular rank observations in results.json and flip_results.json are exploratory
context and are not used as substitutes for this explicit identity.
