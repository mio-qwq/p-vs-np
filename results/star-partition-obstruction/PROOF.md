# Restricted star-partition residual-population obstruction

This note proves statements about an **unsigned expected count of nonzero anchored mixed differences**, not about circuit complexity or algorithmic running time. It makes no novelty or priority claim. Substantial AI assistance was used in the derivation, checking, and preparation of this material.

## 1. Definitions and representation convention

All vector addition below is XOR in the binary cube. For disjoint error supports define

\[
\Delta f(c;u,v)=f(c+u+v)-f(c+u)-f(c+v)+f(c).
\]

For even \(n\), set \(T(x)=1[\operatorname{wt}(x)\ge n/2]\) and \(T_t(x)=T(x+t)\). For a finite shift set \(F\), the statistic is

\[
R_F(c,u,v)=\sum_{t\in F}1[\Delta T_t(c;u,v)\ne0].
\]

There is no independence assumption between these summands. Every gate has the signed unit-weight representation

\[
T_t(x)=1\left[\sum_{i:t_i=0}x_i-\sum_{i:t_i=1}x_i\ge n/2-\operatorname{wt}(t)\right].
\]

Every input is relevant. Distinct shifts give distinct Boolean functions: with \(\chi_i(x)=(-1)^{x_i}\), direct conditioning on the other bits gives

\[
\mathbb E[T(x)\chi_i(x)]=-2^{-n}\binom{n-1}{n/2-1}\ne0.
\]

For \(T_t\) this coefficient is multiplied by \((-1)^{t_i}\), recovering every bit of \(t\). We use the **represented** wire count \(W=|F|(n+1)\): all \(n\) inputs to every gate, plus one outgoing incidence per gate. This is not minimum circuit wire complexity, and no hard top gate is asserted.

A Hamming block has size \(b=2^s-1\), \(s\ge1\). Label its coordinates by the distinct nonzero vectors in \(\mathbb F_2^s\), and let \(C\) be the kernel of that parity-check matrix. Its star errors are \(E=\{0\}\cup\{e_i\}\). Their syndromes run through \(\mathbb F_2^s\) exactly once. Thus \((c,e)\mapsto c+e\) bijects \(C\times E\) with the block cube, and the same holds for each affine translate of \(C\). All centers and errors below have the stated uniform laws and are independent unless explicitly conditioned.

## 2. Explicit two-block theorem

Let \(b=2^s-1\ge7\), \(n=2b\), and choose the partition-independent shift set

\[
F=\{t:\operatorname{wt}(t)\le2\},\qquad m=|F|=2b^2+b+1.
\]

**Quantifiers:** This one explicit set is chosen first. For every balanced coordinate split \(L\sqcup R=[n]\), every Hamming labeling on each block, and every affine translate of the product kernel, take a uniform center \(c\) in that translate and independent uniform star errors \(u\in E_L,v\in E_R\). Then

\[
\mathbb E R_F\ge 2b^2\binom{2b}{b}/4^b
\ge \frac{m}{8\sqrt b}
\ge \frac{\sqrt2}{16}\frac{W}{n^{3/2}}. \tag{1}
\]

### 2.1 Exact ambient probability

For a uniform ambient center \(z\), a zero error makes the mixed difference zero. Otherwise \(u=e_i,v=e_j\) for distinct coordinates. Write \(a=z_i,d=z_j\) and let \(w\) be the weight on the remaining \(2b-2\) coordinates. Direct expansion gives

\[
\Delta T(z;u,v)=(1-2a)(1-2d)
\big(1[w+2\ge b]-2\,1[w+1\ge b]+1[w\ge b]\big).
\]

The parenthesis is nonzero exactly for \(w=b-2,b-1\). Consequently

\[
p_b:=\Pr[\Delta T(z;u,v)\ne0]
=\left(\frac b{b+1}\right)^2
\frac{\binom{2b-2}{b-2}+\binom{2b-2}{b-1}}{2^{2b-2}}
=2\left(\frac b{b+1}\right)^2\frac{\binom{2b}b}{4^b}. \tag{2}
\]

For completeness, \(c_b=4^{-b}\binom{2b}b\) satisfies
\(c_{b+1}/c_b=(2b+1)/(2b+2)\). Induction from \(b=1\), using \((2b+1)^2\ge4b(b+1)\), proves \(c_b\ge1/(2\sqrt b)\). Hence \(p_b\ge1/(4\sqrt b)\).

### 2.2 Exact transversal identity

Put \(S=E_L+E_R\), with \(|S|=(b+1)^2\). Disjoint supports make its shifts distinct and of weight at most two. For every fixed affine translate \(C+a\) of the product kernel, the syndrome property gives a bijection

\[
(C+a)\times S\longrightarrow\mathbb F_2^n,\qquad(c,t)\longmapsto c+t.
\]

Since \(\Delta T_t(c;u,v)=\Delta T(c+t;u,v)\), for fixed errors and then after averaging them,

\[
\mathbb E_{c,u,v}R_S=|S|p_b
=2b^2\binom{2b}b/4^b. \tag{3}
\]

This equality holds for **each** translate, not merely an average over translates. Since \(S\subseteq F\), nonnegativity proves the first inequality in (1). Also \((b+1)^2\ge m/2\); combining this with (2) proves its second inequality. Finally \(W=m(n+1)\le2mn\) and \(n=2b\) prove its third inequality.

For a fixed split, the smaller family indexed by \(S\) satisfies equality (3) for every labeling and coset on those blocks. That equality is not claimed for a different split with the old \(S\) held fixed. The full set \(F\) is what gives partition-uniformity. At \(b=7\), \(p_b=21021/65536\), \(|S|=64\), and \(\mathbb E R_S=21021/1024\); the full family has 106 gates.

## 3. Elementary multiblock ambient bound

Let \(n,r\) be even, \(r\ge2\), with \(r\) disjoint blocks of common size \(b\ge1\), \(rb\le n\), and \(n-r\ge6\). Split the blocks evenly into two bundles. Independently choose a uniform star error on each block, and let \(u,v\) be the sums in the two bundles. Let \(z\) be independently uniform on all \(n\) coordinates, including unused ones. Then

\[
\Pr[\Delta T(z;u,v)\ne0]\ge\frac1{2048r\sqrt n}
\ge\frac1{4096r\sqrt n}. \tag{4}
\]

Here is a proof with elementary constants. For \(B_k\sim\operatorname{Bin}(k,1/2)\), \(k\ge1\), Chebyshev's inequality gives probability at least \(3/4\) to the interval \(|B_k-k/2|<\sqrt k\), which contains at most \(3\sqrt k\) integers. A largest atom therefore has probability at least \(1/(4\sqrt k)\); the adjacent ratio \((k-j)/(j+1)\) shows that a central atom is largest. Set \(d_k=1\) for odd \(k\), and \(d_k=2\) for even \(k\). The atom at \((k-d_k)/2\) is central or has ratio at least \(1/2\) to a central atom. Thus

\[
\Pr[k-2B_k=d_k]\ge1/(8\sqrt k). \tag{5}
\]

If \(N\ge6\) and \(q=\lfloor N/2\rfloor\), every atom at \(q,q+1,q+2\) has probability at least \(1/(16\sqrt N)\). Indeed for \(N=2h\), \(h\ge3\), the smallest ratio to the central atom is \(h(h-1)/((h+1)(h+2))\ge3/10\ge1/4\); for \(N=2h+1\), \(h\ge3\), the relevant ratios are 1 and \(h/(h+2)\ge3/5\).

Condition on any fixed nonempty error supports of sizes \(a,c\), where \(1\le a,c\le r/2\). Put \(N=n-a-c\ge6\). The weights of \(z\) on these two supports and their complement are independent binomials. Force their first two weights to be \((a-d_a)/2,(c-d_c)/2\), so the flips increase total weight by \(d_a,d_c>0\). Force the complement's weight to

\[
j=N/2-1+(d_a+d_c)/2,
\]

so the initial total weight is \(n/2-1\). Parity shows that this integer is one of \(q,q+1,q+2\). The four threshold values are \(0,1,1,1\), so the mixed difference is \(-1\). The probability of this event is at least

\[
\frac1{1024\sqrt{acN}}\ge\frac1{512r\sqrt n}.
\]

The probability that both bundle errors are nonzero is
\((1-(b+1)^{-r/2})^2\ge1/4\). Averaging proves (4). This argument requires no code property; uniform ambient bits are essential. It does not directly apply to a fixed coset center.

## 4. Existential polynomial carrier for growing block counts

For sufficiently large even \(n\), let \(R=\lfloor n^{1/4}\rfloor\). Admit configurations \(P\) consisting of:

* an even \(2\le r\le R\), and \(b=2^s-1\ge1\) with \(rb\le n\);
* \(r\) indexed disjoint blocks of size \(b\), with any Hamming labeling in each;
* any balanced division of these blocks into two bundles;
* any affine translate of their product code.

The center is uniform on that translate on used coordinates; unused coordinates are independently uniform. Errors are the independent uniform block stars, grouped into \(u,v\) as above. Every gate shares the same configuration. Define

\[
Z_t(P)=\mathbb E_{c,u,v}1[\Delta T_t(c;u,v)\ne0]\in[0,1].
\]

**Theorem.** For every sufficiently large even \(n\), there exists a set \(F_n\) of \(m\) distinct shifts, chosen before \(P\), such that for **every** admitted \(P\), with its own value of \(r\),

\[
\mathbb E R_{F_n}\ge\frac{m}{8192r\sqrt n}
\ge\frac{W}{16384r n^{3/2}},\qquad W=m(n+1), \tag{6}
\]

where the following integer choice suffices:

\[
L=\lceil\log_2(n+1)\rceil,\quad J=2+2L+2nL+2n,\quad
m=32768R\lceil\sqrt n\rceil J=O(n^{7/4}\log n).
\]

### 4.1 Averaging and a finite configuration count

For uniform \(t\), conditional on any fixed \((c,u,v)\), \(c+t\) is uniform on the whole cube. Thus \(\mu_P=\mathbb E_tZ_t(P)\) equals the ambient probability in (4), for every fixed coset as well. In particular

\[
\mu_P\ge\frac1{4096r\sqrt n}\ge p_*:=\frac1{4096R\lceil\sqrt n\rceil}.
\]

There are at most \(K=n^2(n+1)^{2n}4^n\) configurations. To see this, encode \((r,b)\) in at most \(n^2\) ways, each coordinate's indexed block or unused status in at most \((n+1)^n\) ways, and each coordinate's syndrome column in at most \((n+1)^n\) ways. Columns are canonically encoded by integers among \(1,\ldots,b\); allow invalid choices when counting. A full \(n\)-bit translation has at most \(2^n\) choices and bundle designations have at most \(2^r\le2^n\) choices. Every allowed configuration is encoded; duplicates and invalid encodings only overcount. No nonlinear codes, arbitrary affine coordinate maps, or masks are included.

### 4.2 Concentration and distinctness

Sample \(m\) independent uniform shifts \(t_i\). For fixed \(P\), put \(X_i=Z_{t_i}(P)\). The \(X_i\) are independent bounded real variables, not necessarily Bernoulli. Convexity gives for \(\lambda>0\)

\[
\mathbb E e^{-\lambda X_i}\le1-\mu_P+\mu_Pe^{-\lambda}
\le e^{-\mu_P(1-e^{-\lambda})}.
\]

Markov's inequality with \(\lambda=\ln2\) yields

\[
\Pr\left[\sum_iX_i<m\mu_P/2\right]
\le e^{-m\mu_P(1-\ln2)/2}\le e^{-m\mu_P/8}.
\]

The elementary inequality \(\ln2<3/4\) follows, for example, by integrating the convex function \(1/x\) below its chord on \([1,2]\). Since
\(\ln(4K)=2\ln2+2\ln n+2n\ln(n+1)+2n\ln2\le J\), our choice gives \(m\ge8\ln(4K)/p_*\). Each failure probability is at most \(1/(4K)\), so a union bound gives simultaneous success with probability at least \(3/4\).

The collision probability is at most \(m(m-1)/2^{n+1}<1/4\) for sufficiently large \(n\), because \(m\) is polynomially bounded. Therefore a positive-probability event has no collisions and satisfies all the inequalities. Distinct shifts give distinct gates by Section 1. This proves existence of the required set, and individual-mean preservation gives (6), not merely the weaker bound with \(R\) in place of \(r\).

This is an existential statement, not an efficient explicit construction. Although random sampling has constant success probability, verifying success over every configuration is not shown to be polynomial time. The proof does not specify a numerical threshold for “sufficiently large.”

## 5. Consequence and strict limits

For any fixed \(\epsilon>0\) and \(C>0\), a purported universal bound \(C r(n)^{3/2}W/n^{3/2+\epsilon}\) for this statistic, even after choosing the best common admitted configuration, contradicts (6) for any admissible even polylogarithmic schedule \(r(n)\): the lower/upper ratio is at least \(n^\epsilon/(16384C r(n)^{5/2})\), which tends to infinity. Such a schedule eventually lies below \(R\). The same existential family covers all admitted configurations, independently of the schedule. This does not rule out every power improvement for every \(r\) as large as \(n^{1/4}\), and does not match the \(r^{3/2}\) factor or exclude improvements only in \(r\) or logarithms.

The expectation is essential: zero errors give zero residual, and there is no pointwise or constant-probability lower-tail conclusion. These are counts before signed cancellation and before top-gate simplification. For example, OR of all weight-at-most-two translates in Section 2 is simply \(1[\operatorname{wt}(x)\ge b-2]\). Gate-specific partitions, masks, nonlinear partition families, correlated errors, cancellation, aggregation, and cheaper downstream contraction remain outside these results. No circuit lower bound, CAPP running-time lower bound, hard language, or P-versus-NP conclusion follows. Nor is this a certification or refutation of any entire external manuscript.
