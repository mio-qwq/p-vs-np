# Independent audit: general-graph parity matching by pair color coding

17 October 2026. Verdict: mathematical PASS, conditional on the stated
permutation support theorem. This is a deterministic FPT result for the
specified parameterization; neither novelty nor any general P-versus-NP
consequence is asserted. Work is local, with no prior-art search.

## Statement and algebraic reduction

Let G be a simple undirected graph on vertices 0,...,2n-1, with k-bit labels
and target b. Initially take G complete. Fix baseline matching
M0={(2i,2i+1):0<=i<n}. For a permutation matrix with row r mapping to p(r),
put

 E_uv(P)=sum_i [P_(2i,u) P_(2i+1,v)+P_(2i,v) P_(2i+1,u)] (u<v).

Over GF(2), E_uv on permutation matrices is exactly the indicator that the
image of M0 contains {u,v}. It cannot have two contributing baseline pairs,
because a permutation uses each vertex once. Every perfect matching is an
image of M0 under some permutation. If L_j=sum_(u<v) label_j(uv) E_uv, then
F=product_j (1+L_j+b_j) has degree at most 2k and takes value one exactly on
target matchings. When a target exists and k>=1, the support theorem supplies
such a permutation moving at most min(2n,4k+1) vertices.

Let S be its moved vertices and let T be the set of baseline pairs meeting S.
Every baseline pair outside T has both vertices fixed, so remains in the
image matching. Thus the number of changed baseline pairs is at most
|T|<=min(n,|S|)<=min(n,4k+1)=t. This argument does not require T to consist
only of genuinely changed pairs. Some pairs meeting S can still map to
baseline pairs. Equivalently S union its baseline partners is invariant
under p: S is invariant, and each vertex outside S is individually fixed.
When k=0, the baseline already solves the complete instance; degree-zero
support is zero, and using the looser t=min(n,1) is harmless.

The symmetric difference between M0 and another perfect matching is a union
of disjoint even alternating cycles. Each has at least two baseline pairs.
Contracting those pairs gives a cycle of pairs with two distinguished ports
per pair. A two-pair cycle is permitted: it has two different cross edges
joining the two pairs. It must not be mistaken for a forbidden duplicate edge
or excluded by requiring three pairs.

## Exact port DP and reconstruction

Write pair i's vertices as (i,0)=2i and (i,1)=2i+1. Set
B_i=label({2i,2i+1}) and D=b XOR (XOR_i B_i).
For a fixed coloring h:[n]->[t], fixed start pair s, and fixed start ENTRY
port a, maintain states (C,i,e,z), where C is the used color set, i the last
pair, e its entry port, and z the accumulated delta. Initialize
({h(s)},s,a,0). Starting with entry port a conceptually traverses the
baseline edge inside s to exit 1-a; no graph edge is emitted yet.

For any new-color pair j and entry port f, emit the new matching edge
{(i,1-e),(j,f)}, add B_i XOR label(this edge) to z, and enter
(C union {h(j)},j,f,new_z). At a state with at least two used colors, close
by emitting {(i,1-e),(s,a)} and adding B_i XOR its label. Store one concrete
cycle for each (C,final_z), across all starts and orientations.

Each participating pair contributes exactly one outgoing new edge and one
baseline label. Every vertex is used exactly once: its entry port is an
incoming edge endpoint and its opposite port is an outgoing endpoint.
The closing edge uses the initially unused start entry port. Hence every
stored object is a replacement matching on its pairs, and its stored XOR
is exactly new labels XOR removed baseline labels. No loops occur because
all transitions and closure connect distinct pairs. This remains valid for
a two-pair cycle; the two cross edges use complementary ports.

State compression is safe only with fixed start pair AND start entry port,
and with the last entry port retained. These determine exit and closing
endpoints. A fresh-color pair cannot occur earlier in either representative
path. Thus retaining one path per state preserves all possible extensions.
After closing, one representative per (C,z) suffices: compatibility of cycles
uses disjoint colors, hence disjoint pairs and vertices, independently of
which representatives were kept.

Pack stored cycles using states (U,z), initially (empty,0), adding any cycle
with color set disjoint from U. Accept z=D for ANY U, including the empty
set. Reconstruct each emitted new edge and append all baseline edges whose
pairs do not occur in reconstructed cycles. Do not return the baseline edges
from inside the cycles: they are removed, not selected.

For completeness choose a target matching with at most t changed baseline
pairs. A t-perfect coloring is injective on these pairs, after padding the
set to size t if necessary. Orient each alternating cycle and choose its
entry ports. The stated DP generates its mask and delta. State compression
can replace a cycle but preserves exactly the information needed to pack
all masks and reach D. Soundness follows from the port incidence and XOR
identities above.

## Explicit deterministic family and complexity

Use the independently stated family in the supplied complete-bipartite proof,
now applied to baseline pair IDs. For n>=2 and t>=2, L=ceil(log2 n),
r=min(L,t-1); enumerate r bit positions and all t-subsets of their 2^r
codes, assign those codes distinct colors and send other codes to color zero.
Every t-set is separated by at most t-1 bits, so this is t-perfect. Its size
H=binom(L,r) binom(2^r,t) is bounded by

 H <= (2/ln 2)^(t-1) (t-1)! 2^(t(t-1)) n.

Use a constant coloring for t<=1. Empty instances are direct base cases.

Across all 2n choices of start pair/entry port there are at most
4n^2 2^(t+k) path states. Each has at most 2n extensions and one closure.
At most 2^(t+k) cycle states and packing states exist. A simple implementation
can examine at most 4^(t+k) packing-state/cycle pairs. Predecessor storage
avoids path-copy overhead; an implementation copying at most t edges per
witness still fits the safe per-color bound

 O(t n^3 2^(t+k) + t^2 4^(t+k) + nt).

Multiply by H and add input reading/verification costs O(n^2 k), with
polynomial factors for k-bit XOR and log n-bit indexing in a bit model.
The exponent of n can be taken as four (up to ordinary input/index bit
factors), independent of the parameter. Memory is f(t+k) poly(n).
Thus t<=4k+1 yields deterministic f(k) poly(input-size) time. Established
Derksen radius 3d with d=2k instead gives t<=6k and the same FPT conclusion.
The new sharp radius is unnecessary for the qualitative FPT claim.

## Forbidden edges covered by q vertices

Let C be a VERIFIED vertex cover of the complement graph, |C|=q. Define
arbitrary labels on forbidden edges, e.g. zero. For each v in C put
A_v(P)=sum_(u:uv allowed) E_uv(P). Each has degree at most two and equals
one precisely when v's selected matching edge is allowed, since exactly one
matching edge is incident to v. Every forbidden edge meets C. Consequently

 F(P)=product_(v in C) A_v(P) product_j(1+L_j(P)+b_j)

is exactly the allowed-target indicator on all permutation matrices, of
degree at most 2(k+q). The support theorem therefore gives at most
 t=min(n,4(k+q)+1)
changed baseline pairs. The row-swap proof is still applied to all
permutations, with legality encoded by the polynomial, not by restricting
the row-swap domain.

Let Q={i:baseline edge i is forbidden}. These baseline edges are disjoint,
so |Q|<=q, and every valid matching changes every pair in Q. For each
coloring reject collisions on Q. Reserve each h(i), i in Q, exclusively
for pair i: exclude every other pair with that color from the cycle DP.
Permit only allowed emitted cross edges, BOTH extensions and closures.
Pack cycles as before, now requiring U to contain h(Q). This ensures the
actual mandatory pairs occur, not merely some pairs of their colors.
Every leftover baseline edge is allowed, proving soundness. A small valid
witness survives reservations under an injective coloring on its changed
pair set, proving completeness despite representative compression.

The degree-zero case k=q=0 is complete and immediately solvable. There is
no parity-only baseline shortcut when Q is nonempty. A singleton pair with
a forbidden baseline edge is correctly NO: no cycle of two pairs exists.

The complement is now a GENERAL graph. Unlike the bipartite extension,
minimum vertex cover is not known to be polynomial-time computable. Either
accept a supplied verified cover; find one by the standard bounded-search
vertex-cover algorithm; or take endpoints of a maximal complement matching,
a polynomial-time vertex cover of size at most twice optimum q. The last
option proves FPT parameterized by optimum q without an exact cover oracle,
using support bound at most 4(k+2q)+1. Never transfer the bipartite exact
cover-computation claim to this setting.

## Required controls and evidence scope

- Validate undirected labels and a supplied complement cover.
- Pair IDs, not individual vertices, are the color-coded objects.
- Keep fixed start entry port and last entry port in path states.
- Permit two-pair cycles; exclude one-pair closures.
- Add the current pair's baseline label on every emitted edge, including closure.
- Restrict both emitted-edge types to allowed edges in the extension.
- Reserve mandatory colors for their actual pairs and require their coverage.
- Accept arbitrary used masks; do not require all t colors.
- Validate the reconstructed matching, legality, and target directly.

The independently written check.py exhausts all 3^6 assignments on four
vertices with each edge forbidden, allowed label 0, or allowed label 1;
compares every target with exhaustive matching enumeration; directly checks
quadratic matching indicators and the complete legality/parity product on
permutations; runs seeded randomized instances; and checks port incidence
on every ordered/ported pair cycle through five pairs. check.log contains
the final outcome. These finite tests corroborate rather than prove the
all-input argument. This audit does not review a root implementation.

## Frozen implementation review and completed checks

After completing the independent model, I reviewed the frozen root files:

- GENERAL_MATCHING.md SHA256 cd28495cd9e6095f6474d18946295a9c53da3965cf0f7e92a5f2854fa85eaaab
- general_solver.py SHA256 620ff7610c7fb16004ed849990af624eefb69e60df8abb470a88f83e959d6413

Their directory is ... I also inspected
its imported packing routine. No substantive proof or implementation gap
was found. The code retains precisely the required port information,
reserves mandatory colors, checks closure legality, correctly emits edges
from the port path, and directly validates its reconstructed answer.
It explicitly requires a supplied complement cover and does not claim to
compute a minimum general-graph cover.

Final check.py/check.log: PASS, 983 instances, 2,354 target decisions compared
both with exhaustive perfect-matching enumeration and the frozen root solver,
52,432 direct polynomial evaluations, 884 cycle-incidence checks, and 2,494
independent per-color solver runs. All root witnesses were independently
validated. Four complete 12-vertex instances have n=6>t=5, including an
unattainable nonzero target on the all-zero labels, exercising a nontrivial
color family and exhaustive NO behavior. A separate deliberately colliding
coloring checks that a mandatory isolated pair cannot be replaced by another
pair of its reserved color. No root files were modified.
