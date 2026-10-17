# Model linkage audit: unrestricted pair covers and cyclic AND cost

Date: 2026-10-17. Result: the two measures used by the parity-four certificate and the seed recurrence are exactly equal, with no additive or multiplicative AND loss. This audit concerns definitions and mathematical reductions; it does not claim historical novelty or a Lean compilation of the new recurrence.

## Frozen references inspected

1. Cavalar–Oliveira, *Boolean Circuit Complexity and Two-Dimensional Cover Problems*, arXiv:2503.14117v1, Section 2.5 and Theorem 30 (also introduction Theorem 3):
   https://arxiv.org/html/2503.14117v1#S2.SS5
   https://arxiv.org/html/2503.14117v1#S3.SS4
   Theorem 30 states equality of cover complexity and cyclic intersection complexity for a nontrivial target and nonempty generator family. Section 2.5 uses binary union/intersection equations evaluated from the empty state, with inflationary updates.
2. complexitylib2, frozen commit ffc377b51c1faac475b8cb5376d658fec457e70a:
   https://github.com/SamuelSchlesinger/complexitylib2/tree/ffc377b51c1faac475b8cb5376d658fec457e70a
   - Complexity/Computability/Circuit/Fusion/Semifilter.lean: Semifilter, SemifilterWitness, PairCover (lines 65–155).
   - Complexity/Computability/Circuit/Fusion/Cyclic.lean: PairCover.ofCyclicCircuit and PairCover.length_ofCyclicCircuit (lines 55–103).
   - Complexity/Computability/Circuit/Fusion/Cyclic/Compiler.lean: readState (62–75), updateFormula (169–173), PairCover.toCyclic, cost_toCyclic, eval_toCyclic, pairCoverComplexity_eq_cyclic_ecomplexityFrom (298–334).
   These source definitions use unrestricted upward-closed proper families, least-fixed-point cyclic semantics, free constants and ORs, and one charged binary AND per pair occurrence.
3. ROOT_SEED_RECURRENCE.md and independent-root-audit.md were read in full. Their stated model is the same supplied-literal least-fixed-point model audited below.

## Exact common model

For m>=1 let Gamma={0,1}^m, T={x:parity(x)=1}, V=Gamma minus T. Supply the 2m generator sets B_(i,b)={x:x_i=b}. These are both input polarities, not merely positive variables. They are evaluated only on consistent m-bit inputs. Treating the 2m supplied wires as independent inputs would change the problem.

A witness consists of x in T and an upward-closed family F of subsets of V with V in F and empty not in F, such that every B_(i,x_i) intersection V is in F. There is no intersection-closure requirement and no additional ultrafilter/complement-choice requirement. A pair (A,B) of arbitrary subsets of V defeats F precisely when A,B are in F but A intersection B is not. A finite list covers every witness if at least one pair defeats it. Repetitions may be charged, but removing duplicate pairs never harms a cover, so minimum list and set cardinalities agree.

Let rho_m be this minimum pair count. Let r_m be minimum number of binary AND gates in a finite cyclic monotone circuit with supplied literals, binary ORs and constants, evaluated by its least fixed point at each input. Only ANDs are charged. The output may be a wire or an OR expression; an output wire can be padded by an OR with itself at zero AND cost.

We prove rho_m=r_m directly, independently of any convention hidden in a citation.

## Direction 1: a k-AND cyclic circuit gives a k-pair cover

Evaluate the circuit at its least fixed point over all inputs in Gamma. Every gate/wire has a final truth set C contained in Gamma. For each AND gate retain the ordered pair of its two final operand truth sets, restricted to V. This produces exactly k pair occurrences, including gates that are unused or have repeated truth sets.

Suppose a witness (x,F) preserves every retained pair. Induct on activation rounds at x, maintaining: if a wire has become true at x, F accepts that wire's FINAL truth set restricted to V. For supplied inputs this is the above-x condition. True constants give V; false constants never activate. For OR, an activated predecessor has its final set contained in the final OR set, so upward closure suffices. For AND, both predecessors satisfy the induction hypothesis and preservation of that gate's retained pair gives acceptance of the final intersection. Cycles cause no difficulty because the induction is on finite activation time, not a presumed topological order.

The output eventually activates at x. Its final truth set is T, so the invariant says F accepts T intersection V=empty, contradiction. Consequently the retained pairs cover all witnesses and rho_m<=k. Taking a minimum gives rho_m<=r_m.

## Direction 2: a k-pair cover gives a k-AND cyclic circuit

Write the pairs as (A_j,B_j), j=1,...,k, and C_j=A_j intersection B_j. Introduce k Boolean state variables z_j. For each requested subset S of V define the following finite OR expression at input x:

    R_S(x,z) = [S=V]
               OR OR_{i,b : B_(i,b) intersection V subset S} [x_i=b]
               OR OR_{j : C_j subset S} z_j.

The subset tests select fixed circuit wiring. They are not runtime tests and introduce no input-dependent oracle or AND gate. Use equations

    z_j = R_(A_j)(x,z) AND R_(B_j)(x,z),

and output R_empty(x,z). There is exactly one AND per pair. Each R expression is a finite OR of constants, supplied input wires, and state wires; expand it into binary OR gates if necessary. Empty OR is false. No AND is introduced by this expansion, by the output, or by closing feedback.

To verify correctness, fix a negative input y in V. At every stage, z_j=1 implies y belongs to C_j. Inductively, every true term of R_S then implies y belongs to S: this is immediate for the top constant, for a true supplied literal whose restricted generator lies in S, and for a state term with C_j subset S. Thus state updates maintain the invariant, and R_empty remains false.

Now fix x in T and take the least state solution z*. Define F={S subset V:R_S(x,z*)=1}. This family is upward closed, contains V, and accepts every true-literal match set. Also it preserves each selected pair: acceptance of A_j and B_j forces z*_j=1 by the state equation, and then the C_j term forces acceptance of C_j. If output R_empty were false, F would therefore be a proper above-x semifilter preserving every pair, contradicting the cover assumption. Hence the output is true on every positive input.

This circuit computes exactly T, proving r_m<=k and r_m<=rho_m. Together with Direction 1, r_m=rho_m. This direct compiler is precisely the readState/updateFormula construction visible in the frozen Lean source.

## Semantic and convention checks

### Inflationary versus ordinary least-fixed-point updates

For a monotone Boolean state map F, the sequence z_0=0, z_(t+1)=F(z_t) is ascending. Therefore along this sequence z_t OR F(z_t)=F(z_t), so the inflationary iteration used in the paper produces the identical sequence. Both reach the least fixed point. For finite Gamma the set interpretation and pointwise Boolean interpretation coincide. OR-only cycles without a seed remain false.

### Binary versus unbounded OR

Every finite OR can be expanded into a finite binary tree without adding ANDs. Conversely collapsing an OR subsystem to reachability does not change its least solution. Extra OR stages change activation times but not the eventual output. Thus free unbounded OR notation is an exact cost-preserving convenience, not a strengthened AND model.

### Constants

Free 0 and 1 are present in the frozen Lean model and in the root recurrence. Even if the paper's generator list is read as excluding explicit constants, this creates no parity-domain gap for m>=1: 1 is x_1 OR NOT x_1, with zero ANDs; 0 can be a seedless OR self-loop z=z OR z, also with zero ANDs and least value zero. In the direct compiler the top seed is essential for an arbitrary generator family that does not cover Gamma; it is valid here and costs no AND. Adding explicit constant generators also imposes no extra semifilter restriction: true constant restricts to V, always accepted, and false constant never contains a positive point.

### Nontrivial target and zero-cost cases

For every m>=1 parity is nontrivial and the generator family is nonempty, so the stated hypotheses of CO25 Theorem 30 hold. For m=1 the target is itself a supplied literal and both costs are zero; above-target witnesses do not exist because a required match set is empty. The m=0 constant-domain case is outside the paper theorem and outside the recurrence's use. The frozen Lean theorem is more general because free constants handle empty/full targets, but that extension is unnecessary here.

### No hidden admissibility restriction

The source PairCover definition permits a parameter restricting admissible semifilters, but the compiler and equality theorem use its unrestricted default. The parity-four certificate validates precisely these unrestricted original families. The argument does not invoke Semifilter.IsUltra. Neither pair endpoint is required to be a generator, a circuit truth set, or definable by a short circuit. The reverse compiler handles arbitrary finite-carrier subsets by choosing fixed inclusion flags.

## Consequences and remaining scope

The independently verified rho_4=5 is therefore an exact base value for r_4, not merely a lower bound against acyclic circuits. Applying the independently audited odd-arity recurrence r_5>=r_4+2 yields rho_5=r_5>=7.

The matching upper bound uses both parity rails on four coordinates with six ANDs: compute two-bit parity and its complement for each pair of coordinates (four ANDs), then compute parity-four and its complement (two ANDs). A final AND, (parity4 OR x5) AND (complement-parity4 OR NOT x5), computes parity-five. Thus r_5<=7 and rho_5=r_5=7, conditional only on the separately audited recurrence proof and the already checked finite base certificate. No additional model-linkage gap remains.

This audit establishes a mathematical correspondence. It does not assert efficient uniform synthesis from a cover, formal verification of the new recurrence in Lean, historical novelty, or a P versus NP separation.
