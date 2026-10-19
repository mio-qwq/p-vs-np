# A separated all-red rectangle plus one disjoint red entry

19 October 2026. Local structural cancellation result. This proves a genuinely nonrectangular family and identifies the remaining leading-order boundary obstruction. It makes no claim about arbitrary binary colorings, P versus NP, or complexity lower bounds.

## 1. Setup and exact identity

Use zero-based original indices. Let `r≥1`, `q≥1`, `n≥2r+q`, `|I|=r`, `|J|=r+q`, and choose `p∉I`, `c∉J`. All offsets `a_i` are distinct real numbers and all exponents `e_j` are distinct nonnegative integers. Assume either

    max_(i∈I) a_i < min_(i∉I) a_i,

or the reverse strict separation. Write `V_ij=(Λ+a_i)^(e_j)`. The original and new determinants are

    F_R(z,Λ)=det[z^(1_(i∈I,j∈J)) V_ij],
    F_+(z,Λ)=det[z^(1_((i,j)∈(I×J)∪{(p,c)})) V_ij].

These are actual binary red/blue colorings: the added entry is blue before the change, and the two red sets are disjoint. Put `w=z−1`. Let `F_−` be the determinant obtained from the rectangle matrix by deleting row `p` and column `c`, retaining the order of every surviving row and column. Multilinearity at the changed entry gives the exact polynomial identity

    F_+ = F_R + w (Λ+a_p)^(e_c) (−1)^(p+c) F_−.       (1)

There is no evaluation or division in this identity. Its cofactor is independent of the changed entry.

Every target `0≤t≤r+1` is feasible. For `t=r+1`, use the added edge and match all `I` rows into `J`. For `0≤t≤r`, do not use the added edge: match `t` rows of `I` into `J`, the other `r−t` rows of `I` into `Jᶜ`, and row `p` into a remaining column of `J`. This is possible since `|Jᶜ|=N≥r` and `|J|−t≥q≥1`. All residual rows can be matched arbitrarily to residual columns, since they have no red entries left. No target outside `0,…,r+1` is feasible.

We use the audited all-red rectangle theorem included as `../general-omission-20261018/PROOF.md`, and its explicitly proved maximal-layer and moment lemmas. Write

    m=r+q, N=n−r−q, M=n−r,
    D=Σ_j e_j−binom(r,2)−binom(M,2).

For the original rectangle let `κ` be its moment-pivot loss and `C_R≠0` its complete leading constant, so

    [Λ^(D−κ)] F_R = C_R w^r.                         (2)

All higher Λ-coefficients vanish. Separation ensures `C_R≠0`.

## 2. Main theorem with one row of slack

**Theorem A.** If `n≥2r+q+1`, all `r+2` feasible fibers `[z^t]F_+`, `0≤t≤r+1`, are nonzero. They have one common exact degree

    L = D+M−1−κ_−,                                  (3)

where `κ_−` is the pivot loss for the deleted rectangle. If `C_−≠0` is the complete leading constant of that rectangle, with signs computed in its retained row/column order, then

    [Λ^L]F_+ = (−1)^(p+c) C_− (z−1)^(r+1),          (4)
    [Λ^L z^t]F_+
      = (−1)^(p+c+r+1−t) C_− binom(r+1,t).           (5)

The edge term dominates the original by at least `N−1≥r` degrees:

    L−(D−κ) = M−1+κ−κ_− ≥ N−1 ≥ r > 0.             (6)

### Proof

The deleted determinant has size `n−1`, the same `r`, `q`, and `J`, and complementary offsets with just `a_p` removed. Thus `(n−1)≥2r+q` and the strict row separation is preserved. The rectangle theorem applies without any transformed offsets or exponents. Its raw degree is

    D_−=Σ_j e_j−e_c−binom(r,2)−binom(M−1,2)
       =D+M−1−e_c.

Hence multiplying it by `(Λ+a_p)^(e_c)` produces exact degree (3), and its leading coefficient is `C_−w^r`.

It remains to prove the loss comparison

    κ_−≤κ+q.                                        (7)

Let `X=(e_j:j∈J)`, `Y=(e_j:j∉J)`, `y=e_c`, and

    f(T)=∏_(x∈X)(T−x),
    g(T)=∏_(v∈Y)(T−v),
    g_−(T)=g(T)/(T−y),
    ρ_x=g(x)/f′(x), ρ_x^−=g_−(x)/f′(x).

The distinctness assumptions make all weights nonzero, and

    ρ_x=(x−y)ρ_x^−.

For a symmetric polynomial `P` in `q` variables, use the exterior moment functionals

    E_q(P)=Σ_(Z⊆X,|Z|=q) Δ(Z)^2(∏_(x∈Z)ρ_x)P(Z),
    E_q^−(P)=Σ_(Z⊆X,|Z|=q) Δ(Z)^2(∏_(x∈Z)ρ_x^−)P(Z).

Then exactly

    E_q(P)=E_q^−( [∏_(x∈Z)(x−y)] P(Z) ).             (8)

The rectangle pivot lemma says that `E_q` first survives in symmetric degree `κ`, on a Schur polynomial `s_θ` with `E_q(s_θ)=γ≠0`; likewise `E_q^−` annihilates all symmetric polynomials of degree strictly less than `κ_−`. In (8), take `P=s_θ`. The argument on the right has total degree `κ+q`, and its evaluation is nonzero. Therefore `κ_−≤κ+q`, proving (7). Substitution yields (6). Thus no term of `F_R` can cancel the highest edge coefficient, and (1) yields (4)–(5). ∎

This proof requires neither positivity of the moment weights nor any unproved monotonicity of pivot positions under deletion.

## 3. Tight boundary with at least two rectangle rows

**Theorem B.** If `n=2r+q` and `r≥2`, every feasible fiber is still nonzero. The zero-red fiber has exact degree `D`, and the other `r+1` fibers have exact degree

    L=D+r−1.

There is a nonzero constant `C_*` such that

    [Λ^L]F_+ = (−1)^(p+c) C_* z(z−1)^r,              (9)
    [Λ^L z^t]F_+
      = (−1)^(p+c+r+1−t) C_* binom(r,t−1)
        for 1≤t≤r+1.                                (10)

The zero-red fiber is exactly the original zero-red fiber, not merely asymptotically equal to it.

### The deleted rectangle's boundary leading term

The prior whole-rectangle theorem does not directly apply to `F_−`, whose size is one below its stated threshold. We instead use the prior proof's maximal-layer calculation and bound the remaining layers explicitly.

Here `|X|=r+q`, `|Y\{y}|=r−1`, and `M_−=r+q−1`. Lagrange interpolation gives

    μ_l^−=0 for 0≤l<q,   μ_q^−=1.

In the first `q` moment rows, column zero is zero; columns `1,…,q` form an anti-triangular nonsingular matrix. The pivot indices are therefore `1,…,q`, and

    θ_−=(1^q),  κ_−=q,
    γ_−=(−1)^(q(q−1)/2).                              (11)

The maximal-layer formula of the prior proof applies because `M_−≥q`; that derivation only needs this inequality, not the stronger whole-theorem threshold. Its leading constant is

    C_* = A_− K_− ε_− γ_− B_(1^q)(Arow,Crow\{a_p}),  (12)

using the same definitions as the rectangle theorem in the surviving index order, with `ε_−=(−1)^(q((n−1)−q))`. The row-factor sign proof also needs only `M_−≥q` and `θ_1≤r`, so separation makes `C_*≠0`. The maximal layer first survives at degree `D_−−q`.

For the `s=r−h` layer, the raw degree loss relative to `D_−` is

    δ_h=h((n−1)−2r+h)=h(q−1+h).

If `h≥2`, then `δ_h>q`, so even its raw degree is below `D_−−q`. If `h=1`, `δ_1=q`; that layer can tie, but cannot appear above the claimed degree. Thus, at the largest possible degree, the full minor is

    [Λ^(D_−−q)]F_− = C_*w^r + C_1 w^(r−1).

It is impossible to obtain zero red edges in `F_−`: its `r` rows in `I` have just `r−1` blue columns. Consequently `F_−(0,Λ)=0` identically. Evaluating the displayed highest coefficient at `z=0`, namely `w=−1`, gives `C_1=C_*`. Hence

    [Λ^(D_−−q)]F_− = C_*z(z−1)^(r−1).               (13)

The polynomial on the right is nonzero. There are no higher coefficients, by the preceding layer bounds.

### Completing Theorem B

The original rectangle is at its own threshold, so `κ=0` and its exact degree is `D`. The edge term's exact degree is

    e_c+D_−−q=D+M−1−q=D+r−1.

For `r≥2` this strictly exceeds `D`, proving (9)–(10). At `z=0`, identity (1) and `F_−(0,Λ)=0` give `F_+(0,Λ)=F_R(0,Λ)`, a nonzero polynomial of degree `D`. ∎

## 4. The remaining one-row, tight-boundary leading obstruction

Suppose `r=1`, `n=q+2`, and write `I={i}`. Formula (13) remains valid, now with leading polynomial `C_*z`; but the edge term and the original have equal degree `D`. Put

    C_E=(−1)^(p+c)C_*.

Their combined leading polynomial is

    [Λ^D]F_+=(z−1)(C_R+C_E z).                        (14)

Thus the zero-red and two-red fibers are nonzero; their leading coefficients are `−C_R` and `C_E`. The one-red leading coefficient is `C_R−C_E`, and can genuinely vanish.

Its exact offset-dependent ratio is

    C_E/C_R
      =∏_(s∉{i,p}) (a_s−a_i)/(a_s−a_p).              (15)

To verify this ratio, the one-column shape row factor in (12) reduces to

    B_(1^q)(a_i,C')
      =Σ_(u=0)^q (−a_i)^u e_(q−u)(C')/q!
      =∏_(s∈C')(a_s−a_i)/q!,

where `C'` is the list of offsets other than `a_i,a_p`. The Vandermonde deletion ratio, the external cofactor sign, and the original/minor index signs cancel to leave (15); also `H_(q+1)/H_q=q!`. All exponent factors cancel, so (15) is independent of the choice of distinct exponents.

Consequently, if the product in (15) differs from one, all three fibers have exact degree `D`. The equality case is a precise obstruction to proving the one-red fiber nonzero merely by gluing the two leading rectangle coefficients. We make no universal assertion about the later degree of that fiber in the equality case.

A concrete separated equality case is

    n=4, r=1, q=2,
    a=(0,1,2,3), I={0}, p=3,
    e=(0,1,2,3), J={0,1,2}, c=3.

Here the product in (15) is `(1·2)/((1−3)(2−3))=1`. Direct exact expansion gives

    [z^0]F_+ = −2Λ^3,
    [z^1]F_+ = −18Λ^2−54Λ−42,
    [z^2]F_+ = 2(Λ+3)^3.

The one-red fiber is nonzero in this certificate, but loses its predicted degree-three term. This is a genuine leading-coefficient cancellation, not an infeasible target or an offset-separation failure.

## 5. Exact finite certificates and reproducibility

`checker/check.py` computes the determinant by signed permutation expansion over integer polynomial arithmetic, independently of the cofactor identity and the moment formula. It tests:

1. A positive-loss original rectangle: `n=6,r=2,q=1`, offsets `(0,1,2,3,4,5)`, exponents `(0,1,2,4,5,6)`, `I={0,1}`, `J={0,3,4}`, added edge `(5,5)`. The exponent root polynomials satisfy `g−f=−12`, hence `κ=2`, and the original leading polynomial is `21600(z−1)^2` at degree 9. The minor has `κ_−=0`, and the new leading polynomial is `20(z−1)^3` at degree 14. This checks a genuine original cancellation before the new-edge dominance argument.
2. The tight boundary `r=2,q=1,n=5`, standard offsets/exponents, `I={0,1}`, `J={0,1,2}`, added edge `(4,4)`. The zero-red fiber has degree 6 and leading coefficient 2; the other fibers have degree 7 with leading polynomial `−4z(z−1)^2`. The deleted minor has the required leading tie `−4z(z−1)`.
3. The one-row obstruction above, including all three exact fiber polynomials.

All runs check the full polynomial cofactor identity, actual binary colors, feasibility of every asserted target, and equality of the independently expanded determinants. Failures raise exceptions even under optimized Python. Run `python checker/check.py` or `python -O checker/check.py`; exact outputs are saved to `checker/results.json`.
