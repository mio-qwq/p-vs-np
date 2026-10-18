# Independent audit: one partial row, three full rows

Audit date: 2026-10-18.

Target: the original one-partial-row proof and auxiliary symbolic derivation, as read at 13:52 UTC. The proof is published as `README.md`; original and publication SHA-256 hashes and editorial changes are recorded in `PROVENANCE.json`.

## Verdict

**The stated theorem and its proof are correct.** No gap or incorrect identity was found. This audit concerns exactly the stated four-row, four-column, one-partial-row support theorem; it establishes no broader arbitrary-mask claim.

The independent exact verifier `verify_identities.py` uses only Python's standard library. It represents polynomials by dictionaries of monomials with rational coefficients and compares all coefficients. All 38 identities passed. These are symbolic identities, not numerical examples, parameter sampling, or randomized testing. The sign and positivity arguments below complete the proof audit beyond those identities.

## Normalizations and Cauchy–Binet

1. One may explicitly permute the partial row to the first row. Permutations only change determinant sign. Adding this sentence would improve exposition but is not needed to repair the proof.
2. Factoring `(x+a_i)^m` from row `i`, where `m` is the smallest exponent, is valid even in a masked row: a zero entry is still zero times the factor. The product of these factors is a nonzero polynomial, so this preserves the question of identical vanishing.
3. Translation of the variable makes the partial-row offset zero; the other offsets `a,b,c` remain pairwise distinct and nonzero. In the Laurent-polynomial ring, factoring the indicated powers of `x` from the columns and putting `z=1/x` is reversible for the question of zero versus nonzero.
4. With the partial row first, zero-based cofactor column index `j` gives sign `(-1)^j`. For every increasing triple `K`, Cauchy–Binet orders the selected binomial indices increasingly in both factors, with no additional sign. Thus the displayed formula for `C_K` is correct.
5. Repeated binomial indices give zero alternants; the lowest sum of three distinct nonnegative indices is `0+1+2=3`. Up to degree five the only possible index triples are `(0,1,2)`, `(0,1,3)`, `(0,1,4)`, and `(0,2,3)`. No coefficient is omitted.

## All nonempty subsets are covered

There are 15 nonempty subsets: four singletons, six pairs, four triples, and the full set.

The four displayed weights equal twice the associated singleton `C_(0,1,2)`, including all signs. Their sum is zero. Since `0<p<q<r`, every weight is nonzero. Singleton and triple cases therefore have nonzero degree-three coefficient; the two same-sign pairs do as well.

For the four opposite-sign pairs the following exact factorizations independently verify the case division:

- `w0+w1 = -p(r-q)(r+q-p)`;
- `w2+w3 = p(r-q)(r+q-p)`;
- `w1+w2 = r(p-q)(r-p-q)`;
- `w0+w3 = -r(p-q)(r-p-q)`.

The first two cannot vanish. Since `r` and `p-q` are nonzero, precisely the latter two vanish at `r=p+q`. These factorizations could replace the inequality discussion, but the inequalities in the target proof are also correct.

## Full-row case

For the full set, the four-row Cauchy–Binet expansion first permits indices `(0,1,2,3)`, at total degree six. The binomial determinant equals

`p q r (q-p)(r-p)(r-q) / 12`.

The offset determinant equals `a b c V`, where `V=(b-a)(c-a)(c-b)`. Both factors are nonzero under the theorem's hypotheses. The verifier also independently sums all three-row cofactor contributions at degree six to reproduce this coefficient, and verifies all possible lower-degree contributions vanish.

## Exceptional pairs

With `r=p+q` and `B=pq(p-q)(p+q)`, the exact identities are:

- `C_(0,1,3)=B/6`;
- `C_(0,1,4)=B(p+q-3)/12`;
- `C_(0,2,3)=B(p+q-1)/12`.

The offset alternants are exactly `V s1`, `V h2`, and `V s2`, in the order displayed in the target proof. Hence the complete degree-five coefficient, before any conditional substitution, is

`VB[(p+q-3)s1²+2s2]/12`.

This independently confirms the substitution `s1=0` gives `VB s2/6`. Distinct real `a,b,c` cannot all be zero, so

`s1=0  =>  s2=-(a²+b²+c²)/2<0`.

Consequently the degree-four and degree-five coefficients cannot both vanish. `V` and `B` are nonzero. Since the full determinant has no terms below degree six, the complementary endpoint pair has the negatives of these coefficients, so it is also settled.

The smallest possible symmetric exponent case `(0,1,2,3)` causes `p+q-3=0`, but leaves the `(0,2,3)` contribution nonzero when `s1=0`. This boundary case is fully covered.

## Real-field hypothesis is essential

The proof's reliance on real offsets is genuine, rather than an artifact of its method. Let `omega` be a primitive cube root of unity, take offsets `(0,1,omega,omega²)`, exponents `(0,1,2,3)`, and retain only columns with exponents `1,2` in the offset-zero row. These four offsets are distinct.

For arbitrary `a,b,c` with these exponents and this subset, the entire normalized determinant is exactly

`-V[(a+b+c)z⁴+(ab+ac+bc)z⁵]`.

There are no omitted higher terms, since all binomial indices lie between zero and three. At `(a,b,c)=(1,omega,omega²)`, both symmetric expressions vanish, so the determinant is identically zero over the complex numbers. The verifier checks every coefficient of this exact finite formula.

## Reproduction

Run:

`python3 verify_identities.py`

Expected final line:

`All 38 coefficientwise polynomial identities verified over Q[p,q,r,a,b,c].`

This is an independent AI-assisted audit, not human peer review or proof-assistant verification. The complete release verifier also exercises altered-identity rejection and exact boundary counterexamples under ordinary and optimized Python. Theorem and audit mathematics are unchanged by publication edits.
