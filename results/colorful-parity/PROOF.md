# Deterministic parameterized algorithm for complete bipartite parity matching

Research draft, 17 October 2026. Novelty has not been established. This is a
restricted matching algorithm, not a resolution of P versus NP.

## Input and dependency

Given an n by n complete bipartite label matrix with entries in GF(2)^k and a
target, decide whether a permutation has that label sum and construct one.
Input labels are explicit k-bit words. The sharp support-radius theorem proves
that if a solution exists, one differs from the identity on at most
t=min(n,2k+1) indices. This is the sole non-elementary dependency here.

The same color-coding argument also works with Derksen's established 3k
support bound, using t=min(n,3k). Therefore FPT itself must not be presented
as requiring the new sharp radius. The improvement changes the parameter
bound in this construction; historical novelty of the algorithm is unresolved.

If the identity has the requested sum, return it. Empty and singleton instances
are then settled directly. Otherwise k>=1, n>=2 and 2<=t<=n.

For each directed arc i to j define delta(i,j)=label(i,j)+label(i,i).
The target difference from the identity is D. A changed permutation is a
collection of vertex-disjoint directed cycles of length at least two. Its
delta sum is D, and its changed support is their vertex union.

## An explicit deterministic color family

Number vertices 0,...,n-1. Let L=ceil(log2 n) and r=min(L,t-1). For every
r-subset of bit positions, project vertex IDs onto those bits, giving codes
in [2^r]. For each t-subset S of this code range, assign its sorted members
distinct colors 0,...,t-1; send every other code to color zero.

Every t-set of distinct IDs is distinguished by at most t-1 bit positions:
start with the indiscrete partition and repeatedly choose a bit separating
two IDs still in one part. Each step increases the number of parts, so at
most t-1 steps suffice. Pad with unused positions to r. Its t distinct codes
form one of the enumerated sets S. Also 2^r>=t: if r=L use 2^L>=n>=t;
otherwise use 2^(t-1)>=t. Thus the family is well defined and contains a
coloring injective on every t-set. Any smaller support can be padded to a
t-set because n>=t.

The family size H is at most L^(t-1) 2^(t(t-1)). Put a=t-1. For n>=2,
L<=2 log2 n, and (ln n)^a<=a! n follows from the exponential power series.
Hence H<=(2/ln 2)^a a! 2^(t(t-1)) n. This elementary construction has very
large parameter constants but is sufficient for fixed-parameter tractability.

## Exact dynamic programs for one coloring

For every start vertex, enumerate colorful directed paths by dynamic programming
on (used color set, endpoint, delta sum), retaining one concrete path for each
state. Extension uses only a new color, so paths have distinct vertices. Closing
a path containing at least two vertices back to its start produces a colorful directed
cycle. Retain one cycle for each (color set, delta sum).

Path-state compression is safe: future extensions only inspect the endpoint,
used colors and accumulated sum. A vertex with a new color cannot occur in
either representative path. Cycle-state compression is safe for the next step
because compatibility is decided by disjoint colors, which implies disjoint
vertices irrespective of the particular cycle representative.

A second dynamic program starts with the empty collection and adds stored
cycles whose color sets are disjoint from the colors already used. Its states
are (union of used colors, total delta). It accepts D for ANY used-color set,
not only all t colors. Recording predecessor witnesses constructs the actual
permutation. Every returned object is checked directly against the original
matrix and target in solver.py.

Soundness follows from vertex-disjoint directed cycles and the delta identity.
For completeness, take a small-support witness from the support theorem and
choose a coloring injective on its support. Its cycles appear in the first
dynamic program with their color sets and sums. The second program combines
these disjoint sets, even if some cycles were replaced by other representatives.
It therefore reaches D. Exhausting every coloring without success certifies NO.

## Explicit complexity and limits

For each coloring, path dynamic programs have at most n^2 2^(t+k) states
over all starts and at most n extensions per state. Copying a witness costs
O(t). The current simple cycle-packing implementation considers at most
4^(t+k) state/cycle pairs, with witness-copy costs polynomial in t. A safe
arithmetic-operation bound is H times O(t n^3 2^(t+k)+t^2 4^(t+k)+nt).
Bit-operation costs add polynomial factors in k and log n; these remain FPT.
Since t<=2k+1 and H<=f(t)n, the total is f(k) times a polynomial in n and the
explicit input size with parameter-independent exponent. Memory is also
f(k) polynomial in n. This is a deterministic FPT statement, stronger than
the earlier support enumeration's XP bound, without a claim of useful constants.

No conclusion for arbitrary missing-edge graphs follows: such a graph need
not have a target matching near identity. The support theorem, exact DP,
and color family are separate obligations. Finite tests corroborate the
implementation and do not prove all-input correctness by themselves.
