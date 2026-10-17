# Direct matching-polynomial support upper bound: independent audit

17 October 2026. Verdict: PASS. This is only an upper-bound theorem. Neither
sharpness nor historical novelty is asserted. The argument is field-uniform.
This is separate from the earlier frozen permutation-lift implementation;
none of its files were modified.

## Theorem

Fix a perfect matching B of the complete simple graph on 2n vertices. For a
perfect matching M let x(M) be its zero/one incidence vector on unordered
edges. Let f be a polynomial over any field K in those edge variables, of
total degree at most d, whose restriction to the perfect matchings is not
identically zero. For d>=1, there exists M with f(x(M)) nonzero such that
at most min(n,2d+1) edges of B are missing from M. Equivalently, M differs
from B on at most min(n,2d+1) baseline pairs. For d=0, B itself suffices.

## Construction of a switch cube

Choose a nonzero matching M minimizing lexicographically (m,c), where
m=|B minus M| and c is the number of nontrivial alternating cycles in the
symmetric difference B triangle M. Each such cycle has an equal number of
baseline and M edges, at least two of each. Count its length here in M edges,
not in ordinary graph edges. There are exactly m M edges across these cycles.

Orient each alternating cycle, writing its M edges as

 (a_1,b_1), (a_2,b_2), ..., (a_l,b_l),

so that {b_i,a_(i+1)} belongs to B, with cyclic subscripts. Pair M edges
consecutively as (1,2), (3,4), and so on. For odd l, leave edge l unpaired.
Each consecutive pair receives the following INTERNAL switch:

 remove {a_i,b_i} and {a_(i+1),b_(i+1)};
 insert {b_i,a_(i+1)} and {a_i,b_(i+1)}.

All four vertices are distinct. This is a matching on the same four vertices,
and its first inserted edge is in B. If l=2, its second inserted edge is also
in B, which is permitted and gives a larger support decrease.

Pair the leftover edges from distinct odd cycles arbitrarily, leaving at most
one leftover edge globally. For each such pair (a,b), (u,v), choose the CROSS
switch

 remove {a,b} and {u,v}; insert {a,u} and {b,v}.

The four vertices belong to two disjoint original alternating cycles. Neither
new edge belongs to B, since B edges stay inside those original cycles.
Deleting one M edge from each original cycle opens two disjoint alternating
paths. The cross switch connects their endpoints into exactly one alternating
cycle. Either of the two cross reconnections would work; the displayed choice
makes the construction explicit.

These operations pair exactly floor(m/2) M edges-pairs: internal pairings
account for sum floor(l/2), while pairing odd-cycle leftovers accounts for
floor(number of odd cycles/2). Different operations remove disjoint M edges,
so their vertex sets are disjoint. In particular, an odd cycle's leftover
edge is vertex-disjoint from every internally paired edge in that cycle.

## Every nonempty toggle improves the minimization criterion

Apply any nonempty subset of these switches simultaneously.

If it includes an internal switch, at least one new baseline edge is inserted.
No other switch can touch either endpoint of that baseline edge because
switch vertex sets are disjoint. No switch removes a previously selected
baseline edge: all removed M edges lie in the nontrivial symmetric-difference
cycles. Thus the number of missing baseline edges strictly decreases, whether
or not some cross switches are also selected. The changed-pair count cannot
increase elsewhere to offset this decrease, because all previously selected
baseline edges survive.

If it includes only cross switches, each joins two different ORIGINAL odd
cycles. Each original odd cycle supplied at most one leftover edge, hence
appears in at most one cross switch. The selected cross switches therefore
join disjoint pairs of original cycles. No selected baseline edge is lost,
and no baseline edge is gained, so m is unchanged. If r cross switches were
selected, c decreases exactly by r. Thus (m,c) decreases lexicographically in
every nonempty case.

This handles simultaneous internal/cross operations without assuming that
internal switches preserve cycle structure. Once any internal switch occurs,
only the strict decrease in m is needed.

## Polynomial contradiction

Suppose m>=2d+2. Choose any d+1 switches from the floor(m/2) available ones.
For switch j, let Delta_j be the new incidence vector minus the old incidence
vector on its four vertices. The incidence vector obtained from toggle bits
y_1,...,y_(d+1) is exactly

 x(M) + sum_j y_j Delta_j.

This equality is an equality over the integers before reduction to K. Switches
have disjoint endpoint sets, so no inserted or removed edge can overlap an
edge changed by another switch. Consequently it truly describes every
Boolean cube vertex, with no products of toggles or hidden interference.
Every cube vertex is a perfect matching of the complete graph.

Substituting this affine expression into f yields a polynomial in d+1 toggle
variables of total degree at most d. Its full alternating finite difference
on {0,1}^(d+1) is zero over every field: every monomial misses at least one
toggle variable, and summing over that variable cancels its two contributions.
This remains valid in characteristic two, where subtraction equals addition.

Every nonempty-toggle evaluation is zero by lexicographic minimality of M.
The untoggled evaluation is nonzero, and its coefficient in the alternating
sum is either +1 or -1, nonzero in any field. Contradiction. Therefore
m<=2d+1. Also m<=n automatically, proving the theorem. Constant polynomials
are handled separately by evaluating at B.

## Consequence for labeled allowed-edge matchings

For k-bit edge labels, the k target-parity factors are linear in the direct
edge-incidence variables. If the forbidden-edge graph has a verified vertex
cover C of size q, each covered vertex's allowed incident-edge sum is also
linear. Their product is the exact allowed-target indicator on all perfect
matchings and has degree at most d=k+q over GF(2). Every matching selects
exactly one incident edge per vertex, so these sums are genuine zero/one
legality checks, not parity approximations to legality.

The theorem gives a valid matching differing from the fixed baseline on at
most min(n,2(k+q)+1) pairs. The previously audited pair-coloring/port-cycle DP
therefore remains complete with this improved parameter, with mandatory
forbidden baseline pairs reserved and covered exactly as before. The original
4(k+q)+1 bound and frozen code remain correct but use a looser cutoff. This
proof does not assert that 2(k+q)+1 is best possible for this application.

## Scope, prior art, and executable evidence

The earlier audited argument obtained 4(k+q)+1 by lifting matchings to
permutation matrices, doubling the degree. This direct argument avoids that
degree doubling. It does not establish novelty. In particular, a switch-cube
lemma of this form could already exist in work on matching polynomial
functions or matching association schemes. No historical claim should be
made without a separate literature investigation.

The accompanying independent check.py enumerates every perfect matching on
0,2,4,...,12 vertices. For each it constructs all internal and cross switches
as above and tests EVERY nonempty subset of the full constructed switch set.
It verifies vertex-disjoint switches, proper matching reconstruction, integer
affinity of all changed edge coordinates, strict support decrease whenever
an internal switch occurs, and exact cycle-count decrease for cross-only
subsets. Checking the full switch set also checks every subset of any chosen
d+1 switches. The test is structural and does not substitute finite checks
for the polynomial proof.

Final check.log: PASS, 11,465 matchings and 57,834 nonempty cube vertices,
including 57,194 subsets containing internal switches and 640 cross-only
subsets. There were no failed assertions or counterexamples.
