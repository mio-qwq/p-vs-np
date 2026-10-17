# Finite pair-state unrolling and an explicit circuit lower-bound target

2026-10-17. Status: a mathematical derivation applying elementary finite Boolean fixed-point iteration to an inspected formal construction. Independently checked by the parent and a quantifier auditor; finite tests pass. This note is not a Lean formalization, a new historical novelty claim, or a P-versus-NP result.

## Prior-result attribution

A literature check identified the quadratic fusion upper bound in Bruno P. Cavalar and Igor C. Oliveira, *Boolean Circuit Complexity and Two-Dimensional Cover Problems* (2025), [Theorem 24](https://arxiv.org/html/2503.14117v1): D_cap(A|B) <= rho(A,B)^2. The paper gives the corresponding fusion characterization and propagation proof. The present note is therefore a reproduction/application to the pinned compiler, with explicit source-level iteration and total-gate accounting, not a new quadratic fusion theorem or a new P/poly characterization. The exact paper link is https://arxiv.org/abs/2503.14117 .

## 1. Pinned source

Repository: SamuelSchlesinger/complexitylib2.
Commit: `ffc377b51c1faac475b8cb5376d658fec457e70a`.

[Compiler source](https://github.com/SamuelSchlesinger/complexitylib2/blob/ffc377b51c1faac475b8cb5376d658fec457e70a/Complexity/Computability/Circuit/Fusion/Cyclic/Compiler.lean)

Relevant definitions/results in namespace `Cslib.Circuits.Fusion.PairClosureCompiler`:

- `readState`, lines 62–75: unions of fixed source sets and selected pair-state sets.
- `readState_pairValues`: reconstructs generated closure from the pair values.
- `readFormula`, lines 137–148: selects finite Boolean wiring through classical subset tests.
- `updateFormula`, lines 168–173: one conjunction per pair, followed by free output readout.
- `cost_updateCircuit`: exactly one charged AND per listed pair.
- `eval_updateCircuit`, lines 223–237: gives the precise autonomous pair-state equations.
- `eval_circuit`: identifies their least fixed point and the output closure.

Relevant results in namespace `Cslib.Circuits.Fusion`:

- `PairCover.eval_toCyclic`: the compiled unrestricted cover evaluates to its target.
- `pairCoverComplexity_eq_cyclic_ecomplexityFrom`: unrestricted pair-cover complexity equals cyclic AND complexity with free OR/constants.
- `PairCover.ofCircuit`, `PairCover.length_ofCircuit` in [Semifilter.lean](https://github.com/SamuelSchlesinger/complexitylib2/blob/ffc377b51c1faac475b8cb5376d658fec457e70a/Complexity/Computability/Circuit/Fusion/Semifilter.lean): extract an unrestricted pair cover from an ordinary monotone circuit, preserving its AND count.

The compiler source explicitly does not claim an efficient compiler or an iteration bound. The following argument concerns its particular point-local set interpretation. It does not modify or contradict the generic complete-lattice caveat in `Cyclic.lean`.

## 2. Theorem: k pair coordinates suffice for k rounds

Let U be any carrier, possibly infinite. Let I_1,...,I_q be supplied subsets of U. Fix a target subset T and a finite list of k pairs from the complement of T, as in the source construction. For each queried complement subset a, write

R_a(S) = C_a union union_{i in A_a} I_i union union_{j in B_a} S_j,

where C_a is either U or the empty set, A_a is a fixed subset of [q], and B_a is a fixed subset of [k]. The subsets A_a,B_a and the choice C_a are fixed by the source's global subset tests. They do not depend on the current state S or on the current carrier point.

For pair j=(a_j,b_j), define

F(S)_j = R_{a_j}(S) intersect R_{b_j}(S).

Starting with S^0=(empty,...,empty), set S^{t+1}=F(S^t). Then:

1. S^k=S^{k+1}.
2. S^k is the least fixed point of F.
3. If the pair list is an unrestricted cover of T, then R_empty(S^k)=T.
4. T therefore has an ordinary finite acyclic binary circuit from the q supplied sets, using at most k^2 AND gates, with OR and constants free.

### Proof

Fix u in U. Membership in all the R_a depends only on the q fixed input-membership bits at u and the k state-membership bits at that same u. Thus F induces a monotone Boolean map F_u:{0,1}^k -> {0,1}^k. No information at another carrier point enters this map.

The bottom trajectory z^0=0, z^{t+1}=F_u(z^t) is increasing. The first step is increasing because 0 is bottom, and subsequent steps are increasing by monotonicity. If two consecutive states agree, the trajectory is fixed thereafter. Every strict step changes at least one previously zero coordinate to one, and no coordinate can revert. There can be at most k strict steps. Therefore z^k=z^{k+1}.

This argument has the SAME bound k for every u, so it implies S^k=S^{k+1} as sets even when U is infinite. By induction S^t lies below any fixed point, proving leastness. The source's `readState_pairValues` and `eval_circuit` identify this least pair state with its pair values; the unrestricted cover property makes the empty-index closure equal T. Hence R_empty(S^k)=T.

To realize this computation acyclically, build k successive stages, sharing the preceding stage's k output wires. Each stage has k designated AND gates; all R_a computations use only ORs and constants. Finally evaluate R_empty on the last pair state. This final readout uses no AND. This is a DAG construction: unfolding the DAG into a formula would not preserve this gate bound. QED.

### Which iteration is bounded?

The bound is k rounds of the autonomous PAIR-STATE map followed by one output readout. In the source's combined k+1-coordinate update, the output may lag a round: the entire state can require k+1 rounds. The argument also does not assert that k iterations of a gate-by-gate relaxation of the feedback circuit suffice. Internal OR gates can add propagation delays to such a different schedule.

For k=0, there are no state updates and the target is the free OR/constant readout. The edge case is included.

## 3. Total size, wiring advice, and constructivity

An R_a in the source is a binary union of q+k possible terms and a seed constant. A direct construction uses q+k OR gates and at most q+k+1 constants. There are two such reads per pair and k rounds, followed by one output read. Consequently:

- AND gates: at most k^2.
- OR gates: at most 2k^2(q+k)+(q+k).
- Constants: at most 2k^2(q+k+1)+(q+k+1)+k, even without sharing constants.
- Total gates: O((k^2+1)(q+k+1)).

Only 2k+1 R_a queries are relevant: two pair endpoints per pair and the empty-index output. At most (2k+1)(q+k+1) fixed yes/no flags select their topology. Given these flags, the unrolling is a finite polynomial-size syntactic construction.

Obtaining the flags from arbitrary supplied sets is still noncomputable in general. The derivation provides an existential/nonuniform circuit-size bound, not a uniform algorithm for finding covers or deciding subset relations. It does not assume a succinct representation of the arbitrary sets in a cover. The finitely many selected flags suffice for the nonuniform existence argument, but their consistency is not thereby an efficiently checkable certificate.

## 4. Exact bridge to general Boolean circuits

Fix a standard binary encoding of SAT. For each bit length m let

- U_m={0,1}^m;
- T_m be the subset of valid satisfiable encodings, with invalid encodings rejected;
- the q=2m supplied sets be all literal sets {x:x_i=0} and {x:x_i=1};
- K_m be the minimum unrestricted pair-cover size for this target and these sources.

Let C_m be ordinary fan-in-two Boolean circuit complexity over AND, OR and NOT, with constants allowed and no uniformity requirement.

Then:

K_m <= C_m,

and

C_m <= O((K_m^2+1)(m+K_m+1)).

For the first direction, represent both polarities of every circuit wire. An original AND gate becomes one AND for its positive output and one OR for its negative output. An original OR gate becomes one OR and one AND. A NOT gate swaps the two wires. Inputs are supplied as their two literal sets. Thus a circuit with S gates yields a monotone circuit over the supplied literals with at most S charged ANDs. The source's `PairCover.ofCircuit` and `PairCover.length_ofCircuit` extract a cover of that size.

For the reverse direction, apply the unrolling theorem with q=2m. Realize the negative input literals using at most m ordinary NOT gates. The total circuit bound remains O((K_m^2+1)(m+K_m+1)).

Consequently, polynomially bounded K_m across all lengths is equivalent to SAT belonging to P/poly. The superpolynomial pair-cover lower-bound target is:

For every constant c, there are infinitely many lengths m with K_m>m^c.

Such a bound would prove SAT outside P/poly, hence NP not contained in P/poly, and therefore P!=NP. This is a stronger conclusion than P!=NP alone. We do not claim equivalence between this target and P!=NP.

No bound of this strength, or any new asymptotic lower bound on K_m, is established here. The result is an explicit, quantitatively checked reformulation of a nonuniform lower-bound target. One finite cover counterexample, one restricted family of covers, or one polynomial exponent cannot establish it.

## 5. Scope counterexample

Monotonicity alone on a powerset is insufficient. On U=natural numbers with one state coordinate, let

G(S)={0} union {j+1:j in S}.

Then G^t(empty)={0,...,t-1}; no finite t is a fixed point. This map moves information between carrier points, unlike the point-local union/intersection maps above. Thus the generic complete-lattice warning remains necessary.

Similarly, replacing unrestricted semifilters by an arbitrary restricted witness class does not preserve the source's converse. The upper bound here uses an unrestricted cover.

## 6. Reproducible finite checks

Run `python check_pair_state_unrolling.py` in this directory. The program enumerates all distinct coordinate functions of the form (OR of state bits or constant) AND (OR of state bits or constant), then tests maps assembled from those coordinates.

- k=0: 1 map.
- k=1: 3 maps.
- k=2: 36 maps.
- k=3: 5,832 maps.
- Total exhaustive maps: 5,872.
- Another 10,000 seeded random maps at k=4,...,8.
- Tight chains at every k=1,...,12 need exactly k simultaneous pair-state rounds.

All tests checked monotone bottom trajectories, fixedness by round k, and leastness against every fixed point in the tested finite state space. Results are in `pair_state_unrolling_results.json`. The tests validate the finite Boolean argument; the proof, not testing, handles arbitrary k and infinite U. No Lean build or formal kernel verification of this newly stated corollary is claimed.

## 7. Research status and stopping condition

The elementary finite Boolean iteration principle is standard. The inspected source subtree does not state the particular k-round/k^2-AND corollary; no comprehensive historical novelty search has been performed. The useful result of this round is an audited application to the pinned compiler, with a polynomial total-gate bound and the exact literal-source bridge to unrestricted nonuniform circuits.

The missing step is now explicit: a superpolynomial unrestricted pair-cover lower bound for the SAT slices. The construction and its converse supply no method to prove that bound. A next productive research step would require a concrete semifilter witness distribution or invariant that defeats every small pair list, with quantified control strong enough to exceed every polynomial. Without such a candidate and independent counterexample checks, extending the experiment alone is not progress toward P!=NP.
