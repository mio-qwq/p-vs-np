# Independent audit: equal-halves rectangular moment hierarchy

18 October 2026. Local mathematical audit and exact finite verification. No remote edits or publication.

## Verdict

**Accept the theorem, with precisely its stated hypotheses and scope.** The first-differing-moment coefficient, all signs and factorial normalizations, absence of interfering smaller Laplace layers, separated-offset nonvanishing, and standard-offset closed form are correct. For arbitrary distinct offsets the coefficient is only a candidate: its offset factor can vanish. The theorem treats the rectangle with n=2r+2, r selected rows, and r+1 selected columns. It does not resolve arbitrary binary colorings, prove novelty, or produce an ASNC counterexample.

The audit reviewed `../PROOF.md` against the earlier obstruction checkpoint and independently reconstructed 15 complete bivariate determinants. The frozen audited proof SHA-256 is `f796d745708ca05d4f69e3c55949cc053ab8b6c8561dc07cc090c5838556183f`, also recorded in `SOURCE_MANIFEST.json`.

## Mathematical checks

1. **Existence and index range.** The two disjoint exponent classes each have m=r+1 elements. Equality of all elementary symmetric functions through m would identify their monic root polynomials and hence their root multisets, impossible under global distinctness. The first differing index therefore satisfies 1<=k<=r+1. Newton's identities give exactly

   (-1)^(k-1)(e_k(Y)-e_k(X))=(p_k(Y)-p_k(X))/k.

2. **Weighted column sign.** If x is in position t of the original-index-ordered X class and q members of Y precede its original index p=t+q, then

   Delta(X)=(-1)^(m-1-t) Delta(X without x) f'(x),

   Delta(Y with x)=(-1)^(m-q) Delta(Y) g(x).

   Together with the Laplace factor (-1)^(sum B-sum J)=(-1)^(-p), this gives w_x/K=-g(x)/f'(x), including arbitrary exponent ordering. Lagrange interpolation then annihilates every polynomial in x below degree k-1 and returns (-1)^(k-1) delta_k at degree k-1.

3. **Minor normalization.** A size-M translated minor has leading coefficient Delta(b)Delta(U)/H_M. For correction h, the quotient by this leading coefficient is symmetric in U of degree at most h. Its homogeneous degree-h part has the Schur/factorial form in the proof. On removing x from X, only the column partition (1^h) contributes to its highest power x^h; its sign is (-1)^h and factorial ratio is 1/(r falling h). On adding x to Y, only the row partition (h) contributes; its factorial ratio is 1/((r+2) rising h). Their convolution is exactly q_l, with no omitted factorial.

4. **Lower layers.** Put s=r-j, m=r+1 and let t=u+v be a correction order. In the refined range t<=k-j-2, the inequality k<=r+1 gives u<=t<=s-1. Thus the s-u low-degree top rows really exist; there is no unhandled u>=s case. Reduction modulo f and g changes a degree-d polynomial by a difference of degree at most d-k; for d<m the two remainders coincide. Negative degree bounds mean the zero polynomial. After removing difference terms of degrees below s-u, all bottom differences lie in a common space of dimension at most

   L=max(0,2j+2+t-k)<=j.

   Bottom rows consequently lie in a space of dimension at most m+L<=m+j, whereas there are m+j+1 such rows. Every fixed row-subset and degree-list term vanishes. This proves the stated per-layer first-possible loss

   max(j(j+2), k-1+j(j+1)).

   In particular, smaller layers cannot affect degree D-k+1 or anything above it.

5. **Correction made during audit.** An initial draft's weaker bound t<=k-2j-2 already sufficed for the main theorem, but did not justify its additional k=3 assertion that the size-(r-1) leading term also vanishes. The refined rank count above now proves that assertion and is included in the reviewed proof. This was a proof-completeness correction, not a counterexample to the theorem.

6. **Positivity.** For V a uniform-simplex convex combination of complementary offsets,

   q_l=E[e_l(V-Arow)]/(r falling l).

   Expanding the elementary symmetric polynomial and using the Dirichlet moment formula gives the displayed q_l exactly. This proves positive q_l when all selected offsets precede all complementary offsets, and sign (-1)^l in the reverse separation. It also establishes translation invariance and affine scaling by c^l. It supplies no arbitrary-offset positivity claim.

7. **Standard offsets.** The formal divided-difference identity for W(t) and the substitution u=e^t-1 in the residue calculation are correct, including j=r (where e_r(0,...,r-1)=0). Comparing the coefficient of x^(r-j)u^r in (1+u)^x supplies the stated factorial ratio. Hence q_l=(r+1)^l/l! for 0<=l<=r, and the power-sum leading coefficient is

   A K (r+1)^(k-1) (p_k(Y)-p_k(X))/k!.

8. **Edges.** The r=1,k=1 and r=1,k=2 cases are included and agree with direct full reconstruction. q_0=1. The expression with r(r-1) occurs only for k=3, which forces r>=2. The empty-row case r=0 is excluded. All fibers t=0,...,r are feasible; a nonzero multiple of (z-1)^r gives every one the claimed common degree and signed binomial leading coefficient.

## Independent exact reconstruction

`check_independent.py` does not import the producer's code or use its Cauchy-Binet/minor expansion. For a given case it:

- Evaluates the actual determinant with integer Bareiss elimination.
- Uses E+1 lambda values and r+1 values of w=z-1, where E=sum e_j. The determinant has degree at most E in lambda and at most r in w, so these grids uniquely determine the entire polynomial.
- Converts finite differences to ordinary coefficients with exact rational arithmetic and verifies integrality.
- Checks every coefficient above D-k+1, the complete coefficient at D-k+1, and the sharpened bound separately in every w layer.
- Checks three additional points outside the reconstruction grid as implementation consistency checks. These extra points are not the reason the reconstruction is complete.

All checks use explicit exceptions, and ordinary/optimized Python runs agree. The 15 complete reconstructed polynomials are stored in `independent-results.json`. Cases cover k=1,...,5; r=1,...,4; arbitrary order and nonprincipal subsets; separated and nonseparated offsets; and zero offset factors.

### Higher-moment examples

- n=8,r=3, X={0,7,9,16}, Y={1,4,12,15}, standard offsets and I={0,1,2}: first three power sums agree, k=4, D=51. Exact degree is 48 and the coefficient is 118970202193920 (z-1)^3. The potentially interfering size-2 layer vanishes, also at its next correction as required by the sharpened bound.
- n=10,r=4, X={1,2,10,14,18}, Y={0,4,8,16,17}, standard offsets and I={0,1,2,3}: the first four power sums are respectively 45,625,9585,153409 in both classes; fifth sums are 2527425 and 2502225. Thus k=5, D=69, and exact degree is 65 with coefficient 20071103433434726400000 (z-1)^4. The size-3 layer vanishes through corrections 0,1,2. An unsorted, nonprincipal-row variant independently checks signs and offset dependence.

`check_qclosed.py` separately verifies q_l=(c(r+1))^l/l! for affine offsets b+ci in 90 exact families: 1<=r<=30, all 0<=l<=r, and (b,c)=(0,1),(7,-3),(19,5). These finite tests supplement the formal proof; they do not replace it.

## Entirely integer offset obstruction

The arbitrary-offset caveat needs no irrational numbers. Take

- n=6, r=2, exponents e=(0,1,2,4,5,6), J={0,3,4};
- offsets a=(-5,5,-13,-9,9,13), I={0,1}.

The exponent classes X={0,4,5},Y={1,2,6} match the first two power sums and differ at the third. The offset means are zero, Var(Arow)=25, Var(Crow)=125, hence q_2=0. All offsets and exponents are distinct integers. With w=z-1, full reconstruction gives

F(w+1,lambda)=4638965760 lambda [
  8115 w^2 lambda^6 -908500 w^2 lambda^4
  +14584375 w^2 lambda^2 +706406250 w^2
  -756000 w lambda^4 +48448512 w lambda^2
  -413532000 w +10160640 lambda^2 -558835200].

Thus D=11, the candidate degree 9 coefficient vanishes, and the actual degree is 7 with leading coefficient 37645207142400 (z-1)^2. All three target polynomials remain nonzero. The sorted nonnegative offset version a=(0,4,8,18,22,26), I={2,3}, is also fully reconstructed; it has the same degree and leading coefficient. It is obtained by an even row permutation and the translation lambda -> lambda+13.

## Reproduction

Run from this directory:

    python check_independent.py
    python -O check_independent.py
    python check_qclosed.py
    python -O check_qclosed.py
    python check_negative_controls.py
    python -O check_negative_controls.py

Everything in those two checkers uses the Python standard library. No network, numerical tolerance, random sampling, or third-party symbolic algebra is involved in the certificates.

`check_negative_controls.py` deliberately reverses the expected leading sign and changes the third-order factorial normalization. Both wrong formulas are rejected by explicit exceptions under ordinary and optimized Python. Their recorded rejections are in `negative-control-results.json`.
