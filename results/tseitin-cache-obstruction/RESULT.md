# Hidden Tseitin stress test: a proved algebraic obstruction and the correct caching model

## Result and stopping point

This round found a concrete growing family that defeats the solver's initial local simplifications, but did not establish an asymptotic runtime lower bound for the cached SCC-augmented solver. It established two useful proof facts instead:

1. An ordinary-only, interface-preserving run has a polynomial translation to contradiction caching with weakening (CC+W), rather than an automatic translation to ordinary resolution.
2. Every split-clause cubic Tseitin instance has a polynomial-calculus refutation over GF(2) of degree at most four. Thus this family cannot satisfy the high-degree premise of the recent degree–size preprint, even on expander graphs.

The tests also expose an actual same-interface cache hit for which the first context's learned nogood cannot close the second context. This rules out one naive proof-reuse construction. It does not prove that another polynomial simulation is impossible.

## 1. The family and its initial invariants

Let G be any connected simple cubic graph, with an edge variable for each edge and one parity charge per vertex whose total is odd. Encode each cubic parity constraint by its four forbidden-assignment 3-clauses. For each original clause C=(a OR b OR c), introduce a distinct variable y_C and replace C by

    (a OR b OR y_C) AND (NOT y_C OR c).

The order of a,b,c is their edge-index order, with their original signs. Original edge variables precede all private variables. There are 4|V| original clauses, 8|V| split clauses, and 3|V|/2+4|V| variables. This is a linear-size transformation before binary names are counted. The formula is UNSAT: existentially eliminating each y_C recovers C, and summing the vertex parity constraints gives a contradiction.

Initial units and pure literals are absent. Every clause support is unique because it contains its own private variable, so initial complete parity-block extraction finds nothing. The incidence graph stays connected. Binary clauses give only edges y_C -> c and NOT c -> NOT y_C in the implication graph; no private negative literal has an outgoing edge, and no private positive literal has an incoming edge. Thus no nontrivial binary SCC or contradictory SCC exists initially. No clause subsumes another.

This proves survival of the initial unit/pure/component/SCC/parity preprocessing for every G, not survival of every later simplification. The distinction matters: SCCs created during search greatly accelerate the prism examples below.

With no initial extracted equations, the frozen solver never creates a multivariable affine form: branches and units only fix ordinary variables. Optional SCC substitution identifies ordinary literals with signed representative literals, so it also preserves the ordinary-literal invariant. The frozen solver performs parity extraction only initially; a stronger repeated parity recognizer is outside this experiment.

## 2. What is actually simulated by the cache

Consider an UNSAT execution on ordinary clauses, with no extracted initial equations. Suppose every repeated dense cache key is reached with the same ordered list of surviving original variables. This is an explicit run condition, not an established invariant for all hidden Tseitin instances.

Then the run has a CC+W refutation of size O((S+1) poly(L)), where S is its number of distinct nonterminal states and L its input length. Here CC denotes the CNF-lemma contradiction-caching system of Beame, Impagliazzo, Pitassi and Segerlind, with branching and CNF weakening.

Proof: translate each key back to its original variable names using its recorded interface. Reverse each ordinary branch using the two restricted CNF lemmas. Reverse a unit-propagation step by branching on that unit: its inconsistent value immediately gives a CNF containing the empty clause, while its consistent value is the already refuted residual. Reverse deletion of pure-literal clauses, deletion of subsumed clauses, and selection of an UNSAT component by adding the removed clauses through CNF weakening. Each operation uses polynomially many lines and symbols. The interface condition ensures that a repeated key is literally the same CNF theorem, so its proof can be reused without renaming. Replay the recorded normalization steps in reverse and process the run DAG bottom-up. This establishes the claimed size bound.

This theorem concerns the frozen solver without the experimental SCC addition. A complete SCC-step translation into a stated caching system is not supplied here. Nor does the theorem establish CC+W upper bounds for runs with different interfaces at a shared key.

The primary 2003 paper defines these CNF-lemma systems in Section 3 and relates basic formula caching to CC in Theorem 4.1. It also gives depth-2 Frege upper simulation and separations showing that natural stronger caching variants can exceed resolution. Consequently one cannot silently replace CNF-lemma caching by clause-resolution DAG sharing. This source-based comparison also subsumes the ordinary/no-renaming part of a more general Frege upper-simulation project; it does not cover this solver's entire affine local-namespace model.

Source: https://homes.cs.washington.edu/~beame/papers/caching.pdf

## 3. An actual failed clause-reuse shortcut

On the six-vertex prism instance, the frozen solver's identity-tracking specialization reaches the same original-variable residual under branch paths

    alpha = [-3, -1, 4],
    beta  = [-3,  1,-4].

The lifted nogood from the first context is [3,1,-4], the disjunction of negated alpha decisions. It is already true under beta, since beta sets variable 1 true. It therefore cannot close beta as a conflict clause. The shared CNF lemma is valid in both contexts; the first context's lifted clause is not a reusable conflict in the second.

The SCC-augmented eight-vertex prism has the analogous paths [-3,-5,7] and [-3,5,-7]. Its first lifted nogood [3,5,-7] is again true in the second context. These are exact finite counterexamples to directly replacing a cached residual refutation by the first path's full context nogood. They do not rule out a stronger learned clause, duplicated subproofs, or another simulation.

## 4. Constant-degree PC refutation: why the recent lower bound does not apply

Work over GF(2), treating a,b,c as the truth polynomials of the three signed original literals. The two split clauses have falsity polynomials

    q1=(1-a)(1-b)(1-y),       q2=y(1-c).

Polynomial calculus derives the original clause's falsity polynomial by

    (1-c)q1 + (1-a)(1-b)q2 = (1-a)(1-b)(1-c).

Each multiplication by a signed literal is implementable using variable multiplication and linear combination. Intermediate degree is at most four. The identity is valid in the ordinary polynomial ring, with distinct a,b,c variables and fresh y; no high-degree multilinearization assumption is needed.

For a cubic vertex, summing its four forbidden-assignment falsity polynomials cancels the higher-degree terms and yields the affine polynomial expressing violation of that vertex's parity equation. Summing these linear polynomials across all vertices cancels every edge twice and leaves the constant one, since total charge is odd. This is a degree-at-most-four PC refutation for every graph in the family, with polynomially many explicitly written lines.

Pang's arXiv:2610.00837v1, Theorem 1.1, assumes that 1 has no degree-D PC derivation, with D at least max(32(p-1)^2 r,8w(F)), and concludes a lower bound on the size of a syntactic polynomial-equation resolution DAG. For p=2,r=1 and width three, its premise requires a degree threshold at least 32; our degree-four construction directly violates that premise. The theorem's proof was not independently validated here, but the applicability obstruction is unconditional.

Braun's arXiv:2609.23015v1 claims a DAG Res(⊕) lower bound for the bit pigeonhole encoding with n=2^ell holes, ell>=32, exceeding exp(n/(32768 ell^2)). That is a different formula family and proof system. Neither its proof/formalization nor an encoding-preserving simulation from this cached solver was verified here. These new preprints therefore supply no runtime lower bound for the present experiment.

Primary statements inspected:
- https://arxiv.org/html/2610.00837v1 (Theorem 1.1 and Corollary 1.3)
- https://arxiv.org/abs/2609.23015

## 5. Reproducible tests and limits

The immutable arb_pc.py from round 3 has SHA256 32ba57a17c8af1fc1045314fd89b849743bd6ba810fdfdb96f3a4ac9cde577c5. It was imported, not edited.

`probe.py` implements an original-name tracking ordinary specialization and a separate optional SCC normalizer. For prisms on 6,8,10,12,14,16 vertices, its no-SCC result, distinct-state count and cache-hit count match the frozen solver exactly. Distinct states were 11,23,47,95,191,383 without SCC and 7,11,15,19,23,27 with SCC. These are observations, not asymptotic theorems. Prism graphs are low-width graphs, not an expander family.

`check_graphs.py` tests 48 seeded cycle-plus-perfect-matching cubic graphs on 6–16 vertices with dynamic SCC normalization. All were UNSAT; all observed cache hits preserved original interfaces. Expansion was not certified, and this finite evidence proves no general interface invariant or asymptotic runtime bound.

`check_specialization.py` checks both ordinary modes against direct assignment enumeration on 1,800 small CNFs and checks all eight split-gadget projections. `check_pc_degree.py` verifies 336 symbolic split-clause identities and the complete degree-four contradiction for seven prism sizes.

Run the commands in README.md to reproduce the JSON files. The scripts resolve the frozen solver relative to the public results layout, or use the explicit ARB_PC_SOURCE development override. Its mandatory SHA256 check runs before module execution. Each JSON result is written beside the scripts, independently of the working directory. This specialization is research instrumentation, not a new proposed polynomial-time SAT algorithm.

## 6. Precise remaining obligation

A lower-bound transfer would need a size-controlled simulation into a system actually hard for the chosen encoding, not merely singleton affine masks or absence of renaming collisions. For this family, the established target is a conditional CC+W upper simulation, while the stronger parity-sensitive degree premise fails. Proving that all cache interfaces coincide would therefore still not finish a resolution lower bound.

This stops the present route at a concrete obstruction. No further selector gadgets or minor preprocessing patches are proposed. No asymptotic bound for the SCC-cached solver and no P-versus-NP conclusion is claimed.
