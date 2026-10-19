# A first-differing-moment theorem for the equal-halves rectangle

18 October 2026. Local mathematical derivation and exact finite checks. This concerns one structured all-red rectangular family. It is not a theorem about arbitrary binary colorings, an ASNC counterexample, or a novelty claim.

## Theorem

Let n=2r+2, r≥1. Let a_0,…,a_{n−1} be distinct real numbers and e_0,…,e_{n−1} distinct nonnegative integers. Let I,J be original-index-ordered subsets with |I|=r and |J|=r+1. Color exactly I×J red and put

    F(z,λ)=det[z^{1_{i∈I,j∈J}}(λ+a_i)^{e_j}].

Write Arow=(a_i:i∈I), Crow=(a_i:i∉I), X=(e_j:j∈J), Y=(e_j:j∉J), and m=r+1. Use e_k(U) and h_k(U) for the elementary and complete homogeneous symmetric polynomials, with e_0=h_0=1. Let k be the first index for which e_k(X)≠e_k(Y). Such k exists and satisfies 1≤k≤r+1, because otherwise X and Y would be the same root multiset. By Newton's identities this is also the first differing positive power sum.

Define

    D = Σe_j − binom(r,2) − binom(r+2,2),
    H_b = ∏_{h=0}^{b−1} h!,
    A = (−1)^ΣI Δ(Arow)Δ(Crow)/(H_r H_{r+2}),
    K = (−1)^ΣJ Δ(X)Δ(Y),
    δ_k = e_k(Y)−e_k(X),

and, for 0≤l≤r,

    q_l = Σ_{u=0}^l (−1)^u
          e_u(Arow)/(r falling u)
          · h_{l−u}(Crow)/((r+2) rising (l−u)).               (1)

Here falling and rising products of length zero are 1. Then all coefficients above degree D−k+1 vanish and

    [λ^{D−k+1}]F = A K (−1)^{k−1} δ_k q_{k−1}(z−1)^r.     (2)

Equivalently, put Δp_k=Σ_{y∈Y}y^k−Σ_{x∈X}x^k. Newton's identities give (−1)^{k−1}δ_k=Δp_k/k, so the same coefficient is

    [λ^{D−k+1}]F = A K (Δp_k/k) q_{k−1}(z−1)^r.           (2′)

Equation (2) is valid for arbitrary distinct real offsets. It is a candidate first coefficient: q_{k−1} may vanish. If q_{k−1}≠0, every fiber P_t=[z^t]F, t=0,…,r, has exact degree D−k+1 and leading coefficient

    A K (−1)^{k−1+r−t} δ_k q_{k−1} binom(r,t).              (3)

Every t=0,…,r is feasible: for instance, any t chosen rows of I can use t columns of J, the other r−t rows can use Jᶜ, and the unused rows/columns complete a bijection.

### Separated offsets give unconditional nonvanishing in this family

If every offset in Arow is less than every offset in Crow, then q_l>0 for 0≤l≤r. If every offset in Arow is greater than every offset in Crow, then (−1)^l q_l>0. Thus (2) is nonzero, and the exact fiber degree is D−k+1 for any such separated row blocks and any distinct nonnegative integer exponents.

The offsets need not be equally spaced, the exponent order is arbitrary, and the selected exponent sets need not be intervals.

## 1. The weighted column functional

For x=e_p with p∈J put B=J\{p} and

    w_x = (−1)^ΣB Δ(e_B)Δ(e_{Bᶜ}),
    f(T)=∏_{x∈X}(T−x),       g(T)=∏_{y∈Y}(T−y).

Keeping all Vandermondes in original index order gives the exact identity

    w_x/K = −g(x)/f′(x).                                     (4)

One can check the sign by removing x from the X Vandermonde and inserting it into the complementary ordered Y list; the original-index insertion signs give the displayed minus sign.

Let L(P)=Σ_{x∈X} w_x P(x)/K. Since the first k−1 elementary symmetric sums match,

    deg(g−f)=m−k,
    [T^{m−k}](g−f)=(−1)^k δ_k.

Lagrange interpolation at the roots of f implies ΣR(x)/f′(x)=[T^{m−1}]R(T) for every polynomial R of degree at most m−1. Therefore

    L(x^h)=0                   for 0≤h<k−1,
    L(x^{k−1})=(−1)^{k−1}δ_k.                              (5)

In particular L annihilates every polynomial of degree less than k−1.

## 2. A translated minor and its highest dependence on the removed exponent

For a translated minor with M rows b and M exponents U,

    det[(λ+b_i)^{u_j}]
      = Σ_{d_0<…<d_{M−1}}
          det[b_i^{d_h}] det[binom(u_j,d_h)]
          λ^{Σu_j−Σd_h}.                                  (6)

This is finite Cauchy–Binet. Its leading degree is Σu−binom(M,2), with nonzero leading coefficient Δ(b)Δ(U)/H_M.

After dividing a coefficient of correction order h by this leading coefficient, the result is a symmetric polynomial in U of total degree at most h. If the index sequence in (6) corresponds to a partition ν of h, its top homogeneous term is

    s_ν(b) s_ν(U) H_M / ∏_i d_i! .                         (7)

Indeed, replacing falling factorials u^{falling d_i} by their leading monomials gives the usual Schur alternant; all other terms have lower total degree.

For U=X\{x}, symmetric functions are interpreted through

    e_j(X\{x}) = Σ_{v=0}^j (−x)^v e_{j−v}(X).

Thus the degree-h part in x of s_ν(X\{x}) is zero unless ν=(1^h); for that column partition it is (−1)^h x^h. This is the elementary identity s_ν[−x]=(−1)^h s_{ν′}[x], or follows from the Jacobi–Trudi determinant. The factorial ratio for this column is 1/(r falling h).

For U=Y∪{x}, the degree-h part in x of s_ν(Y∪{x}) is zero unless ν=(h); for that row partition it is x^h. Its factorial ratio for a size-r+2 minor is 1/((r+2) rising h).

Consequently, at correction order l of the product of the size-r selected minor and size-r+2 complementary minor, the normalized coefficient is a polynomial in the removed exponent x of degree at most l. Its x^l coefficient is precisely q_l from (1). Summing with weights w_x and applying (5) proves cancellation for l<k−1 and gives (2) for the maximal-size Laplace layer.

## 3. Why smaller Laplace layers cannot interfere

Generalized Laplace expansion is

    F = Σ_{s=0}^r (z−1)^s
        Σ_{R⊆I,B⊆J; |R|=|B|=s}
        (−1)^(ΣR+ΣB) det V[R,B] det V[Rᶜ,Bᶜ].             (8)

For s=r−j its candidate leading degree is D−j(j+2).

We prove a cancellation bound within each such layer. Fix a row subset R. At correction order t in the product of minors, (6) supplies degree sequences α of length s and β of length n−s with respective excesses u and v over their minimal sums, where u+v=t. Summing over B by Laplace expansion produces a determinant whose first s rows are the polynomials binom(e,α_i) supported on J and whose last n−s rows are binom(e,β_i) on all columns. The row-offset alternants are scalar factors and do not affect whether this determinant vanishes.

There are two simple bounds:

- The first s−u values of α are 0,…,s−u−1 whenever u<s. A first deviation at position i forces at least s−i units of total excess.
- max β ≤ n−s−1+v = m+j+v.

If f and g share their first k−1 nonleading coefficients, remainders of any polynomial p of degree d modulo f and g differ by a polynomial of degree at most d−k (and coincide when d<m). To see this, write p=qf+R_f. Then R_g−R_f is q(f−g) modulo g, whose degree before reduction is at most (d−m)+(m−k)=d−k.

Order columns as X,Y and right-multiply each block by its inverse Vandermonde evaluation matrix. The bottom rows become pairs of coefficient vectors (p mod f,p mod g). Suppose

    t≤k−j−2.                                                (9)

Then t≤r−j−1=s−1, since k≤r+1; in particular u≤t<s, so the claimed s−u low-degree top rows do exist. Subtracting suitable combinations of them removes every term of degree below s−u from each bottom remainder difference. The remaining difference is supported in degrees from s−u to at most m+j+v−k, within the m-dimensional remainder space. Hence these differences span a space of dimension at most

    L = max(0,2j+2+t−k) ≤ j.

Each bottom row now lies in the sum of the m-dimensional diagonal subspace {(c,c)} and an at-most-L-dimensional subspace supported in the X block. The rank of all bottom rows is therefore at most m+L≤m+j, less than their number n−s=m+j+1. The determinant vanishes.

Thus the size-(r−j) layer vanishes at every nonnegative correction order t≤k−j−2. At global loss k−1, a smaller layer j≥1 would need

    t=k−1−j(j+2).

If t<0 the layer is already below that degree. Otherwise t≤k−j−2 because j²+j−1≥1, so (9) applies. This proves no smaller layer can contribute at or above D−k+1. More precisely, its first possible global loss is at least

    max(j(j+2), k−1+j(j+1)).                                (9′)

For k=3 in particular, the size-(r−1) layer's candidate term at degree D−3 also vanishes. Its first possible contribution is at degree D−4. Thus when q_2=0, a size-(r−1) contribution at D−3 is not an unavoidable obstruction.

## 4. Positivity for separated offsets

Let M=r+2, and let V=Σ_{b∈Crow} T_b b where T is uniform on the simplex T_b≥0, ΣT_b=1. Its moments satisfy

    E[V^h] = h! h_h(Crow)/(M rising h).

Expanding e_l(V−Arow) gives

    e_l(V−Arow)
      = Σ_{u=0}^l (−1)^u binom(r−u,l−u)e_u(Arow)V^{l−u}.

Therefore

    q_l = E[e_l(V−Arow)]/(r falling l).                      (10)

If Arow<Crow pointwise across the two sets, then V−a>0 for every a∈Arow, and every summand of e_l(V−Arow) is positive. The reverse separation gives sign (−1)^l. This proves the claimed sufficient condition.

The same argument also shows q_l is not the zero polynomial in the offsets. Hence, for each fixed exponent partition, the stated first candidate is nonzero for offsets outside the proper algebraic hypersurface q_{k−1}=0 (in addition to requiring distinctness).

### Closed form for standard consecutive rows

For a_i=i and I={0,…,r−1}, every coefficient in (1) simplifies to

    q_l=(r+1)^l/l!,                0≤l≤r.                  (11)

Consequently the exact leading coefficient in (2′) becomes

    A K (r+1)^{k−1} Δp_k/k! · (z−1)^r.                    (12)

An affine progression a_i=b+ci, c≠0, multiplies q_l by c^l.

Here is an algebraic proof of (11). Let

    U(t)=Σ_{j=0}^r (−1)^j e_j(0,…,r−1)t^j/(r falling j),
    W(t)=Σ_{h≥0} h_h(r,…,2r+1)t^h/((r+2) rising h).

Then q_l=[t^l]U(t)W(t). The divided-difference formula for the exponential on the consecutive nodes r,…,2r+1 gives the exact formal-series identity

    W(t)=e^{rt}((e^t−1)/t)^{r+1}.

For 0≤j≤r, a change of variable u=e^t−1 in coefficient extraction gives

    [t^j] e^t(t/(e^t−1))^{r+1}
      = Res_{t=0} e^t t^{r−j}/(e^t−1)^{r+1} dt
      = [u^r](log(1+u))^{r−j}
      = (r−j)!/r! · [x^{r−j}]x(x−1)…(x−r+1)
      = (−1)^j e_j(0,…,r−1)/(r falling j).

The penultimate equality follows by comparing x^{r−j}u^r in (1+u)^x. Thus U(t) agrees through order r with e^t(t/(e^t−1))^{r+1}. Its product with W agrees through order r with e^{(r+1)t}, proving (11).

## 5. Explicit second-order coefficient and its limitations

If the first two power sums of X and Y agree, then their first two elementary symmetric sums agree. If their third elementary sums differ, k=3 and

    q_2 = e_2(Arow)/(r(r−1))
          + h_2(Crow)/((r+2)(r+3)) − mean(Arow)mean(Crow)
        = 1/2[(mean(Arow)−mean(Crow))²
               − Var(Arow)/(r−1) + Var(Crow)/(r+3)].          (13)

Population variances are used. This locus requires r≥2: two disjoint 2-element exponent sets cannot have matching first two elementary symmetric sums.

In fact q_2>0 whenever mean(Crow) is outside the interval spanned by Arow. Centering Arow at mean(Crow) makes all its entries have one sign, so its e_2 is nonnegative, while the strictly positive variance of Crow supplies the positive remainder in (13).

For a_i=i and I={0,…,r−1}, the variance terms cancel and q_2=(r+1)²/2.

### Standard n=8 example

For r=3, I={0,1,2}, J={0,3,5,6}, a_i=e_i=i,

    X=(0,3,5,6), Y=(1,2,4,7),
    p_1(X)=p_1(Y)=14, p_2(X)=p_2(Y)=70,
    p_3(X)=368, p_3(Y)=416,
    δ_3=16, A=−1, K=291600, q_2=8.

Thus D=15 and

    [λ^13]F=−37324800(z−1)^3.

Each fiber has degree 13, with leading coefficients 37324800, −111974400, 111974400, −37324800 for t=0,1,2,3. Independent exact Cauchy–Binet arithmetic reproduces the coefficient, rather than interpolating the full determinant.

### Distinct offsets can cancel q_2

Take r=2,

    Arow=(−1/√2,1/√2), Crow=(−2,−1,1,2),
    X=(0,4,5), Y=(1,2,6).

All six offsets and all six exponents are distinct. The exponent power sums match at orders 1 and 2: 9 and 41. Their third power sums are 189 and 225, so δ_3=12. Both offset means are zero, Var(Arow)=1/2 and Var(Crow)=5/2, giving q_2=0 exactly.

Therefore the degree-D and degree-(D−1) coefficients vanish by exponent moments, and the degree-(D−2) coefficient also vanishes by row geometry. No unrestricted nonvanishing claim is possible for (2). The parent independently computed the full determinant of this example, obtaining actual degree 7 when D=11; an independent permutation-based check is included in `check_cancellation.py`.

An all-integer version is also available: take Arow=(−5,5), Crow=(−13,−9,9,13), with the same exponent classes. Their variances are 25 and 125, so q_2=0. The independent audit reconstructs the full determinant and obtains exact degree 7 and leading coefficient 37645207142400(z−1)². After adding 13 to all offsets and sorting rows, the equivalent example has nonnegative ordered offsets (0,4,8,18,22,26), I={2,3}, and the same degree and leading coefficient. The complete polynomials are recorded in the audit's `independent-results.json` under `r2_k3_integer_qzero` and its shifted ordered version. These examples demonstrate further cancellation of the candidate coefficient, not a zero fiber.

## 6. Exact verification scope

`check.py` uses only standard-library exact rational arithmetic. For each finite case it computes the maximal-layer coefficients directly from (6), including all degree lists, and compares with (2). Checks raise exceptions under both ordinary and optimized Python. It checks:

- n=8, first one and first two moments equal;
- n=6 with gapped exponents and two equal moments;
- unsorted rational offsets and shuffled exponents;
- n=10 with X=(1,2,10,14,18), Y=(0,4,8,16,17), matching the first four moments; here D=69, q_4=625/24, degree=65 and leading scalar 20071103433434726400000. Direct smaller-layer checks cover size3 corrections t=0,1,2, size2 corrections t=0,1, and size1 correction t=0;
- n=8 with X=(0,7,9,16), Y=(1,4,12,15), matching the first three moments; here D=51, q_3=32/3, degree=48 and leading scalar 118970202193920;
- n=16 with the binary-digit-parity partition of 0,…,15, whose first three moments match and fourth differs. Here k=4,D=63,q_3=256/3, and the exact degree is 60. Smaller-layer leading and first-correction coefficients in the cancellation range (9) are independently summed and are zero.

`check_cancellation.py` independently expands all 6! permutations over Q(√2) for the q_2=0 example and compares the complete bivariate polynomial against the parent's symbolic-determinant output.

The theorem rests on the algebraic proof; these finite calculations are checks, not an enumeration of all colorings or evidence of a general ASNC claim.
