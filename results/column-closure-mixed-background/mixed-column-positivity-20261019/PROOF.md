# One-outlier mixed backgrounds: an exact differential equation

19 October 2026. Local research note. This proves a restricted family of the one-column conjecture; it does not prove the arbitrary-background conjecture. All other columns remain full.

## 1. Main theorem

Let n>=3, let a_0<...<a_(n-1) be distinct real offsets, and let h>=0 and d>=1 be integers. Put m=n-1. Suppose the nondistinguished exponents are

    h,h+1,...,h+n-3,h+n-2+d.

There are n-1 such exponents. Let the distinguished exponent k be a nonnegative integer distinct from them. Arrange the background columns increasingly, insert the distinguished column at index c, and define

    T_s(L)=(-1)^(s+c)(L+a_s)^k
           det[(L+a_t)^b]_(t!=s,b in the background).

Then the n polynomials T_s are linearly independent over C in every one of the following cases:

1. d is odd;
2. d is 2, 4, or 6;
3. d is even and gcd(d/2,n-1)=1;
4. k<h or k>h+n-2+d, for arbitrary d.

Any other fixed column order multiplies every T_s by the same permutation sign, so the conclusion is unchanged.

For arbitrary d and the remaining k, their kernel has dimension at most one. A nonzero kernel can exist only if the polynomial

    H(L)=h_d(L+a_0,...,L+a_(n-1))

is a proper polynomial power over C, with a precisely specified divisibility condition on its root multiplicities. Here h_d denotes the complete homogeneous symmetric polynomial, not the common exponent shift h.

In particular these cases prove nonvanishing for every nonzero complex weighting of the distinguished column, hence for every nonempty nonnegative or binary weighting. For n>=4 these backgrounds contain both parities and, when d>0, are generally not arithmetic staircases.

## 2. Rational cofactor reduction

Write

    x_s=L+a_s,
    g(z)=product_s(z-a_s),
    Delta(a)=product_(r<s)(a_s-a_r),
    G(L)=product_s x_s^h,
    ell=k-h,
    w_s=u_s/g'(a_s),
    M_j(L)=sum_s w_s x_s^j.

The background cofactor after removing its row factors is the alternant for exponents 0,1,...,m-2,m-1+d. Its Schur partition is (d), so its Schur factor is h_d on the retained variables. The Vandermonde signs give

    sum_s u_s T_s
      =(-1)^(m+c) G(L) Delta(a)
         sum_s w_s x_s^ell h_d(X without x_s).       (1)

This is an identity in C(L), including ell<0. Its original left side is polynomial, and the common factor is not identically zero.

The generating-function identity for complete homogeneous polynomials gives

    h_d(X without x_s)=h_d(X)-x_s h_(d-1)(X).

Set H=h_d(X) and B=h_(d-1)(X). A kernel is therefore equivalent to

    H M_ell-B M_(ell+1)=0.                         (2)

For simultaneous translation of n variables,

    H'=(n+d-1) B=(m+d) B.                         (3)

For example, differentiating product_s(1-x_s z)^(-1) gives (3) by comparing coefficients; equivalently it follows from the simplex identity below.

If ell!=-1, put

    Y=M_(ell+1),       alpha=(ell+1)/(m+d).

Since Y'=(ell+1)M_ell, equation (2) becomes the first-order equation

    H Y'-alpha H'Y=0.                              (4)

This identity is the structural step. It uses the one-row Schur partition; no analogous first-order equation is claimed for arbitrary partitions.

## 3. Negative normalized distinguished exponents

Suppose ell<-1. If u!=0, Y is a nonzero rational function: each nonzero w_s produces a pole of order -(ell+1) at the distinct point -a_s, and no other summand has a pole there. Its degree at infinity, meaning deg(numerator)-deg(denominator) after reduction, satisfies

    deg_infinity Y <= ell+1 <0.

Equation (4), compared at infinity, instead forces

    deg_infinity Y=d alpha=d(ell+1)/(m+d)>ell+1,

because m>0 and ell+1<0. This is impossible.

When ell=-1, let U=M_0=sum_s w_s. At infinity,

    M_(-1)=U/L+O(L^(-2)),
    H=C L^d+O(L^(d-1)),
    B=[d/(m+d)]C L^(d-1)+O(L^(d-2)),

where C=binom(m+d,d)>0. Thus (2) forces

    C[1-d/(m+d)]U=0,

so U=0. Equation (2) then gives M_(-1)=0, and its distinct simple-pole residues give every w_s=0. This completes k<h without using oddness of d.

## 4. The degree-and-moment obstruction

Now suppose ell>=0. Since the background contains 0,1,...,m-2, distinctness forces ell>=m-1. For u!=0 define the first nonzero barycentric moment

    r=min{j>=0: sum_s w_s a_s^j !=0}.

The ordinary n-by-n Vandermonde matrix on the distinct a_s is invertible, so 0<=r<=m. Since ell+1>=m, the binomial expansion of Y gives

    deg Y=ell+1-r.

In particular Y is not zero. Comparing the leading degrees in (4) gives

    deg Y=d alpha,
    r=m alpha=m(ell+1)/(m+d).                     (5)

Consequently 0<alpha<=1. Equality alpha=1 would give ell=m+d-1, exactly the omitted background exponent, and is forbidden. Every nonzero kernel therefore requires

    0<alpha<1,
    r=m alpha is an integer in {1,...,m-1}.       (6)

In particular ell>m+d-1 is impossible, proving the claimed high-exponent independence for every d. Conditions (5)--(6) are necessary for a kernel and often already exclude it; they do not alone prove nonnegative-kernel exclusion.

## 5. Odd d supplies a simple real root

Let (V_0,...,V_(n-1)) be uniform on the probability simplex, and set A=sum_s V_s a_s. Direct integration of simplex monomials and the multinomial theorem give

    E[(L+A)^j]= h_j(L+a_0,...,L+a_(n-1))
                / binom(n+j-1,j).                (7)

For even j>0 this is strictly positive for every real L. Indeed A is not constant when the offsets are distinct, and the affine function L+A is not zero almost everywhere on the simplex. For j=0 the expression is 1.

If d is odd, equations (3) and (7) imply H'(L)>0 for every real L. The polynomial H has odd degree and positive leading coefficient, so it has exactly one real root rho, and H'(rho)>0 makes that root simple.

Let q>=0 be the multiplicity of Y at rho. In (4), the lowest-order coefficient at rho is a nonzero factor times

    q-alpha.

Thus q=alpha. But (6) says 0<alpha<1, whereas q is an integer. This contradiction proves full complex linear independence for odd d.

Only the offsets must be real in this argument; kernel coefficients u_s may be complex. The simple-root argument does not assume H has only real roots.

## 6. Exact remaining criterion when d is even

For ell>=0 satisfying (6), write alpha=p/q in lowest terms, where 1<=p<q. A nonzero polynomial solution of (4) exists if and only if every complex root multiplicity of H is divisible by q. Equivalently,

    H=C Q^q

for some polynomial Q and nonzero constant C. The polynomial solutions are then exactly the scalar multiples of Q^p. This follows either from logarithmic derivatives or by comparing valuations of (4) at each root. It also proves that the kernel of the original Laplace family has dimension at most one, because u -> Y is injective in this exponent range.

There is one additional requirement for an actual kernel: Q^p must belong to the n-dimensional span

    span{(L+a_s)^(ell+1): 0<=s<n}.

This membership condition is both necessary and sufficient. If it holds, the coefficients w_s are unique; the original kernel vector is u_s=g'(a_s)w_s. Their signs must still be checked before concluding anything about nonnegative weights. A proper power by itself is not a nonnegative counterexample and is not even sufficient for a signed kernel without this span condition.

For even d, H>0 on the real line by (7). Normalize H to be monic. Its monic qth root Q, when it exists, has real coefficients: its complex conjugate is another monic qth root, and uniqueness makes them equal. Since H has no real roots, Q has no real roots and its degree d/q is even. Also (5) implies q divides m. Consequently every possible kernel requires

    q>1 and q divides gcd(d/2,m).                  (8)

Thus gcd(d/2,n-1)=1 proves independence. This argument does not assert that H is squarefree; it excludes only proper powers with the denominator required by the kernel.

Positivity on the real line does not by itself exclude repeated nonreal roots or a proper power. No broad squarefreeness or log-concavity theorem is assumed here.

## 7. The remaining even cases d=2,4,6

These cases in fact have no proper-power H at all. Translate the offsets to arrange sum_s a_s=0, which only translates L and preserves every issue above. Set

    p_j=sum_s a_s^j,        mu_j=E[A^j].

Then p_2>0, mu_1=0, and H/binom(n+d-1,d)=E[(L+A)^d] is monic. Elementary simplex integration gives

    mu_2=p_2/[n(n+1)],
    mu_4=(3p_2^2+6p_4)/[n(n+1)(n+2)(n+3)].

For d=2, H is a positive quadratic, so it cannot be a proper polynomial power: such a power would be the square of a real linear polynomial and would have a real root.

For d=4, a proper-power positive real quartic must be a square of a real monic quadratic. Centering removes its linear term, so the monic polynomial would be (L^2+c)^2. Matching coefficients gives mu_3=0 and mu_4=9mu_2^2. However p_4<=p_2^2 gives the strict bound

    mu_4/mu_2^2
      <=9n(n+1)/[(n+2)(n+3)]<9,

which is a contradiction.

For d=6, a proper-power positive real sextic must be a cube of a real monic quadratic: a square of a cubic or a sixth power of a linear polynomial would have a real root. Centering again gives (L^2+c)^3. Matching coefficients forces

    mu_3=mu_5=0,
    mu_4=5mu_2^2,
    mu_6=125mu_2^3.

The odd moment equations imply p_3=p_5=0. With these zero,

    mu_6=(15p_2^3+90p_2 p_4+120p_6)
          /[n(n+1)(n+2)(n+3)(n+4)(n+5)].

Put r_4=p_4/p_2^2 and r_6=p_6/p_2^3. Solving the required fourth and sixth moment equations gives

    r_4=(n^2+11n+15)/[3n(n+1)],
    r_6=(2n^4+34n^3+202n^2+470n+375)
          /[3n^2(n+1)^2].

Therefore

    r_6-r_4=(n^4+22n^3+176n^2+455n+375)
               /[3n^2(n+1)^2]>0.

But each a_s^2<=p_2, so p_6<=p_2 p_4 and hence r_6<=r_4. This contradiction excludes the last proper-power possibility and proves d=6.

The moment exclusions do not assert that every complex root is simple. Excluding a proper power is sufficient for the kernel argument.

## 8. An explicit strictly positive functional in a mixed example

Take offsets (-3,-1,1,3), sorted full exponents (0,1,3,5), and distinguish exponent 3, so c=2. The background (0,1,5) has d=3 and is mixed-parity and nonarithmetic. Exact expansion gives

    T0= 160L^6-960L^5+800L^4+1920L^3+4320L^2-8640L-12960,
    T1=-480L^6+960L^5-2400L^4+5760L^3-5280L^2+960L+480,
    T2= 480L^6+960L^5+2400L^4+5760L^3+5280L^2+960L-480,
    T3=-160L^6-960L^5-800L^4+1920L^3-4320L^2-8640L+12960.

The coefficient functional

    Phi(f)=[L^3]f/5376-[L]f/13440

satisfies Phi(T_s)=1 for every s. This illustrates the theorem with an exact positive-functional certificate; the structural proof is the differential equation, not an enumeration of certificates.

## 9. Boundary and provenance

The result concerns one weighted column with every other column full. It does not survive a second arbitrary weighted column merely by applying the same proof: the cofactor alternant and equation (2) change. Independently known two-column weighted cancellations therefore do not contradict this theorem.

Nonnegative weighted nonvanishing implies the binary one-column statement. Neither implies nonvanishing for arbitrary sparse supports, arbitrary colored matching fibers, a polynomial-time implicit separation oracle, or any P-versus-NP conclusion. Coefficient expansion with binary-encoded unbounded exponents also remains pseudopolynomial unless a separate implicit algorithm is supplied.

The universal mixed-background conjecture remains open here. The even-d power-and-span condition is an exact reduction within this particular one-outlier family, not a characterization of arbitrary backgrounds.

Nor should a general positive-functional proof insist on equal values at all T_s. In the previously proved hook family, n=6, offsets (-3,-2,-1,1,2,3), exponents (0,1,2,3,4,6), and distinguished exponent 1 give the signed kernel (80,-30,48,48,-30,80), whose coordinate sum is 196. Thus no functional can assign the same nonzero value to all six terms. Unequal strictly positive values remain possible; the example does not refute the nonnegative-kernel conjecture.

The cofactor/ODE reduction and odd-d argument were developed in this constructive branch. The independent ODE auditor supplied the gcd(d/2,n-1) corollary and checked the exceptional exponents and span condition. The parent researcher and this branch independently derived the d=2,4,6 moment exclusions, which the auditor also checked. The parent's supporting derivation is preserved at `/workspace/shared/mixed-background-root-moments-20261019/DERIVATION.md`; that is a provenance pointer for this local research package, not an additional theorem being counted separately.

## 10. Reproduction

`check.py` uses exact rational arithmetic to verify the cofactor identity, the translation derivative identity, independence on representative odd-d and negative-normalized-exponent examples, and the explicit functional above. These checks are implementation checks; the proof above supplies the universal quantifiers. Run both `python check.py` and `python -O check.py`.
