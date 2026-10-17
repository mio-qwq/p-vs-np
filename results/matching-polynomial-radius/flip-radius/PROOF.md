# Exact flip-distance testing radius: separate audit

17 October 2026. PASS, with no novelty or odd-characteristic lower-bound claim.
A flip replaces two matching edges by one of the other two perfect matchings
on their four vertices. All intermediate matchings are in the complete graph.

## Metric identity

Let m be the number of changed baseline pairs, and c the number of nontrivial
alternating cycles against the baseline. The flip distance is m-c. Each
alternating cycle with l baseline edges can be resolved in l-1 flips, each
restoring a baseline edge until the last two-pair cycle is resolved. This
gives the upper bound. Count all alternating components, including shared
baseline edges as doubled-edge components. Their number is n-m+c. A flip
increases their number by at most one: it either cuts two matching edges in
one component or touches two components, producing at most one extra
component. Reaching the baseline's n components requires at least m-c flips.

For n>=2, the diameter is n-1, attained by a single alternating cycle using
all pairs. For n<=1, the graph has a single matching and diameter zero.

## Upper bound over every field

The separately audited direct matching support theorem supplies a nonzero
polynomial evaluation with m<=2d+1 for d>=1. If m=0 its distance is zero;
otherwise c>=1 and its distance m-c is at most 2d. Together with the diameter,
the universal testing radius is at most min(n-1,2d) for n>=2. Degree-zero
polynomials require radius zero.

## Characteristic-two lower bounds

Use the contracted alternating matrix B from the separate support-sharpness
proof: B_ij is the sum of the four actual edge-incidence variables joining
baseline pairs i and j, and B_ii=0. At a matching, a changed-pair component of
length l contributes a block with the all-ones vector in its kernel, hence
rank at most l-1. Unchanged pairs contribute zero rows. Therefore

 rank(B) <= sum_components(l-1) = m-c = flip distance.

For n>=2d+1, take the principal Pfaffian on 2d indices. If it is nonzero,
that principal block is nonsingular by det=Pf^2, so rank(B)>=2d and the
matching has distance at least 2d. A simple contracted (2d+1)-cycle realizes
value one and has distance 2d. Its degree is d.

For odd n=2r+1>=3 with n<=2d+1, take the principal Pfaffian on n-1=2r
indices. Its degree r is at most d. The same rank argument forces distance
at least n-1, and a full n-cycle realizes value one.

For even n>=4 in the saturated regime n-1<=2d, choose distinct pair indices
a,b and let S be all other n-2 indices. Use

 g = B_ab * Pf(B[S,S]).

Its degree is 1+(n-2)/2=n/2<=d. If B_ab is nonzero at a matching, exactly
one matching edge joins pair a to pair b. Thus a and b belong to the same
nontrivial alternating component of length at least three. They cannot form
a two-pair component, whose two cross edges cancel in B_ab.

If there were any other component, all its indices would lie in S. An
unchanged pair gives a zero row in B[S,S]. A nontrivial component gives an
isolated block with an all-ones kernel. In either case B[S,S] is singular,
so its Pfaffian is zero. Therefore a nonzero g forces every pair into the
single component containing a,b, and hence distance n-1. Conversely take
a full simple contracted n-cycle with a,b adjacent. Then B_ab=1, and
removing a,b leaves a path on n-2 even vertices with a unique perfect
matching. The principal Pfaffian and g both equal one.

For n=2, an individual cross-edge variable has degree one and requires
one flip, establishing the remaining case.

Thus over EVERY characteristic-two field the exact radius is
min(n-1,2d) for n>=2,d>=1, and zero for n<=1 or d=0. The lower proof uses
characteristic-two cancellation; no general odd-characteristic sharpness
is claimed. These are polynomial testing radii, not algorithmic runtime
lower bounds. Historical novelty remains unverified.

## Independent evidence

check.py evaluates the lower constructions on every perfect matching for
n=2,...,6 and d=1,...,4. All 45,852 polynomial evaluations pass, with minimum
nonzero distance exactly the proposed radius in all 20 parameter cases.
It separately compares the metric formula with exhaustive breadth-first
search of the actual complete flip graphs through ten original vertices:
1,069 matching distances agree. The files check.py and check.log preserve
the executable check and its output. All frozen previous artifacts remain
unchanged.
