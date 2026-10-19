# A sharp three-row boundary for column-certificate closure

19 October 2026. Local exact result. This note refutes a weighted closure principle, classifies its smallest examples, and proves a limited closure statement. It does not refute full-background one-column nonnegative-kernel exclusion, binary sparse noncancellation, or any P-versus-NP assertion.

## Results first

1. A positive-functional certificate for a full translated-power background does **not** generally survive one binary mask in another column, even if a new functional may be chosen. At canonical offsets and exponents `(0,1,2)`, one deleted entry suffices to create a strictly positive kernel for the second column.
2. This failure is minimal in matrix size and admits a complete three-row classification. For exponents `(0,1,2)` and arbitrary ordered distinct offsets, the nonnegative relation cone of the six signed matching polynomials is exactly one explicit ray.
3. The classification also gives a genuine limited closure theorem: keep the exponent-zero column full, and arbitrarily nonnegative-weight the other two columns. Every feasible matching support still has a nonzero determinant.
4. No nonzero binary vector belongs to the relation ray. Thus the weighted counterexample is not a binary-mask or binary-color fiber counterexample. In fact every nonempty subset of the six signed matching polynomials has a nonzero sum in this three-row consecutive-exponent setting.

The distinction matters for the proposed bridge: coefficient-space LP positivity excludes **all nonnegative** relations. Binary noncancellation asks to exclude a much smaller set of relations. The stronger LP invariant already fails after one binary column mask.

## 1. The explicit closure obstruction

Use canonical offsets `a=(0,1,2)`, exponents `e=(0,1,2)`, and write `t=L+1`. The full matrix is

    V(t) = [[1, t-1, (t-1)^2],
            [1, t,   t^2],
            [1, t+1, (t+1)^2]].

For column `c`, let `T^(c)_i` be its signed entry-times-cofactor polynomial. The full-background columns give

    c=0: (t^2+t,       2-2t^2, t^2-t),
    c=1: (-2t^2+t+1,   4t^2,   -2t^2-t+1),
    c=2: (t^2-2t+1,   -2t^2,   t^2+2t+1).

Here are exact positive-functional certificates, each sending all three corresponding polynomials to one:

    phi_0(f) = [t^2]f + (3/2)[t^0]f,
    phi_1(f) = (1/4)[t^2]f + (3/2)[t^0]f,
    phi_2(f) = -(1/2)[t^2]f + (3/2)[t^0]f.

Consequently every nonzero nonnegative weighting of any one column of the full background has a nonzero determinant.

Now mask column zero by `u=(1,0,1)`. This only deletes its middle entry. The determinant with all other entries unchanged is `2t^2`, hence is nonzero. In this masked background, the column-one signed entry-times-cofactor polynomials become

    S_0=t^3-t^2,    S_1=4t^2,    S_2=-t^3-t^2.

They satisfy the strict positive relation

    2 S_0 + S_1 + 2 S_2 = 0.                         (1)

All three polynomials are nonzero. The numbers of perfect matchings using their distinguished entries are respectively `(1,2,1)`, so no entry is merely unsupported by a perfect matching.

Equation (1) proves that **no** linear functional can be strictly positive on all three `S_i`. This is stronger than showing that the old functional fails. In the finite alternative of the preceding column-kernel note, the exact normalized primal certificate is `(2/5,1/5,2/5)`.

Equivalently, nonnegative weighting `v=(2,1,2)` of column one gives

    det [[1, 2(t-1), (t-1)^2],
         [0, t,       t^2],
         [1, 2(t+1), (t+1)^2]] = 0.                 (2)

The support has four perfect matchings. Weighting column one by `v` in the **full** background instead gives `4-4t^2`, which is nonzero. Thus both operations separately preserve noncancellation; their composition need not.

There is also a second-column-two variant: after the same first mask, weighting column two by `(1,2,1)` makes the determinant zero.

## 2. The complete nonnegative relation cone

Let the offsets satisfy `a_0<a_1<a_2`, put

    h=a_1-a_0>0,    k=a_2-a_1>0,    t=L+a_1,
    x_0=t-h,       x_1=t,          x_2=t+k.

For exponents `(0,1,2)`, name the six signed matching polynomials in this order:

    A: permutation (0,1,2),  +x_1 x_2^2;
    B: permutation (0,2,1),  -x_2 x_1^2;
    C: permutation (1,0,2),  -x_0 x_2^2;
    D: permutation (2,0,1),  +x_2 x_0^2;
    E: permutation (1,2,0),  +x_0 x_1^2;
    F: permutation (2,1,0),  -x_1 x_0^2.

Permutations list the column chosen in each row. Let the corresponding nonnegative coefficient vector be `(A,B,C,D,E,F)`; the same letters now denote coefficients, not the displayed polynomials.

**Theorem 1.** The sum of these six signed polynomials with nonnegative coefficients is identically zero if and only if

    (A,B,C,D,E,F)
      = lambda (h^2, h(h+k), 0, 0, k(h+k), k^2),
    lambda>=0.                                      (3)

**Proof.** At `t=0`, the sum equals

    h k^2 C + h^2 k D.

Both terms are nonnegative, so an identity forces `C=D=0`. The remaining sum is `t` times

    A(t+k)^2 - B t(t+k) + E t(t-h) - F(t-h)^2.

Its three coefficient equations are

    k^2 A-h^2 F=0,
    2k A-k B-h E+2h F=0,
    A-B+E-F=0.                                      (4)

Write `A=lambda h^2`. The first equation gives `F=lambda k^2`. Solving the other two gives `B=lambda h(h+k)` and `E=lambda k(h+k)`. Conversely these values make every coefficient zero. Nonnegativity is equivalent to `lambda>=0`. This also handles `A=0`, when all four remaining coefficients vanish. QED.

This proof establishes the whole cone, not only one relation found by numerical search.

## 3. Exactly which two-column weightings cancel

For a nonnegative weight mask, its support consists of entries with strictly positive weights. A feasible support means that at least one perfect matching has a positive weight product.

Theorem 1 gives all possible zero determinants for two independently weighted columns, with the remaining column full. Positive scaling of either weighted column does not affect whether its determinant is zero.

### 3.1 Columns zero and one weighted

Let `u` weight column zero and `v` weight column one. Then

    (A,B,C,D,E,F)
      =(u_0 v_1, u_0 v_2, u_1 v_0, u_1 v_2,
        u_2 v_0, u_2 v_1).

For a feasible support, the determinant is identically zero **if and only if**, for some `p,q>0`,

    u=p(h^2,0,k^2),
    v=q(h(h+k),hk,k(h+k)).                           (5)

Indeed (3) requires `A,B,E,F>0`, making `u_0,u_2,v_0,v_1,v_2` positive. Then `C=D=0` forces `u_1=0`. Ratios in (3) give

    u_2/u_0=k^2/h^2,
    v_0/v_1=(h+k)/k,    v_2/v_1=(h+k)/h,

which are exactly (5). Substitution proves sufficiency. Degenerate cases do not disappear through division: if the relation scalar is zero, all matching products vanish, contrary to feasible support.

In particular, a binary first mask can create this weighted kernel precisely when `h=k`, in which case its nonzero entries are `(1,0,1)` and the second weights are proportional to `(2,1,2)`.

### 3.2 Columns zero and two weighted

Let `u` weight column zero and `v` weight column two. Then

    (A,B,C,D,E,F)
      =(u_0 v_2, u_0 v_1, u_1 v_2, u_1 v_0,
        u_2 v_1, u_2 v_0).

For a feasible support, the determinant is identically zero **if and only if**, for some `p,q>0`,

    u=p(h,0,k),    v=q(k,h+k,h).                      (6)

As before the four positive matching products force `u_1=0`; their ratios give `u_2/u_0=k/h`, `v_0/v_2=k/h`, and `v_1/v_2=(h+k)/h`. These are (6), and direct substitution suffices.

### 3.3 Columns one and two weighted: a genuine closure case

Keep column zero full, weight column one by `u` and column two by `v`. Then

    (A,B,C,D,E,F)
      =(u_1 v_2, u_2 v_1, u_0 v_2, u_2 v_0,
        u_0 v_1, u_1 v_0).

**Theorem 2.** Every feasible support has a nonzero determinant for arbitrary nonnegative `u,v`.

**Proof.** A feasible zero would require the nonzero ray (3), so `A,F>0` imply `u_1,v_0,v_2>0`. Conditions `C=D=0` then force `u_0=u_2=0`. But this makes `B=E=0`, contradicting their strict positivity in (3). QED.

This is a closure result with a stated invariant, not an iteration rule for higher dimension. In the three-row setting, two nonconstant columns may be masked independently while the constant column stays full.

## 4. Binary fibers and why the obstruction does not transfer

No nonzero vector in (3) is binary. In a nonzero binary vector, its four positive coordinates would all equal one, whereas

    B/A=(h+k)/h>1.

Consequently **every nonempty subset** of the six signed matching polynomials has a nonzero sum. A sparse binary matrix, or a single color-count fiber of it, selects such a subset. Therefore all such fibers are nonzero for three rows, arbitrary distinct ordered offsets, and exponents `(0,1,2)`.

This includes both two-column binary masks and arbitrary three-by-three binary supports/colorings. It is a finite-dimensional theorem; it does not establish arbitrary-size ASNC. The weighted coefficients `(1,2,0,0,2,1)` in the canonical obstruction are not the indicator of a matching fiber. Treating them as binary multiplicities through a gadget would require a separate determinant-preserving construction with the prescribed offsets and exponents. None is supplied or assumed.

The same statements hold for consecutive exponents `(r,r+1,r+2)`, `r>=0`: factor the nonzero polynomial `product_i x_i^r` from the determinant. Arbitrary row or column permutations change only a common determinant sign after the offsets/exponents and weight positions are relabeled consistently.

## 5. Minimality and the precise failed implication

For one or two rows there is no nonnegative weighted zero determinant with a feasible support, for arbitrary distinct offsets and distinct nonnegative integer exponents. The one-row assertion is immediate. For two rows, the determinant is

    alpha (L+a_0)^e_0 (L+a_1)^e_1
      - beta (L+a_0)^e_1 (L+a_1)^e_0,
    alpha,beta>=0.

If just one matching product is positive, this is nonzero. If both are positive, identity would make `((L+a_1)/(L+a_0))^(e_1-e_0)` constant, impossible because the offsets and exponents are distinct. Thus the three-row obstruction is minimal for feasible nonnegative weighted cancellation.

The failed implication is:

    full-background one-column positive certificates
       => positive certificates after a binary mask in another column.

It fails even when every new distinguished entry extends to a perfect matching, and even when the second-column weights causing failure are all strictly positive. Replacing the old coefficient functional by an arbitrary new one cannot repair this implication: the strictly positive relation (1) forbids every such functional.

The original full-background one-column conjecture remains untouched. The binary sparse noncancellation question also remains untouched in general dimension. The arbitrary-omission rectangle theorem has different hypotheses and is neither contradicted nor iterated here.

## 6. Verification and scope

`check.py` is a standard-library exact checker with explicit exceptions, not Python `assert` statements. It reconstructs all signed matching polynomials and column Laplace contributions, checks the three full-background certificates, both weighted cancellations and their separate nonzero determinants, all seven nonempty binary subsets of the new column contributions, the general relation identities, and bounded exhaustive nonnegative integer masks against the complete classification. It also tests every nonempty subset of the six matching polynomials at several positive rational gaps.

Run `python check.py` and `python -O check.py`. Its finite tests support the exact written certificates; the universal three-row statements follow from Theorems 1 and 2 and the ratio arguments. No remote files, PRs, merges, tags, or releases were changed by this task.
