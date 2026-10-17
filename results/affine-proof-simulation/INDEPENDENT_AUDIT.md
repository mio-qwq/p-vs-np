# Independent audit: polynomial SF / EF upper simulation

Date: 2026-10-17. Scope: mathematical construction audit against frozen implementation, plus finite semantic regressions. This is not a checked EF/SF derivation, a lower bound, a new proof-complexity theorem, or a P versus NP result.

## Verdict

No fatal mathematical gap found. The stated construction gives a credible constructive polynomial SF upper simulation, followed by the established uniform EF simulation, at the usual level of explicit proof-template mathematics. It does not infer EF simulation merely from polynomial-time certificate verification. The implementation-specific projection, purity, rank, and initial-extension obligations check out. A complete proof emitter and proof checker remain unimplemented, exactly as disclosed.

Two small precision edits are advisable before treating this as a finished exposition: include variable-name encoding in the formula-size sentence (O(D^2) counts connective/atom occurrences, not necessarily bits); and explicitly say that the final balanced-formula bridge is proved gate-by-gate, not by globally expanding the prefix extensions. Neither changes a polynomial bound.

## Hash-bound inputs

- PROOF_CANDIDATE.md: 3830cea58550bb99ff57e072ae1b798c9ded2360ce87f906b4bd46b36eaacf55
- MODEL_TRANSLATION.md: 2eb0000011fb691617d4a8ee15c30789a7c612eaca5abb2c1871e475074774b0
- arb_pc.py: 32ba57a17c8af1fc1045314fd89b849743bd6ba810fdfdb96f3a4ac9cde577c5

Candidate was read, not modified. Tests and this report are confined to the requested temporary directory.

## Implementation-specific findings

### 1. Coordinate direction

In normalize_base, RREF substitutes pivot occurrences out of masks but retains the original nonpivot coordinate indices. The dense function only replaces the ordered list of used indices by 0,...,k-1. A succession of those maps is still a projection. split_components independently uses precisely the same ordered-subset operation. Therefore a normalized child's formula can be evaluated on the surviving parent variables, without any affine expression substitution. The inverse assignment reconstruction may use affine expressions; it is not the map needed for the proof's forward implication. This is a valid strengthening/correction of the older model-translation document's more permissive interface language.

### 2. Safe purity

Every eligible variable occurs only in singleton forms of one polarity. All clauses containing such a form become satisfied, and every remaining clause omits the variable. Consequently calling normalize_base with those pure equations produces exactly the same residual key as deleting those clauses first and calling normalize_base with no equations. The forward proof uses conjunct deletion. It never infers a pure equation from the original antecedent. This distinction is essential, and the candidate observes it.

### 3. RREF, units, and termination

The row dictionary uses least-set-bit pivots, eliminates earlier pivots before insertion, and clears each inserted pivot from prior rows. Later clause reduction therefore eliminates pivot columns without changing surviving variables. A unit's affine truth value m(x) XOR c is one exactly when m(x)=c XOR 1, which matches the unit equation emitted by the code. Initial/branch equations are genuine assumptions; unit equations follow from the current clauses. Dropping equations after the substituted clause conjunction has been derived is weakening in the valid direction.

A nonterminal unit round removes an occurring pivot from all subsequent clauses; removed columns do not reappear when old equations are discarded. Each nonterminal pure round removes at least one appearing column. Thus the aggregate number of effective elimination rounds is O(D), even though normalize_base's integer n is not decremented inside its loop. A branch query is nonzero; if its result is nonterminal its free dimension is strictly smaller. All normalized coordinates appear, so each component of a proper split has smaller dimension too.

### 4. Local EF templates

Let E(u,v) be a fixed De Morgan formula for XOR. For mask inputs a_i,b_i,c_i, the equation c_i=E(a_i,b_i) has a bounded Boolean proof because each input is x_i or zero. From prefix identities C_(i-1)=E(A_(i-1),B_(i-1)) and the three defining gates, the next prefix identity follows by one fixed Boolean identity instantiated with gate variables. Each step has bounded arity; no exponential truth-table search is involved.

For a balanced subtree on interval (i,j], prove that its gate equals E(P_j,P_i); combine adjacent intervals using cancellation of their common prefix. Prove each balanced-tree gate equal to its explicit balanced subtree formula by bottom-up congruence. Its expanded subtree contains O(D^2) occurrences, and there are O(D) gates, so even a loose O(D^3) occurrence bound suffices for this bridge. This avoids expanding the nested prefix circuits. Clause congruence and the ordinary deduction transformation discharge the intended antecedent. Fresh extension atoms are absent from the final implication, satisfying EF's final-formula side condition.

These templates plus polynomially many syntactic row operations are enough for a uniform proof generator in principle. No claim that every polynomial-time computation has a short EF correctness proof is used.

### 5. Sharing in SF

Each local implication is itself a theorem, with its assumed parent formula inside the antecedent. A child negation is likewise a theorem. Thus the unrestricted SF substitution rule is applied only to already established tautologies, never to a derivation under untransported assumptions. Separate incoming projection instances refer to the same proved child formula. At most two child instances per node suffice. Branch exhaustiveness is a fixed Boolean proof, including the affine literal's constant bit. Component selection is conjunct weakening. There is no recursive replay of a child's entire proof.

### 6. Long clauses

For the sorted normalized clause l_1 OR ... OR l_r, the exact chain witnesses are y_j = NOT(l_1 OR ... OR l_(j+2)), for j=0,...,r-4, using the fresh-variable ordering of to_3cnf. The first chain clause is a tautology after substitution; each interior clause expresses a prefix-extension tautology; the last substituted clause equals the original disjunction up to association. Negative literal signs and the implementation's sorting are included in the test. The implication for a CNF follows by conjunction. The total explicit witness length is O(L^2) up to name encoding. Equisatisfiability alone is not substituted for a proof.

Parity extraction works on supports of size at most three after the 3-CNF conversion; complete forbidden-parity sets have bounded truth-table proofs. Empty clauses and the simultaneous extraction of both parity values are sound terminal cases.

## Total symbol and uniformity accounting

An input of bit length L has D=O(L) expanded coordinates and O(L) literal occurrences. Normalization does not increase clause widths or occurrences. Each mask requires O(D) bits, giving polynomially bounded keys and local formulas. Balanced XOR formulas have O(D^2) occurrences; names add logarithmic factors. Sparse original labels can each have O(L) bits but occur only polynomially many times in the final renamed formula. For actual runs, the number of distinct keys is at most 2^(poly(L)), so log(S+1) bits for globally distinct proof variable names and line references can be absorbed into poly(L). For arbitrary encoded certificates, account instead in poly(L+|pi|); irrelevant records need not be processed beyond safe parsing/reachability. The verifier's pre-normalization dimension/mask checks are important to this argument.

There are O(S+1) useful calls for a run certificate, each with polynomial-size local construction, and interface instantiation does not enlarge an affine formula beyond its polynomial node size. Applying the EF-to-SF simulation separately to each local proof preserves O((S+1)poly(L)) before the final global EF simulation. The latter may increase dependence on S polynomially, which the candidate explicitly allows.

## Source verification: uniform simulations

Primary source checked: https://www.karlin.mff.cuni.cz/~krajicek/ds1.pdf . Definition 1.0.3, p.9, defines p-simulation by a polynomial-time computable proof translator. Lemma 3.3.2, pp.52–53, gives the EF-to-SF construction and its quadratic size bound. Immediately before Theorem 3.3.3 on p.53, the notes explicitly describe the reverse result as a combinatorial p-simulation and point to references [31] and [25, Section 4.5]. Thus the cited statements support uniform polynomial translation, not only nonuniform proof-length comparison. The reverse simulation's full proof is not reproduced in these draft notes; this audit relies on the established cited theorem, not an independent reproof of it.

## Exact regression results

Run: python audit_exact_tests.py

- 4,200 seeded normalization samples, dimensions 0 through 6.
- 7,896 satisfying-assignment checks of the actual forward projection implication.
- 234 nonterminal results; 3,111 FALSE results checked against source assignments.
- 35 eligible safe-purity cases compared exactly with clause deletion.
- 87,296 long-chain witness evaluations: all input assignments and all polarity vectors, clause lengths 4 through 8.
- All checks passed.

The tests expose only the exact columns at the dense return and otherwise execute the frozen normalizer's source; they compare results with the uninstrumented function. They are finite semantic regressions, not formal proof-system verification, and do not by themselves establish the universal theorem. See audit_exact_results.json for test and solver hashes.

## Final-source acceptance (2026-10-17, 08:48 UTC)

Reviewed the full diff from the hash-bound candidate to PROOF.md, SHA256 60fda338be9e9b0af86fea307f3f6d515b9ebdd6d59166127bc9287c948a94b4. The final source incorporates both requested precision clarifications correctly: atom/connective counts are distinguished from encoded bit length, and the balanced-tree bridge uses bottom-up congruence rather than globally expanding prefix circuits. The uniformity citation now accurately reflects the independent source check.

The additional canonical reusable alphabet is valid. Every SF line in this assembly is a theorem with no open hypotheses; a substitution is simultaneous and applies to the selected theorem, not to other proof lines. Thus overlapping names across different node formulas introduce no capture or dependency problem. Local EF temporary variables must be fresh within their own local EF derivation, as usual. After converting that local proof to SF, all its lines are tautologies, so reusing those symbols in other local SF translations is also harmless. No proof-wide EF freshness assumption is being imported into the SF concatenation; the final uniform SF-to-EF translator supplies its own valid extension bookkeeping.

Accepted at the same mathematical proof-template level as the original verdict. No new gap found in these revisions. The finite regression checks remain applicable because neither frozen solver nor preprocessing changed. The proof-emitter and proof-checker qualification still applies.
