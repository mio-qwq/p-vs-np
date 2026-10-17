# Independent audit of the parity seed recurrence

## Conclusion

I find the proposed recurrence valid in the stated finite monotone cyclic AND/OR model with least-fixed-point semantics and free supplied input literals of both polarities:

- rho_m >= rho_(m-1) + 1 for m >= 2.
- rho_m >= rho_(m-1) + 2 for odd m >= 3.

This is a proof audit, not a historical novelty claim. I did not perform exhaustive circuit enumeration. The main initially delicate point, double-occurrence cleanup, has a finite graph-theoretic termination proof below. The CNF claim remains valid for parallel edges / 2-cycles.

## Model and preliminary reductions

Collapse the OR-only network, including its cyclic SCCs, by reachability. Each of the k binary AND states has equation

    y_j = (OR S_j) AND (OR T_j),

where each set consists of supplied literals, AND states, and possibly constants. The output is an OR of such sources. Empty OR is 0. Reachability closure is precisely the least solution of an OR-only subsystem, so this reduction preserves the global least fixed point.

A direct output literal is impossible for parity on at least two variables: that literal alone would imply output 1. Constant output sources are similarly easy to handle. Prune any AND state with no directed path to the output, where edges run from a state to states consuming it. Every surviving state has an output path.

Direct state self-loops can be removed by deleting y_j from its own operands. For example replace (y_j OR A) AND B by A AND B, and likewise if both sides contain y_j. If F is the old map and G the new map, G <= F. The least fixed point v of G is also fixed by F, since v_j=A(v) AND B(v) implies v_j<=A(v), and similarly for the two-sided case. Therefore lfp(F)=lfp(G). This works even though A and B depend on other cyclic states.

A constant-one operand converts its AND gate to an OR gate, which can be absorbed into the OR subsystem. Constant-zero gates can also be eliminated. These reductions save gates and preserve least semantics, including when several eliminated states form cycles.

## Universal increment by one

Any parity circuit on m>=2 must have at least one input literal entering an AND state, because the output cannot have direct literals and cannot be a constant. Set such a literal true. That AND gate becomes OR-only and is eliminable. The restricted function is parity or its complement on m-1 variables. Complemented parity has the same cost as parity for m-1>=1, by flipping the two supplied polarities of one remaining input. Thus rho_m >= rho_(m-1)+1.

Similarly, if one literal enters two distinct AND states, setting it true eliminates both simultaneously and gives the +2 bound. OR cycles among the eliminated states cause no difficulty.

## Rigorous double-fanin cleanup

Suppose we are auditing an odd-m circuit with k gates. Any equivalent circuit with at most k gates in which a literal appears in two distinct AND states already proves the desired bound. Any equivalent m-variable circuit with at most k-1 gates also proves it, by the universal increment applied to that circuit. Hence reductions saving a gate can be treated as an immediate success.

Suppose literal l occurs in only one state j but in both operands:

    y_j = (l OR A) AND (l OR B) = l OR (A AND B).

Replace state y_j by l OR z_j everywhere and retain the single AND equation z_j=A AND B, with the substitution performed throughout the circuit. There is no direct self-loop at j. This uses the same number of AND gates and preserves the state-dependency graph: references to state j become references to z_j, with an extra literal l.

Least-fixed-point preservation can be proved algebraically. Let phi(z) replace coordinate j by l OR z_j and leave other coordinates unchanged, and let F' be the transformed state map. Then F(phi(z))=phi(F'(z)). Moreover 0<=phi(0)<=F(0). Iterating F from phi(0) therefore has the same limit as iterating from 0. By finiteness, phi(lfp(F'))=lfp(F). The output substitutions preserve its value.

After this operation, l appears precisely at all consumers of state j (possibly also the output). If at least two distinct state consumers exist, we have the +2 restriction. If the output receives l directly, the circuit cannot compute parity. Otherwise there is one state consumer q. If l occurs in only one operand there, cleanup for l is complete. If it occurs in both, repeat at q.

Crucially, this is a walk along unique-outdegree vertices in the fixed state-dependency graph. Every vertex has a directed path to output. Such a walk cannot repeat a vertex, since the resulting closed unique-outdegree cycle would have no output path. Consequently the procedure terminates after finitely many distinct vertices at a single-fanin occurrence, a branch, or output. Factoring one literal does not change occurrences of any other literal, so applying this procedure to all literals terminates.

Zero operands created along the way may be retained syntactically during this walk, or eliminated immediately as the gate-saving success case. No reliance on unproved dynamic pruning is necessary.

## At most one literal per operand

After cleanup each literal occurs in at most one operand globally. If an operand contains two literals l and h of different variables, choose an assignment with both true and parity output 1; this is always possible for m>=3.

Because the circuit is finite and interpreted by its least fixed point, output 1 has a finite activation derivation. Unroll its finite proof as a tree, choosing one true source at each OR. At every use of the operand containing l and h, choose l. This omits h from the entire proof because h has no other direct occurrence. The opposite polarity of h's variable cannot occur in this true proof either, since h is true on the selected assignment. The resulting conjunction of proof leaves is thus a parity implicant omitting that variable, an impossibility: flipping that variable preserves all proof leaves but flips parity.

Proof sharing does not obstruct this argument: a finite activation derivation can be duplicated to a tree, and the same choice l can be made at every duplicated occurrence of that operand.

If an operand contains complementary literals of the same variable, it is constant 1 and its AND gate is eliminated, which is already a gate-saving success. Repeated identical terms do not matter. Therefore each operand has at most one literal.

## Seed CNF and its parity characterization

Assume no previous success. Form H by inserting clause (NOT l OR NOT h) for each AND state whose two operands both have input literals l,h. Identical literals in both operands would contradict the completed double-fanin cleanup. Complementary literals in different operands are possible, but yield a tautological clause, which is discarded. Every remaining clause therefore involves two distinct variables.

Each signed literal occurs in H at most once, since it occurs in at most one circuit operand. There are no unit clauses. H's variable incidence multigraph has degree at most two. Tautologies have been discarded, so components are isolated vertices, paths, or cycles, including parallel-edge cycles of length two.

H is satisfiable. Every path component has two satisfying assignments differing at an endpoint: make the other literal in its endpoint clause true, leaving the endpoint free, and extend along the remaining path. Any fixed assignment at a vertex of a path extends by proceeding outward, since each next constraint leaves at least one choice for its new variable. Isolated variables are also freely flippable.

In a cycle component each variable occurs once positively and once negatively. Orient the cycle and flip variables as necessary so each clause reads (a_i OR NOT a_(i+1)). These are a directed implication cycle, forcing all a_i equal. The component therefore has exactly two satisfying assignments, and they are complements in the original variables. Their parities differ exactly when the cycle has odd length. This argument covers length-two multigraph cycles.

Since satisfying assignments of distinct components combine independently, H can have constant total parity only if every component is an even cycle. In particular, when m is odd, H has satisfying assignments of both parities. Variables absent from H count as isolated vertices; they must not be omitted from this argument.

Choose an H-satisfying assignment with parity output 1. Starting from all state values zero, no AND state activates: for any state, either some operand has no input literal and is false at zero, or both have literals and H forbids them from being simultaneously true. Constant-one operands were already eliminated. Hence zero is the least fixed point. The output has no direct literals or true constant, so it is false, a contradiction.

## Important correction / precision

A seed gate can have complementary literals in its *different* operands, e.g. (x OR states) AND (NOT x OR states). This does NOT make either operand constant 1 and cannot in general be eliminated. Its seed clause is tautological and must simply be discarded from H. This does not weaken the argument: such a gate never seeds at zero. The literal-incidence bound and odd-variable parity argument still apply after discarding it. Only complementary literals in the SAME operand yield a constant-one operand and an eliminable gate.

## Consequence

The +1/+2 recurrence yields asymptotic lower bound 1.5m-O(1). If the stated exact rho_4=5 is taken as established, it yields rho_(2t)>=3t-1 for t>=2 and rho_(2t+1)>=3t+1 for t>=2. The proof above does not independently verify those small exact optima.
