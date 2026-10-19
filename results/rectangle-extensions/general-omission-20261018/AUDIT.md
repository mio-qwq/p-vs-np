# Independent audit of the arbitrary-omission argument

18 October 2026. This audit checks the mathematical argument in `PIVOT_COMPARISON.md` and the proposed extension of the two-omission translated-minor and separated-row calculations. It concerns the all-red rectangle only.

## Verdict

The proposed generalization is correct. I found no gap in the greedy-pivot argument, the nested-pivot comparison, or the arbitrary-q separated-offset positivity argument. The latter needs the explicit assumption `M >= q`, which follows here from `M=n-r >= r+q`. A general theorem must retain the omitted-set sign `(-1)^(q(n-q))`; its absence from the two-omission maximal-layer formula was special to even q.

The arguments provide a finite, exact algorithm for the surviving shape, rather than a case-by-case classification of every possible shape. Such a classification is not needed for the nonvanishing theorem.

## 1. Greedy pivots and the unique first Schur shape

For distinct nodes and nonzero weights, `H_m=V diag(rho) V^T` is nonsingular, even when the weights have mixed signs. Thus the first k rows have rank k and all greedy pivots occur among columns `0,...,m-1`.

The exterior identity is exactly

    E_k(s_lambda)=det[mu_(i+c_j)],
    c_j=lambda_(k-j)+j,  0<=i,j<k.

There is no extra `k!`: Cauchy-Binet sums unordered k-element column subsets, exactly as the definition of `E_k` does.

If this determinant is nonzero, its first `j+1` columns are independent. A putative `c_j<b_j` would put all of them in a prefix of rank j. Hence `c_j>=b_j` coordinatewise. This remains true for columns extending beyond the finite matrix, because its first m columns already span its full k-dimensional column space.

It follows that

    kappa_k = sum_j b_j - k(k-1)/2,
    lambda^(k)_(k-j)=b_j-j.

Equality of total degrees forces equality of every column index. This proves uniqueness of the first surviving Schur shape, not merely uniqueness of its size. Its first row is at most `m-k`. In particular the maximal-layer shape satisfies `lambda_1<=r`, `length(lambda)<=q`, and `0<=kappa_q<=rq`.

## 2. The nesting claim is valid

For a subspace of a finite coordinate space, the pivot positions of its reduced row-echelon form are precisely the positions that can occur as the first nonzero coordinate of one of its nonzero vectors. In any nonzero row combination, the earliest row with nonzero coefficient supplies the earliest nonzero coordinate; later rows vanish there and at every earlier coordinate.

Consequently inclusion of rowspaces implies inclusion of these pivot sets. This is stronger than monotonicity of prefix ranks and is not a mistaken inference from rank inequalities alone. Applied to the nested moment-row spaces, it gives `B_q subset B_(q+h)`.

If `C=B_(q+h)\B_q`, its h distinct nonnegative indices have sum at least `h(h-1)/2`. Therefore

    kappa_(q+h)-kappa_q >= -qh,
    delta_h+kappa_(q+h)-kappa_q
      >= h(n-2r+h-q) >= h^2 > 0.

The comparison covers every smaller Laplace layer, including the size-zero layer (`h=r`, `k=m`). There is no unhandled boundary case.

The quotient-polynomial verification in `PIVOT_COMPARISON.md` is also correct. For `deg p=d<m`, the first nonzero coordinate of `Phi(p)` occurs at `m-1-d`, before any modular reduction can affect its value. This identifies leading-degree sets with reversed pivot sets exactly.

## 3. General-q normalized-Schur calculation

Let `Z` consist of q variables. For a partition padded to length b, put

    T_b(alpha;B)=H_b s_alpha(B)/product_i(alpha_i+b-i)!.

Common translation differentiation obeys

    D_B T_b(alpha;B)=sum_(eta=alpha minus one removable box) T_b(eta;B).

The factorial normalization is important: it removes the derivative's exponent factor exactly. The identity follows by differentiating the alternant numerator, while the Vandermonde denominator has zero common-translation derivative. It extends to coincident offset entries by polynomial identity.

Write the selected series using `mu=alpha'`:

    U=sum_(length(mu)<=q, mu_1<=r)
          (-1)^|mu| T_r(mu';A) s_mu(Z),
    W=sum_(length(beta)<=q) T_M(beta;C) s_beta(Z).

These are formal graded series; every coefficient used below is a finite sum. `U` is actually finite. The condition `M>=q` makes every displayed `T_M` valid.

Pieri's rule gives the exact identities

    D_C W=s_(1)(Z) W,
    D_A U=-s_(1)(Z) U+E,

where the entire error series is

    E=sum_(length(mu)<=q, mu_1=r)
          (-1)^|mu| T_r(mu';A)
          s_(r+1,mu_2,...,mu_q)(Z).

The sign in E is positive relative to the existing coefficient of `s_mu` in U. This is because E cancels the forbidden width-r+1 additions contained in `-s_(1)U`. Additions producing length q+1 vanish in q variables. No other boundary exists. For W, there is no width cutoff; its only length boundary likewise vanishes in q variables.

Thus

    (D_A+D_C)(UW)=EW.

Every partition occurring in E has first row r+1. The containment condition of the Littlewood-Richardson rule says that a partition appearing in its product with `s_beta` contains that partition, and hence has first row at least r+1. Specializing to q variables only discards overlength shapes; it does not turn them into narrower shapes.

It follows for every target `lambda` with `length(lambda)<=q` and `lambda_1<=r` that

    B_lambda(A,C)=[s_lambda](UW)
    B_lambda(A+t,C+t)=B_lambda(A,C).

This proves the required common-translation invariance independently of the exponent functional and without assuming its nonvanishing.

## 4. Strict positivity and reverse-separation sign

If `max A<t<min C`, translate by `-t`. Homogeneity gives

    (-1)^|alpha| T_r(alpha;A-t)=T_r(alpha;t-A).

The exact cancellation-free expression is therefore

    B_lambda(A,C)
      =sum_(alpha,beta) c_(alpha',beta)^lambda
          T_r(alpha;t-A) T_M(beta;C-t),

where `length(alpha)<=r`, `alpha_1<=q`, `length(beta)<=q`, and the Littlewood-Richardson coefficient forces `|alpha|+|beta|=|lambda|`.

All summands are nonnegative: the LR numbers are nonnegative integers, all factorial denominators are positive, and the Schur arguments are strictly positive with valid partition lengths. The summand `alpha=empty`, `beta=lambda` has LR coefficient one and equals `T_M(lambda;C-t)>0`. Thus `B_lambda>0`.

Under reverse separation the same argument gives the constant sign `(-1)^|lambda|`. Indeed after translation selected variables are positive and complementary variables negative; each nonzero summand acquires `(-1)^(|alpha|+|beta|)=(-1)^|lambda|`.

Neither proof requires distinct offsets within each list; distinctness is needed in the full theorem to make its exterior Vandermonde prefactor nonzero. With nonseparated offsets, B can vanish, and no later-degree claim follows from this argument.

## 5. Combining with the translated minors: signs and degree bounds

For a translated size-b minor, the normalized coefficient at correction order l is symmetric in its exponent alphabet of total degree at most l. Its top homogeneous part is `sum_(|alpha|=l) T_b(alpha;B)s_alpha(E)`. This follows from the binomial alternant, not from an assumption about the exponent nodes.

For the maximal layer, replacing the two exponent alphabets by `X-Z` and `Y+Z` produces a polynomial in Z of degree at most l. Its homogeneous degree-l part is exactly `[degree l](UW)`, because

    top_Z s_alpha[X-Z]=s_alpha[-Z]=(-1)^|alpha|s_(alpha')(Z),
    top_Z s_beta[Y+Z]=s_beta(Z).

These are identities of symmetric functions in virtual alphabets; they apply to the omitted subsets after evaluation. Lower exponent-homogeneous terms cannot contribute degree l in Z.

Thus the exact coefficient at first loss `kappa_q` is

    A K (-1)^(q(n-q)) gamma B_lambda (z-1)^r,

where

    gamma=E_q(s_lambda)=det[mu_(i+b_j)] != 0,
    A=(-1)^sum(I) Delta(Arow)Delta(Crow)/(H_r H_M),
    K=(-1)^sum(J) Delta(X)Delta(Y).

The sign `(-1)^(q(n-q))` comes from the omitted-set Vandermonde identity and must be retained in a general-q statement. There is no additional sign from reversing the partition indices: the displayed increasing column indices already match the ordinary Schur alternant convention.

For each smaller layer with `k=q+h` omitted nodes, the same degree bound annihilates corrections below `kappa_k`. The strict comparison in Section 2 puts its first possible coefficient below `D-kappa_q`. This proves the assertion for the full determinant, rather than only for its maximal layer.

Finally, `D-kappa_q` cannot be a negative formal degree under the stated distinct nonnegative integer exponent assumption. Distinctness gives `sum e_j>=binom(n,2)`, hence `D>=rM`, while `kappa_q<=rq<=rM`.

## 6. Useful consistency checks and limitations

- At the boundary `n=2r+q`, `g` is monic of degree r, the first nonzero scalar moment is `mu_(q-1)=1`, and `lambda=empty`, `kappa_q=0`, `gamma=(-1)^(q(q-1)/2)`. For q=2 this gives the earlier gamma=-1.
- If R is a nonzero constant, the first shape is the rectangle `(r^q)`, the loss is rq, and `gamma=(-1)^(q(q-1)/2)R^q`.
- The pivot comparison itself needs only distinct nodes and nonzero weights. Real-rootedness and nonnegative integer exponents enter elsewhere in the determinant problem, not in this comparison.
- The old two-omission proof's final sentence saying that three or more omissions require a separate first-shape classification is superseded by the general pivot argument. It should not be copied into the new theorem as a remaining obstruction.
- No conclusion about arbitrary colorings, novelty, computational complexity, or later leading coefficients in the nonseparated vanishing case follows from this audit.

The audit is algebraic; it does not claim an independent numerical checker run.

## 7. Final integrated-proof review

I separately read the finished `PROOF.md` after its assembly. Its theorem statement and Sections 1–6 integrate the ingredients correctly. In particular:

- The general sign is now explicitly `epsilon=(-1)^(q(n-q))`, occurs exactly once in the maximal-layer coefficient, and is carried consistently into every fiber's leading coefficient.
- The finite row-factor sum has all necessary partition restrictions. `M>=q` follows from the theorem's dimension assumption and is explicitly used both in the translation identity and in the strictly positive empty-alpha summand.
- The translated-minor argument has the correct normalization. For full explicitness about the omitted-variable degree bound, any symmetric polynomial of exponent degree at most l can be expressed over the rationals in power sums of weighted degree at most l. Substituting `p_j(X-Z)=p_j(X)-p_j(Z)` and `p_j(Y+Z)=p_j(Y)+p_j(Z)` preserves this bound. This supplies the formal justification for the degree assertion already made in Section 3; it is not an additional hypothesis.
- The size-zero layer is valid under the stated empty-product convention: its selected minor is 1, and the complementary minor is the full determinant. Equivalently, `k=m`, the exterior functional is a single nonzero weighted evaluation at `Z=X`, `kappa_m=0`, and the greedy pivots are `0,...,m-1`. Its raw loss is `rM`, exceeding `kappa_q` by at least `r^2`, since `kappa_q<=rq` and `M>=r+q`. Thus it requires neither a positive-sized selected minor nor a separate cancellation assumption.
- For q=1, the first moment index is `r-deg R`, the coefficient is `lc(R)`, the LR sum forces `alpha=(1^u)` and `beta=(kappa-u)`, and the sign `(-1)^(n-1)` is correct.
- For q=2 and `deg R<=r`, the first two independent columns really are `(d,d+1)`, because the first nonzero moment is at `d+1`. This gives `(d,d)` and the negative square. In the other branch, column 0 is nonzero and the first independent column is `kappa+1`, giving `(kappa)` and `a lc(S)`. Both reductions include their zero-loss boundary cases, and epsilon is 1.

Final verdict: the finished integrated proof is mathematically sound as written. No repair to `PROOF.md` is required by this audit. The separate exact q=3 checker and certificate were not executed or re-audited here; this verdict rests on the general algebraic proof.
