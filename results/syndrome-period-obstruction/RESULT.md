# Positive-route stress test: exact affine-slack compression and its clause-copy barrier

2026-10-17. Research prototype, not a polynomial-time general SAT algorithm. No historical novelty is asserted for syndrome trellises, translation stabilizers, bounded-width dynamic programming, or small-core search. The useful result is a precise tested refinement and a proof of where it gives no compression.

## 1. Input and exact interface algorithm

Input consists of ordered disjoint variable blocks B_1,...,B_k, a local CNF F_i on each block, and global equations Ax=b over GF(2). Columns are explicit r-bit vectors; all row dimensions and variable names are charged to input bit length L. Let t=max |B_i|. Build the feasible block syndrome set S_i={A_i x_i:F_i(x_i)=1} by explicitly enumerating at most 2^t assignments per block. This is not a polynomial step when t is unrestricted.

The uncompressed dynamic program stores exact reachable prefix syndromes s, discarding s unless b+s belongs to the linear span V_i of suffix columns. Prefix syndromes lie in U_i, the span of prefix columns. Therefore surviving states belong to U_i intersect (b+V_i). If nonempty, this is a translate of U_i intersect V_i, with at most 2^w states where w=max_i dim(U_i intersect V_i). This bound is proved, never assumed polynomial. Updating by all feasible local syndromes takes O(k 2^(w+t) poly(L)) time. Gaussian membership tests and rank computations require only explicit vector bases, not enumerated linear spans.

Equal exact syndromes have the same possible suffix completions because the remaining equations depend on the prefix only through that syndrome. Induction over blocks proves correctness. The implementation also returns one witness. A tempting alternative, quotienting prefix syndromes by the whole suffix span, is unsound: at a cut with one equation a=b, both a=0 and a=1 lie in one suffix-span coset, yet a suffix unit b=0 extends only a=0. The supplied test exhibits prefix counts [1,2,1].

More generally, with n equality coordinates, every two distinct syndromes can be separated by a suffix fixing the n copies to one of those syndromes. Thus no context-independent merge of distinct exact syndromes is correct for all local CNF suffixes. This does not forbid context-specific semantic compression or other representations.

## 2. Safe stronger quotient: absorb all local translation periods

For each nonempty S_i choose s_i^0 in S_i, set T_i=S_i+s_i^0, and replace the target by b'=b+sum_i s_i^0. Now every T_i contains zero. Define

    H_i={h:T_i+h=T_i},    H=H_1+...+H_k.

H_i is a vector subspace: zero is a period, and composing translations adds periods. Because 0 belongs to T_i, all candidate periods lie in T_i. Test each candidate h by checking t+h belongs to T_i for every t in T_i. This costs O(|T_i|^2 poly(L)), using explicit sets, not a semantic oracle. Gaussian elimination gives H.

Let pi be the quotient map by H, implemented by canonical linear remainder under a fixed echelon basis. Then

    b' belongs to T_1+...+T_k  iff  pi(b') belongs to pi(T_1)+...+pi(T_k).

Forward implication is linearity. Conversely, a quotient solution has representatives t_i whose error b'+sum_i t_i lies in H. Express that error as sum_i h_i with h_i in H_i; replacing t_i by t_i+h_i keeps every local choice feasible and corrects the error. Thus this quotient is sound even if none of the original local CNF relations is affine. The implementation returns the decision only; it does not implement witness reconstruction for this quotient.

Run the exact interface DP on quotient sets pi(T_i), using their linear spans for prefix/suffix membership pruning. Let w' be the largest intersection dimension of those spans. Total time is

    O((k 2^t + sum_i |S_i|^2 + k 2^(w'+t)) poly(L)).

In particular t=O(log L) and w'=O(log L) define a checkable, presentation-dependent polynomial-time subclass. If every S_i is affine, H_i is its direction space and every quotient set is {0}; the remaining decision is Gaussian target membership, regardless of original cut rank. These are structural facts, not a claim of a newly discovered complexity class.

## 3. Why arbitrary clause copies do not acquire affine slack

A universal SAT encoding puts a private copy of every literal occurrence into its clause's block and ties copies of each original variable together by equality-star equations. It has polynomial encoding size and local block size three for 3-CNF. For d occurrences of one variable, the star's columns are e_1,...,e_(d-1) and their sum. They form one circuit: any proper subset is independent, and the full set has rank d-1 (for d=1 the sole column is zero). Different original variables occupy disjoint equation-row components.

At a block cut, an original variable appearing on both sides contributes exactly one to dim(U intersect V): ranks of the two proper column subsets sum to d, while their union has rank d-1. A variable wholly on one side contributes zero. Direct sums across original variables show that cut rank equals exactly the number of original variables straddling the clause cut, for every ordering. Introducing equality copies therefore does not lower the original variable-frontier parameter.

The stronger stabilizer quotient has an exact rank dichotomy. A strict width-q clause permits all assignments of GF(2)^q except one a. Let its linear syndrome map be A_i.

* If rank(A_i)=q, the image is im(A_i) minus the single point A_i a. Any period must lie in im(A_i); a nonzero translation moves the uniquely missing point and cannot preserve the set. Thus H_i={0}.
* If rank(A_i)<q, every nonempty fiber has at least two assignments. Removing one assignment leaves every image point represented, so S_i=im(A_i), an affine space, and H_i=im(A_i).

For strict 3-CNF in which every original variable occurs at least twice, the three columns of every clause belong to independent original-variable row components and are all nonzero. Hence rank(A_i)=3, |S_i|=7, and H_i={0} for every clause. An alternative short argument: a nonzero translation has only two-point orbits, so it cannot preserve an odd-sized set. Translating a seven-point subset of a three-dimensional space to contain zero leaves full span. Consequently H=0, and even the strengthened DP has exactly the original clause-frontier width. This is a decisive obstruction to obtaining a general polynomial bound by this encoding and quotient alone.

In this strict occurrence-copy encoding, rank deficiency occurs exactly when a clause has an original variable with only one occurrence: its column is zero. That is ordinary private-variable slack and can be handled by eliminating the clause using that variable's satisfying value. This does not subsume general pure-literal elimination when a pure variable has multiple occurrences. For general XOR matrices, a non-coordinate kernel direction can also produce rank deficiency; the precise general statement is linear slack, not necessarily a free original coordinate.

## 4. Explicit remaining exponential behavior

Raw exact DP on two consecutive copies of blocks {0,e_i}, i=1,...,k, reaches all 2^k syndromes at the middle. The stabilizer quotient absorbs their entire span and has one state. This demonstrates that the repair changes behavior rather than merely renaming the same DP.

However, take two consecutive copies of k blocks T_i={0,e_(2i),e_(2i+1)}, with target zero. Each T_i has odd cardinality three, so every period space is zero. At the middle, all 3^k combinations are distinct and extendible by selecting the same elements from the second half. Therefore the repaired DP enumerates exactly 3^k middle states, with w'=2k. Each block is represented by just two variables and local clause (not a or not b), with the two independent unit-vector equation columns. Input size is polynomial in k, whether using dense or sparse equation encodings. This is an exact candidate-specific superpolynomial family.

The family is satisfiable and easy: component decomposition or interleaving corresponding blocks removes the difficulty. No lower bound for optimal ordering, semantic state merging, arbitrary SAT algorithms, or P versus NP follows. The all-repeated strict-3CNF rank theorem above is the broader encoding obstruction; it too does not prove every formula has large frontier in every useful representation.

## 5. Cross-direction control of the new anchor family

The independently developed fixed-priority family contains, on every five anchors, both the all-positive and all-negative clause for each triple. Those twenty clauses are UNSAT: among five Boolean values, at least three share one value, falsifying one of their two triple clauses. A generic preprocessor that enumerates all five-variable subsets and truth-tables clauses supported entirely inside each subset finds this contradiction in O(n^5 * 32 * L) time. It does not need to identify anchor names or the family.

The companion control checks all 32 assignments of the five-anchor core. This explains precisely why that exponential frozen-branching trap cannot establish hardness against unrestricted polynomial preprocessing. We did not add another patch to the frozen solver or claim that fixed-size core detection solves general SAT.

## 6. Reproduction and stopping condition

Commands:

    python test_syndrome_dp.py
    python test_stabilizer_dp.py
    python test_clause_dichotomy.py
    python check_anchor_control.py

Executed successfully: 1,800 random local-CNF/XOR comparisons with exhaustive assignment search; 500 random clause-copy equivalence/frontier checks; 3,500 random syndrome-set quotient comparisons with explicit sumsets; all 4,096 combinations of 3x3 binary map and deleted point for the clause rank dichotomy; raw and repaired exponential-family controls; and the five-anchor core truth table. Finite tests support the code, while the general claims above require the stated proofs.

The frozen baseline was inspected and not edited. This new prototype does not import or modify it. No bounded-degree polynomial-calculus solver was implemented: its known applicability to the split-Tseitin test would not resolve the universal state bound, and the anchor control already has the elementary fixed-size certificate above.

Stop this positive route at its demonstrated obstruction: unrestricted block enumeration is exponential; clause-copy blocks keep local size three but have no nonzero translation periods on repeated-variable strict 3-CNF; exact interface DP can still be exponential. A worthwhile continuation would need a new representation or a stronger, efficiently recognizable nonlinear relation compression with a provable uniform bound. Neither is supplied here. No P=NP result or genuinely new general tractable-class claim is made.
