# Correctness, accounting and explicit obstruction for frozen ARB

## Correctness of the algorithm

For a long clause C=(l1 or ... or lr), the chain construction introduces y1,...,y_(r-3) and clauses (l1 or l2 or y1), (not y1 or l3 or y2), ..., (not y_(r-3) or l_(r-1) or lr). If all original literals are false, the chain forces every y to one and then violates the last clause. If at least one original literal is true, take each y to indicate that all original literals to its left are false; this satisfies the chain. Thus existential quantification of the fresh variables gives C exactly.

For a support S and bit b, the explicit clauses forbidding every assignment of parity other than b represent XOR(S)=b. Replacing a complete such block is an equivalence; retained additional clauses remain conjuncts. Both parity blocks on a support yield inconsistent equations, as required. Only supports of size at most three are enumerated.

Gaussian elimination detects exactly inconsistent affine equations and otherwise parametrizes their solution set by free variables. Substituting this parametrization into every remaining literal gives precisely the residual Boolean function over free coordinates. Constant simplification, complementary literals in a clause, duplication and syntactic subsumption are equivalences. An affine unit is itself an equation and is processed the same way. Previously eliminated pivots never reappear, so after substitution the old equations need not be retained when processing new units. Removing unused free variables preserves satisfiability.

If a normalized nonterminal clause contains affine form l, then l is nonconstant. Its two values partition all remaining assignments, and either branch fixes one independent affine condition. Thus free dimension strictly decreases. The returned OR of both recursively correct answers is correct. Terminal empty conjunction is SAT; empty clause or inconsistent equations is UNSAT. Identical normalized syntactic keys describe the same residual problem, even if their coordinates represent different original variables. Induction on dimension proves exact all-input correctness. Memoization does not require a semantic-equivalence test.

## Resource accounting

Let L be the explicit input bit length. Densification and 3-CNF conversion leave n'=O(L) variables and O(L) literal occurrences. All affine vectors use O(n') bits. A normalized state contains at most the original expanded number of literals because substitution changes coefficients but does not introduce disjuncts. A state therefore has polynomial size. RREF, constant/complement checks, sorting, syntactic subsumption and repeated unit substitution all have polynomial bit cost. Each successful unit-elimination round lowers the free dimension. Each branch lowers it too, hence depth is at most n'.

This gives a valid deterministic O(2^n' poly(L)) time bound. Caching can consume exponential memory. The instrumented `cache=False` option still retains a seen-key set for measurement, so it is **not** a polynomial-space implementation. A depth-first implementation omitting both caches and seen-key instrumentation would have polynomial space, but its time bound remains exponential. No polynomial total-time claim follows from polynomial state size or polynomial transition cost alone.

## Counterfamily F_k

Let H be the usual pigeonhole CNF PHP(4,3): variables h_(p,j), p=1..4, j=1..3; four positive pigeon clauses (h_(p,1) or h_(p,2) or h_(p,3)); eighteen negative collision clauses (not h_(p,j) or not h_(q,j)) for p<q. H is UNSAT: each pigeon would need at least one of three holes, while no hole may contain two of the four pigeons.

For i=1..k introduce selector x_i, partner t_i, star center a_i, and leaves b_(i,1),...,b_(i,i). Define

    F_k = H
          AND all_i (x_i or t_i)
          AND all_i all_(j=1..i) (x_i or a_i or b_(i,j)).

Variable indices increase in this order: all x_i, all t_i, all H variables, then star variables. This is exactly `families.selector_stars(k)`. It has

    variables = 12 + 3k + k(k+1)/2,
    clauses   = 22 + k + k(k+1)/2,
    literals  = 48 + 2k + 3k(k+1)/2.

Every F_k is UNSAT because it contains H. No initial support contains a complete parity block: H supplies one clause per support, selector supports are distinct pairs, and star supports are distinct triples. There are no initial units or subsumptions.

### Selector processing

While any selector remains, the earliest shortest clause is (x_i or t_i) for the least remaining i. Selector indices precede H and marker indices, and normalization preserves this relative order when densifying. If x_i=0, unit propagation sets t_i=1 and leaves exactly the positive star

    S_i = AND_(j=1..i) (a_i or b_(i,j)).

If x_i=1, both the selector clause and all its star clauses disappear. Other selectors and H are unchanged. No pure-literal or component rule removes the retained stars, because neither rule exists in frozen ARB. Both branches must eventually return UNSAT since H is unchanged.

### Distinct prefix keys; memoization cannot suppress the selector tree

At a fixed selector depth, different assignments to processed selectors retain different subsets of positive binary-only connected star components. S_i has i+1 variables, so distinct subsets have distinct multisets of these component sizes. The unresolved selector components contain ternary clauses, while the H component has negative literals. Neither can be confused with a retained star by any variable renaming. Therefore keys from different prefix zero-subsets are distinct, even under a stronger arbitrary-variable-isomorphism cache.

At different selector depths, the number of ternary clauses is

    4 + sum of i over unprocessed selectors,

which strictly decreases with depth. Thus keys cannot collide across those depths. After all selectors are processed, each of the 2^k subsets leaves H plus its retained stars, yielding 2^k distinct nonterminal keys with exactly four ternary clauses.

### Core work cannot create earlier matching keys

Immediately after all selectors are processed, H is unchanged and contains its original negative binary collision clauses. Their variable indices precede the retained-star variables. Thus the first branch after any selector-complete key is on an H variable, rather than a marker variable.

That selected variable occurs in one of the four positive ternary pigeon clauses. Setting it to one removes that clause; setting it to zero shrinks it. Hence either child has at most three ternary clauses. Subsequent branching, substitution, unit processing and syntactic normalization never increase the number of literals in a clause and never create additional clauses; initial parity extraction is not repeated. Every subsequent descendant therefore still has at most three ternary clauses, irrespective of which variables it branches on. Such a descendant cannot coincide with any selector-stage key, which has at least four ternary clauses.

Combining the distinct-prefix and stage-count arguments, cache hits from earlier work cannot prevent traversal of all 2^k selector-complete nonterminal keys.

### Consequence

The exact implemented ARB visits at least 2^k distinct states on F_k. Under explicit binary-index CNF encoding, L_k=Theta(k^2 log k). For any fixed exponent c,

    2^k / L_k^c -> infinity.

Hence no universal polynomial in input length bounds this candidate's state count or runtime. The measured stronger identity `6*2^k-1` for k<=10 is not needed for the theorem and is not asserted as a general theorem here.

## Scope and elementary repair

All selector and marker literals are positive; pure-literal elimination satisfies and removes their clauses, leaving H. Connected-component decomposition can also isolate H immediately. The counterfamily therefore does not survive either improvement. It refutes the exact round-2 compression hypothesis and motivates a stronger next candidate; it proves nothing about unrestricted SAT complexity.
