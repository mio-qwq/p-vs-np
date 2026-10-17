# Independent review: exact degree-two matching flip radius

Date: 2026-10-17. Verdict: PASS.

The frozen theorem and certificate hashes are respectively
765cb35eb5830be5b2d97601abf38be465f87a2a457f0aa64905db69b2cf0fe8 and
9ea13e4436d83da1942fd7b98156f93bc7a0a75ee570841c3eab388de02c263d.
The review did not import or execute the discovery, Gaussian elimination,
or orbit-reduction scripts, or the supplied certificate checker. The separate
standard-library check.py reads only the frozen theorem bytes and JSON data.

## Precise statement and scope

For a fixed baseline perfect matching B of the complete simple graph K_(2n),
let R be the least nonnegative integer such that any polynomial of total
degree at most two whose restriction to perfect matchings is nonzero has a
nonzero evaluation at flip distance at most R from B. Here a flip replaces
two matching edges by one of the other two pairings of their four endpoints.
Over every field of characteristic different from 2 and 3,
R=min(n-1,3) for n>=2 and R=0 for n<=1. The statement concerns functions
nonzero on the matching domain, not merely nonzero formal polynomials.
No historical novelty, complexity lower bound, or P-versus-NP consequence is
established. The characteristic-two comparison in the source is an external
result, unnecessary for this audited theorem. Characteristic three is not
resolved by this certificate.

## Independent combinatorial metric reconstruction

The union of B and M decomposes into alternating cycles, counting a common
edge as a component of size one. If there are C components in total, the
flip distance is n-C. Equivalently, if m baseline pairs change and c of the
components are nontrivial, it is m-c.

One flip removes two M edges. If they lie in distinct union components, a
nontrivial reconnection joins those components; if they lie in one component,
it can split that component into at most two. Hence a flip increases the
number of components by at most one, proving distance at least n-C. A
component involving l baseline pairs can be broken into common baseline
edges using l-1 flips: take adjacent M edges around that alternating cycle,
reconnect to insert their intervening B edge and reconnect the remaining
endpoints. This isolates that baseline edge and leaves an alternating cycle
on l-1 pairs (or finishes the l=2 component). Sum over components. This proves
the metric formula and diameter n-1 without relying on finite computation.

The checker separately generates every perfect matching on ten vertices by
recursive pairing, and generates the entire flip graph by BFS. Both yield
exactly the same 945 objects. The BFS distances agree with n-C for all of
them. Thus the metric interpretation of the certificate is independently
verified twice.

## Integer evaluation identity and full test-space completeness

The JSON has 49 terms expanding to 346 distinct matchings with integer
coefficients. Every listed matching is a valid perfect matching on vertices
0,...,9 and has BFS distance at most three. The target is valid and has
BFS distance four, hence is a five-pair alternating cycle. The multiplier
is exactly 48.

There are 45 edge variables. All formal monomials of degree at most two
number 1+45+45*46/2=1081, including squares and pairs of incident distinct
edges. The independent checker evaluates the proposed integer linear
identity directly on ALL 1081, and every equality holds exactly. No field,
numerical rank, or matrix reduction enters this check. Altering the first
expanded coefficient by one causes rejection.

For comparison, the smaller valid test space has 1+45+3*C(10,4)=676
monomials: constant, individual edges, and products of disjoint edges.
Squares evaluate as their linear variables, and products of distinct
incident edges evaluate to zero. Thus these 676 would also suffice. Testing
a spanning family of evaluations is enough; their linear independence is
neither needed nor asserted. Since every formal degree-two polynomial is a
linear combination of the 1081 checked monomials, the integer identity
holds on all such polynomials over every commutative coefficient ring.

## Independent recheck of the uniform support reduction

For completeness the needed support bound can be derived directly. Choose a
nonzero evaluation M minimizing (m,c) lexicographically, where m is changed
baseline-pair support and c its number of nontrivial alternating components.
On each component, pair consecutive M edges, leaving one M edge over exactly
when that component has odd size. Each consecutive pair can be switched to
insert the B edge between them. Pair leftover M edges from different odd
components and switch each pair across the components, thereby merging them.

All these switches have disjoint vertex sets. Their number is floor(m/2),
since every M edge in the changed support is paired except possibly one.
Any nonempty set of switches containing an internal switch inserts a baseline
edge and loses none, strictly reducing m. If a set contains only cross
switches, it joins disjoint pairs of original odd components, preserves m,
and strictly reduces c. Consequently all nonempty toggles have zero
polynomial evaluation by the chosen lexicographic minimum.

If m>=6, select three switches. Their incidence vectors form an affine
Boolean cube x(M)+y1*Delta1+y2*Delta2+y3*Delta3. Substituting this affine map
into a degree-two polynomial gives degree at most two. Its full third
alternating finite difference is zero, because each monomial omits at least
one variable. All seven nonempty cube evaluations vanish, whereas the
remaining evaluation is plus or minus f(M), a contradiction. Therefore m<=5.
This argument requires no division and holds in every characteristic. It
also covers constant polynomials. All switches exist because the host graph
is complete.

## Transport to arbitrary n and arbitrary baseline

When m<=4 the metric m-c is at most three (or zero for m=0). If m=5, each
nontrivial component has size at least two, so the only possible partitions
are 5 and 3+2. The latter already has distance three. For a five-cycle,
label its five baseline edges cyclically and label each pair's two endpoints
according to the direction around the alternating cycle. This gives a
baseline-preserving isomorphism from the certificate target to the witness.
Conversely such relabelings preserve matching incidence and flip distance.

As an additional finite check, the verifier explicitly acts by all 5!*2^5
baseline-preserving permutations and endpoint swaps. The resulting target
orbit has 384 matchings and equals the set of all distance-four matchings
on the ten vertices. Thus no five-cycle orientation or port pattern is
missing from the certificate's coverage.

Restrict the original polynomial to these ten vertices: substitute one for
all retained outside baseline edges and zero for every other edge not fully
inside the ten vertices, including boundary-crossing edges. These constant
substitutions cannot increase degree. Relabel and apply the identity.
Multiplication by 48 is injective in every field of characteristic other
than 2 or 3, so a nonzero target evaluation implies some nonzero RHS
evaluation. Extend that matching by the fixed outside baseline edges. Its
global distance is its internal distance, at most three. When n<5 the
diameter bound gives the smaller claimed upper bound directly. Relabeling
all vertices transports the result to any initial baseline B.

The field restriction is sufficient and exact for what THIS identity proves:
48=2^4*3, so it is invertible in precisely the stated fields. In
characteristics two or three the left multiplier vanishes, and this identity
cannot force a nonzero nearby evaluation. This is not evidence that the
radius formula fails in characteristic three. The optional ring statement
is valid under the stated injectivity of multiplication by 48; invertibility
is stronger than necessary.

## Uniform lower bounds and small cases

For n>=4 let q=(x02-x13)(x46-x57), with baseline pairs 01,23,45,67.
For the first factor to be nonzero, exactly one of edges 02 and 13 is
present. Its two baseline pairs then lie in a common alternating component.
That component cannot have size two, since containing 02 in a two-pair
component forces 13, and conversely. Thus its size is at least three.
The same argument applies to the disjoint pair-index set underlying the
second factor.

At distance at most two, the nontrivial component pattern is empty, 2, 3,
or 2+2. A size-two component cannot activate either factor. A sole size-three
component cannot contain all four distinct baseline pairs required to
activate both factors. Therefore q vanishes at distance at most two over
the integers. On edges 02,34,57,16, together with remaining baseline edges,
q=-1 and the alternating component has size four, giving distance three.
This works in every field, including characteristic two where -1=1.

For n=3 the monomial x12*x34 is one only on matching {12,34,05}, a
three-pair cycle at distance two. For n=2, x02 vanishes at the baseline and
is one on {02,13}, which has distance one. For n=0 or n=1 only one perfect
matching exists (the empty matching for n=0), so radius zero suffices and
is the least allowed radius.

The independent checker exhaustively confirms these lower polynomials on
all 11,463 perfect matchings across n=2,...,6, including attained minimal
nonzero distances 1,2,3,3,3. The symbolic argument, rather than those finite
tests, establishes the result for every n.

## Files and outcome

check.py is the independently written executable verifier; check.log records
its successful run. No source theorem or certificate file was modified.
No corrections are required to the frozen degree-two statement. The only
qualification worth making explicit in a presentation is that a nonzero
polynomial means a nonzero restriction to the matching domain.
