> Portable copy of the independent audit. Only scratch-path references were changed; original audit SHA256: ac5066028f28c5f6eb55cb7a72d4a4f9329a7c78cc3718c1bd449e3acb9ee323. Listed script/log hashes describe the original review run; see SOURCE_PROVENANCE.json and the repository manifest for packaged hashes.

# Independent adversarial audit

Verdict: PASS. No substantive mathematical gap or counterexample found. This is an independent mathematical/code audit, not formal verification or a historical novelty certificate.

Frozen proof: `PROOF.md`
SHA256: `d46686373a10634f6976fa7c97cbdecf47b4876409ad7111829a821beab41f79`
Hash checked before and after review, unchanged.

## Proof audit

- Lines 7–11: Correct for every field, n >= 2 and d >= 1, with stated constant/trivial-group exceptions. The lower constructions are field-uniform, including the finite fields. Nonzero means nonzero as a function on permutation matrices, as required.
- Lines 18–20: Lexicographic minimization exists because the symmetric group is finite. Consecutive matching inside even cycles and all but one vertex of odd cycles, followed by pairing the odd leftovers, yields exactly floor(k/2) disjoint pairs. Each odd cycle supplies at most one leftover, so distinct cross pairs use disjoint original cycles.
- Line 22: Disjoint row supports imply the matrix at every toggle vector is P plus a sum of fixed matrix differences. There are no cross terms at matrix level. Substitution into a degree-d polynomial preserves the degree bound. Each monomial of degree <= d omits at least one of d+1 toggle variables, so its alternating sum is zero by pairing terms in that variable. No division by 2 or factorial occurs. This proves the identity in characteristic two too.
- Line 26: Under the row-image convention P[i,sigma(i)] = 1, swapping adjacent rows a,b with sigma(a)=b fixes b. Other disjoint row swaps cannot change row b, and no originally fixed row is touched. Thus every subset containing any internal pair reduces support, even when cross swaps are also present.
- Line 27: Swapping outgoing images of vertices in distinct cycles merges those cycles. Pure cross subsets use disjoint pairs of original odd cycles and hence reduce the cycle count by precisely the number of swaps, with support unchanged. The resulting cycles are nontrivial and even. This supplies the essential secondary minimization argument.
- Line 29: All other cube vertices are lexicographically earlier, so vanish. The remaining coefficient is a unit, ±1, in every field. The contradiction is valid.
- Lines 33–39: The Pfaffian is the integral matching-sum polynomial, valid for alternating matrices in characteristic two. A fixed index in S really gives a zero row and column: bijectivity prevents any other index from mapping there. If all 2d indices move and total support is <=2d, the support is exactly S, making S invariant. The all-ones kernel vector is nonzero over every field. The universal integral identity det(A)=Pf(A)^2 and absence of nonzero nilpotents in a field imply Pf(A)=0. No characteristic restriction is hidden.
- Line 41: Deleting one vertex from the directed odd-cycle skew matrix gives a path. Its unique perfect matching contributes a single product of unit edge entries, so the value is ±1 even after reduction modulo 2.
- Lines 43–47: For even n=2r <=2d+1, integer parity implies r<=d. The specified odd-row assignments occupy every even column; therefore even rows cannot be fixed either. The paired transpositions witness value 1. For odd n=2r+1 <=2d+1, r<=d and the previous Pfaffian example applies. These exhaust all finite-n boundary cases, including n=2 and n=3.
- Lines 51–57: Each GF(2) factor equals 1 exactly when its target bit matches. Their product detects precisely the target. For r=min(n,2k+1), every support of size <=r fits into an r-set; counting permutations on each such set gives at most binomial(n,r)r! <= n^r <= n^(2k+1) for n>=1. Duplicate counting is harmless. Evaluating changed rows and enumerating bounded support gives XP for fixed k. It provides neither an FPT bound nor a missing-edge-graph transfer. The solver also correctly handles n=0 and k=0.

Nonblocking editorial improvement: explicitly define P_sigma[i,sigma(i)]=1 before line 26. With the other common convention, the named fixed endpoint is a instead of b; the argument and theorem are unchanged.

## Primary historical comparison

Read the actual Derksen PDF through the web tool:
https://sites.lsa.umich.edu/hderksen/wp-content/uploads/sites/614/2018/05/A.I.a.38.pdf

Journal of Symbolic Computation 59 (2013), pages 90–91, Lemmas 2.7–2.9. Lemma 2.8 states the sufficient support radius 3d. Its proof uses d+1 disjoint adjacent transpositions, each increasing fixed points. Lemma 2.7 supplies the degree obstruction on their Boolean subgroup, and Lemma 2.9 bounds the number of bounded-support permutations. This verifies the draft's stated comparison. It does not establish historical novelty of 2d+1.

## Independent computations

Environment: Python 3.12.14, Linux 6.18.55 x86_64, glibc 2.41. Standard library only.

Executed:

    python check.py > check.log 2>&1
    python rank_check.py > rank_check.log 2>&1
    sha256sum PROOF.md solver.py *.py *.log

Both scripts returned PASS.

- Exhaustively checked every permutation for 2<=n<=8 and every nonempty subset of the full constructed pairing: 420,903 toggle cases. Checked disjointness, exact pairing cardinality, strict lexicographic descent, support descent for mixed/internal subsets, and exact cycle decrement for pure cross subsets. Checking the full pairing's subsets covers every selection of d+1 pairs.
- Recursively computed integer Pfaffians for all permutations with 3<=n<=8 and all 1<=d<=floor((n-1)/2): 137,790 evaluations. Checked vanishing at support <=2d and existence of a unit-valued example. Integer calculations also verify vanishing after reduction in every characteristic for these cases.
- Checked the alternating finite difference over the integers for all 2,352 monomials of total degree <=d in d+1 variables for 1<=d<=6.
- Imported the frozen solver and compared 6,200 calls with complete permutation brute force. Used n=0,...,7, k=0,...,4, 25 deterministic random label matrices per pair and every target. Checked both decision correctness and returned witness validity/support. Random seed: 20261017.
- Independently generated complete degree-<=d partial-bijection monomial evaluation matrices over GF(2), n=2,...,7 and d=1,2. In all twelve cases the radius min(n,2d+1) ball had full evaluation rank, while the preceding radius had strictly smaller rank. For n=7,d=2 the full/ball rank was 458 versus 372 one radius below.
- Exhaustively checked the even monomial example for n=2,4,6,8. Every nonzero evaluation moved all n points, with respectively 1,2,6,24 nonzero permutations.

Hashes:

- solver.py: 2125c16ba82f41a1679d1aab94f72e2a8578480f03c6859c846a245bfb100166
- check.py: abab0c9440a0dbd9c3bc34fd04ffbef0cc88987398b850ff8526e12d1f434586
- rank_check.py: d2d0f2c4ffe31b00a787089b7465331dcdda0c39d226cdb7e1c399b5012da12f
- check.log: ecce5e323d76aca68c7caf75760af40f7e83da4ed7527ceaa1b68c38aa1b0cdb
- rank_check.log: eeedbde61a6097157874d4bb1eb79faaa391e33eca2578d428afddf509413243

These finite computations corroborate rather than replace the field-uniform proof above. No external publication or contact was performed.
