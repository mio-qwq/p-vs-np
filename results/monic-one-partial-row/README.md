# One partial row and three full rows: arbitrary exponent gaps

2026-10-18. Auxiliary masked-determinant lemma, not ASNC or P versus NP. No novelty claim. Independently audited in a separate AI-assisted review; 38 exact coefficientwise identities checked. No human peer review or Lean verification.

## Statement
Let four offsets be distinct real numbers and four exponents distinct nonnegative integers. In a 4 by 4 matrix with entries (x+a_i)^{e_j}, retain any nonempty subset of the entries of one row and all entries of the other three rows. The determinant is not identically zero.

## Proof
Permute the partial row to the first row and columns to increasing exponents, subtract the smallest exponent by factoring a nonzero polynomial from each row, and translate x so that the partial row has offset zero. Write the exponents as (0,p,q,r), with 0<p<q<r, and the remaining offsets as a,b,c. Put z=1/x and factor x^{e_j} from each column. The normalized determinant is a polynomial in z whose partial row is the indicator of a nonempty subset S of {0,1,2,3}, and whose other entries are (1+az)^{e_j}, etc.

For each increasing triple K=(k_0,k_1,k_2), the contribution is
 z^{k_0+k_1+k_2} det[u^{k_l}]_{u=a,b,c;l=0,1,2} C_K,
where
 C_K = sum_{j in S} (-1)^j det[binom(e_t,k_l)]_{l=0,1,2;t != j}.
This is Cauchy–Binet applied to each cofactor, equivalently the finite binomial expansion and multilinearity. The first possible degree is three, from K=(0,1,2).

Twice C_(0,1,2) is the sum over S of the weights
 w_0=(q-p)(r-p)(r-q),
 w_1=-qr(r-q),
 w_2=pr(r-p),
 w_3=-pq(q-p).
Their total is zero and none is zero. Thus singleton and triple subsets have a nonzero coefficient. Same-sign pairs also do. For opposite-sign pairs {0,1} and {2,3}, strict inequalities (q-p)(r-p)<qr and r(r-p)>q(q-p) exclude cancellation. For the two remaining pairs {1,2} and {0,3}, cancellation occurs exactly when r=p+q. Because det[u^{k_l}] for (0,1,2) is a nonzero Vandermonde, all these non-cancelling cases are settled.

For S all four columns, the usual binomial/Cauchy–Binet expansion has leading degree six, coefficient
 det[u_i^k]_{i=0,1,2,3;k=0,1,2,3} det[binom(e_j,k)]_{k,j=0,1,2,3},
with u=(0,a,b,c). Both determinants are nonzero: the second is the exponent Vandermonde divided by 0!1!2!3!.

It remains to handle S={1,2}, r=p+q; the endpoint pair is its complement, and its coefficients below degree six are negatives because the full-row determinant begins in degree six.

Set V=det[u^k]_{u=a,b,c;k=0,1,2} and B=pq(p-q)(p+q), both nonzero. Direct finite polynomial identities give
 C_(0,1,3)=B/6,
 C_(0,1,4)=B(p+q-3)/12,
 C_(0,2,3)=B(p+q-1)/12.
The corresponding offset alternants are V times, respectively,
 s_1=a+b+c,
 h_2=a^2+b^2+c^2+ab+ac+bc,
 s_2=ab+ac+bc.
Consequently the degree-four coefficient is VB s_1/6. If it vanishes, s_1=0, so h_2=-s_2. The degree-five coefficient is then
 VB[(p+q-3)h_2+(p+q-1)s_2]/12 = VB s_2/6.
But s_2=-(a^2+b^2+c^2)/2 is strictly negative for distinct real a,b,c. Thus the degree-five coefficient cannot also vanish. This settles both exceptional pairs and proves the statement.

## Boundary and reproduction
The real-field hypothesis is used only in the last sum-of-squares step. This proof permits all exponent gaps and extends the previously certified one-partial-row support case; it does not address arbitrary support masks. The proof above is a complete algebraic argument independent of execution. The accompanying `verify_identities.py` uses only the Python standard library; `AUDIT.md` records the independent AI-assisted audit. Run `python3 verify_identities.py` and `python3 check_negative_controls.py`, or use `python3 ../verify-gapped-20261018.py` for all publication checks, including ordinary and optimized Python. All 38 identities are checked coefficientwise. The original exploratory SymPy derivation is not needed for reproduction and is not included.
