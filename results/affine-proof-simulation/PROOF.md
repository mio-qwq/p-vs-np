# Polynomial upper simulation of the frozen affine-residual certificate system

2026-10-17. Mathematical proof-template translation; the initial version passed an independent audit, and this exposition includes the two precision clarifications requested there. No proof-emitter implementation, new SAT algorithm, lower bound, or historical novelty is claimed.

## Target

Use exactly arb_pc.py at SHA25632ba57a17c8af1fc1045314fd89b849743bd6ba810fdfdb96f3a4ac9cde577c5 and the ranked residual certificate specified in MODEL_TRANSLATION.md. Let F be a valid CNF of encoded length L and pi an accepted UNSAT certificate. There should be a uniform polynomial-time translation to a substitution-Frege (SF) proof of not F, and hence to an extended-Frege (EF) proof, with size polynomial in L+|pi|. For a certificate extracted from a run with S distinct reachable normalized states, the SF assembly has O((S+1)poly(L)) size before the final standard EF simulation.

This is only an upper simulation. It does not justify importing resolution or Res(xor) lower bounds into the solver. It does not assert a reverse simulation or polynomially bounded certificates.

## 1. Forward coordinate interfaces are only projections

The actual RREF eliminates pivot coordinates and rewrites affine forms using the remaining nonpivot coordinates. It does not replace those remaining coordinates by new linear combinations. Dense naming then lists surviving coordinates in inherited order. Safe purity removes coordinates; component selection restricts to a coordinate subset. Consequently every forward map from a normalized child's coordinates to its parent is a projection/renaming. The inverse map extending child assignments to eliminated coordinates may be affine, but is not the substitution used to instantiate a child's UNSAT tautology.

Every reachable node contains polynomially many symbols in L: initial3CNF expansion is linear, D=O(L), clause/literal counts never increase thereafter, and masks have at most D bits. A general certificate's unreachable records can be ignored. Dimension/mask bounds are checked before normalization, as required by the existing verifier specification.

Encode each affine literal as a balanced XOR formula in a fixed Boolean basis. Its expanded formula has O(D^2) atom/connective occurrences; encoded variable names add only polynomial factors. Each node formula G_v has polynomial bit size in L. Use the canonical local alphabet x_1,...,x_D for all node formulas. Reusing symbols across independently proved tautologies is harmless: edge instantiation is a simultaneous propositional substitution, not an open-assumption context. This avoids any large global node-index naming overhead. Original sparse input names are restored at the final renaming and contribute at most the input encoding length.

## 2. Local normalization obligation, with the correct implication direction

For a call N(H), where H denotes the supplied clauses together with any genuinely assumed branch/initial equations, produce a polynomial-size EF proof of

    H(x) -> G_child(pi(x))

when the result is a nonterminal child, or a proof of not H if normalization returns FALSE. Here pi selects surviving coordinates. A TRUE result cannot be used as an UNSAT child. This is a one-way implication, not a claim that pure assignments are logical consequences of H.

The following explicit trace templates suffice:

- Duplicate removal, clause sorting and tautology deletion are fixed Boolean equivalences. Subsumption deletes a weaker conjunct; constant-false empty clauses refute H.
- A unit affine clause entails its corresponding equation. Add it under the current antecedent and perform Gaussian elimination.
- A Gaussian row addition uses the identity parity(a xor b)=parity(a) xor parity(b), including RHS constants. Swapping rows is reordering conjunctions; deleting a zero equation is tautological; obtaining 0=1 refutes the current antecedent.
- Under the derived RREF equations, replacing an affine mask by its reduced mask/RHS gives an equivalent Boolean value. Congruence through the bounded clause disjunctions derives the substituted clause conjunction. The old equations may then be dropped: only the forward implication is required.
- Dense removal of unused coordinates is syntactic projection/renaming.
- Safe purity must be treated differently. An eligible coordinate appears only as one singleton literal polarity, never inside a multi-coordinate affine form. Assigning its satisfying value deletes precisely clauses containing that literal; all remaining clauses are independent of it. The original conjunction implies the remaining conjunction by weakening. DO NOT derive the pure assignment equation from H. The subsequent normalization proof starts with this weakened conjunction, which is exactly the simplification produced by the algorithm.

Compose these implications within one normalization call. Each unit-elimination round removes at least one effective free dimension; each successful purity round removes at least one appearing coordinate. Thus there are O(D) rounds, with polynomially many row/Boolean operations per round. No semantic tautology oracle is used.

## 3. Explicit polynomial EF treatment of parity algebra

Temporary extension variables encode XOR prefix circuits rather than expanding a left-nested XOR formula. For masks a,b, let a_i,b_i be x_i or0 according to their bits, and c_i the corresponding input for a xor b. Introduce prefixes A_i,B_i,C_i with constant-size XOR gates.

For every i, the equality c_i=a_i xor b_i has a constant-size proof (both masks contain x_i, only one does, or neither). Inductively derive C_i=A_i xor B_i from the previous equality and the fixed four-input associativity/commutativity identity. This uses O(D) extension gates and fixed Boolean inference templates. RHS constants are handled by the same identities.

To connect a balanced formula encoding to a prefix output, introduce its balanced-tree gate variables. For each tree interval(i,j], derive its output equals prefix_j xor prefix_i by induction on that tree, using a fixed XOR cancellation identity. Prove each balanced-tree gate equal to its explicit balanced subtree formula by bottom-up congruence. There are O(D) such gates and each subtree has O(D^2) occurrences, so even an O(D^3) occurrence bound is polynomial. The final conclusion is thereby expressed using the explicit balanced formula; the nested prefix circuits are never globally expanded. Thus all local implications end without extension variables, while temporary circuits avoid exponential formula expansion. Total proof size and construction time are polynomial in D and the clause count.

This is a description of a proof generator from syntactic row-operation traces, not an appeal to the fact that the normalizer happens to run in polynomial time.

## 4. Assemble the shared certificate in SF

Use the established EF-to-SF polynomial simulation on each local EF implication proof from Sections2--3. It applies separately to polynomial-size local proofs. Process certificate nodes in increasing dimension rank.

- A child already has the proved tautology not G_child(y). Apply the SF substitution rule with y_i equal to the appropriate surviving parent coordinate. Only its final theorem is instantiated; its derivation is not copied.
- At a branch, the local implications are (G_parent AND(l=b))->G_child(pi_b(x)), for b=0,1, or direct contradictions for FALSE children. Combining them with the instantiated child negations yields G_parent->not(l=0) and G_parent->not(l=1). The Boolean exhaustiveness of the two values derives not G_parent.
- At a component node, G_parent implies the selected conjunct, which implies its normalized child by the local template. Its instantiated negation refutes G_parent.

Each node has at most two relevant child references. No substitution is recursively expanded along root-to-leaf paths: every local proof starts with that node's own polynomial-size encoding. Different incoming contexts may rename the same child's variables differently; this is exactly what the SF rule permits. Sharing therefore contributes O(S) local assemblies rather than a duplicated proof tree.

## 5. Initial preprocessing and return to the original CNF

Dense relabeling of occurring input names is a variable renaming with polynomial encoded cost. Explicit forbidden-parity blocks have support at most3 after the initial conversion; their equivalence to an affine equation is a fixed finite truth-table template. Hence the initial extraction/normalization has the same polynomial local proof treatment.

The long-clause3CNF conversion is only equisatisfiable, so it needs a witness substitution before deriving not F. For a clause(l_1 OR ... OR l_r), each fresh chain variable is the negation of the already processed literal prefix. The corresponding prefix-OR formulas have size O(r), and the total written witness substitution is polynomial in L. A direct fixed-template proof gives

    F(x) -> Expanded3CNF(x,sigma(x)).

After deriving the negation of the expanded3CNF, SF substitutes these explicit auxiliary witnesses in its final tautology. Combining with the implication above yields not F in the original variables. This step does not pretend that equisatisfiability alone is a propositional equivalence.

## 6. Size and system citations

There are O(S+1) reachable local calls. Each uses only polynomially many row operations, masks and clause occurrences in L; each local EF proof and its SF translation therefore has polynomial size in L. Instantiated child formulas remain polynomial size because the interface substitutions are variable projections. The final auxiliary witness substitution has polynomial size. This gives the asserted O((S+1)poly(L)) SF assembly for actual-run certificates, and polynomial size in L+|pi| generally. The standard SF-to-EF simulation then gives a polynomial EF proof, without asserting preservation of linear dependence on S.

The two established system simulations are stated in Jan Krajicek's author notes, Lemma3.3.2 (SF simulates EF) and Theorem3.3.3 (EF simulates SF): https://www.karlin.mff.cuni.cz/~krajicek/ds1.pdf . The independent audit checked that the source defines simulation through a polynomial-time translation. The construction uses those uniform simulations, not mere nonuniform existence.

Ordinary formula caching already has published proof-system upper simulations (Beame--Impagliazzo--Pitassi--Segerlind,2003). This candidate only fills the explicit affine-normalization/local-coordinate interface obligation for this particular solver. It does not claim a new general relation between SF and EF.

## Audit gates before accepting this candidate

Check the exact frozen implementation against every normalization template, especially safe purity and rank descent; verify the prefix-XOR EF templates really end in the stated explicit formulas; verify the auxiliary-variable substitution for every long-clause chain position; check the uniformity of the cited simulations; and check total symbol counts rather than merely counting nodes. A complete executable EF/SF proof emitter is not supplied or claimed.
