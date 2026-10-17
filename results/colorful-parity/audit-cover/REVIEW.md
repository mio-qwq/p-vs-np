# Independent audit: parity matching with a small forbidden-edge vertex cover

Date: 17 October 2026. Verdict: mathematical PASS, conditional on the stated
permutation-polynomial support theorem. No novelty or general P-versus-NP claim.
This audit uses only local files and a separately written standard-library model.

## Precise statement

Let G be an allowed-edge bipartite graph with indexed parts R=[n], S=[n],
k-bit edge labels, and target b. Let C be a verified vertex cover of its bipartite
complement, with |C|=q. There is a deterministic f(k+q) poly(input-size) algorithm
that finds a target perfect matching or decides none exists.

The needed support statement is existential: if a valid matching exists, SOME
valid matching moves at most min(n,2(k+q)+1) indices relative to the identity.
It does not assert this bound for every valid matching. Complete graphs with
zero labels have arbitrarily large-support valid permutations even at k=q=0.

## Algebraic reduction, including mixed covers

Extend the labels to forbidden edges arbitrarily, e.g. by zero. For every
covered row r put A_r(X)=sum_{j:(r,j) in E(G)} X[r,j]. For every covered column
s put A_s(X)=sum_{i:(i,s) in E(G)} X[i,s]. Both are linear over GF(2).

On a permutation matrix P each such sum is exactly 0 or 1: the relevant row
or column contains exactly one selected edge. It equals 1 exactly when that
edge is allowed. There is no parity cancellation among several selected edges
because only one can occur. A product over covered rows AND covered columns
is valid. Repeated checking of an edge selected at two covered endpoints
leaves its Boolean indicator unchanged. Any forbidden selected edge has a
covered endpoint, making at least one factor zero. Conversely every factor
is one on an allowed matching. Thus product_{v in C} A_v(P) is exactly the
allowed-matching indicator on all permutation matrices.

For each bit j let L_j(X) be the extended label sum. The polynomial

    F(X) = product_{v in C} A_v(X) product_{j=1}^k (1 + L_j(X) + b_j)

has degree at most d=k+q and evaluates to one exactly on valid target matchings.
The permutation-polynomial support theorem therefore yields a nonzero F-value
within support t=min(n,2d+1). The identity need not be allowed or satisfy the
target. The theorem acts on all permutations, while the polynomial enforces
the graph restriction; one does not restrict the row-swap proof to G.

For d=0 the polynomial is constant and radius zero suffices. Using t=min(n,1)
is harmless. Empty graphs/instances n=0 and singleton n=1 should be handled
explicitly or by an empty-cycle state; a forbidden singleton diagonal is NO.

The local sharp-radius proof is field-uniform and uses no division by two.
Using the previously established radius 3d instead also yields the same
qualitative FPT result for d>=1. Consequently this extension's FPT conclusion
does not depend on novelty of the sharp constant.

## Mandatory moved indices

Let M={i:(i,i) is forbidden}. These forbidden diagonal edges are pairwise
vertex-disjoint. Every one needs a distinct endpoint in the vertex cover, so
|M|<=q. Every allowed permutation must move every member of M. Conversely,
once all vertices in M are moved along allowed cycles, every remaining
fixed point has an allowed diagonal. This equivalence is central.

## Color coding with reservations

Use any explicitly enumerable t-perfect family on [n]. The local complete-case
family projects vertex IDs onto at most t-1 bit positions and enumerates every
t-subset of the projected code range, assigning its members distinct colors.
For t>=2 its size is at most f(t)n by the elementary bound
(ln n)^(t-1) <= (t-1)! n; its listing and evaluation remain FPT.
For t=0 or 1 use the single constant coloring.

For each coloring h, reject it if h collides on M. Otherwise let B=h(M).
For every m in M, delete every vertex v != m with h(v)=h(m) from the cycle
search. Thus m is the sole remaining representative of its reserved color.

Search colorful directed paths on remaining vertices. Permit extensions i->j
only if i!=j and (i,j) is allowed. Use arc weight
Delta(i,j)=label(i,j)+label(i,i), with arbitrary extended diagonal labels.
For each fixed start s, retain one path for each (color mask, endpoint, sum).
Only close paths of length at least two and only when the closing arc is
allowed. Retain one cycle per (color mask, sum). Pack cycles with pairwise
disjoint masks using a second DP. Accept precisely states with sum
b + sum_i label(i,i) and mask containing B, with any other colors optional.
The empty collection is accepted only if its sum and mandatory-mask tests pass.

Path-state compression is safe because any next vertex has a new color and
therefore cannot already occur in either representative. Its availability and
closing edge depend only on the endpoint, fixed start, and graph. Cycle-state
compression is safe because compatibility uses disjoint color sets, implying
vertex disjointness. Reservation makes any representative carrying a mandatory
color contain the actual mandatory vertex. This remains true after arbitrary
state compression.

Soundness: the packed cycles define a permutation, use allowed moved edges,
and move every vertex of M. Its fixed diagonal edges are therefore allowed.
The arc-delta identity telescopes by row, so the result has exactly target b.

Completeness: choose a valid solution of support at most t, and a coloring
injective on that support (pad to a t-set if necessary). M lies in its support,
so h is injective on M. No vertex of that solution is deleted by reservation,
because no two support vertices share a color. The solution's cycles are
allowed and colorful. Each cycle's state survives possibly with a different
representative; those representatives have the same disjoint masks, sums,
and mandatory vertices. The packing DP therefore reaches an accepting state.

## Complexity and cover handling

The complete-case bounds apply unchanged, with t<=2(k+q)+1: at most
n^2 2^(t+k) path states across starts and polynomial transitions per state,
and at most 2^(t+k) cycle/packing states. Even a naive pairwise packing update
costs only f(k+q) per coloring times a polynomial in n. Multiplying by the
explicit family's f(t)n size gives deterministic FPT. Label bit costs and
explicit input reading add polynomial factors.

A supplied C must be checked against every forbidden edge. An invalid cover
cannot be silently accepted. A minimum cover can instead be obtained from a
maximum matching in the complement by the standard bipartite alternating-path
construction. This audit does not implement that polynomial matching routine;
the test model finds a minimum cover by enumeration only for tiny instances.
The parameter is the bipartite complement's vertex-cover size, not a vertex
cover of the original graph or a cover of an index-collapsed graph.

## Necessary implementation controls

1. No parity-only early return of identity if M is nonempty.
2. Check cover validity before applying q or the radius bound.
3. Check allowed closing arcs as well as path extensions.
4. Reserve mandatory colors for exact vertices, not merely require those colors.
5. Reject colliding mandatory colors.
6. Accept ANY used-color set containing all mandatory colors; requiring all t
   colors can introduce false negatives.
7. Retain fixed-start information during the path phase.
8. Give labels on forbidden edges a defined arbitrary extension, especially
   forbidden diagonal labels used in the delta baseline.
9. Directly validate returned bijection, allowed edges, and original label sum.
10. Distinguish an implementation of the new algorithm from the pre-existing
    complete-graph solver, which does not enforce these controls.

## Scope and evidence

The accompanying check.py is an independent executable model, not a production
implementation claim. It checks every graph through n=3, representative labels,
mixed/nonminimum covers, random n<=7 inputs, polynomial indicator values and
radius existence against exhaustive permutation enumeration. Mutation controls
show that deleting reservation, deleting mandatory coverage, or ignoring closing
edge legality each creates an invalid accepted witness. The exact counts and
execution outcome are in check.log. Finite tests corroborate the proof only.

Prior-art searches were not performed because this task was explicitly local.
The local audited documents identify Derksen's 3d support theorem; the prior-art
status of this specific complement-cover parameterization remains unresolved.

## Frozen root implementation review and completed results

After developing the independent model, I inspected the new root implementation
and its proof without modifying their bytes:

- COVER_EXTENSION.md SHA256: 437023bef75e6935d35438d20f01317afe7d8e37f24f632785c1bb694cdbc874
- cover_solver.py SHA256: 2fb9213eee0e03ff17e26be6db05cbdc690ff484621fc9880c8604132331dce6

Their root directory is ... The proof already
states the correct existential quantifier. The implementation preserves all
mandatory controls listed above. No substantive mathematical or code gap found.
The input interface deliberately requires a complete label matrix, including
arbitrary k-bit entries for forbidden edges; this is compatible with the proof.

Completed check.py results: PASS, 3,298 target cases checked independently against
all permutations and also against the frozen root solver, 581,801 direct
polynomial-indicator evaluations, 251 mixed-cover test inputs, and 3 successful
negative mutation controls. Every returned witness was independently validated.

The initial reservation-mutation example accidentally admitted a valid earlier
representative and therefore did not force a bad returned answer. Its only
failure was the intended mutation assertion, after the base comparisons passed.
The corrected control forbids (0,0) and (0,2), uses colors (0,0,1), and thereby
forces the unreserved search to substitute vertex 1 for mandatory vertex 0 in
the 1<->2 cycle. The corrected complete rerun passes. This is a test-fixture
correction, not a correction to the proposed algorithm or root implementation.
