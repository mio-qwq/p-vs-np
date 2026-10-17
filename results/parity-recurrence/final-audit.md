# Independent final-source audit

Date: 2026-10-17.

## Reviewed immutable source identities

- PROOF.md SHA-256: `41a9d8d1f734b679953a49d7d74f10ae34d147410e859b423d925e5e3dc89786`
- check_lfp_transforms.py SHA-256: `b74113223faa399f72ac3e9ee338ecb09d6542878da594a0991bd5bd99e759c1`

The conclusions below apply to these source bytes. I did not edit PROOF.md or its original candidate during this audit.

## Verdict

No genuine mathematical gap found in the recurrence proof or its stated arithmetic consequences. My earlier complete proof audit is in independent-root-audit.md. The final proof incorporates the important distinction between complementary literals in one operand (constant-one operand, removable AND) and complementary literals across operands (tautological seed clause, discard that clause only).

The proof is specifically for finite cyclic monotone circuits with binary charged AND gates, free OR, supplied literals of both polarities, consistent Boolean inputs, and least-fixed-point semantics. It is not a claim about arbitrary cyclic-circuit semantics.

## Final-proof checks

1. OR closure and positive self-reference removal preserve least semantics. The fixed-point absorption proof in the earlier audit independently establishes the self-reference step, without assuming acyclicity.
2. Restriction of a literal occurring in two charged states removes at least two ANDs, even if those states become part of a free OR cycle.
3. The factoring transformation preserves least output, including feedback. Its fixed dependency graph and output reachability justify termination of unique-consumer pushes. With self edges removed, a one-consumer non-output state has output-distance exactly one greater than its consumer.
4. The accepting-certificate argument is sound for m>=3 and for shared cyclic states, because a finite first-activation proof has an acyclic derivation. Both chosen literals can be true on a positive-parity input, and the other polarity of the omitted coordinate cannot appear in a true proof.
5. After dropping tautological seed clauses, the incidence graph consists of paths, cycles, and isolates. Degree-two variables occur in opposite signs. Parallel-edge two-cycles are covered. All m original variables must count, including variables absent from clauses; the proof's isolated-vertex treatment does so.
6. An odd total number of variables forces a seed-free assignment of positive parity. The zero vector is then a fixed point of the charged-state update, contradicting positive output.

No concern about finite checking is being used to replace any of these universal arguments.

## Base cases and bound arithmetic

The free literal proves r(1)=0. For m=2, one AND computes `(x OR y) AND (NOT x OR NOT y)`, and the +1 recurrence gives the matching lower bound, so r(2)=1.

Summing the +1 increments for m=2,...,M and the additional +1 for odd m=3,...,M gives

    r(M) >= M-1 + floor((M-1)/2).

Starting instead from the separately established r(4)=5 yields

    r(2t) >= 3t-1       for t>=2,
    r(2t+1) >= 3t+1     for t>=2.

In particular r(5)>=7. These strengthened bounds, unlike the universal recurrence, remain conditional within this audit on the separately certified four-variable optimum and its exact linkage to this circuit model. I did not independently rerun that four-variable certification or audit the separate linkage document in this task.

## Dual-rail upper bound

For complementary prefix rails p and q, the final source defines

    p_new = (p OR x) AND (q OR NOT x),
    q_new = (p OR NOT x) AND (q OR x).

At x=0 these return p and q; at x=1 they return q and p. Thus the first is odd parity of the enlarged prefix and the second its complement.

For m>=3, retaining both rails through prefix length m-1 costs 2(m-2) ANDs: start with free one-bit rails, then spend two per extension. Computing only the odd rail on the last bit costs one more, for 2m-3. At m=2 its direct one-AND CNF has the same count. The construction is acyclic and needs no additional complemented internal wires: q is explicitly computed.

Therefore the final source's conclusion r(5)=7 is valid once r(4)=5 and the asserted exact model linkage are established. There is no need for exhaustive enumeration of five-variable circuits to obtain that corollary.

## Regression checker audit and rerun

I read and reran check_lfp_transforms.py at the hash above. It passed with:

    random seed: 741903
    input-circuit cases: 27000
    direct-self-loop deletion: pass
    duplicate-literal factoring: pass
    least-fixed-point negative control: pass

The count is correct: 6 gate counts times 150 generated circuits times (2+4+8+16) consistent inputs = 27000. There are 3600 randomly generated circuit configurations; each input-circuit case tests both transformations. The factoring test starts from a self-loop-cleaned circuit, explicitly inserts a duplicate literal on both sides of the chosen state, substitutes that literal at all consumers and the output, and compares least output values. State indices and polarity indexing are consistent.

The solver starts from all false, iterates synchronously, checks monotonic ascent, and permits enough iterations for a k-state Boolean monotone system to stabilize. Its negative control is y=y AND true, whose least value is false despite a true fixed point. It correctly distinguishes least semantics from choosing an arbitrary fixed point.

Limitations are accurately labeled: this is randomized finite regression, checks output equality on its generated cases, and is not exhaustive over finite circuits. The checker does not test the full recurrence itself, OR-only normalization as a separate circuit layer, or the earlier four-variable optimum.

Separately, I evaluated the two rail formulas exhaustively for every input at each m=2,...,10; all outputs equal odd parity and the second rail remains complementary. This corroborates, but does not replace, the elementary two-case proof above.

## Attribution and scope

No historical novelty claim is established or endorsed by this audit. Bibliographic attribution in PROOF.md was not independently verified here. No formal proof-assistant verification or P-versus-NP implication is claimed.
