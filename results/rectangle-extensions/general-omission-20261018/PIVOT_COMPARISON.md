# Strict separation of all omitted-column Laplace layers

18 October 2026. This note proves the remaining comparison for arbitrary omission number. It uses only elementary linear algebra; no restriction beyond distinct nodes and nonzero weights is needed for the comparison.

## Statement

Let `m=r+q`, with `r≥1`, `q≥1`, and `n≥2r+q`. Let `x_1,…,x_m` be distinct real numbers and let `ρ_1,…,ρ_m` all be nonzero. Define

    μ_j = Σ_a ρ_a x_a^j,
    E_k(P) = Σ_{Z⊆X, |Z|=k} Δ(Z)² (∏_{x∈Z}ρ_x) P(Z).

For `1≤k≤m`, let `κ_k` be the least degree of a symmetric polynomial in `k` variables on which `E_k` is nonzero. For every `h=1,…,r`,

    h(n−2r+h) + κ_(q+h) − κ_q
      ≥ h(n−2r+h−q)
      ≥ h² > 0.                                      (1)

In particular, every smaller Laplace layer is strictly below the first surviving degree of the maximal layer. The claim applies to `ρ_x=g(x)/f′(x)` because disjoint roots of `f` and `g` give nonzero weights. The degree and real-rootedness of `g` do not enter this comparison.

## 1. Greedy pivots describe the first surviving Schur shape

Let `H_k=(μ_(i+j))_(0≤i<k, 0≤j<m)`. The square matrix `H_m` factors as

    H_m = V diag(ρ_1,…,ρ_m) Vᵀ,
    V_(i,a)=x_a^i.

It is nonsingular. Thus `H_k` has row rank `k`, and its greedy column-pivot set is a `k`-element subset

    B_k={b_0<⋯<b_(k−1)}⊆{0,…,m−1}.

For every partition `λ` of length at most `k`, the exterior moment identity is

    E_k(s_λ)=det[μ_(i+c_j)]_(0≤i,j<k),
    c_j=λ_(k−j)+j.

The indices `c_0<⋯<c_(k−1)` are nonnegative. Conversely every strictly increasing nonnegative index set gives exactly one partition. If its determinant is nonzero, then

    c_j≥b_j for all j.                                (2)

Indeed, before column `b_j` the matrix has rank exactly `j`; `j+1` independent columns cannot all lie before `b_j`. This argument also applies to columns beyond `m−1` in the infinite moment matrix, since the greedy pivots have already attained full row rank within the first `m` columns.

Consequently

    κ_k = Σ_j b_j − k(k−1)/2,                         (3)

and the unique Schur shape surviving at that degree is

    λ^(k)_(k−j)=b_j−j.                                (4)

Uniqueness follows because (2), together with equality of the sums, forces `c_j=b_j` for all `j`. In particular,

    λ^(k)_1=b_(k−1)−(k−1)≤m−k.

All symmetric polynomials of smaller degree are annihilated, since Schur polynomials form a homogeneous basis. At degree `κ_k`, every other Schur polynomial is annihilated.

## 2. Pivot sets nest when the moment-row spaces nest

For any finite-dimensional subspace `W⊆R^m`, its row-echelon pivot indices are exactly the possible positions of the first nonzero coordinate of a nonzero vector of `W`.

To verify this, put a basis of `W` in reduced row-echelon form. Each row realizes its pivot position. In a nonzero linear combination of the rows, the first row with nonzero coefficient supplies its pivot as the first nonzero coordinate; every later row is zero before its own later pivot. Thus no other position occurs.

It follows immediately that `U⊆W` implies inclusion of pivot sets. Since

    rowspace(H_q) ⊆ rowspace(H_(q+h)),

we obtain

    B_q⊆B_(q+h).                                      (5)

This inclusion is not special to Hankel matrices. It holds for the column-pivot sets of any full-row-rank matrix and a matrix obtained by appending independent rows.

Let `C=B_(q+h)\B_q`. It consists of `h` distinct nonnegative integers, so

    Σ_(c∈C)c ≥ 0+1+⋯+(h−1)=h(h−1)/2.                 (6)

Using (3), (5), and (6),

    κ_(q+h)−κ_q
      = Σ_(c∈C)c − [(q+h)(q+h−1)−q(q−1)]/2
      ≥ h(h−1)/2 − h(2q+h−1)/2
      = −qh.                                          (7)

Adding the raw degree gap `δ_h=h(n−2r+h)` proves (1).

## 3. Independent verification using quotient-polynomial degrees

For the original rational-function setting, let `f(T)=∏_(x∈X)(T−x)`, `R=g mod f`, and

    L_f(p)=[T^(m−1)](p mod f),
    U_k=span{R,TR,…,T^(k−1)R} mod f.

Because `R` is a unit modulo `f`, `dim U_k=k` for `k≤m`. The moment rows are the images of these vectors under the map

    Φ(p)=(L_f(p), L_f(Tp), …, L_f(T^(m−1)p)).

If `p≠0` has degree `d<m`, then the first nonzero coordinate of `Φ(p)` is exactly position `m−1−d`, and equals `lc(p)`: the products before that position have degree below `m−1`, and the product at that position has degree exactly `m−1`, without reduction modulo `f`.

Let `D_k` be the distinct leading degrees in a degree-echelon basis of `U_k`. Equivalently, `D_k` is the set of all possible degrees of nonzero vectors of `U_k`. Then

    B_k={m−1−d:d∈D_k},
    κ_k=k(m−1)−k(k−1)/2−Σ_(d∈D_k)d.                 (8)

Nested subspaces give `D_q⊆D_(q+h)`. The `h` new distinct degrees have sum at most

    (m−1)+(m−2)+⋯+(m−h)
      =h(m−1)−h(h−1)/2.

Substitution into (8) again gives (7). Thus the quotient-degree proof and the nested-row-space proof agree exactly.

## Scope

This note proves the comparison and the unique first Schur shape. It does not independently rederive the translated-minor coefficient identity or separated-offset row-factor positivity. Combining those identities with (1) proves that no smaller Laplace layer can change or cancel the maximal-layer first coefficient.
