# Independent review: restricted five-row finite exponent-height reduction

Date: 2026-10-27. Reviewed model: two partial rows with supports `{a,b}` and `{a,c}`, followed by three full rows; five distinct integer exponents and five distinct complex offsets. For initially negative exponents, identity-zero is interpreted in the rational-function field, and a common exponent shift reduces to polynomials. No general five-mask result or complexity consequence is asserted.

**Conclusion: PASS.** I independently checked the mathematical steps in `../structural/PROOF.md`; the bound is valid in the stated restricted model, including complex offsets. Every identity-zero example, if one exists, must have every consecutive exponent gap at most **408**, and normalized exponent span at most **1632**. This is a structural reduction, not a proof that all remaining bounded exponent shapes are nonzero.

## 1. Wronskian bound

Take any minimal constant-linear dependence of `k` of the 18 supported determinant monomials. Every monomial has the same total degree. Divide their common polynomial gcd, leaving polynomials `g_i` of common degree `D`, with gcd one and with all roots among the five distinct shifted roots.

Set `n=k-1` and `C=n(n-1)/2`. Every subset of `n` polynomials is independent, so each corresponding Wronskian (derivative orders `0,...,n-1`) is nonzero. Constant-coefficient Gaussian elimination gives a basis with distinct degrees; the falling-factorial determinant of distinct degrees is a nonzero Vandermonde, proving the nonvanishing rather than assuming a converse Wronskian theorem. The minimal constant relation implies every omitted-column Wronskian is a nonzero constant multiple of the others.

At each shifted root, at least one `g_i` has valuation zero. Omit that polynomial. The derivative valuation estimate `ord(f^(r)) >= ord(f)-r` gives

`ord(W) >= sum_i ord(g_i) - C`.

It remains valid if its right side is negative or some derivative vanishes. Because the Wronskians are proportional, these estimates all apply to a single nonzero polynomial W. Summing the five estimates gives `deg(W) >= kD - 5C`: each `g_i` contributes total root multiplicity exactly D. The argument may use all five listed roots even if some disappear after gcd division.

A constant basis change to distinct degrees `d_1<...<d_n<=D` preserves W up to a nonzero scalar. Thus

`deg(W) <= sum d_i - C <= nD - 2C`.

The second subtraction of C is justified by distinct degrees, not by merely subtracting differentiation orders twice. Combining the inequalities gives `D<=3C<=3*binom(17,2)=408`.

For two terms in the same circuit, if their exponents at a given root differ by t, the polynomial with the larger exponent has residual degree at least t after division by the circuit-wide gcd. Therefore every same-row exponent difference within one circuit is at most 408.

## 2. Why no circuit crossing implies separate class cancellation

Split the columns at an exponent gap larger than 408. Partition the 18 terms by the set of rows assigned to the lower group. Terms in two different classes differ at some row by more than 408, so no minimal circuit crosses classes.

Choose a basis of terms from each class. If their union were dependent, an inclusion-minimal dependent subset would be a circuit. It could neither lie in a single class basis nor cross classes. Hence the class spans form a direct sum. In particular, the signed determinant relation would have to vanish independently in every class. This does not assume the 18 terms are linearly independent.

There are exactly 18 supported terms: the partial-row column assignments are `(a,c),(b,a),(b,c)`, with six completions each. Unique root factorization and distinct exponents ensure distinct supported permutations give distinct monomials.

## 3. A class that cannot vanish

One side S of the exponent cut contains at least two of `{a,b,c}`. Its size m is in `{2,3,4}`. Assign both partial rows and any `m-2` full rows to S. The corresponding class sum is, up to one fixed sign, a product of two block determinants by Laplace expansion. The complementary block is full.

A full block is nonzero over C: its first nonzero coefficient at infinity is the product of the exponent and offset Vandermondes divided by `0!1!... (r-1)!`.

The selected block is also nonzero:

* If S contains exactly two of `{a,b,c}`, there is a unique assignment of those two columns to the two partial rows. Factoring those entries leaves a full block (possibly empty, with determinant one).
* If S has size three and contains all three special columns, its binary support determinant is -1. Hence its top-degree coefficient is nonzero.
* The only remaining shape is the four-row overlap mask `(3,5,15,15)`, not an arbitrary four-row mask.

For that overlap mask normalize partial offsets to `0,1`, full offsets to `u,v`, and exponent a to zero, writing exponents `(0,B,C,D)`. All of B,C,D are nonzero and pairwise distinct, and u,v are distinct and avoid 0 and 1. Let C_j be the coefficient of z^j in the directly normalized determinant at infinity. Independent direct permutation expansion gives:

```
C1 = -(u-v)(B+C-D)
C2 | D=B+C = BC(u-v)(u+v-1)
C3 | D=B+C,v=1-u = -uBC(u-1)(2u-1)(B+C+2)/2
C4 | D=B+C,v=1-u,C=-B-2 = uB(u-1)(2u-1)(B+1)(B+2)/6
```

Identity-zero first forces `D=B+C`, then `v=1-u`, then `B+C=-2`. The factors `u`, `u-1`, and `2u-1` are nonzero (the last by u!=v), while `B+2=-C!=0`. Finally C4 could vanish only if `B=-1`, which forces `C=-1=B`, a contradiction. No ordering or realness of the offsets was used. The broader unrestricted complex four-mask conjecture is not used and is known to be false.

Thus the selected class sum is nonzero, contradicting the direct-sum consequence. The gap bound follows; four gaps imply the span bound.

## 4. Independent exact controls

`check_height_inputs.py` was newly written for this review. It does not import the derivation agent's coefficient expressions or execute repository code. It regenerates C0 through C4 directly from the six supported four-row permutation products, checks the full factor chain, enumerates all 30 nontrivial labelled column cuts of the five columns, and checks that the selected class is nonempty and one of the three proved cases. It also checks the 18-term count, arithmetic constants, and an altered-coefficient negative control. Ordinary and optimized Python runs both pass with identical output. These controls support specific identities and finite combinatorics; the Wronskian argument above is the proof of the unbounded claim.

## 5. Exact C3 divisor parameterization for a finite engine

After subtracting the exponent a (not necessarily the minimum), put `B=b-a,C=c-a,D=d-a,E=e-a`. Swapping the two partial rows together with b,c preserves the model, so assume `B<C`; swapping the two full-support columns d,e gives `D<E`.

The C3 equation

`DE=(D+E)(B+C)-B^2-C^2`

is equivalent, with `S=B+C`, to

`(D-S)(E-S)=2BC`.

Thus every necessary tuple is recovered exactly by a signed factor pair `h<k` with `hk=2BC`, via `D=S+h,E=S+k`. Because the normalized span is at most H=1632, the outer ranges may be `-H<=B<C<=H`, excluding zero and requiring `C-B<=H`. The latter, together with the outer ranges, is exactly the span bound on `{0,B,C}`. Retain only five pairwise distinct values `{0,B,C,D,E}` of total span at most H.

For `BC>0`, both positive-positive and negative-negative factor pairs are required. For `BC<0`, h is negative and k positive; both absolute-value divisor orientations must be included. Repeated h=k is excluded by D!=E. These rules cover all 30 reduced order types; any restriction to six remaining types must separately invoke the prior 24-type theorem. Necessary low-coefficient or modular sieves must not silently divide by a quantity that can vanish. The final global offset feasibility problem remains to be certified independently.

## Editorial correction only

The original determinant equals the minimum-shift-normalized determinant times a nonzero product of row powers. Subtracting the common minimum divides by that product, rather than itself multiplying by it. Identity-zero is preserved either way. This wording does not affect the proof.

## Later all-30 extension

The subsequent full-engine plan enumerates all 30 canonical orders, not only the six formerly open over the reals. The real-only import in Section 5 is therefore unnecessary for that plan. `UNIVERSAL_GUARD_PROOF.md` gives the independent algebraic L/A/K exclusions and undivided C7 implication over C. `COMPLEX_EXTENSION_AUDIT.json` records a passing source audit and all-30 H=80 cross-check with sanitizers. These additions do not change the original 408/1632 proof.
