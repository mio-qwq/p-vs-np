# An odd-arity gate-elimination recurrence for cyclic AND complexity

Status: mathematical proof independently audited on 2026-10-17. This is an AI-assisted proof audit, not peer review or a historical novelty claim. See independent-root-audit.md for full fixed-point and termination details. No Lean formalization is claimed.

Model: finite cyclic monotone circuits over binary AND, OR and constants, supplied with both literals of each of m Boolean coordinates. Semantics is the least fixed point at each consistent input. Cost counts AND gates; OR gates are free. Let r(m) be minimum cost for odd parity. Complementary parity has the same cost by flipping one supplied coordinate.

Claim: r(m)>=r(m-1)+1 for m>=2, and r(m)>=r(m-1)+2 for odd m>=3. Thus r(m)>=m-1+floor((m-1)/2). The second claim is the odd-arity strengthening.

## Normal form

Collapse the finite OR-only subgraph by reachability. Each charged state has equation y_j=(OR L_j)(OR R_j), where each factor is a disjunction of supplied literals and charged states. The output is another disjunction. OR cycles without a seed contribute false. This preserves least-fixed-point semantics and introduces no ANDs.

Remove states with no directed path to output. Eliminate constant AND states and direct self references. For fixed other states the least solution of y=(y OR A) AND B is A AND B, and of y=(y OR A) AND (y OR B) is A AND B. Simultaneous least-point preservation can be proved by first-activation witnesses: a state's first activation cannot use its own earlier activation. Conversely deleting positive self references only decreases the update operator, so equality of least solutions follows. A Bekić argument is an alternative.

If a literal occurs in two distinct charged states, set it true. Each affected AND becomes free OR; collapse the resulting OR subgraph. At least two charged states disappear and the restricted output is parity or its complement on m-1 coordinates. This proves the desired recurrence in this case. At least one charged occurrence exists for each input polarity of parity when m>=2: omitting a polarity would make the original function unate in that coordinate, while a literal entering the output directly would force an entire half cube to be positive. Eliminating one occurrence gives the first recurrence.

## Duplicate-side cleanup

Assume no literal occurs at two distinct charged states. If literal l is present on both sides of one state,

    y=(l OR A) AND (l OR B)=l OR (A AND B),

introduce z=A AND B and replace every reference to y by l OR z. AND count does not increase. For each fixed input, if l=0 this is a renaming; if l=1 the original y is forced true and the remaining least system is identical after substitution. Therefore the least output is preserved.

If l now appears in two different charged consumers, the earlier elimination case applies. If it reaches the output directly, parity is impossible. Otherwise it has only one charged consumer. If l is present on both sides there again, push it forward. While the AND count stays fixed, the charged dependency graph stays fixed apart from removed self edges: only direct literal seeds change. On an output-relevant node with one consumer and no output occurrence, distance to the output strictly decreases on that consumer edge. Thus such pushes terminate. If a gate becomes redundant and is removed, restart with a smaller AND count. No other literal's direct positions change during a push. Applying this to all literals leaves each literal on at most one factor, or reaches the repeated-state case.

The independent audit supplies a fixed-graph termination proof and a fixed-point conjugacy proof for this transformation. Neither is inferred from finite tests.

## At most one input literal per factor

Suppose a factor contains two literals l,h of different coordinates. For m>=3 choose a positive parity input making both true. Extract a finite acyclic first-activation proof of the positive output: one predecessor suffices at each OR, both at each AND. Every such proof must contain a true literal of every coordinate, since otherwise flipping the omitted coordinate preserves the proof but changes parity.

The unique direct occurrence of h is in this one factor. If the proof uses the factor, choose l as its OR justification, thereby omitting h globally. If it does not use the factor, h was already omitted. A shared charged node uses one first-activation justification, and cannot reappear as its own earlier dependency. Either case contradicts the preceding implicant property. Complementary literals in one factor make it constantly true on the consistent-input domain and allow removing its AND. Therefore every factor has at most one input literal.

## The seed-free 2-CNF

Initially all charged states are false. A state can initially activate only if both its factors contain true input literals. Form H by forbidding each such seed: for every state with two literal factors l,h add the clause NOT l OR NOT h. Tautological clauses from complementary l,h can be dropped. There are no unit clauses: equal literals on both factors were removed by cleanup.

Each original literal occurs at most once in H. Every assignment satisfying H has no initial activation; all charged states remain false forever. There is no literal or true constant in the output. Hence every satisfying assignment of H must have negative parity.

Consider the variable-incidence multigraph of H. Each variable has degree at most two, and a degree-two variable occurs once in each polarity. Components are paths, cycles, or isolated vertices; parallel edges are allowed, self loops were tautologies and dropped.

A path admits a pair of satisfying assignments differing only at an endpoint: choose its neighbor to satisfy the endpoint clause independently of that endpoint, extend along the remaining path, then choose either endpoint value. An isolate is likewise free. A cycle has opposite signs on the two occurrences of every variable. By flipping coordinate names and orienting the cycle, all clauses become a directed implication cycle. It has exactly two complementary satisfying assignments. A cycle of odd length therefore also admits both parities; a cycle of even length has a fixed parity. All components are satisfiable independently.

Consequently H can have only negative-parity satisfying assignments only if every component is an even cycle. This forces m even. For odd m the no-repeated-literal normal form is impossible, proving the +2 recurrence.

## Limits

This is a linear lower bound for this cyclic supplied-literal model, and hence for its equivalent fusion-cover measure, not a superpolynomial lower bound or P-versus-NP separation. It does not follow by deleting two arbitrary columns from a restricted cover: circuit elimination substitutes free OR expressions and can transform other columns. Historical status requires source review. The finite values at m=2,3,4 are checks, not proof of the recurrence.

## Base cases, stronger consequence and upper bound

The free input literal computes one-bit odd parity, so r(1)=0. The XOR CNF gives r(2)=1. Starting at r(1) yields r(m)>=m-1+floor((m-1)/2). If the separately certified four-bit cover optimum and the exact model linkage are used, r(4)=5 gives r(2t)>=3t-1 for t>=2 and r(2t+1)>=3t+1 for t>=2. In particular r(5)>=7.

For an explicit upper bound, maintain both parity rails for a growing prefix. If p is odd parity and q is its complement on the prefix, adjoining input x uses

    p_new = (p OR x) AND (q OR NOT x)
    q_new = (p OR NOT x) AND (q OR x).

For the first two coordinates both rails cost two ANDs. Each subsequent intermediate coordinate costs two; only the desired odd rail is needed at the last coordinate and costs one. Thus for m>=2 the desired single output uses 2m-3 ANDs (the m=2 case uses its single CNF directly). This is acyclic and hence valid in the cyclic model. For m=5 this gives seven, matching the lower bound once the exact model-linkage proof is included.

The independent audit and finite regression tests do not establish historical novelty. The known cyclic-circuit/fusion characterization is explicitly attributed to Cavalar and Oliveira, arXiv:2503.14117v1, Theorem 30, adapting Nakayama and Maruoka (1995). No P-versus-NP conclusion follows: the parity function already has polynomial-size circuits.
