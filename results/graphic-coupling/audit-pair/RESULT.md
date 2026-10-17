# Independent audit: pair-sum graphic localization

2026-10-17. Verdict: criterion and target transport are correct. The restricted polynomial algorithm follows from classical constructive graphic-matroid recognition plus the already-described local forbidden-pair matching solver. General recognition has not been implemented in the peer's current GL(3,2) validation code. Earlier audits are unchanged.

## Exact criterion

Let A be a binary matrix with labeled nonzero columns a_e, and let P be a collection of distinct-index pairs. Form A+ by adjoining one separately labeled column a_e+a_f for every pair whose two columns are unequal. Equal nonzero columns are parallel and need no extension.

Then A has a graph representation in which every pair in P consists of incident edges if and only if A+ represents a graphic matroid. Graphs must allow parallel edges. Pair disjointness is not needed for this recognition equivalence; it is needed for the stated downstream local matching class.

### Why binary matroid data are enough

If two binary matrices have the same labeled column matroid, their kernels coincide. Every nonzero kernel vector has a dependent support containing a circuit. The indicator of that circuit also lies in the kernel. XOR removes that circuit from the support; induction expresses every kernel vector as a sum of circuit indicators. Hence the kernel is determined by the labeled circuits.

Consequently, a graph incidence representation B of A has the same kernel, and the map sending Az to Bz is a well-defined linear isomorphism between their column spans. This argument accommodates redundant rows and disconnected graphs. The labels or a returned edge-label permutation must be retained. An abstract isomorphism with an unrecorded permutation is insufficient for target transport.

### Forward direction

Given a graph representation making a pair incident, two unequal nonzero columns are nonparallel edges sharing exactly one endpoint. Their incidence-column sum is the edge joining their other endpoints. Add that closing edge. The column-span isomorphism above maps the added a_e+a_f to precisely this closing-edge incidence column. Doing this simultaneously for all pairs gives a graph representation of A+, including any necessary parallel added edges.

### Reverse direction

For unequal nonzero columns, the three labeled columns a_e,a_f,a_e+a_f form a 3-element circuit: none is zero and no two are equal. In every graph realization this circuit is a triangle, so e and f are incident. Equal nonzero columns form a 2-element circuit, hence are parallel edges and already incident. Delete the added edges from the realizing graph; all original pair incidences remain.

There is no assumption that the originally supplied A already looks like an incidence matrix.

## Target transport and solving

1. Use the original A to solve Az=b by Gaussian elimination. If inconsistent, reject the SAT instance. The vector z need not satisfy any NAND constraints.
2. Recognize A+ and obtain a labeled realizing graph. If nongraphic, the instance is outside this recognized class; this does not mean the SAT instance is unsatisfiable.
3. Delete all recognition-only added edges and let B be the incidence matrix on the original columns only.
4. Put t=Bz. Because ker(A)=ker(B), t does not depend on the chosen solution z. For every original variable vector x,

   Ax=b iff A(x+z)=0 iff B(x+z)=0 iff Bx=t.

5. Host each forbidden pair at a common endpoint and apply the local parity-plus-forbidden-pairs matching solver. For disjoint original pairs, the hosted groups are disjoint at every vertex. Extract and verify x against the original A and NAND constraints.

The pair-sum columns are recognition gadgets only. They must not be made new selectable SAT variables; doing that changes the feasible target fibers.

## Zero columns, loops, parallels and empty cases

For the pure NAND-plus-linear-system input, each zero-column variable may be set to zero without losing a solution: it contributes nothing to Ax, and reducing a variable from one to zero preserves every NAND. Delete these variables and discard any forbidden pair involving one; its surviving mate becomes unrestricted. This avoids loop conventions in the matching backend. An all-zero A reduces to testing b=0 and has the all-zero witness.

Nonzero parallel columns should remain separate labeled edges, even though their matrix values are equal. Their forbidden pair is local at either common endpoint. The graph may have multiple components; since t=Bz, each component automatically has even total target parity. Isolated vertices can be discarded.

## Classical recognition dependency

P. D. Seymour, *Recognizing graphic matroids*, Combinatorica 1 (1981), 75–78, DOI 10.1007/BF02579179, gives polynomial graphicness recognition even from an independence oracle. The original author/institution record confirms the theorem: https://collaborate.princeton.edu/en/publications/recognizing-graphic-matroids/ . Matrix rank supplies such an oracle in polynomial time.

The constructive form needed here is stated explicitly as Proposition 7.8 in the Charles University matroid lecture notes: https://iuuk.mff.cuni.cz/~pangrac/vyuka/matroids/matroid-ch7.pdf . It outputs a graph in polynomial time when the binary input is graphic. These are classical algorithmic results, not new recognition claims.

The original W. T. Tutte paper, *An algorithm for determining whether a given binary matroid is graphic*, Proc. Amer. Math. Soc. 11 (1960), 905–917, was located at the official AMS URL below, but the tool could not retrieve its full PDF (403). This audit therefore does not claim to have checked its original implementation details:
https://www.ams.org/journals/proc/1960-011-06/S0002-9939-1960-0117173-5/S0002-9939-1960-0117173-5.pdf

## Small controls and obstruction

With one vertex row deleted, K4 has the six distinct columns 001,010,011,100,101,110. The opposite-edge pair 011,100 has sum 111. Its extension contains all seven nonzero rank-three vectors. Any graph representing this simple rank-three matroid would be a simple graph of total rank three; the maximum number of edges is six, attained by K4. Therefore the extension is nongraphic. This confirms that being graphic before pair extension is insufficient.

Conversely a displayed cycle can have opposite paired edges yet admit another graphic representation making them incident. The peer's C4 control exhibits this; localization is existential over representations, not limited to the current picture.

Independent check.py passes:
- 1,074 rank-two localization-versus-extension cases, including repeated/parallel columns;
- 500 random zero-column preprocessing comparisons of complete achievable syndrome sets;
- 4,096 fiber comparisons under a rectangular, redundant-row representation change.

Peer controls exhaustively compare 1,562 rank-three cases using all 168 GL(3,2) transformations. This finite exhaustive search is a test oracle, not a polynomial-time general graphic recognizer. The general algorithmic conclusion invokes the cited classical recognition theorem.

No general P-versus-NP consequence or historical novelty is claimed. No external publication or third-party communication occurred.
