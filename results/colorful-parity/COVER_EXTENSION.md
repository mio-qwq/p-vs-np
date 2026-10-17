# Forbidden-edge-cover extension

Status: research proof and executable prototype; historical novelty unverified.

Let G be an allowed-edge bipartite graph on two labeled n-vertex sides, with
k-bit labels on each allowed edge and a target. Suppose C is a supplied vertex
cover of the forbidden-edge bipartite graph, of size q. Mixed row and column
vertices are allowed in C. The cover is checked directly by cover_solver.py.

For a covered row i let A_i(X) be the sum of its allowed entries X_ij. For a
covered column j use the analogous column sum. On every permutation matrix,
each such linear expression is exactly zero or one in GF(2): there is only
one selected entry in that row or column. The product over C is one precisely
when every selected edge is allowed, since every forbidden edge has a covered
endpoint. Multiply by the k linear parity-target indicators. The resulting
degree-at-most-(k+q) polynomial detects precisely the valid target matchings.

Consequently, if any valid target matching exists, at least one valid target
matching differs from the identity on at most t=min(n,2(k+q)+1) vertices. This
does not assert that every valid matching is close to identity. Assign arbitrary
k-bit labels to forbidden entries, for example zero; these labels cannot affect
the value on a valid matching.

Let M be the indices whose diagonal entries are forbidden. Each must move in
any valid permutation. Also |M|<=q, because different forbidden diagonal edges
have disjoint endpoints and each requires a distinct cover vertex.

Use the explicit t-perfect color family from PROOF.md. For each coloring:

1. Skip it if two vertices of M have the same color.
2. Reserve each color of M for its exact vertex: remove every other vertex
   with that color from the cycle search.
3. In the colorful-cycle DP allow only allowed directed arcs, including the
   arc closing a cycle. Arc deltas still use the identity's formal label sum.
4. In the cycle-packing DP require that the used-color set contains all colors
   reserved for M, in addition to the desired parity delta. Other colors may
   remain unused.

For soundness, reservation and the used-color condition force every vertex of
M to occur in a selected cycle. Every selected arc is allowed. Every vertex
outside the cycles is fixed and lies outside M, so its diagonal is allowed.
The usual delta identity gives the target parity. Final output is checked
against the original allowed matrix and labels.

For completeness, choose a small-support valid witness from the polynomial
theorem, and a coloring injective on that support. All vertices of M are in
the support, so their colors are distinct; reservation deletes none of its
vertices. Every cycle uses allowed arcs, and the packing DP can combine their
color sets and deltas. Representative replacement remains safe by disjoint
colors. Thus exhausting the family gives an exact NO, not an inconclusive result.

The previous complexity proof applies with t<=2(k+q)+1, establishing a
deterministic FPT algorithm parameterized by k+q. No bound polynomial in n
uniformly for unbounded k,q is claimed. A cover need not be minimum for correctness;
its actual size controls the bound. No complement-cover optimization is
implemented or needed by this prototype.

Edge cases are explicit: the identity is accepted only if every diagonal is
allowed and its parity matches; an illegal singleton has no matching even at
zero target and k=0. A cover missing any forbidden edge is rejected.

This remains an algorithm for a parameterized matching problem, not a general
P versus NP result. The older Derksen support bound also suffices for FPT;
the sharp radius improves the support parameter used here.
