# Independent audit: colorful parity-target permutations

17 October 2026. Verdict: **valid deterministic FPT algorithm**, conditional only on the supplied bounded-support theorem (whose proof is already separately frozen). The cycle/color DP is sound even without that theorem; the theorem supplies completeness for the full complete-bipartite problem. This is a mathematical audit and executable finite testing, not formal verification. Novelty is unestablished.

## Precise problem and reduction

Input: an n by n matrix A of elements of GF(2)^k and target b. Find a permutation p with XOR_i A[i,p(i)]=b. Let b0=XOR_i A[i,i], d=b XOR b0, and D[i,j]=A[i,j] XOR A[i,i]. The XOR of D[i,p(i)] is exactly d if and only if the target is met. Fixed points contribute zero. Every permutation's nontrivial cycles are vertex-disjoint directed cycles of length at least two, and conversely any such cycle collection extends by the identity to a permutation. Completeness of the bipartite graph ensures every arc and every untouched diagonal is legal.

Use t=min(n,2k+1); handle n<=1 directly, and k=0 by returning identity. The supplied theorem guarantees a successful permutation whose moved support has size at most t whenever any successful permutation exists.

## Single-coloring DP

For h:[n]->[t], keep P[S,s,v,z] recording existence of a directed path from s to v, using each color in S exactly once, with arc-XOR z. Initialize P[{h(s)},s,s,0]. Extend to w only if h(w) is not in S, and update z by XOR D[v,w]. This ensures vertices cannot repeat. Process states in increasing |S|. A predecessor pointer records a witness. The only nontrivial closure is for |S|>=2: add v->s and record C[S,z XOR D[v,s]]. Keep one cycle witness for each C state.

Induction on |S| proves that P records precisely all colorful paths, and therefore C precisely all colorful cycles. Crucially, no loop is recorded as a nontrivial cycle.

Initialize Q[empty,0]. For disjoint S,T, if Q[S,z] and C[T,w], set Q[S union T,z XOR w]. Process in increasing used subset size and keep predecessors. Induction shows Q records exactly the possible colorful cycle collections.

The apparently dangerous compression to one cycle per (T,w) is safe: two objects whose color subsets are disjoint cannot share any vertex. Thus any chosen witness for a C state is compatible with every Q witness with disjoint color subset. No actual vertex-support information needs to survive in Q.

Accept Q[S,d] for **any** S, including the empty subset. Requiring S=[t] would be wrong, because the support bound is an upper bound. A d=0 instance already has identity as its answer. Reconstruct cycles and fix all other vertices. This gives a directly verifiable witness.

## Completeness across colorings

A t-perfect family means that every t-element vertex subset is injectively colored by some h. A support of size <=t is covered by extending it to a t-element subset (t<=n). Under that coloring the successful small-support permutation's cycles are all colorful and their color sets are pairwise disjoint, so the DP accepts. If every coloring rejects, no small-support solution exists, and the bounded-support theorem implies no solution exists at all.

## Runtime and storage

Write G=2^k. There are at most 2^t n^2 G path states, with n possible extensions each, costing O(2^t G n^3). Closure is O(2^t G n^2). Combining color-disjoint subsets costs O(3^t G^2): each color is in the previous collection, the next cycle, or neither, and label-pairs contribute G^2. Thus a safe per-coloring time is O(2^t G n^3+3^t G^2), plus polynomial preprocessing. With all starts retained, O(2^t G n^2) predecessor records suffice, plus cycles and Q. If starts are processed sequentially and actual cycle lists of length <=t are saved, space improves to O(2^t G(n+t)+n^2), in word units. The finite checker uses this simpler sequential-start variant and full short path tuples; it is for verification rather than optimized memory.

Factor in O(k+log n) bit-operation overhead for labels, indices and pointers if needed. This does not change FPT status. Hash colorings should be generated/processed sequentially; storing the full family is unnecessary.

## Self-contained hash-family construction supplied by root, independently checked

For 2<=t<=n let L=ceil(log2 n), r=min(L,t-1), q=2^r. Identify vertices with distinct L-bit integers 0,...,n-1. Enumerate all r-subsets B of bit positions and all t-subsets U of [q]. Project each vertex onto the bits in B. Codes in U receive their distinct sorted ranks 0,...,t-1; all other codes receive color 0.

Why it works: starting with no positions, if two of the desired t IDs still agree in all selected positions, choose any position where they differ. This increases the number of nonempty equivalence classes by at least one. At most t-1 choices distinguish all IDs. At most L positions can be selected. Pad to exactly r. Their t projected codes are a U included in the enumeration. The extra codes colored 0 cause no problem for injectivity on the selected t IDs.

q>=t: if r=L, then q>=n>=t; otherwise q=2^(t-1)>=t. Consequently the t-subset enumeration always exists.

Family size H is at most L^(t-1) 2^(t(t-1)). Put a=t-1. For n>=2, L<=2 ln(n)/ln(2). Since exp(x)>=x^a/a!,

H <= (2/ln 2)^a a! 2^(ta) n.

Thus H<=F(t)n for an explicit computable F. Construction by simple enumeration and evaluation is itself FPT. Together with the DP this gives a self-contained deterministic bound O(F(t)n[2^t 2^k n^3+3^t 4^k]) up to polynomial bit overhead. Since t<=2k+1, this is f(k)poly(n), with an n exponent independent of k. It is important not to mistake (log n)^(t-1) for n^(t-1); the displayed factorial inequality is the step establishing uniform FPT.

Use integer L=(n-1).bit_length() in code, avoiding floating-point ceilings.

## Standard efficient derandomization and primary source

N. Alon, R. Yuster, U. Zwick, “Color-Coding,” Journal of the ACM 42(4), 844–856 (1995), Section 4, pp. 850–851, explicitly constructs perfect hash families. The section first describes a 2^{O(t)}log^2 n family with constant-time evaluations and then reduces the family size to 2^{O(t)}log n through composition via t^2 colors. The small sample spaces used in the construction have explicit FPT construction time. Hence standard color-coding can improve the self-contained bound to 2^{O(k)}poly(n); it is not merely a nonuniform existence argument.

Primary paper copy: https://csaws.cs.technion.ac.il/~hadas/Seminar/Winter1011_236801/Papers/Color_coding.pdf
Publication DOI: https://doi.org/10.1145/210332.210337

Only a standard, modest summary is intended here: the independently supplied elementary family already removes any algorithmic dependence on a black-box hashing theorem.

## Prior-art search: cautious conclusions

The group-weighted formulation is longstanding. Relevant primary sources located:

* R. Aharoni, R. Meshulam, B. Wajnryb, “Group Weighted Matchings in Bipartite Graphs,” J. Algebraic Combinatorics 4 (1995), 165–171. It studies finite-abelian-group edge labels, prescribed identity-product matchings, and complete-bipartite structural/counting statements. https://www.kurims.kyoto-u.ac.jp/EMIS/journals/JACO/Volume4_2/hn7w011496416q14.fulltext.pdf
* J. Kahn, R. Meshulam, “On the Number of Group-Weighted Matchings,” J. Algebraic Combinatorics 7 (1998), 285–290. Abstract gives lower bounds on the number of identity-weight matchings from degree and group size. https://doi.org/10.1023/A:1008671206536 . Author bibliography confirms publication: https://meshulam.net.technion.ac.il/e-prints/
* N. El Maalouly et al., “Exact Matching: Correct Parity and FPT Parameterized by Independence Number,” ISAAC 2023. This concerns scalar red-edge parity/exact count and structural graph parameters, not directly the k independent label bits here. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ISAAC.2023.28

A targeted search did not identify a prior theorem stated as this exact complete-bipartite k-bit FPT result. This is not evidence of novelty: the old group-weighted literature and the very standard bounded-support/color-coding combination make novelty claims inappropriate without substantially deeper review. Color-coding itself is explicitly classical; no claim that the DP technique is new is justified.

## Boundaries and failure modes

* The bounded-support theorem is the only bridge from small-support search to unrestricted solution existence. For missing-edge graphs that bridge is unavailable.
* A DP may correctly find nearby solutions in a noncomplete graph with a baseline matching, but that does not establish full decision completeness there.
* The parameter is k (number of bits), not the target vector's numeric magnitude. Running time exponential in k is permitted for FPT and is not a uniform polynomial-time result.
* Empty input, single vertex, zero-bit labels, baseline already meeting target, and unused colors require the explicit handling above.
* The algorithm returns one witness; it does not count all solutions, since state compression intentionally loses multiplicities.

## Finite checker

`check.py` independently implements per-coloring path/cycle/packing DP, compares its entire attainable parity set against exhaustive permutation enumeration, and verifies every reconstructed witness. `check.log` records 19,955 passing cases: exhaustive label matrices/colorings for n<=3 under the listed bit widths and seeded randomized n=4,...,7 cases. These tests support implementation correctness; proofs above, rather than tests, establish the general claim.

## Inspection of root implementation

The separate root prototype `solver.py` was read after the independent proof and checker were complete. No correctness defect was found. Its layered path frontier correctly retains the start externally; missing colors do not matter because it loops only up to the number of occupied colors. Integer-mask ordering is topological since each transition adds new bits. Its packing implementation scans all cycle states rather than only disjoint-subset candidates, so a safe bound for that implementation is O(4^t 4^k), not the optimized O(3^t 4^k) above. Full tuple copying adds factors bounded by t. All these costs remain FPT.

`check_root.py` independently compares root's per-coloring subroutines with the exhaustive-permutation oracle on 300 random matrices/colorings (n=2,...,7, k<=4), testing all targets and verifying reconstructed witnesses. See `check_root.log`.

A further novelty limitation: the established sufficient radius 3k from Derksen, already cited in the frozen theorem, suffices for the same FPT reduction. The sharp 2k+1 bound improves the parameter constants but is not needed for FPT itself. Therefore even a new sharp-radius theorem would not by itself establish novelty of the FPT conclusion.
