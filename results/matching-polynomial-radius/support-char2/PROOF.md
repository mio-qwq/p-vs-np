# Exact matching-polynomial support radius in characteristic two

Independent audit, 17 October 2026. Verdict: PASS with the necessary trivial
case correction n<=1. This document adds only a characteristic-two lower
bound to the separately audited all-field upper bound. It does not modify
the earlier frozen proof or implementation. Novelty is unverified.

## Precise statement

Fix baseline perfect matching M0 on 2n vertices. For a field K and d>=0,
let R_K(n,d) be the least integer radius such that every degree-at-most-d
polynomial in ordinary unordered edge-incidence variables that is nonzero
on some perfect matching is nonzero on a matching missing at most that many
baseline edges.

For every field K of characteristic two,

 R_K(n,d) = min(n,2d+1) when n>=2 and d>=1;
 R_K(n,d) = 0 when n<=1 or d=0.

The exception n=1 is essential: K2 has only its baseline perfect matching,
so no nonzero restricted polynomial can require one changed pair. In
particular the zero-by-zero Pfaffian does not establish a radius-one lower
bound. The all-field switch proof provides the upper bound used here.

## Contracted alternating matrix

Index baseline pairs by i=0,...,n-1, with ports 2i and 2i+1. Let x_uv=x_vu
be the matching-incidence variable on unordered edge {u,v}. For distinct
i,j set

 B_ij = x_(2i,2j) + x_(2i,2j+1)
      + x_(2i+1,2j) + x_(2i+1,2j+1),
 B_ii = 0.

Over characteristic two this symmetric zero-diagonal matrix is alternating.
Each entry has degree one in the ACTUAL matching-edge variables. Contracting
baseline pairs is a description of its evaluations, not a quadratic
permutation substitution.

On a perfect matching, an unchanged baseline pair has no edges to other
pairs, hence its row of B is zero. A changed pair has both ports matched
outside itself, so exactly two selected matching edges leave it. Therefore
the sum of its B row is 2=0 in K. Two cross edges to the same pair cancel
in B; they must not be replaced by a single Boolean adjacency indicator.
This cancellation is required, and correctly makes a two-pair alternating
cycle's contracted block zero.

## Lower bound when n>=2d+1

Assume d>=1 and select S of 2d pair indices. Define

 f(x)=Pf(B[S,S]).

The Pfaffian polynomial has degree at most d and is defined in characteristic
two by reduction of its integer polynomial; signs simply coincide there.

Suppose a matching changes at most 2d baseline pairs. If any index in S is
unchanged, the principal alternating matrix has a zero row and column, so
its Pfaffian vanishes. Otherwise all 2d indices in S are changed. The support
bound forces these to be the entire changed-pair set. Every outside pair
retains its baseline edge, using both its vertices, so no selected matching
edge can connect S to its complement. Each row of B[S,S] then sums to zero.
The nonzero all-ones vector lies in its kernel. Its determinant is zero,
and the polynomial identity det(A)=Pf(A)^2 for even alternating matrices
implies Pf(A)=0 over a field, including every characteristic-two field.

For a nonzero evaluation, take a simple contracted cycle on S and one extra
pair, of length 2d+1>=3. Explicitly, if the cycle pair indices are
0,...,2d, select the actual matching edges

 {2i+1, 2*((i+1) mod (2d+1))}, i=0,...,2d,

and retain baseline edges on all other pairs. These edges use each port
exactly once, so they form an actual perfect matching. Its contracted B
has entry one on each simple cycle edge. Deleting the extra index leaves
the adjacency matrix of a path on 2d vertices. That path has a unique perfect
matching, so its Pfaffian is one. This establishes that radius 2d fails,
while the nonzero witness changes exactly 2d+1 pairs.

## Saturation for smaller n

If n=2r+1>=3 is odd and n<=2d+1, then 1<=r<=d. Apply the preceding
construction with S of size n-1=2r and degree r. It vanishes whenever fewer
than n pairs change and evaluates to one on a simple contracted n-cycle.
Therefore the necessary radius is n.

If n=2r>=2 is even and n<=2d+1, then r<=d. Use the monomial

 g(x)=product_(j=0,...,r-1) x_(4j,4j+2).

Each chosen edge connects two different baseline pairs, and the chosen
edges together touch all n baseline pairs. A matching with g=1 contains
all those edges, forcing every baseline pair to change. The evaluation is
realizable: add the edges {4j+1,4j+3} for all j, pairing the remaining ports.
The resulting perfect matching has g=1 and changes exactly n pairs. Thus
radius n is necessary. This even-n lower example also works in other
characteristics, but no general odd-characteristic sharpness is asserted.

Combined with the all-field upper bound and the trivial cases, these lower
examples prove the exact characteristic-two formula above.

## Applicability and limits

This is sharpness for arbitrary degree-d polynomial FUNCTIONS on all perfect
matchings, measured by changed baseline pairs. It does not by itself show
that the matching-search runtime, the color-coding algorithm, or the
particular parity-plus-legality polynomial family needs this radius.
A valid lower example here is not automatically an instance realizing the
worst case in every more restricted algorithmic application.

The direct support upper bound, this characteristic-two lower bound, and
the port-coloring algorithm are separate obligations. No historical novelty
claim is made. No odd-characteristic sharpness claim should be inferred
from characteristic-two row-sum cancellation.

## Independent exact checks

check.py exhausts all perfect matchings for n=2,...,6 baseline pairs and
d=1,...,4. It evaluates the actual contracted Pfaffian or even-n monomial,
checks vanishing below the claimed radius, and confirms that the minimum
nonzero support is exactly min(n,2d+1) in each case. It also verifies the
K2 singleton exception. These evaluations use GF(2); the symbolic argument
above extends to every characteristic-two field because all construction
coefficients and evaluated matrix entries belong to its prime subfield.

Final check.log: PASS, 45,852 polynomial evaluations across 20 parameter
cases. The frozen upper-bound proof and root implementation were not changed.
