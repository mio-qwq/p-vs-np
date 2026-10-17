# Uniform cyclic-cover route to SAT: exact algorithmic target

## 1. Two different input spaces

For a particular CNF F of bit length L with n occurring variables, its assignment-evaluation function is f_F(a)=F(a), on n assignment bits. Its satisfying set is A_F={a:F(a)=1}. A circuit computing f_F already has size polynomial in L: compute each literal, OR each clause, and AND the clauses. Supplying both input polarities gives a small monotone circuit and hence a small unrestricted pair cover in the previously audited framework. Constructing this cover uniformly from F therefore does not solve SAT. SAT asks whether A_F is nonempty, not for its membership at one supplied assignment.

The relevant SAT slice instead has carrier U_m={0,1}^m consisting of formula-encoding strings. Fix a standard polynomial-overhead binary CNF encoding that is polynomial-time intertranslatable with the usual CNF SAT representation, and reject malformed strings. In particular, encoding an ordinary SAT instance has polynomial output length and takes polynomial time. Merely polynomial-time decoding is insufficient: exponentially padded encodings could make their language easy as a function of padded input length. Its target is

    T_m={z in {0,1}^m : z encodes a satisfiable CNF}.

Its 2m supplied source sets are the positive and negative literals of the encoding bits z_i. These are not the n assignment-variable literals of one fixed formula.

## 2. One precise sufficient uniform target

There must exist ONE deterministic machine A and constants c,d such that for EVERY integer m>=1:

1. A(1^m) halts in at most (m+1)^c steps.
2. It outputs an integer k<=(m+1)^d and explicit Boolean wiring for 2k+1 read functions. Each read is an OR of a constant flag, a selected subset of the 2m input literal bits, and a selected subset of the k state bits.
3. With states initially all zero, each of k simultaneous updates sets state j to the AND of its two specified reads. A final specified read is the output.
4. For EVERY z in {0,1}^m, this output is 1 if and only if z belongs to T_m.

The explicit wiring uses (2k+1)(1+2m+k) Boolean flags, plus a polynomial-size header. No arbitrary set, truth table of length 2^m, unbounded integer, membership oracle, subset oracle, or advice depending on m is left implicit. The pair-cover route may produce these flags by first producing a valid cover, but the algorithmic target is the complete executable wiring. A correctness proof must justify its target behavior on all strings; testing does not supply this universal guarantee.

### Sufficiency and evaluation cost

On input z, compute m=|z|, run A(1^m), form its 2m literal bits, and evaluate the k simultaneous updates plus final read. The cost is O((k^2+1)(m+k+1)) Boolean operations, in addition to A's polynomial construction cost. The point-local monotone pair-state argument ensures bottom stabilization by k rounds. Thus this target implies SAT in P and hence P=NP.

For m=0 the fixed encoding's single empty string can be handled separately in constant time. The k=0 case is simply the final free read.

### Converse, to locate the difficulty

If SAT is in P, its fixed polynomial-time machine can be uniformly unrolled into polynomial-size circuits for all length-m inputs. Double-rail each wire so internal NOT gates become swaps and AND/OR swap between positive and negative rails. Flatten OR-only paths into the selected-source/state reads and assign a state coordinate to each AND gate. The resulting acyclic dependency network is a special case of the stated cyclic network. It stabilizes within k updates and has polynomially many explicit flags, constructible in polynomial time. The source's circuit-to-cover theorem supplies corresponding unrestricted covers if actual set-theoretic cover objects are desired.

Consequently this sufficient executable-wiring target is equivalent to SAT in P. It precisely states a remaining algorithmic obligation; it is not a simplification already achieved by the existence theorem.

## 3. Nonuniform existence and hidden subset tests

The weaker statement

    there exists a constant d such that for every m there exists
    a cover with k<=(m+1)^d (and corresponding finite wiring)

does not specify a uniform algorithm choosing those covers or flags. By the audited cover/circuit equivalence it gives SAT in P/poly. It does not by itself imply SAT in P. The order and effective content of the quantifiers matter: polynomial-size advice for each length is not a polynomial-time generator.

Nor does an efficient list of succinct endpoints automatically give efficient wiring. The compiler's flags are determined by subset tests among represented sets. For arbitrary circuit/CNF predicates, deciding A subseteq B is coNP-complete: already A=A_phi and B=empty asks whether phi is UNSAT. Thus a compilation step treating these flags as unit-cost semantic queries can hide the original decision difficulty. This observation concerns general succinct-set inclusion; it does not prove that every specially constrained family of cover endpoints has hard inclusion tests. A proposed construction must either compute its own flags efficiently or prove an efficient structural test for precisely its endpoint family.

If an endpoint description uses membership in T_m as an oracle, evaluating it already invokes SAT. If it is literally T_m or its complement represented only by its semantic name, it is not an explicit computable output representation. If validity of a guessed cover is merely asserted, no polynomial-time generator has been given. Neither a short description nor an existential correctness proof licenses oracle calls in the runtime bound.

## 4. Exact shortcut refutation

The natural attempted shortcut replaces each source set by its nonemptiness bit and runs the same union/intersection network. Nonemptiness preserves union but does not preserve intersection:

    A={1}, B={0}; A and B are both nonempty, but A intersect B is empty.

Equivalently F=(x) AND (NOT x) has each clause individually satisfiable, yet F is UNSAT. Point-local closure combines source values at the SAME assignment, while independently existentially projecting each clause can use different assignments. Merely reaching a fixed point quickly does not resolve this cross-assignment consistency problem.

The companion checker enumerates all CNFs with at most three distinct non-tautological clauses over n=1,2,3 variables, including the empty clause and empty formula. It checks 3,442 formulas and 26,968 assignment evaluations. Ordinary dual-rail evaluation agrees in every case. The premature clause-by-clause existential projection returns a wrong SAT result on 122 formulas. These finite checks illustrate the exact counterexample, not a complexity lower bound. No claim is made that the source repository proposes this invalid shortcut.

## 5. Relation to the verified solver and next proof obligation

The earlier affine-residual solver has exact semantics and explicit exponential families; its polynomially checkable UNSAT certificates do not supply a polynomial search algorithm. Similarly, a compact cover or circuit for assignment evaluation supplies a representation, while the existential decision and uniform construction remain separate obligations.

A meaningful positive result here would be a concrete machine A meeting Section 2, with worst-case construction and bit-cost bounds and an all-input correctness proof, or a strictly intermediate structural lemma that provably enables such construction. Another small assignment-function cover is not that result. No such A or new SAT algorithm is established by this audit.

## Source and reproduction

The point-local k-round bound, explicit flag count, and SAT-slice nonuniform equivalence were established in the prior independently audited pair-state-unrolling checkpoint. Its pinned primary compiler is Samuel Schlesinger's complexitylib2 commit ffc377b51c1faac475b8cb5376d658fec457e70a:

https://github.com/SamuelSchlesinger/complexitylib2/blob/ffc377b51c1faac475b8cb5376d658fec457e70a/Complexity/Computability/Circuit/Fusion/Cyclic/Compiler.lean

Circuit-to-cover definitions are in Fusion/Semifilter.lean at that commit. This audit applies that inspected version, not a claim about unseen subsequent revisions. A fresh web fetch of the pinned source failed during this round; the previously audited source analysis is the provenance for compiler-specific statements.

Run `python check_projection.py` to reproduce `projection_results.json`. The mathematical implications and counterexample above do not depend on the finite test range. No novelty claim is made.
