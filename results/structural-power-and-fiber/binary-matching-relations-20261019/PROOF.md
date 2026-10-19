# A four-row binary noncancellation certificate

19 October 2026. Local exact mathematical result. No repository, PR, merge, tag, or release was changed.

## Result and scope

Let a permutation `p` of `(0,1,2,3)` list the exponent/column chosen in each row, and put

    f_p(L) = sgn(p) product_{i=0}^3 (L+i)^{p(i)}.

**Theorem.** If `epsilon_p` is either zero or one for every permutation, then

    sum_p epsilon_p f_p(L) = 0

holds identically only when every `epsilon_p` is zero. In fact, vanishing of just the coefficients of `L^0,L^1,L^2,L^3,L^4` forces this conclusion.

Thus there is no nonempty binary zero subset among these 24 polynomials, whether or not the subset is realizable as a matching fiber. The theorem immediately covers every nonempty matching family selected by a binary support, by a red-count fiber, or by any other selection rule in this four-row canonical setting.

It is not a theorem for arbitrary four-row offsets, arbitrary exponent lists, or arbitrary matrix size. It does not establish a general P-versus-NP bridge. It also makes no claim about weighted nonnegative relations: coefficients other than zero or one fall outside the theorem.

## 1. A short exact proof by valuations

Partition the permutations into four groups `G_r={p:p(0)=r}`. Each group has six elements. Every polynomial in `G_r` is divisible by `L^r`; terms in higher-numbered groups therefore cannot affect the coefficient of `L^r`.

For each group, the table gives its positive leading coefficient magnitudes and its negative leading coefficient magnitudes. Their subset sums are small enough to check directly: each side has only three entries, hence eight subset sums.

| r | Positive leading magnitudes | Negative leading magnitudes | Positive subset sums | Negative subset sums |
|---|---|---|---|---|
| 0 | 108,24,18 | 72,54,12 | 0,18,24,42,108,126,132,150 | 0,12,54,66,72,84,126,138 |
| 1 | 72,27,4 | 108,8,9 | 0,4,27,31,72,76,99,103 | 0,8,9,17,108,116,117,125 |
| 2 | 54,8,3 | 24,27,2 | 0,3,8,11,54,57,62,65 | 0,2,24,26,27,29,51,53 |
| 3 | 12,9,2 | 18,4,3 | 0,2,9,11,12,14,21,23 | 0,3,4,7,18,21,22,25 |

All subset sums in each individual list are distinct, so the matching sums below identify unique subsets.

### Step 0: the constant coefficient

Only `G_0` contributes. Its positive and negative subset-sum lists intersect at `0` and `126`. Consequently there are just two possibilities:

- No term from `G_0` is selected.
- Select `F_0={(0,1,2,3),(0,1,3,2),(0,2,1,3),(0,3,1,2)}`.

The signed sum in the second case is exactly

    sum_{p in F_0} f_p
      = -18L -39L^2 -29L^3 -9L^4 -L^5.              (1)

### Step 1: the coefficient of L

If `G_0` was empty, the positive and negative `G_1` subset sums must agree. They intersect only at zero, so `G_1` must also be empty.

If `F_0` was selected, the `G_1` leading coefficient must be `+18`. The positive subset-sum list intersects the negative list shifted by `+18` only at `27`. This uniquely selects

    F_1={(1,2,0,3),(1,3,0,2)},

whose signed sum is

    sum_{p in F_1} f_p
      = 18L +48L^2 +44L^3 +16L^4 +2L^5.

The combined nonempty branch therefore has sum

    sum_{p in F_0 union F_1} f_p
      = 9L^2 +15L^3 +7L^4 +L^5.                    (2)

### Step 2: the coefficient of L^2

For the empty branch, the two `G_2` subset-sum lists intersect only at zero; therefore `G_2` must be empty too.

The branch (2) requires a `G_2` leading sum of `-9`. This would require a positive subset sum to belong to

    {-9,-7,15,17,18,20,42,44},

the negative subset-sum list shifted by `-9`. The positive list has no such element. Hence the nonempty branch is impossible.

After this step, every selected term must lie in `G_3`.

### Step 3: the coefficient of L^3

The two `G_3` subset-sum lists intersect at zero and `21`. Apart from the empty choice, the unique remaining possibility is

    F_3={(3,0,1,2),(3,0,2,1),(3,1,0,2),(3,2,0,1)}.

Its exact signed sum is

    sum_{p in F_3} f_p = 3L^4 +L^5 = L^4(L+3).      (3)

### Step 4: the coefficient of L^4

Equation (3) has coefficient `3`, so this last nonempty possibility is excluded. Only the empty subset remains. This proves the theorem. No condition on the coefficients of `L^5` or `L^6` was needed.

## 2. The exact meet-in-middle certificate

There are twelve even permutations and twelve odd permutations. Write `g_p(L)=product_i(L+i)^{p(i)}`, without its parity sign. Any binary zero relation is exactly an equality between a subset sum of the twelve even `g_p` and a subset sum of the twelve odd `g_p`.

`check.py` generates all `2^12=4096` subset sums on each side using integer coefficient vectors of length seven. It finds precisely one equal pair: the empty subset on both sides. Every possible binary subset of all 24 signed terms is represented by exactly one such pair, so the comparison exhausts the question without enumerating any edge colorings or any larger-size instances.

The checker repeats this comparison after retaining only the first five coefficients, confirming the stronger truncation statement proved above.

An independently constructed comparison uses evaluation vectors at `L=0,1,...,6`, computed directly by integer products rather than polynomial convolution. All polynomials have degree six; equality at seven distinct points is equivalent to polynomial identity. This check again gives only the empty/empty equality.

Finally the checker reproduces the valuation proof and records all surviving partial subsets. Its survivor counts after enforcing coefficients `L^0` through `L^6` are

    2, 2, 1, 2, 1, 1, 1.

The temporary increase from one to two is expected: the `G_3` terms are first introduced at the fourth stage. The final sole survivor is empty.

`results.json` records all 24 signed coefficient vectors, all scalar tables, every valuation-branching survivor, the meet-in-middle counts, and deterministic SHA-256 hashes of the ordered subset-vector arrays. The checker uses only the Python standard library, exact integer arithmetic, and explicit error checks, so disabling Python assertions does not disable validation.

Run both:

    python check.py
    python -O check.py

## 3. Algebraic extension that requires no further enumeration

The same conclusion holds for four equally spaced distinct offsets

    a, a+h, a+2h, a+3h,    h != 0,

and any four consecutive nonnegative integer exponents

    q, q+1, q+2, q+3,    q >= 0.

Indeed, put `z=(L+a)/h`. For every permutation `p`, its signed matching polynomial factors as

    sgn(p) product_i (L+a+hi)^{q+p(i)}
      = [product_i (L+a+hi)^q] h^6 f_p(z).

The bracketed polynomial and `h^6` are common nonzero factors, and an invertible affine substitution preserves whether a polynomial is zero. Thus any binary zero subset in this family would give a binary zero subset in the canonical theorem, which is impossible.

Row and column permutations only relabel the selected terms and introduce a common determinant sign, so they preserve the conclusion when applied consistently. This extension does not include arbitrary unequal gaps or nonconsecutive exponent sets.

## 4. What this does and does not say about fibers

A graph support or a fixed red-edge-count condition chooses a subset of the 24 permutations, with each selected matching appearing once. The theorem excludes cancellation for every such nonempty subset in its stated four-row family. No separate fiber-realizability argument is needed to use this positive result.

Conversely, in settings where a binary zero subset is found, it would not automatically be a graph/color fiber. Being an arbitrary set of permutations and being exactly one level set of a sum of binary edge colors are different conditions. The present computation produced no candidate subset, so it does not settle any general realizability criterion or provide a counterexample to binary fiber noncancellation outside its stated scope.
