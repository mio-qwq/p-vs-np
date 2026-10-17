# ARB-PC correctness and connected nonpure state-count obstruction

## 1. Correctness and resource accounting of the repair

Initial sparse-name densification and equisatisfiable 3-CNF conversion use polynomial size. A complete wrong-parity clause block on at most three coordinates is exactly an XOR equation. Gaussian elimination either detects contradiction or parametrizes the equation solution set by free coordinates. Substitution into the remaining affine literals preserves precisely that residual problem. Unit equations, constant simplification, duplicate removal and syntactic subsumption retain their round-2 semantics.

For the added purity rule, let a free coordinate x occur only as the same singleton literal x or not-x. No other affine form depends on x, by the explicit eligibility test. Setting x to satisfy that polarity satisfies all clauses containing x and leaves every other clause unchanged. Any satisfying assignment to the remaining problem therefore extends to a satisfying assignment of the previous problem. The converse follows by discarding satisfied clauses. This proves satisfiability preservation. Coordinates occurring inside multi-coordinate forms are deliberately excluded; treating those forms as unrelated propositional atoms would be unsound.

For decomposition, join every coordinate in the total support of each clause, including every coefficient of each affine literal. Different resulting components use disjoint free coordinates. Their constraints therefore admit a joint assignment exactly when every component admits an assignment. Independent recursive solutions may be combined by AND. All initial equations have already been substituted, so no omitted affine equation couples these free-coordinate components.

Branching on a nonconstant affine form partitions all assignments into its two values and lowers free dimension. A decomposition with at least two nonempty components has strictly smaller dimension in every child. Pure elimination also lowers dimension. The explicit stack consequently terminates on every finite input; induction on dimension proves the returned Boolean answer correct. The canonical cache key retains exact syntactic affine clauses after dense order-preserving renaming, which preserves satisfiability without an equivalence oracle.

Let L denote explicit input bit length and n'=O(L) the number of variables after 3-CNF conversion. Bit-vector length is O(n'), and each normalized state has at most the initial expanded number of literals. Purity tests, Gaussian elimination, sorting, subsumption and support-component construction have polynomial bit cost. A coarse valid bound is 2^{O(n')} poly(L) time and potentially exponential memory. Polynomial transition cost is not a polynomial total-time theorem. The instrumented cache=False option still retains a seen-key set for counting and is not a polynomial-space implementation.

## 2. Formula family

Let H=PHP(4,3), with twelve variables h_(p,j), four positive clauses asserting each pigeon chooses a hole, and eighteen negative binary clauses preventing two pigeons from sharing a hole. H is unsatisfiable. Let h be its smallest-index variable.

For i=1,...,k introduce selector variables x_i,u_i,v_i and marker variables a_i,b_i. Include the selector implication cycle

    (not x_i or u_i), (not u_i or v_i), (not v_i or x_i),

the marker implication cycle through the core variable h

    (not h or a_i), (not a_i or b_i), (not b_i or h),

and the gate

    (x_i or a_i or b_i).

Order variables as all x_i first, then u_i,v_i, then the twelve core variables, then a_i,b_i. Call the conjunction with H F_k. This is `connected_markers(k)`.

Counts are n_k=12+5k, m_k=22+7k and 48+15k literal occurrences. With explicit binary variable indices the bit length is Theta(k log k). All F_k are UNSAT because H is a conjunct.

Each variable occurs with both polarities. The clause-support graph is connected: H is connected; marker cycles attach through h; each selector cycle attaches through its gate to its marker variables. No support contains a complete initial parity block. Every cycle support is a distinct pair, each gate has its own triple, and core supports are distinct. There are no initial units or syntactic subsumptions.

## 3. Selector-stage invariant

After assigning the first d selectors, the normalized residual consists of:

- the unchanged core H;
- every marker cycle, still with both a_i and b_i present;
- selector cycles and ternary gates for i>d;
- the binary clause (a_i or b_i) precisely for processed selectors assigned x_i=0.

If x_i=0, unit propagation around its private implication cycle sets u_i=v_i=0. The gate reduces to (a_i or b_i). If x_i=1, propagation sets u_i=v_i=1 and deletes the gate. In either case only that selector's three variables disappear; marker cycles remain.

No resulting optional binary clause is a unit, tautology or syntactically subsumed clause. It differs from the implication clause (not a_i or b_i). It does not contain the core variable h. Every surviving variable still occurs with both polarities, so safe purity makes no change at these stages. All surviving variables remain connected through H and its marker cycles, so decomposition makes no split.

The smallest-index variable in any shortest binary clause is the next x_i: selector indices precede all core and marker indices. Among its two incident clauses, the one with positive x_i sorts first. Thus the prescribed algorithm branches x_i=0 then x_i=1. Every subtree remains UNSAT because H is unchanged, so both branches must be evaluated unless an identical key was already solved.

## 4. Exact cache distinction and reachability

At the same depth d, exactly the same original variables have disappeared on every selector path. Dense order-preserving coordinate naming is therefore identical on those paths. Distinct zero-subsets give distinct sets of optional clauses (a_i or b_i) in those same coordinates. They are distinct exact syntactic keys. This argument is intentionally about the implemented order-preserving dense cache, not arbitrary variable-isomorphism canonicalization: the marker gadgets are symmetric and arbitrary isomorphism could identify different subsets of equal cardinality.

At different depths the ternary-clause count is 4+k-d, which strictly decreases. Thus selector-stage keys from different depths cannot coincide. All keys with d=k have exactly four ternary core clauses, and their 2^k optional-marker subsets are distinct.

It remains to exclude cache entries from completed core work. At d=k, all selector variables have disappeared. The first branch variable belongs to H: core variable indices precede marker indices, and an original binary core collision clause is available (a marker clause with first coordinate h may instead come first, but h is also a core variable). The selected variable appears in a positive ternary pigeon clause. Setting it either way satisfies or shrinks that clause. Thus either child has at most three ternary clauses. Later branching, substitution, unit processing, purity and decomposition never increase clause lengths or add clauses, so all further descendants also have at most three ternary clauses. They cannot equal a selector-stage key, which has at least four.

These observations prove that no earlier cache entry suppresses a new selector-prefix key. By induction the complete binary selector tree is reached, including at least 2^k distinct selector-complete nonterminal keys. There is no early terminal at those keys: H still has its original nonunit clauses and no empty clause, and the syntactic normalizer does not recognize its pigeonhole contradiction.

Consequently ARB-PC has no polynomial-in-input-length bound on its visited state count. On L_k=Theta(k log k) this gives 2^{Omega(L_k/log L_k)} states. This is a candidate-specific asymptotic result, not a lower bound for unrestricted SAT.

## 5. Why this still does not advance a general lower bound

Each selector implication cycle forces x_i=u_i=v_i. Each marker cycle forces h=a_i=b_i. Identifying variables along these strongly connected implication components turns all cycle clauses into tautologies and every gate into (x_i or h). Each x_i then appears only positively, so purity removes these gates, leaving H. A standard implication-equivalence preprocessing step can therefore defeat the family in polynomial time.

The reproducible control substitutes these explicit family identities rather than pretending to implement a general SCC preprocessor. This demonstrates the limit of the construction and justifies stopping this sequence of small preprocessing repairs. No inference from this family to all SAT solvers, all affine representations, or P!=NP is valid.
