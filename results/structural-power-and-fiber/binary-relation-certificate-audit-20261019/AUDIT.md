# Independent audit: canonical signed subsets and matching fibers

19 October 2026. Local mathematical/checker review only.

## Verdict and stopping boundary

**PASS, with strictly finite scope.** There is no nonempty subset of the canonical signed permutation polynomials whose sum is zero for any `1 <= n <= 4`. In particular no proposed canonical `n=4` cancellation subset exists to audit for realizability or minimality. This is a finite certificate, **not general progress**, an all-order noncancellation proof, or a P-versus-NP result.

The real/rational/integer full-fiber affine-closure criterion is correct. It is not by itself a sufficient binary-edge-weight criterion. The additional exact binary condition is stated below. The supplied disjoint-cycle family gives a correct strict separation: its two endpoint matchings form a full nonnegative-integer-cost fiber for every number of blocks, but a binary-cost fiber exactly for at most three blocks.

## 1. Exact object and independent certificate

Rows and columns have labels `0,...,n-1`. For a permutation `p` let

    f_p(L) = sign(p) product_i (L+i)^{p(i)}.

A binary signed-subset relation means `sum_{p in F} f_p = 0` for a nonempty *set* of distinct permutations `F`. Here binary describes the subset indicator; it does not mean that an edge coloring realizing `F` has been found.

`check.py` independently enumerates permutations. It computes signs from cycle counts, `sign(p)=(-1)^{n-number_of_cycles(p)}`, and computes unsigned product values directly at the distinct integers `L=0,...,E`, where `E=n(n-1)/2`. No coefficient expansion, worker-produced polynomial list, polynomial evaluation oracle, floating point, or source-worker code is imported.

Each product has degree exactly `E`; therefore equality of its sums at these `E+1` points is equivalent to equality as polynomials. Split `F` into its even and odd permutations. The required identity is precisely equality of the unsigned subset sums from the two parity classes. The checker generates every subset sum on each side and intersects the exact integer evaluation vectors.

The intersections contain only the all-zero vector, and that vector has exactly one subset representation on each side, the empty subset. For `n=4`, each parity class has 12 permutations, so this means all `4096` even subsets against all `4096` odd subsets. The smaller runs have `(2,1)`, `(2,2)`, and `(8,8)` subset counts for `n=1,2,3` respectively. These counts include the empty subset.

At `L=1` every unsigned product is strictly positive, so a nonempty same-parity subset cannot represent the zero vector. The checker verifies the zero multiplicities anyway. Distinct matchings and distinct product-evaluation vectors are also checked. The latter distinctness follows mathematically from unique factorization: the multiplicity of the root `-i` is exactly `p(i)`.

For a separate determinant-sign orientation check, the sum over *all* signed products is checked at all test points against the canonical Vandermonde constant

    product_{i<j} (j-i).

Thus a local sign error is not silently absorbed into the subset test. Multiplying every determinant term by one common sign would of course preserve the zero/nonzero question.

### Scope, support, and minimality

- Every perfect-matching fiber of a subgraph on these canonical labeled rows and columns is a subset of the same permutations. Consequently the finite result rules out cancellation for every such support graph and every fiber, not just complete-graph binary colorings.
- Edge costs may be binary, integer, or real without affecting this implication: whatever fiber they define is still a subset.
- A multiset of matchings, arbitrary integer coefficients, arbitrary changed offsets/exponents, or `n>=5` is outside the checked finite statement. The separate algebraic extension below covers one specific family of changed labels. Ordinary linear dependence among the 24 degree-six polynomials does not contradict absence of a binary subset relation.
- There is no candidate whose support/cardinality minimality could be asserted. The only permissible size conclusion is that any canonical cancellation subset would need `n>=5`, if one exists.

## 2. Affine-closure characterization of a full real-cost fiber

Fix a finite bipartite graph `G` with equally sized parts, and a nonempty set `F` of its perfect matchings. Write `x_M` for matching incidence vectors in `R^{E(G)}`. Choose `M0 in F` and set

    D = span_R {x_M - x_M0 : M in F},
    W = D^perp.

Then the following are equivalent:

1. There are real edge weights `w` and a target `t` such that
   `F = {M in PM(G) : w dot x_M = t}`.
2. `aff(F) intersect PM(G) = F`, with perfect matchings identified with incidence vectors.
3. Such a full fiber can be realized by integer edge weights.
4. Such a full fiber can be realized by nonnegative integer edge weights.

**Necessity.** A linear functional constant on `F` is constant on its affine hull. An outsider matching in that hull therefore cannot be excluded from the fiber.

**Real sufficiency.** A weight is constant on `F` exactly when it belongs to `W`. For each outsider `N`, the forbidden weights form

    H_N = {w in W : w dot (x_N-x_M0) = 0}.

Condition 2 says `x_N-x_M0` is not in `D`, so `H_N` is a proper linear hyperplane in `W`. Finitely many proper hyperplanes cannot cover a real vector space. Any `w` outside their union gives exactly `F` at target `t=w dot x_M0`. If there are no outsiders, the zero weights suffice.

**Integer sufficiency.** The spanning differences have integer coordinates, so `W` has a basis of rational vectors; clear denominators to obtain integral basis vectors `b_1,...,b_d`. For each outsider, its pairing with

    w(k) = b_1 + k b_2 + ... + k^{d-1} b_d

is a nonzero polynomial in `k`. Finitely many such polynomials have finitely many roots, so an integer `k` avoids all of them. This supplies integer `w` and target. For matchings of size `n`, adding the same sufficiently large integer `c` to every edge weight adds `n*c` to every cost and preserves every fiber. It makes all weights nonnegative. The reverse implications are immediate.

The argument requires finite `PM(G)`, nonempty `F`, and that the matching vectors retain the same coordinate system. No convex-face condition, positivity of an affine combination, or extremal-cost assumption is needed.

### Ambient support

Let `U` be the union of edges used by `F`. Every point of `aff(F)` has zero coordinates outside `U`. Therefore any matching in that affine hull already lies in `PM(U)`. For any ambient graph `G` containing `U`, affine-closure equality is consequently equivalent to

    aff(F) intersect PM(U) = F.

This is a special convenience of the *real* criterion. A specific binary witness on `U` must not be assumed to remain a full-fiber witness after edges are added to `G`; outsiders using added edges must be tested in the actual ambient graph.

## 3. Exact binary condition and forbidden inference

In the notation above, a binary-edge-cost realization exists exactly when

    (W intersect {0,1}^{E(G)}) minus union_{N outside F} H_N

is nonempty. Its target is automatically the integer `w dot x_M0`.

Affine closure is necessary, but the real genericity proof does not establish this condition: a finite union of proper real hyperplanes can cover every point of a particular finite cube section even when it does not cover `W`. Rational scaling and uniform shifts yield nonnegative integer values, not necessarily the two values `0` and `1`. No such normalization is licensed by the integer construction.

This is the precise remaining test; the disjoint-cycle example below proves that it can fail despite affine closure. Likewise, a zero subset plus affine closure would only yield a real/integer-cost cancellation fiber until the binary condition had separately been established. In the present canonical `n=4` run there is no zero subset, so the reduction never reaches either realizability test.

## 4. Strict real-versus-binary separation: independently approved

Let `G_r` be the disjoint union of `r` copies of `K2,2`. Its perfect matchings are indexed by binary strings `x` of length `r`, choosing the diagonal matching for zero and the off-diagonal matching for one in each block. Let `F_r` consist of `x=00...0` and `x=11...1`.

Its affine closure contains no other matching: at any coordinate where the two incidence vectors differ, a point on their affine line can be 0/1 only when the line parameter is 0 or 1. Their union contains every edge of `G_r`.

For `r>=2`, give one off-diagonal edge cost 1 in each of the first `r-1` blocks, one diagonal edge cost `r-1` in the last block, and all other edges cost zero. The matching cost is

    x_1 + ... + x_(r-1) + (r-1)(1-x_r).

The cost-`r-1` fiber consists exactly of the two endpoint strings. For `r=1`, zero costs suffice.

For binary edge costs, each block cost difference `delta_j = off-diagonal cost - diagonal cost` belongs to `{-2,-1,0,1,2}`. Equality of the endpoint costs forces `sum_j delta_j=0`. Full-fiber exactness demands that no proper nonempty subset of these differences sums to zero.

When `r>=4`, that demand is impossible. A zero difference gives a singleton zero subsum. Opposite differences give a pair. With neither present, positive and negative values must be exclusively `+1,-2` or exclusively `+2,-1`. Zero total then supplies respectively two `+1` and one `-2`, or one `+2` and two `-1`, yielding a three-element zero subsum. In each case its size is at most 3 and hence less than `r`.

For `r=2,3`, the differences `(1,-1)` and `(1,1,-2)` are feasible with binary edge costs and have no proper nonempty zero subsum. For `r=1`, the zero difference realizes all two matchings. Therefore `F_r` is a full binary fiber exactly when `r<=3`. This sharpness is only within the specified disjoint-cycle family; it is not a globally minimal graph-size claim.

The first separating case is `r=4`, on eight vertices per side. It has 16 perfect matchings and nonnegative integer witness differences `(1,1,1,-3)`. Both endpoint permutations are even under the standard block order, so their two signed translated-power products plainly do not cancel. The graph is disconnected. This example establishes the geometric distinction, not an ASNC or polynomial-cancellation counterexample.

## 5. Review of the supplied short canonical certificate

Reviewed `binary-matching-relations-20261019/PROOF.md` and its checker. Its valuation proof is correct, including the sign convention, all four scalar subset-sum tables, the displayed polynomials for `F0`, `F1`, and `F3`, and the fact that just coefficients of degrees 0 through 4 suffice to exclude nonempty subsets.

Our `check_valuation.py` supplies an independent computation: it reconstructs each polynomial by exact Newton interpolation from direct integer product values generated by our checker. It does not import the source-worker coefficients. It verifies every scalar leading-coefficient table, each displayed branch polynomial, and the first-five-coefficient subset-sum intersection. Both normal and optimized runs pass and produce byte-identical JSON.

The source's algebraic extension is also correct. For equally spaced offsets `a,a+h,a+2h,a+3h` with `h != 0` and consecutive exponents `q,q+1,q+2,q+3`, factor the common nonzero polynomial `product_i (L+a+hi)^q` and the common nonzero scalar `h^6`, and substitute `z=(L+a)/h`. A binary relation would reduce to one in the canonical case. Negative `h` causes no exception. Consistent row/column permutations introduce only one common determinant sign. Arbitrary unequal gaps and nonconsecutive exponents remain outside this extension.

The geometry worker's final proof, including the general-`r` proposition, is approved. Its checker passes both modes, including exact rank/normal-space tests, all 63 nonempty subsets of the six `K3,3` matchings, and the first four-cycle boundary. The `K3,3` binary/real coincidence must not be extrapolated; the disjoint-cycle proposition explicitly separates them.

## 6. Reproduction and artifacts

Run `python check.py` and `python -O check.py`. Both runs passed; their `results.json` files are byte-identical. All checks use explicit exceptions rather than removable assertions. `results.json` contains all matching evaluation vectors, parity counts, intersection and zero-multiplicity results, and deterministic SHA-256 hashes of both ordered subset-sum lists.

The independent audit is intentionally bounded to the supplied canonical small-order claim and the elementary geometry lemma. It makes no novelty claim, no general matching-complexity claim, and no repository or publication changes.
