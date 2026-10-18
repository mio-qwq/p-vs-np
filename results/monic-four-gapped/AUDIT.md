# Independent audit: infinite one-tail-gap masked determinants

18 October 2026, UTC.

## Verdict

**PASS.** No mathematical gap or checker-completeness defect was found in the frozen theorem package. The following claims are supported:

1. Every binary 4×4 mask with a perfect matching, distinct complex offsets, and exponents `(d,d+1,d+2,d+m)` has a nonzero polynomial determinant for every integer `d≥0` and `m≥4`.
2. For exponents `(d,d+p,d+q,d+r)`, where `d≥0` and `0<p<q<r` are integers, the determinant is nonzero whenever `r≥3(p+q+1)`.

The finite cases were reconstructed independently, rather than established only by rerunning the producer checker. The infinite range was checked as a quantified mathematical proof. This is an independent AI-assisted audit of an exact proof, not human peer review or a proof-assistant formalization. No novelty claim is made.

The audit does not establish arbitrary interior-gap exponent sets, higher-order masked determinants, the color-conditioned ASNC claim, or a P-versus-NP conclusion. The report's reference to the previously proved real-offset consecutive case is ancillary: this audit independently establishes the new complex-offset range `m≥4` and explicitly verifies failure of the complex `m=3` extension.

## Frozen inputs

The original inputs matched these hashes before and after testing. The publication report has reproduction-only editorial changes, recorded in `PROVENANCE.json`; the producer checker remains byte-identical. The expanded certificate is regenerated only in temporary storage and is excluded from this package:

- `REPORT.md`: `85356654eb474399665ac8ffdc65548c786598cddd7a8aa08f96a3f0ae3facb9`
- `check_tail_gap.py`: `4b4f841b3a9796072612b6645bc2bae0d86ee32e47dceb34e78b59ae8987b0d9`
- `exact_certificate.json`: `e4ec005ccd471665c9f7b81ef3116eaf3fa8f1c2b719413583af1e9b67185a78`

The independent checker is `independent_verify.py`, SHA-256 `521ad5e0870f5a63b771d303be4e901f8c45f4430d485de4f9338e3196119e00`. It uses Python and SymPy 1.14.0 with exact rational polynomial rings. It does not import the producer checker or reuse its custom polynomial arithmetic.

## 1. Independent support coverage and determinant reconstruction

The audit enumerates all 65,536 labelled 4×4 binary masks, including masks with zero rows. Matching counts are obtained by deletion-contraction. A binary determinant is evaluated by a signed minor recurrence. An edge is classified as allowed precisely when deleting its incident row and column leaves a perfect matching. Connected components are obtained by alternating row/column closure.

The labelled counts are:

| Category | Count |
|---|---:|
| All labelled masks | 65,536 |
| No perfect matching | 27,713 |
| At least one perfect matching | 37,823 |
| Nonzero binary determinant/top coefficient | 22,560 |
| Singular, disconnected allowed-edge graph | 12,246 |
| Singular, connected allowed-edge graph | 3,017 |

Sorting row-support codes recovers exactly 3,060 nonzero-row classes. Of these, 1,062 have no perfect matching. The 1,998 remaining classes divide into 940 with nonzero top coefficient, 851 disconnected singular classes, and 207 connected singular classes. These independently recover all claimed reduction counts.

The polynomial determinant is independently reconstructed by a six-term generalized Laplace expansion along the first two rows. The products use SymPy's exact ring `QQ[x,b,c]`, rather than the producer's 24-term signed permutation expansion and custom sparse arithmetic.

For every `m=4,…,11`, all 207 residual classes are proved directly from those reconstructed coefficients. The saved certificate's 207-row coverage is checked for omissions and duplicates, its class/method counts are checked, and every supplied direct or affine-line witness is independently verified.

### Independent elimination route

The independent proof first saturates the highest nonzero coefficient by the distinctness polynomial. When that yields an affine relation, it parametrizes the entire line and computes the gcd of the **raw**, unstripped determinant coefficients restricted to that line. It then removes all factors shared with the restricted distinctness polynomial. A nonzero constant residue excludes every distinct-offset common zero over the complex numbers.

This differs from the producer's method, which first strips every coefficient and searches for any direct constant obstruction. Consequently the independent branch counts differ, as expected:

| Exponent | Direct | Raw-coefficient affine-line reduction |
|---|---:|---:|
| `m=4` | 154 | 53 |
| Each `m=5,…,11` | 156 | 51 |

Both approaches prove the same 1,656 classes. The independent method performs more affine-line reductions and validates the saved witnesses separately. It does not take the certificate's chosen relation or final gcd as the premise of its proof.

## 2. Mathematical reductions

All reductions used by the finite proof are valid over the complex numbers.

- Factoring `(x+a_i)^d` from row `i` removes a nonzero polynomial factor, so it preserves whether the determinant is identically zero.
- Sorting row-support codes simultaneously permutes the offsets. The offset tuple remains unrestricted and pairwise distinct; no numerical ordering of complex numbers is assumed.
- With `s=a_1−a_0≠0`, substitution `x=sy−a_0` gives offsets `(0,1,b,c)` after nonzero column scalings. The omitted pairwise-difference factor is `1`, and all remaining collisions are exactly excluded by `D=b c(b−1)(c−1)(c−b)≠0`.
- The coefficient at total exponent sum is precisely the binary mask determinant.
- Edges belonging to no perfect matching appear in no determinant monomial and can be deleted.
- Each allowed-edge component is balanced: any fixed perfect matching restricts to a matching covering that component. A disconnected 4×4 graph therefore splits into blocks of orders at most three. Row/column permutations change only a sign, and the polynomial determinant becomes the product of the block determinants.
- Removing a factor nonzero throughout `D≠0` preserves the common-zero set on that domain. A nonconstant affine parametrization covers the full affine line over the complex numbers. In one variable, a common zero of a finite collection is a zero of its gcd; removing all gcd factors supported on `D=0` leaves exactly the relevant obstruction.

There is no finite sampling of offset values, floating-point calculation, real-only positivity step, or assumption that numerical tests imply a quantified conclusion.

## 3. Characteristic-zero small-order lemma

The order-at-most-three proof is correct. Its combinatorial classification also has a short independent argument:

A full 3×3 mask has six perfect matchings. Each missing entry excludes exactly two. If two distinct entries are missing, their excluded matching sets overlap in at most one matching, so at least three matchings are excluded. Thus a mask with four matchings has exactly one missing entry, and five matchings are impossible. Independently enumerating all 512 masks gives the claimed frequencies `265,150,69,18,9,1` for matching counts `0,1,2,3,4,6`.

The remaining proof cases are exhaustive:

- With an odd number of matchings, the leading coefficient is an odd integer sum of signs and hence nonzero in characteristic zero.
- With two matchings, equal signs give a nonzero leading coefficient. Opposite signs would require equality of two distinct monic products. Unique factorization at the distinct roots `−a_i` forbids this: each root's multiplicity is its assigned exponent, and the exponent labels are distinct.
- For a full order-`k` determinant, `k=2,3`, the first possible nonzero coefficient is at degree `S−k(k−1)/2`. Multilinearity/Cauchy–Binet gives the product of the offset Vandermonde and the binomial-coefficient determinant. The latter equals the exponent Vandermonde divided by `∏ℓ!`, since its row polynomials have degrees `0,…,k−1` and leading coefficients `1/ℓ!`. Distinct offsets and exponents make the product nonzero in characteristic zero. Every higher degree vanishes because it would repeat an offset-power index.
- A full 3×3 determinant has degree `S−3`. Removing one entry subtracts that entry times its signed full 2×2 cofactor, whose product has degree `S−1` and nonzero leading coefficient. These distinct degrees prevent cancellation.

`check_symbolic_identities.py` additionally verifies the displayed order-two and order-three coefficient identities for symbolic offsets and symbolic exponents. The argument itself is uniform in the nonnegative integer exponents and does not depend on this auxiliary check.

## 4. Infinite-tail quantifiers

The structural lemma is valid exactly as stated, for every characteristic-zero field, every distinct offset tuple, and every pair of nonnegative integers `E,m` satisfying `m≥(n−1)(E+1)`.

Set `N=m+E` and `K=n(E+1)`. The threshold is equivalent to `N≥K−1`, so the top `K` coefficient positions exist and their binomial scale factors are nonzero. For derivative orders `0≤s≤E`, the falling factorial `(N)_s` is also nonzero. Thus the proposed powers are nonzero column scalings of derivatives of `(x+a)^N`.

Their selected coefficient matrix is a nonzero diagonal scaling of the Hermite matrix with entries `∂_a^s a^k|_{a_i}`. A polynomial of degree below `K` in its transpose kernel would be divisible by all `(a−a_i)^(E+1)`. Distinct roots make their product have degree `K`, which forces that polynomial to be zero. This proves invertibility without a realness assumption. Expanding each multiplier in the shifted monomial basis proves the equivalent polynomial-multiplier formulation.

For exponents `(0,p,q,r)`, every last-column cofactor has degree at most `E=p+q`. A supported perfect matching supplies at least one last-column edge whose complementary order-three mask has a perfect matching; the audited small-order lemma makes that cofactor nonzero. Consequently the polynomial multipliers in the last-column expansion are not all zero. The structural lemma excludes their cancellation for `r≥3(p+q+1)`.

For `(0,1,2,m)`, `E=3`, giving every integer `m≥12`. The exact finite bridge covers precisely `4≤m≤11`. Their union is every integer `m≥4`, with no uncovered endpoint or quantifier interchange. The separated-exponent criterion does not depend on the finite classifications.

## 5. Adversarial controls and execution

All controls passed:

1. At `m=3`, mask rows `(6,15,15,15)` and offsets `(0,1,t,−1−t)` give a zero determinant modulo `t²+t+1`. The distinctness polynomial is coprime to that quadratic. The independent raw-coefficient method rejects the attempted extension with that remaining quadratic. The producer rejects the same case.
2. The full mask with exponents `(0,1,2,4)` and offsets `(0,1,0,2)` gives a zero determinant, while `D=0` correctly excludes it.
3. A saved coefficient was physically altered. Both producer and independent checkers reject the corrupted full certificate with nonzero exit status in ordinary and `python -O` modes.
4. The independent checker also rejects a malformed empty certificate rather than silently switching to standalone proof mode.
5. The producer's unchanged complete checker passes the original certificate in ordinary and optimized modes.
6. Independent ordinary, optimized, and standalone runs all pass. Their full proof-result JSON objects agree exactly after removing only elapsed runtime.

All validation uses explicit exceptions and remains active under optimization. The producer checker was also reviewed for polynomial arithmetic, coefficient construction, branch completeness, and certificate equality semantics. The independent checker avoids trusting its custom arithmetic and separately validates all saved witness data relevant to the proof.

## Reproduction

The independent checker runs without the original certificate:

```text
python independent_verify.py --output-dir /tmp/monic-tail-independent
python -O independent_verify.py --output-dir /tmp/monic-tail-independent-O
```

Its requested negative controls run by default. To verify an expanded producer certificate as well:

```text
python independent_verify.py --certificate /path/to/exact_certificate.json --output-dir /tmp/monic-tail-independent
```

To reproduce the full frozen-source audit, also supply `--source-dir` pointing to the original directory containing the three frozen inputs. That optional mode pins the original report bytes and should not be used against an editorially reformatted publication report.

The publication verifier `../verify-gapped-20261018.py` exercises the producer's `m=3` control, both checkers' normal/optimized corrupt-certificate rejection paths, and malformed-certificate rejection. `check_symbolic_identities.py` reproduces the auxiliary symbolic small-order identities. Expanded independent proof witnesses and runtime logs are omitted from the source archive. The verifier regenerates them temporarily and compares mathematical output after removing only `elapsed_seconds`; its expected canonical hash is in `GENERATED.json`.

No theorem repair was required. Publication changes only clarify review status, historical hash interpretation, and compact reproduction; the mathematical audit and independent checker are unchanged.
