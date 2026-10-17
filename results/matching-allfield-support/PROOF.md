# All-field exact changed-pair radius via a signed hafnian

Independent audit, 17 October 2026. Verdict: PASS. This separate note strengthens
the characteristic-two changed-pair lower bound. It does not modify staged
characteristic-two proofs, the direct upper proof, or any solver. Historical
novelty is unverified. The flip-distance lower bound remains characteristic-two.

## Exact statement

For n>=2 and d>=1, over EVERY field K, the universal testing radius for
polynomials of degree at most d in ordinary perfect-matching edge-incidence
variables on K_(2n), measured in changed baseline pairs, is

 min(n,2d+1).

For n<=1 or d=0 it is zero. The separately audited switch-cube proof gives
the upper bound. The following lower polynomials have integer coefficients,
vanish as integers at all forbidden-radius evaluations, and attain +1 or -1
at a witness. Their reductions therefore work in every field. In fact both
the lower construction and the switch-cube upper proof work over every
nonzero commutative unital ring: the upper proof uses only additions,
subtractions, affine substitution, and a coefficient +1 or -1; there is no
division or domain assumption. The nonzero-ring qualification is essential.

## Signed contraction and the polynomial

Index baseline pairs by i with ports (i,0)=2i and (i,1)=2i+1. Fix S of size
2d and a distinguished index a in S. For distinct i,j neither equal to a,
define the symmetric matrix entry

 B_ij = sum_(alpha,beta in {0,1}) x_{(i,alpha),(j,beta)}.

For an edge of the contracted matrix incident to a, define

 B_aj = sum_(alpha,beta in {0,1}) epsilon_alpha
                                      x_{(a,alpha),(j,beta)},
 epsilon_0=+1, epsilon_1=-1, and B_ja=B_aj.

Set the diagonal to zero. These are linear polynomials in actual unordered
matching-edge variables. Symmetry is intentional; no skew-matrix convention
or Pfaffian sign is used.

Let

 q(x)=haf(B[S,S])
     = sum_(perfect matchings F of the pair-index set S)
                         product_({i,j} in F) B_ij.

This is the HAFNIAN, with no signs from the ordering of F. Each term has d
matrix entries, so total degree is at most d.

## Meaning of the actual-edge expansion

Evaluate at an actual perfect matching M. Expand every selected B_ij into
its actual cross-edge summands. Every surviving expanded term selects d
actual edges of M such that each pair index in S is incident to exactly one
of those selected edges. Conversely every such actual-edge selection gives
exactly one expanded term: its underlying pairs determine F, and its actual
edges determine the chosen summands. This bijection retains multiplicities
when two different actual edges join the same baseline pairs.

There is exactly one selected edge incident to pair a. The expanded term's
weight is +1 if that edge uses port zero of a and -1 if it uses port one.
All other selected edges have weight +1. This describes the expansion over
the integers before any characteristic reduction.

## Vanishing within 2d changed pairs

Suppose M changes at most 2d baseline pairs. If any i in S is unchanged,
it has no selected cross edges, so row i of the evaluated B[S,S] is zero
and every hafnian term vanishes.

Otherwise every pair in S is changed, so S is exactly the changed-pair set.
Pairs outside S retain their baseline edges and cannot send a matching edge
into S. Contracting baseline pairs in the actual matching cross edges yields
a loopless 2-regular MULTIGRAPH on S: every vertex has degree two because
both its ports are matched externally. Components are simple cycles of
length at least three, or two-vertex cycles with two parallel actual edges.

A surviving expanded term is a perfect matching of this multigraph, with
parallel edges kept distinct. If any component has odd length, there are
no such terms. Otherwise consider the even cycle component containing a.
Every perfect matching of this component is one of its two alternating
edge sets, including the two distinct singleton choices in a parallel
2-cycle. Replace the chosen alternating set by the other one, leaving the
choices in every other component unchanged.

This is a fixed-point-free involution on surviving expanded terms. The two
actual M edges incident to a use its two different ports. Consequently the
involution reverses the selected port at a, and hence reverses the term's
weight. All other sign factors are absent. Paired terms cancel over the
integers. Thus q(M)=0 as an INTEGER for every M changing at most 2d pairs.

Parallel-edge cancellation is fully included, not asserted after collapsing
the multigraph. If the component at a has two vertices, its two terms have
weights +1 and -1. Other parallel 2-cycles contribute multiplicity two,
which does not interfere with the cancellation at a.

## Nonzero witness at 2d+1 pairs

Assume n>=2d+1. Choose an extra pair index outside S and realize a simple
contracted cycle on S plus that index, with all other pairs unchanged. For
cycle indices 0,...,2d, actual matching edges can be taken as

 {(i,1),((i+1) mod (2d+1),0)}, i=0,...,2d.

Each port is used exactly once. Removing the extra index leaves a path on
2d vertices. Its unique perfect matching gives the sole surviving hafnian
term. All its weights equal +1 except possibly the single edge at a, which
has weight +1 or -1. Hence q evaluates to +1 or -1, a unit and therefore
nonzero over every nonzero unital ring. This proves that radius 2d fails.

## Smaller n and trivial cases

For odd n=2r+1>=3 with n<=2d+1, use the same construction on n-1=2r indices,
with degree r<=d. It vanishes whenever fewer than n pairs change and attains
+1 or -1 on a full n-cycle.

For even n=2r>=2 with n<=2d+1, use the degree-r monomial

 product_(j=0,...,r-1) x_{4j,4j+2}.

Every nonzero evaluation contains all these edges, which touch all n
baseline pairs and therefore change every pair. Add edges {4j+1,4j+3} to
realize a perfect matching where the monomial is one. Here r<=d.

For d=0 every nonzero restricted constant already evaluates nonzero at the
baseline. For n=0 or 1 there is only one perfect matching. These cases have
radius zero, not the unqualified formula min(n,2d+1).

## Why the flip-distance claim is NOT upgraded

The signed hafnian's integer vanishing argument concerns changed-pair support,
not the distance m-c in the two-edge-flip graph. A simple contracted 3-cycle
containing a and the omitted index, together with another contracted 2-cycle,
can yield +2 or -2 while using only three flips.

For example take n=5,d=2,S={0,1,2,3},a=0 and actual matching

 {{1,2},{3,8},{0,9},{5,6},{4,7}}.

Its contracted components are the 3-cycle on {0,1,4} and the parallel 2-cycle
on {2,3}. On S, B_01=-1, B_23=2, and all other hafnian terms vanish, so
q=-2. All five baseline pairs change, as required by the support lower bound,
but m-c=5-2=3<2d=4. Thus this polynomial cannot establish the earlier
characteristic-two flip-radius lower bound in odd characteristic. No all-field
flip-distance sharpness conclusion is claimed.

## Independent checks and limits

check.py performs exact INTEGER hafnian/monomial evaluations on every perfect
matching for n=2,...,6 and d=1,...,4: 45,852 evaluations across 20 parameter
cases. Every evaluation below the proposed support radius is zero; each
case has a +1 or -1 witness at the exact radius.

It separately expands actual-edge selections for every matching whose changed
set is a prescribed even S through n=6, including S equal to all indices.
On 6,230 inputs it verifies 14,852 surviving terms: toggling the entire
component at a gives another term, has no fixed point, is involutive, and
reverses the sign. All assertions pass. check.log records both completed
checks.

These finite tests supplement the symbolic proof, not replace it. This is
sharpness for the entire degree-bounded polynomial-function class; it does
not establish runtime lower bounds or tightness for every restricted parity
indicator family. Historical novelty remains unverified.
