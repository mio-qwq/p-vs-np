# Nonnegative column kernels: exact certificate cost and scope

19 October 2026. This note gives a constructive per-instance formulation of the structural group's proposed nonnegative-kernel target. It does not prove that target for all offsets and exponents.

## 1. The exact finite alternative

Fix distinct integer offsets a_0,...,a_(n-1), distinct nonnegative integer exponents e_0,...,e_(n-1), and a column c. Let

    V_sj(L) = (L+a_s)^e_j,
    T_s(L) = (-1)^(s+c) (L+a_s)^e_c det V[not s,not c].

For any constant real column weights u_s, the determinant obtained by multiplying entry (s,c) by u_s is exactly

    P_u(L) = sum_s u_s T_s(L).

Set S=sum e_j and let C be the integer (S+1)-by-n matrix whose s-th column lists the coefficients of T_s from L^0 through L^S. Zero trailing rows are harmless.

Exactly one of the following has a solution:

    A. C u=0, u>=0, sum_s u_s=1;
    B. C^T y>=1.

Thus exclusion of every nonzero nonnegative kernel vector is equivalent to a linear functional on polynomial coefficients that is strictly positive on every T_s. This is a finite rational linear-programming alternative; no integration formula is needed to test a specific instance.

For completeness, let v_s denote the columns of C. Alternative A means that 0 lies in their convex hull. If it does not, let z be the nonzero point of that compact convex hull closest to 0. The derivative of squared norm along the segment from z to any v_s gives `z dot v_s >= ||z||^2`. Hence `y=z/||z||^2` gives B. If A and B both held, `0=y^T C u >= sum u=1`, impossible. This proves the alternative over the reals. Rational data admit rational solutions, with the explicit bounds below.

## 2. Polynomial-size rational certificates

Suppose every C entry has absolute value at most H, with H>=1, and write r=rank C<=n. Keep r independent coefficient rows to obtain C'. This preserves the kernel.

If B is feasible, the full-row-rank polyhedron `(C')^T y>=1` has no lines and has a vertex. A vertex is determined by r linearly independent active column inequalities. Cramer's rule therefore gives rational y coordinates with numerator and denominator bit lengths

    O(r(log(H+1)+log(r+1))).

Indeed the relevant integer determinants are bounded by `r! max(H,1)^r`; numerator determinants replace one column by ones. Place this y on the chosen coefficient rows and zeros elsewhere. It is a polynomial-size rational positive-functional certificate for the original C. The signs and all n inequalities can be checked by exact integer arithmetic after clearing a positive common denominator.

If A is feasible, its bounded simplex intersection has a basic feasible point. Applying the same determinant bound to the augmented matrix consisting of C' and the all-ones row gives a rational u of polynomial bit length with at most r+1 positive coordinates. Checking `u>=0`, `sum u=1`, and `Cu=0` is also exact polynomial work.

The alternatives can be found in deterministic polynomial time in the explicit coefficient-matrix bit length by rational linear programming. This is the standard polynomial-time LP theorem, not a new algorithm: [Khachiyan, Polynomial algorithms in linear programming, 1980](https://www.mathnet.ru/php/archive.phtml?jrnid=zvmmf&option_lang=eng&paperid=5239&wshow=paper).

Enumerating all basic solutions is not being claimed polynomial. The determinant argument bounds certificate length; the polynomial constructor is the established LP algorithm.

## 3. Charging formation of C

Let A=max_s |a_s|. Each T_s has degree at most S. Its coefficient absolute sum is at most

    (n-1)! (1+A)^S,

by its determinant expansion and the coefficient absolute sums of the factors. Consequently coefficient bit length is `O(n log(n+1)+S log(A+1)+1)`.

One deterministic construction evaluates all n cofactors at L=0,...,S, multiplies by the distinguished entry, and uses integer-cleared univariate interpolation. There are O(n(S+1)) determinants of size at most n. All evaluation and interpolation numerators have bit length polynomial in n, S, and log(A+1), because an evaluated determinant term has magnitude at most `(S+A+1)^S` and the common interpolation denominator is S!. Thus forming C and solving either certificate problem is polynomial in n, S, and the offset bit length.

In particular, for canonical offsets a_s=s and exponents e_j=j, S=O(n^2), so this is an actual polynomial-bit computation. For arbitrary binary-encoded exponents, S may be exponential in their bit length. Then the described coefficient construction is only pseudopolynomial. This does not exclude a faster implicit representation, but such a representation and its optimization oracle have not been supplied here.

The structural conjecture is stated for arbitrary real offsets. The bit-cost statement above deliberately restricts to exact integer input. Rational offsets can be handled by explicitly clearing denominators and charging the resulting heights; unspecified real-number oracles are not ordinary binary inputs.

## 4. Exact positive-functional certificate despite signed dependence

For the structural group's signed-dependence example,

    a=(-3,-1,1,3), e=(0,1,2,4), c=1,

the four column Laplace polynomials are

    T0=-128 L^4+896 L^2+768 L,
    T1=384 L^4-1152 L^2+768 L,
    T2=-384 L^4+1152 L^2+768 L,
    T3=128 L^4-896 L^2+768 L.

They satisfy `T0-T1-T2+T3=0`, but the explicit functional

    functional(f) = [L^1]f / 768

sends each T_s to 1. Therefore every nonempty nonnegative column weighting gives a nonzero polynomial for this instance, even though the four polynomials are linearly dependent. This is an exact illustration of the proposed weaker target, not evidence proving its universal version.

## 5. What this does and does not certify

- A positive-functional certificate proves all nonempty nonnegative one-column masks for the given offsets/exponents at once, including every binary mask, without enumerating 2^n masks.
- A feasible nonnegative kernel u refutes the stronger weighted-column conjecture. Unless u is proportional to a binary vector, it is not itself a zero determinant for a binary deletion mask. The original two-hole problem has the very specific weight vector with two zero entries and every other entry one.
- The linear functional can have positive and negative coefficient weights y. Calling it positive means its values on all T_s are positive; it need not be integration against a positive measure or evaluation at one real point.
- All other columns in this definition are the full translated-power columns. Once another column is masked, its cofactors change. An established certificate for the full other columns is not invariant under that operation. A proof for one-column masks alone therefore cannot be iterated to arbitrary sparse supports without a new closure theorem.
- For arbitrary colored sparse graphs, decomposing into individual matching monomials gives as many as n! columns. A coefficient-space LP on that explicitly listed family has no polynomial-input guarantee. An implicit separation oracle would be an additional algorithmic obligation.

The useful open target remains a structural proof that alternative B always holds for the intended family, or a precise exact certificate for A. The finite alternative turns each supplied instance into a verifiable certificate problem, but does not settle the universal quantifier or P versus NP.

## 6. Reproduction

`check.py` reconstructs all four Laplace polynomials by signed permutation expansion and verifies the signed relation and the positive functional using exact fractions. It also checks a generic nonnegative-kernel control that is explicitly not asserted to arise from a Vandermonde mask. Both `python check.py` and `python -O check.py` pass. No floating-point LP outcome is being used as a certificate, and no general-purpose LP solver implementation is claimed in this package.
