# Independent audit: partial-diagonal binary fibers

## Verdict

The asserted degree, leading coefficient, nonrepresentability by a support mask, and parity balance are correct under

\[
n\ge4,\qquad 2\le k\le n-2,\qquad 1\le t\le k-1.
\]

The full-support assertion needs the stricter condition **\(t\le k-2\)**. At \(t=k-1\), precisely the off-diagonal edges whose two endpoints both lie in \(\{0,\ldots,k-1\}\) are absent from the fiber's support. In particular, when \(k=2\), the only allowed interior fiber \(t=1\) is not fully supported.

## Definitions and corrected statement

Write \(R=\{0,\ldots,k-1\}\), \(O=\{k,\ldots,n-1\}\), and \(N=\binom n2\). For a permutation \(\pi\in S_n\), its red count is

\[
r(\pi)=|\{i\in R:\pi(i)=i\}|.
\]

Let \(\mathcal F_t=\{\pi:r(\pi)=t\}\). Set \(\rho(i,j)=1\) precisely when \(i=j\in R\), and set it to zero otherwise. Then

\[
P_t(\lambda)=[z^t]\det\bigl[z^{\rho(i,j)}(\lambda+i)^j\bigr]_{i,j=0}^{n-1}
\]

has exact degree

\[
D=\binom n2-\binom{n-k}{2}
\]

and leading coefficient

\[
[\lambda^D]P_t(\lambda)
=(-1)^{k-t}\binom kt\prod_{q=0}^{n-k-1}q!.
\]

The exact support is

\[
\operatorname{supp}(\mathcal F_t)=
\begin{cases}
\{0,\ldots,n-1\}^2,&1\le t\le k-2,\\
\{0,\ldots,n-1\}^2\setminus\{(a,b):a,b\in R,\ a\ne b\},&t=k-1.
\end{cases}
\]

For every allowed \(t\), \(\mathcal F_t\) contains equally many even and odd permutations and cannot equal the set of perfect matchings admitted by any fixed edge-support mask.

## Degree and leading coefficient

Let \(B_{ij}=(\lambda+i)^j\). Multilinearity in the selected diagonal entries gives

\[
\det\bigl(B+(z-1)\operatorname{diag}(B_{00},\ldots,B_{k-1,k-1},0,\ldots,0)\bigr)
=\sum_{S\subseteq R}(z-1)^{|S|}
\left(\prod_{i\in S}(\lambda+i)^i\right)
\det B_{S^c,S^c}.
\]

No extra cofactor sign appears: deleting the same row and column index set contributes \((-1)^{2\sum_{i\in S}i}=1\).

For \(C=S^c=\{c_1<\cdots<c_m\}\), define

\[
V(C)=\prod_{a<b}(c_b-c_a).
\]

The generalized Vandermonde calculation is

\[
\deg_\lambda\det[(\lambda+c_a)^{c_b}]_{a,b=1}^m
=\sum_{c\in C}c-\binom m2,
\qquad
\operatorname{LC}_\lambda\det[(\lambda+c_a)^{c_b}]
=\frac{V(C)^2}{\prod_{q=0}^{m-1}q!}.
\]

For completeness, expand

\[
(\lambda+c_a)^{c_b}
=\sum_{q\ge0}c_a^q\binom{c_b}{q}\lambda^{c_b-q}.
\]

Cauchy–Binet shows that the largest possible power of \(\lambda\) comes from the unique smallest set of \(m\) distinct powers \(q\), namely \(0,1,\ldots,m-1\). Its coefficient is

\[
\det[c_a^q]_{a,q}\det\left[\binom{c_b}{q}\right]_{q,b}
=V(C)\frac{V(C)}{\prod_{q=0}^{m-1}q!}>0.
\]

The second determinant identity follows because \(\binom{x}{q}\) has degree \(q\) and leading coefficient \(1/q!\). Thus the claimed degree is attained, not merely an upper bound.

If \(|S|=s\), multiplying by the selected diagonal entries yields degree

\[
d_s=\sum_{i\in S}i+\sum_{j\in S^c}j-\binom{n-s}{2}
=N-\binom{n-s}{2}.
\]

These degrees strictly increase with \(s\) throughout \(0\le s\le k\). Consequently the unique highest-degree contribution comes from \(S=R\). Here \(C=\{k,k+1,\ldots,n-1\}\), so with \(m=n-k\),

\[
V(C)=\prod_{q=0}^{m-1}q!,
\qquad
\operatorname{LC}\left(\prod_{i\in R}(\lambda+i)^i\det B_{O,O}\right)
=\prod_{q=0}^{m-1}q!.
\]

Finally,

\[
[z^t](z-1)^k=(-1)^{k-t}\binom kt\ne0.
\]

This proves the degree and leading coefficient without any possibility of cancellation at the leading degree.

## Exact support: explicit completion of every feasible edge

Fix a proposed edge \(a\mapsto b\). The constructions below fix exactly \(t\) elements of \(R\).

### 1. A designated diagonal edge: \(a=b\in R\)

Choose \(F\subseteq R\) of size \(t\) containing \(a\), fix every point of \(F\), and put all points of its complement into one cycle. The complement has size

\[
n-t\ge n-k+1\ge3,
\]

so that cycle has no fixed points. The resulting permutation contains the requested edge and belongs to \(\mathcal F_t\).

### 2. An undesignated diagonal edge: \(a=b\in O\)

Choose any \(F\subseteq R\) of size \(t\), fix every point of \(F\cup\{a\}\), and put the remaining points into one cycle. The cycle length is

\[
n-t-1\ge n-k\ge2,
\]

so there are no additional fixed points. Again the permutation belongs to \(\mathcal F_t\).

### 3. An off-diagonal edge: \(a\ne b\)

Neither \(a\) nor \(b\) can be a designated fixed point in any permutation containing \(a\mapsto b\): \(a\) is visibly not fixed, and column \(b\) is already occupied. Therefore a necessary condition is

\[
t\le k-|\{a,b\}\cap R|.
\]

It is also sufficient. Choose \(F\subseteq R\setminus\{a,b\}\) with \(|F|=t\), fix \(F\), and put the complement into one cycle beginning \((a\ b\ \cdots)\). This cycle includes the edge \(a\mapsto b\), has length \(n-t\ge3\), and has no fixed points.

For the stated parameter range, this feasibility condition fails only when \(t=k-1\) and both distinct endpoints \(a,b\) belong to \(R\). This proves the exact-support formula.

## Obstruction to every support-mask representation

All diagonal edges belong to \(\operatorname{supp}(\mathcal F_t)\), by the first two constructions above. If a mask admitted exactly \(\mathcal F_t\), it would have to contain every edge used by every member of \(\mathcal F_t\), and therefore every diagonal edge. The identity permutation would then be a perfect matching admitted by that mask. But its red count is \(k\), not \(t\). This contradiction proves nonrepresentability even at the boundary \(t=k-1\), where full support fails.

## Parity balance

Choose two distinct elements \(r,s\in O\), possible because \(n-k\ge2\). The map

\[
\pi\longmapsto \pi\circ(r\ s)
\]

swaps the images of rows \(r\) and \(s\), leaves every designated row unchanged, and reverses permutation sign. It is a fixed-point-free involution of \(\mathcal F_t\). Hence exactly half the fiber is even and half is odd.

The proposed determinant proof is also valid if “top coefficient” means the **nominal coefficient of \(\lambda^N\)**, rather than the actual nonzero leading coefficient at degree \(D<N\). Indeed, every permutation product \(\prod_i(\lambda+i)^{\pi(i)}\) is monic of degree \(N\), so

\[
[\lambda^N]P_t(\lambda)
=\sum_{\pi\in\mathcal F_t}\operatorname{sgn}(\pi)
=[z^t]\det\bigl[J+(z-1)\operatorname{diag}(1_k,0)\bigr]=0.
\]

The last determinant vanishes because the \(n-k\ge2\) undesignated rows are identical.

## Small example and checks

- Smallest counterexample to the original full-support scope: \(n=4,k=2,t=1\). Neither \(0\mapsto1\) nor \(1\mapsto0\) belongs to the fiber support.
- A fully supported interior example is \(n=6,k=3,t=1\). Its degree is \(15-3=12\), and its leading coefficient is \((-1)^2\binom31(0!1!2!)=6\). Thus the nominal coefficients at degrees \(15,14,13\) vanish.
- Exhaustive enumeration independently verified the exact-support formula and even/odd balance for every allowed \((n,k,t)\) with \(4\le n\le7\).

## Additional audit: nonsingular square red-block extension

Reviewed `/workspace/shared/red-matching-root-20261018/PROOF.md`, including its square-block extension. **The extension is correct as written.** Its signs, arbitrary offset/exponent ordering, and range \(0\le t\le k<n\) all check out. No full-support conclusion is implied by this extension.

Let \(a_0,\ldots,a_{n-1}\) be distinct real offsets, let \(e_0,\ldots,e_{n-1}\) be distinct nonnegative integer exponents, and write

\[
V_{ij}(\lambda)=(\lambda+a_i)^{e_j},\qquad E=\sum_j e_j.
\]

Suppose every red edge lies in \(I\times J\), with \(|I|=|J|=k<n\), and let \(B\) be the binary incidence block on those rows and columns, listed in their original increasing index orders. Assume \(\det B\ne0\). Let \(R\) agree with \(V\) on red entries and be zero elsewhere. Then

\[
\deg_\lambda [z^t]\det\bigl(V+(z-1)R\bigr)
=E-\binom{n-k}{2},\qquad 0\le t\le k,
\]

with leading coefficient

\[
(-1)^{\sum I+\sum J+k-t}\binom kt\det B\,
\frac{\Delta(a_{I^c})\Delta(e_{J^c})}
{\prod_{q=0}^{n-k-1}q!}.
\]

Here all complementary sequences retain increasing **index** order; their numerical values need not be increasing. Thus a Vandermonde can be negative, and that sign is already included. Using one-based rather than zero-based index sums does not change the cofactor sign, since the two sums together increase by \(2k\).

### Direct generalized Laplace verification

The determinant-of-a-sum identity gives

\[
\det(V+uR)
=\sum_{s=0}^{k}u^s
\sum_{\substack{A\subseteq I,\ C\subseteq J\\|A|=|C|=s}}
(-1)^{\sum A+\sum C}\det R_{A,C}\det V_{A^c,C^c}.
\]

This also verifies the sign directly. For each pair \((A,C)\),

\[
\deg\det R_{A,C}\le\sum_{j\in C}e_j,
\qquad
\deg\det V_{A^c,C^c}
=\sum_{j\notin C}e_j-\binom{n-s}{2}.
\]

Consequently every size-\(s\) summand has degree at most \(E-\binom{n-s}{2}\). At size \(k\), the only possible row/column pair is \((I,J)\), and

\[
[\lambda^{\sum_{j\in J}e_j}]\det R_{I,J}=\det B\ne0,
\]

because the coefficient of the highest columnwise degree is exactly the binary incidence determinant. Multiplying by the translated complementary-minor leading coefficient yields

\[
(-1)^{\sum I+\sum J}\det B\,
\frac{\Delta(a_{I^c})\Delta(e_{J^c})}
{\prod_{q=0}^{n-k-1}q!}.
\]

For every \(s<k\), the upper bound is strictly lower, since \(k<n\). Replacing \(u\) by \(z-1\) and extracting \([z^t]\) multiplies this unique highest-degree contribution by \((-1)^{k-t}\binom kt\), nonzero for every \(0\le t\le k\). This proves the formula and the entire claimed range, including \(t=0\) and \(t=k\).

The assumption \(k<n\) genuinely matters: at \(k=n\), sizes \(n\) and \(n-1\) tie in this degree bound, and cancellation can occur. For example, when \(n=k=2\) and precisely the two diagonal edges are red, the exact-one fiber is empty despite \(B=I_2\) being nonsingular.

If \(n-k\ge2\), swapping two rows outside \(I\) still gives the parity-reversing involution, for every exact-count fiber. If \(n-k=1\), this involution is unavailable and the nominal leading-degree coefficient is already the nonzero coefficient in the theorem; the root proof correctly restricts its parity assertion to \(n-k\ge2\).

### One fixed exact sign check

Used one fixed coloring, not an enumeration of colorings:

\[
n=5,\quad I=(0,1,2),\quad J=(0,1,3),\quad
B=\begin{pmatrix}1&1&0\\0&1&1\\1&0&1\end{pmatrix},\quad \det B=2,
\]

\[
a=(2,-1,4,0,3),\qquad e=(2,0,4,1,3).
\]

This tests a nonprincipal block with multiple red perfect matchings, a negative offset, and unsorted offsets/exponents. Here \(E=10\), \(n-k=2\), \(\sum I+\sum J=7\), \(\Delta(a_{I^c})=3\), and \(\Delta(e_{J^c})=-1\). The common signed prefactor before \((-1)^{3-t}\binom3t\) is therefore \(6\).

Exact polynomial enumeration of the \(5!\) permutations gave, in order \(t=0,1,2,3\), degree \(9\) in all four cases and leading coefficients

\[
(-6,\ 18,\ -18,\ 6),
\]

exactly as predicted.

## Final report review: complete matching, cubic moments, and singular block

Reviewed the mathematical statements in [REPORT.md](REPORT.md). No further mathematical error was found. The complete-red-matching boundary, signed cubic-moment identities, displayed degree-12 polynomial, and singular-block example all check out independently.

### Complete-red-matching boundary

If the red edges form a perfect matching \(\sigma\), the nominal \(\lambda^E\) coefficient is

\[
[z^t]\det\bigl[J+(z-1)P_\sigma\bigr].
\]

Right multiplication by \(P_\sigma^{-1}\) leaves the all-ones matrix \(J\) unchanged. Thus

\[
\det\bigl[J+(z-1)P_\sigma\bigr]
=\operatorname{sgn}(\sigma)\det\bigl[J+(z-1)I\bigr]
=\operatorname{sgn}(\sigma)(z-1)^{n-1}(z+n-1).
\]

The last identity follows from the eigenvalues \(n,0,\ldots,0\) of \(J\), or directly from the rank-one determinant identity. For every \(0\le t\le n\), its coefficient is

\[
\operatorname{sgn}(\sigma)(-1)^{n-t}(t-n+1)\binom nt.
\]

It vanishes exactly at \(t=n-1\), the sole impossible fixed-point count relative to \(\sigma\), and is nonzero at every other target. This establishes the report's boundary claim independently. It does not justify continuing the proper-matching strict-degree proof to \(k=n\); that proof really does lose strictness there.

### Cubic-moment identities

For standard labels, with \(S_\ell(\pi)=\sum_i i^\ell\pi(i)\), the formal logarithm gives

\[
\log\prod_i(1+iu)^{\pi(i)}
=S_1u-\frac{S_2}{2}u^2+\frac{S_3}{3}u^3+O(u^4).
\]

Exponentiating proves

\[
T_1=S_1,\qquad T_2=\frac{S_1^2-S_2}{2},\qquad
T_3=\frac{S_1^3-3S_1S_2+2S_3}{6}.
\]

An independent exact permutation expansion for the report's \(n=6,k=3,t=1\) example verified all 13 displayed nonzero polynomial coefficients, the counts \(117\) even and \(117\) odd, and

\[
\left(\sum\operatorname{sgn}(\pi)T_0,
\sum\operatorname{sgn}(\pi)T_1,
\sum\operatorname{sgn}(\pi)T_2,
\sum\operatorname{sgn}(\pi)T_3\right)=(0,0,0,6).
\]

Therefore the stated cubic-numerator sum \(36\) is correct.

### Singular all-red \(2\times2\) block in \(K_{4,4}\)

Take standard labels \(a_i=e_i=i\), with red edges precisely \(\{0,1\}\times\{0,1\}\). The binary red block is all ones, so \(\det B=0\). The nonsingular-block candidate degree would be \(6-\binom22=5\), and its degree-5 coefficient indeed cancels.

There is an elementary exact verification. The two extreme fibers factor into complementary \(2\times2\) blocks and give

\[
P_0(\lambda)=\lambda^2(\lambda+1)^2,
\qquad
P_2(\lambda)=(\lambda+2)^2(\lambda+3)^2.
\]

At \(z=1\), the full uncolored Vandermonde determinant is \(0!1!2!3!=12\). Hence

\[
\begin{aligned}
P_1(\lambda)
&=12-P_0(\lambda)-P_2(\lambda)\\
&=-2\lambda^4-12\lambda^3-38\lambda^2-60\lambda-24.
\end{aligned}
\]

Thus the low-to-high coefficient list is exactly

\[
[-24,-60,-38,-12,-2].
\]

This was also checked independently by direct permutation expansion, which counted \(8\) even and \(8\) odd members of the exact-one fiber.

The update expansion explains why the degree drops by one without making the polynomial zero. The full selected red-entry determinant is

\[
\det\begin{pmatrix}1&\lambda\\1&\lambda+1\end{pmatrix}=1.
\]

Its nominal degree-one coefficient \(\det B\) vanishes, but its degree-zero coefficient does not. Multiplying by the complementary minor gives degree four, while every size-one selected term has degree at most three. The degree-four coefficient of \(P_1\) is therefore \([z](z-1)^2=-2\). This rigorously supports the stated singular boundary without suggesting that singularity generally implies a zero polynomial or admitting a general singular-block theorem.
