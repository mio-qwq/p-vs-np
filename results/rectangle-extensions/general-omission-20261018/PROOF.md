# Arbitrarily many omitted columns: the all-red rectangle theorem

18 October 2026. Local theorem and proof. This concerns a single all-red rectangle, with a separated-offset unconditional nonvanishing conclusion. It makes no claim about arbitrary colorings or complexity lower bounds.

## The theorem

Use zero-based original row and column indices throughout. Let `r≥1`, `q≥1`, `n≥2r+q`, `|I|=r`, and `|J|=r+q`. Let `a_0,…,a_(n−1)` be distinct real offsets and `e_0,…,e_(n−1)` distinct nonnegative integer exponents. Define

    F(z,Λ)=det[z^(1_(i∈I,j∈J)) (Λ+a_i)^(e_j)].

All lists below retain original index order:

    Arow=(a_i:i∈I), Crow=(a_i:i∉I),
    X=(e_j:j∈J), Y=(e_j:j∉J),
    m=r+q, N=n−r−q, M=n−r=N+q,
    f(T)=∏_(x∈X)(T−x), g(T)=∏_(y∈Y)(T−y),
    ρ_x=g(x)/f′(x), μ_l=Σ_(x∈X)ρ_x x^l,
    D=Σ_j e_j−binom(r,2)−binom(M,2),
    H_b=∏_(i=0)^(b−1)i!,
    A=(−1)^ΣI Δ(Arow)Δ(Crow)/(H_r H_M),
    K=(−1)^ΣJ Δ(X)Δ(Y), ε=(−1)^(q(n−q)).

The weights `ρ_x` are all nonzero. Form the `q×m` Hankel moment matrix

    H^(q)=(μ_(i+j))_(0≤i<q, 0≤j<m).

Its row rank is `q`. Let `b_0<⋯<b_(q−1)` be its greedy column-pivot indices, scanning columns from 0 to `m−1`. Define the partition `θ`, loss `κ`, and nonzero exterior coefficient `γ` by

    θ_(q−j)=b_j−j                 (j=0,…,q−1),
    κ=|θ|=Σ_j b_j−q(q−1)/2,
    γ=det[μ_(i+b_j)]_(0≤i,j<q).

Partition subscripts start at 1. Then `θ_1≤r`, `length θ≤q`, `0≤κ≤qr`, and `γ≠0`.

For a partition `α` of length at most `b`, define

    T_b(α;C)=H_b s_α(C)/∏_(i=1)^b (α_i+b−i)!,

where trailing parts are zero. Let `c_(η,β)^θ` denote the Littlewood–Richardson coefficient in the Schur product `s_η s_β`. Define the explicit finite row factor

    B_θ(Arow,Crow)
      = Σ_(α,β) (−1)^|α| c_(α′,β)^θ
          T_r(α;Arow) T_M(β;Crow),                    (1)

where `|α|+|β|=|θ|`, `length α≤r`, `α_1≤q`, and `length β≤q`. Empty partitions and empty products contribute one.

Every coefficient of `F` above degree `D−κ` in `Λ` vanishes, and

    [Λ^(D−κ)]F(z,Λ)=A K ε γ B_θ(Arow,Crow)(z−1)^r.     (2)

This coefficient identity holds for arbitrary distinct real offsets. Whenever `B_θ≠0`, every fiber `P_t(Λ)=[z^t]F(z,Λ)`, `0≤t≤r`, has exact degree `D−κ` and leading coefficient

    A K ε γ B_θ (−1)^(r−t) binom(r,t).                (3)

If `max Arow<min Crow`, then `B_θ>0`. If `max Crow<min Arow`, then `(-1)^κ B_θ>0`. Thus (2) and every coefficient in (3) are nonzero under either strict separation. This includes standard offsets `a_i=i` with `I={0,…,r−1}`.

The displayed degree is nonnegative: distinct nonnegative integer exponents give `Σe_j≥binom(n,2)`, hence `D≥rM≥rq≥κ`.

At the boundary `n=2r+q`, `deg g=r<m`, so `μ_0=⋯=μ_(q−2)=0` and `μ_(q−1)=1`. Thus the first `q×q` moment block is anti-triangular with nonzero anti-diagonal, giving `θ=∅`, `κ=0`, `γ=(−1)^(q(q−1)/2)`, and `B_θ=1`.

No claim about the later leading degree is made when nonseparated offsets make `B_θ=0`.

## 1. Omitted-set weights and exterior moments

Write `V_ij=(Λ+a_i)^(e_j)`. The generalized Laplace expansion is

    F=Σ_(s=0)^r (z−1)^s L_s(Λ),
    L_s=Σ_(U⊆I,B⊆J; |U|=|B|=s)
        (−1)^(ΣU+ΣB) det V[U,B] det V[Uᶜ,Bᶜ].        (4)

For selected columns `B`, let `Z=X\e_B` and `k=|Z|=m−s`. Define

    w_Z=(−1)^ΣB Δ(e_B)Δ(e_(Bᶜ)).

Then

    w_Z/K=(−1)^(k(n−k)) Δ(Z)²∏_(x∈Z)ρ_x.             (5)

Here is an original-index sign verification. Write the omitted original column indices as `p_i`, their zero-based positions in `J` as `a_i`, and the numbers of `Jᶜ` indices preceding them as `b_i`, so `p_i=a_i+b_i`. Vandermonde deletion and insertion give

    Δ(X\Z)/Δ(X)
      =(−1)^(Σa_i+k(m−k)) Δ(Z)/∏_(x∈Z)f′(x),
    Δ(Y∪Z)/Δ(Y)
      =(−1)^(Σb_i+kN) Δ(Z)∏_(x∈Z)g(x).

The subset-sign quotient contributes `(−1)^Σp_i`; position-dependent signs cancel because their sum is `2Σp_i`. The remaining sign is `(-1)^(k(m−k+N))=(-1)^(k(n−k))`, proving (5).

For symmetric polynomials in `k` variables, set

    E_k(P)=Σ_(Z⊆X, |Z|=k) Δ(Z)²(∏_(x∈Z)ρ_x)P(Z).

Discrete Cauchy–Binet gives, for every partition `ν` of length at most `k`,

    E_k(s_ν)=det[μ_(i+c_j)]_(0≤i,j<k),
    c_j=ν_(k−j)+j.                                    (6)

Indeed, take the evaluation matrices with entries `x^i` and `ρ_x x^c_j`. Their minor product is precisely `Δ(Z)²s_ν(Z)∏ρ_x`. This derivation uses no measure positivity or analytic convergence.

## 2. The unique first surviving shape

For `1≤k≤m`, let `H^(k)` be the first `k` rows and first `m` columns of the infinite moment matrix. Its square case factors as

    H^(m)=V_X diag(ρ_x) V_Xᵀ,
    (V_X)_(i,x)=x^i.

Distinct nodes and nonzero weights make `H^(m)` nonsingular. Thus `H^(k)` has row rank `k`. Let its greedy column-pivot set be

    B_k={b_0^(k)<⋯<b_(k−1)^(k)}.

Any nonzero `k×k` column minor, with ordered column indices `c_0<⋯<c_(k−1)`, satisfies

    c_j≥b_j^(k) for every j.                           (7)

Before column `b_j^(k)` the rank is `j`; hence `j+1` independent chosen columns cannot all precede it. This also covers the infinite matrix because full row rank has already been reached within the first `m` columns.

The correspondence `c_j=ν_(k−j)+j` is a bijection between nonnegative increasing column-index sets and partitions of length at most `k`. Consequently

    κ_k=Σ_j b_j^(k)−k(k−1)/2                           (8)

is the first degree on which `E_k` is nonzero. Its unique surviving Schur shape at that degree is

    θ^(k)_(k−j)=b_j^(k)−j.                             (9)

Indeed, equality of the sums in (7) forces coordinatewise equality. Every Schur polynomial of smaller degree, and every other Schur polynomial at degree `κ_k`, is annihilated. The largest part satisfies

    θ^(k)_1=b_(k−1)^(k)−(k−1)≤m−k.                    (10)

For `k=q` this proves all stated assertions about `θ`, `κ`, and `γ`.

## 3. Translated minors and the maximal-layer coefficient

For a size-`b` minor with offsets `C` and exponents `E`, finite Cauchy–Binet gives

    det[(Λ+c_i)^(e_j)]
      =Σ_(d_0<⋯<d_(b−1))
        det[c_i^(d_v)] det[binom(e_j,d_v)]
        Λ^(Σe_j−Σd_v).                                (11)

The raw leading coefficient is `Δ(C)Δ(E)/H_b`. At correction order `l`, its normalized coefficient is a symmetric polynomial in `E` of total degree at most `l`. Its homogeneous degree-`l` part is

    Σ_(|α|=l, length α≤b) T_b(α;C)s_α(E).              (12)

To see this, put `d_v=v+α_(b−v)`. The offset alternant divided by `Δ(C)` is `s_α(C)`. The binomial alternant divided by `Δ(E)` has degree at most `|α|` and top homogeneous part `s_α(E)/∏_v d_v!`, giving (12).

In the maximal layer `s=r`, the omitted set has size `q`. Substitute `E_selected=X−Z` and `E_complement=Y+Z` in the symmetric-polynomial identities. At correction order `l`, the resulting normalized product is symmetric in `Z` and has total degree at most `l`. Its homogeneous degree-`l` part is

    Q_l(Z)=Σ_(|α|+|β|=l) (−1)^|α|
        T_r(α;Arow)T_M(β;Crow)s_(α′)(Z)s_β(Z),         (13)

with `length α≤r`, `α_1≤q`, and `length β≤q`. This uses the highest-degree-in-`Z` identities

    s_α[X−Z] -> s_α[−Z]=(−1)^|α|s_(α′)(Z),
    s_β[Y+Z] -> s_β(Z).

All discarded terms have smaller total degree in `Z`. More explicitly, express any symmetric exponent polynomial of degree at most `l` in power sums of weighted degree at most `l`; the substitutions `p_j(X−Z)=p_j(X)−p_j(Z)` and `p_j(Y+Z)=p_j(Y)+p_j(Z)` preserve this degree bound. The conditions on `α` and `β` are exactly those for the indicated Schurs not to vanish in `q` variables. Also `M≥q`, so no additional complementary-row length restriction is needed.

Section 2 kills every correction before `κ`, and at correction `κ` retains only the Schur coefficient of `s_θ` in (13). Thus the maximal-layer coefficient is

    [Λ^(D−κ)]L_r=A K ε E_q(Q_κ)
                 =A K ε γ B_θ.                        (14)

The final equality follows directly from the Littlewood–Richardson expansion of (13), giving (1).

## 4. Every lower Laplace layer is strictly below that degree

The size-`s=r−h` layer, `1≤h≤r`, omits `k=q+h` nodes. Its raw degree is

    D_s=Σe_j−binom(s,2)−binom(n−s,2),
    D−D_s=δ_h=h(n−2r+h).                               (15)

For each fixed row subset `U`, the correction-order-`t` coefficient in (4) is a constant times `E_(q+h)(P_t)`, where `P_t` is symmetric of degree at most `t`. This follows from (5) and exactly the degree argument in Section 3, and also applies to `s=0`. It therefore vanishes for `t<κ_(q+h)`.

The key comparison uses only nested row spaces. For any subspace of `R^m`, its row-echelon pivot positions are exactly the possible first nonzero coordinate positions of its nonzero vectors: in a row-echelon basis, the first row with a nonzero coefficient in a linear combination supplies that coordinate. Thus inclusion of row spaces implies inclusion of pivot sets. Since the moment-row spaces nest,

    B_q⊆B_(q+h).                                      (16)

The `h` new pivot indices are distinct nonnegative integers, so their sum is at least `h(h−1)/2`. Using (8),

    κ_(q+h)−κ_q
      =Σ_(b∈B_(q+h)\B_q)b−h(2q+h−1)/2
      ≥−qh.                                           (17)

Consequently

    δ_h+κ_(q+h)−κ
      ≥h(n−2r+h−q)
      ≥h²>0.                                          (18)

No smaller layer can contribute at degree `D−κ` or any higher degree. Equations (14) and (18) prove (2), including its vanishing assertion, for the whole determinant.

## 5. Every separated-offset row factor has a strict sign

Write `D_C=Σ_i∂/∂c_i`. The normalized Schur polynomials satisfy

    D_C T_b(α;C)=Σ_(η=α−one removable box)T_b(η;C).     (19)

For a direct proof, differentiate the alternant formula. The Vandermonde is invariant under common translation. Lowering a numerator exponent by one gives zero when two exponents coincide, which excludes all non-removable boxes. In each remaining term its derivative factor cancels the factorial change.

Work in the formal Schur series in `q` variables `Z`:

    U(Z;Arow)=Σ_(η⊆(r^q)) (−1)^|η|T_r(η′;Arow)s_η(Z),
    W(Z;Crow)=Σ_(length β≤q)T_M(β;Crow)s_β(Z).

Their degree-`l` product is `Q_l`. The one-box Pieri rule and (19) imply

    D_Crow W=s_(1)W,
    D_Arow U=−s_(1)U+E,

where the boundary is

    E=Σ_(η⊆(r^q), η_1=r)
        (−1)^|η|T_r(η′;Arow)s_(r+1,η_2,…,η_q)(Z).     (20)

Terms of length greater than `q` vanish in `q` variables. The only nonvanishing terms excluded by the width bound in `U` are exactly those shown in (20). Therefore

    (D_Arow+D_Crow)(UW)=EW.                            (21)

Every Schur factor from `E` has first row `r+1`. A Schur constituent of a product contains the diagram of each factor, by the Littlewood–Richardson rule. Thus `EW` has zero coefficient in every Schur shape whose first row is at most `r`. Since `θ_1≤r`, (21) proves

    B_θ(Arow+t,Crow+t)=B_θ(Arow,Crow)                   (22)

for all real `t`.

If `max Arow<t<min Crow`, translate by `−t`. In every summand of (1), Schur homogeneity gives

    (−1)^|α|s_α(Arow−t)=s_α(t−Arow).

All entries of `t−Arow` and `Crow−t` are positive. Every Littlewood–Richardson coefficient is nonnegative; the factorial denominators and Schur values are positive for permitted partitions. At least the term `α=∅, β=θ` is strictly positive, since `c_(∅,θ)^θ=1` and `length θ≤q≤M`. Hence `B_θ>0`.

Under reverse separation, negate both offset lists to reach forward separation. The polynomial `B_θ` is homogeneous of degree `κ`, so `B_θ(−Arow,−Crow)=(−1)^κB_θ(Arow,Crow)>0`.

Finally, all target counts `0≤t≤r` are feasible because `|J|=r+q≥r` and `|Jᶜ|=N≥r`. Extracting coefficients from `(z−1)^r` proves (3).

## 6. Reduction to one and two omitted columns

For `q=1`, put `R=g mod f` and `d=deg R`. Lagrange interpolation gives

    μ_l=[T^(m−1)](T^lR mod f).

Its first nonzero value is at `l=m−1−d=r−d`. Thus `θ=(r−d)`, `κ=r−d`, and `γ=lc(R)`. Formula (1) reduces to the one-row sum

    B_(κ)=Σ_(u=0)^κ (−1)^u e_u(Arow)h_(κ−u)(Crow)
              /((r falling u)(M rising (κ−u))).

The sign is `ε=(−1)^(n−1)`, as the general omitted-set identity requires.

For `q=2`, the moment analysis in the preceding two-omission proof yields exactly its two branches:

- If `deg R≤r`, write `d=r−deg R`. The pivots are `(d,d+1)`, the shape is `(d,d)`, `κ=2d`, and `γ=−lc(R)²`.
- If `deg R=r+1`, set `a=lc(R)`, `c=μ_1/μ_0`, and `S=((T−c)R) mod f`. With `κ=r−deg S`, the pivots are `(0,κ+1)`, the shape is `(κ)`, and `γ=a lc(S)`.

The Littlewood–Richardson sum (1) reduces to the earlier rectangular or single-row row factors, and `ε=1`. Thus this theorem genuinely contains the one- and two-omission formulas; it does not merely assume their lower-layer comparisons.


## 7. Exact three-omission certificate with a genuine lower-layer collision

Take

    X=(0,5,6,16,17,22), Y=(1,2,10,12,20,21).

Their monic root polynomials obey `g−f=100800`. Use the sorted union

    e=(0,1,2,5,6,10,12,16,17,20,21,22),
    n=12, r=q=3, I=(0,1,2), J=(0,3,4,7,8,11),
    a_i=i.

The constant remainder gives pivots `(3,4,5)`, shape `θ=(3,3,3)`, `κ=9`, and `γ=−100800³`. The exact row factor and leading degree are

    B_(3,3,3)=590339/600, D=93, D−κ=84.

The resulting coefficient is

    [Λ^84]F
      =349455192072211821543155615882280960000000000 (z−1)^3.

The size-2 layer has raw global loss 7, so its own correction losses 0, 1, and 2 genuinely compete with coefficients above or at the claimed leading degree. Direct translated-minor sums verify that all three vanish; the checker additionally verifies that this size-2 layer first survives at own loss 8, or global loss 15. The size-1 and size-0 raw losses are 16 and 27 and need no further cancellation for this certificate.

The standard-library checker `checker/check_q3.py` computes the actual maximal-layer corrections through loss 9 by (11), before comparing them with the exterior/Schur formula. It also checks the competing lower-layer coefficients; every first-surviving Schur value for omitted counts 1 through 6 by direct node-subset summation; all 42 original-index weight identities for omitted counts 3 through 6; and row-factor translation and reversal. The same sextic pair supplies exact q=1 and q=2 translated-minor regression checks, including their competing smaller layers. Failures raise explicit exceptions even under optimized Python.

Run `python checker/check_q3.py` or `python -O checker/check_q3.py`. Exact inputs and results are recorded in `checker/q3_results.json`. These are supplementary certificates: the theorem for every omission number follows from Sections 1–5.

A second exact q=3 regression uses the prior eleven-node example with the six complementary columns selected. Its moment pivots are `(0,4,5)`, giving the shorter-height shape `(3,3)`, `κ=6`, and omitted-set sign `ε=+1`. Its raw next-layer gap is also 6, and the directly summed collision coefficient vanishes. This independently checks a nonconstant remainder, a target with fewer than q rows, and the parity sign opposite to the compact sextic example. Full inputs and coefficients are in `checker/Q3_CERTIFICATE.md` and the JSON.
