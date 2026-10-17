# Affine residual sharing: a precise proof-model translation and its limits

Status: a local certificate construction, a concrete counterexample to a naive model identification, and a source-based simulation question. No proof-system separation, historical novelty, or P versus NP result is claimed. The frozen round-3 solver is unchanged.

## 1. What a cache node actually means

A normalized node stores a conjunction G(y) of affine clauses in its own free coordinates y. Its meaning, when marked UNSAT, is the universally quantified statement that no y satisfies G. Different incoming calls can identify these local coordinates with different surviving coordinates or affine expressions in their parent contexts. A shared node is therefore a reusable UNSAT lemma with a coordinate interface, not automatically a node querying one fixed affine form of the original input variables.

The map from child free coordinates to parent coordinates comes from Gaussian parametrization and dense renaming. Eliminated unused coordinates can be assigned arbitrary constants for witness extension; pure coordinates receive their satisfying constants. On a component edge the child uses a coordinate subset. These operations are explicit and polynomial. Across a path their composition is affine, but two paths reaching the same cached key need not induce the same composition.

## 2. A sound polynomially checkable residual certificate

Fix the exact round-3 normalizer N, initial dense relabeling/conversion/extraction P, component splitter C and branching rule B. The certificate proves UNSAT of the explicitly given original CNF F.

It contains a root reference and a list of normalized affine-clause keys G, each with its local dimension and one of these record types:

- **Branch:** the prescribed nonconstant affine query l, and references for both values b=0,1. The verifier recomputes N(G AND (l=b)). A result FALSE is represented by a terminal token; a nonterminal result must equal the referenced key exactly. TRUE is rejected in an UNSAT certificate.
- **Component:** if C(G) has more than one component, an index of one component and a reference to its normalized key, or a verified FALSE token. Only one UNSAT conjunct is needed to refute the whole conjunction.

The preprocessing P first densely relabels the distinct occurring input variable names, before constructing coefficient masks or the 3-CNF expansion, and then performs the specified initial parity extraction. Let D be the resulting expanded variable count, which is O(L) even for sparsely encoded large input labels.

Before calling normalization or component splitting on any supplied key, the verifier checks that its encoded dimension is an integer between zero and D and that all coefficient masks fit that dimension. It checks all referenced keys and their strictly descending dimension ranks before processing their normalization. These checks precede any dimension-indexed loop; a malicious binary-encoded huge dimension is rejected without allocating or iterating over that dimension.

The verifier then recomputes N(P(F)). FALSE accepts a terminal root; TRUE rejects; otherwise the root must match exactly. It checks key encodings, Boolean constants and coefficient-mask bounds, and verifies that each reachable nonterminal key is unchanged by normalization. Every referenced nonterminal has strictly smaller free dimension: a branch fixes a nonconstant affine form, and a proper component has fewer coordinates. Consequently cyclic certificates are rejected by this rank condition. Normalization itself includes all Gaussian, unit, syntactic and safe-purity checks; no supplied semantic-equivalence assertion is trusted.

### Soundness

Induct on the dimension rank. A FALSE token is justified only by replay of a sound normalization. At a branch node, every satisfying assignment would give one of the two values of l, and extend to a satisfying assignment of that normalized child, contradicting its certificate. At a component node, any satisfying assignment of G would restrict to a satisfying assignment of the selected component. The root preprocessing preserves satisfiability. Hence every accepted certificate refutes F.

### Completeness and size relative to an actual run

For an UNSAT execution of the frozen solver, keep its UNSAT nodes, both children of each branching node and one executed UNSAT component at each decomposition node. Omit irrelevant SAT component work. Each cache key is recorded once, regardless of how often it is instantiated in another coordinate context.

Let S be the number of distinct normalized nonterminal keys reached by that execution and L the input bit length. Initial expansion has O(L) variables and literals; each state has polynomial-in-L bit length, and each local normalization/splitting computation has polynomial bit cost. The extracted certificate has O((S+1) poly(L)) bits and is checkable in O((S+1) poly(L)) time. Every finite UNSAT formula has such a certificate because the exhaustive finite search terminates. The added 1 covers a terminal-root refutation with S=0. This is a concrete Cook–Reckhow-style refutation system for CNF UNSAT, not a proof that its certificates are polynomially bounded in L.

This construction does not establish p-equivalence or even a polynomial simulation by Res(⊕), SRC-II, Frege or extended Frege. Polynomial checkability alone does not identify a certificate system with any one of those systems.

The certificate verifier above is specified and justified mathematically; a general executable certificate verifier has not been implemented in this checkpoint. The supplied executable checks only the finite example in Sections 3–4.

## 3. Executable obstruction to a fixed-global-query interpretation

Let H(a,b,z1,z2,z3,z4) be obtained from the four contradictory clauses

    (a or b), (a or not b), (not a or b), (not a or not b)

by replacing each clause (r or s) with (r or z) AND (not z or s), using a fresh z. H is an unsatisfiable 2-CNF with six variables, eight clauses, no units, no pure variables, and no complete initial parity block.

Take disjoint six-variable copies H(U) and H(V), and define

    F = AND_{C in H(U)} (x or C)
        AND_{D in H(V)} (not x or D).

Order x first, then U, then V. This 13-variable, 16-clause formula is already 3-CNF. The frozen solver branches on x. The x=0 child is H(U); the x=1 child is H(V). Both normalize to the same six-coordinate key. The run has two distinct nonterminal keys and one cache hit.

At the shared node the local query is coordinate 1. On the x=0 path this means u1, while on the x=1 path it means v1. There is no affine function of the original variables realizing both queries on the respective path domains. Here a path domain means all assignments satisfying the preceding branch query x=0 or x=1, not assignments satisfying the unsatisfiable input formula. Restrict all irrelevant variables and suppose

    q(x,u1,v1) = c + alpha*x + beta*u1 + gamma*v1  (over GF(2)).

The x=0 requirement q=u1 forces c=0, beta=1 and gamma=0. The x=1 requirement q=v1 then demands alpha+u1=v1 for all u1,v1, impossible. The piecewise query is instead u1 + x*u1 + x*v1, of degree two.

The executable check brute-forces the full formula, observes the actual shared key in the unchanged solver, and enumerates all sixteen affine forms on these three relevant bits. It confirms the algebraic obstruction.

**Exact scope:** this disproves interpreting the existing shared node, verbatim, as one fixed affine-query node on original variables. It does not rule out duplicating nodes, choosing a different query schedule, adding extension variables, or constructing a polynomial-size Res(⊕) proof by another method. It gives no lower bound on the blow-up of such a transformation.

## 4. A positive translation of the same example into a published symmetry rule

There is a short exact proof in resolution with one global symmetry inference. Resolve each private auxiliary in the guarded H(U) block, yielding the four original contradictory 2-clauses with x appended (four steps). Resolve on u1 twice and u2 once to derive x (three further steps).

The literal permutation rho that flips x and exchanges U with V preserves the entire input F. The global symmetry rule therefore derives rho(x)=not x. One final resolution derives the empty clause. This uses nine derived lines: seven ordinary resolutions, one symmetry inference, and one closing resolution. The executable check verifies every resolvent and the input-preserving permutation.

The global/local symmetry rules are precisely described in Schweitzer–Seebach, *Resolution with Symmetry Rule applied to Linear Equations*, Section 2.1. Their local rule requires tracking which original axioms support a derivation and verifying that their renamed images remain available. This ancestry condition is substantive; arbitrary affine-normalized cache reuse has not been shown here to satisfy it. [Primary paper](https://arxiv.org/pdf/2101.05142)

Ordinary resolution can also refute this small example by deriving both guarded units separately, in fifteen derived lines. Thus the example demonstrates interface bookkeeping, not a separation between proof systems.

## 5. Published models and current-status qualification

Itsykson–Sokolov's published Res(⊕) work relates tree-like parity reasoning to DPLL with affine branching and gives tree-like lower bounds. Those bounds concern trees, not the number of shared local-namespace states. [Published paper](https://doi.org/10.1016/j.apal.2019.102722)

Bhattacharya–Chattopadhyay–Dvořák, CCC 2024, Section 3, gives the relevant fixed-global-coordinate affine-DAG definition, its relation to ResLin, and distinguishes top/bottom regularity. Their separation shows that bottom-regular lower bounds cannot simply be promoted to general ResLin. Our cached residual DAG has not been proved to satisfy either regularity condition. [Primary proceedings paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol300-ccc2024/LIPIcs.CCC.2024.23/LIPIcs.CCC.2024.23.pdf)

Current-status check, 2026-10-17: the September 2026 preprint by Kamil Braun claims general DAG-like Res(⊕) lower bounds for bit pigeonhole; the October 2026 preprint by Shuo Pang claims a degree–size transfer with further general lower bounds. Their primary full texts were retrieved, but neither proof nor associated formalization was independently validated in this review. They are therefore recorded as recent claims, not used as established premises. In particular, repeating the 2024 blanket statement that general Res(⊕) lower bounds are currently unknown would be unjustified without addressing these newer papers. [Braun](https://arxiv.org/abs/2609.23015), [Pang](https://arxiv.org/abs/2610.00837)

Even if those general Res(⊕) bounds are accepted, applying them to cached ARB-PC still requires a size-preserving simulation into that exact proof system. The namespace issue and the preprocessing/initial encoding must be accounted for first. In particular, long-clause conversion introduces extension variables: a lower bound for an original CNF encoding does not automatically apply to its equisatisfiable 3-CNF extension.

## 6. Precise remaining research question

A concrete next question is whether the residual certificate system above admits a polynomial-time, polynomial-size translation into a stated published system with controlled substitution, and whether an appropriately restricted version translates into Res(⊕). Precisely, one would seek a uniform translator and fixed polynomial p such that, for every input F and every valid residual certificate pi, the output is a refutation of the stated target encoding with size at most p(|F|+|pi|). Required deliverables are explicit local proof templates for Gaussian elimination, purity, component selection and affine-interface instantiation, followed by a bound on total shared-proof size. A mere semantic argument that a child is UNSAT does not supply this translation.

Substitution Frege is a natural upper-simulation target because it reuses tautologies under variable/formula substitutions. The classical EF simulation of substitution Frege is stated in Krajíček's author notes, Theorem 3.3.3. That established theorem does not itself give the missing translation from our residual certificates. No EF/SF equivalence or upper simulation for this candidate is claimed here. [Author's notes, Sections 3.2–3.3](https://www.karlin.mff.cuni.cz/~krajicek/ds1.pdf)

This is a sharply specified model-comparison obligation, not a claim that it is a newly discovered open problem. The source review has not settled its precise position in the existing literature. It is more informative than another sequence of ad hoc preprocessing repairs because a successful simulation would determine which existing lower-bound theorems can legitimately constrain the candidate family.

A superpolynomial lower bound for this one residual certificate system would still not prove NP!=coNP or P!=NP. Conversely, short certificates alone would not provide a polynomial-time algorithm for finding them. These quantifiers remain separate from the local model translation.
