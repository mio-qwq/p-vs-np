# Translated complete homogeneous polynomials: an all-degree root criterion

Date: 2026-10-19. Local research supplement.

## Findings and boundary

This note does **not** prove that h_d(L+a_1,...,L+a_n) is never a proper power for arbitrary distinct real offsets. It gives an independently verifiable all-degree sufficient criterion, including two infinite offset families. It also records why an unconditional squarefreeness claim is unavailable.

For arbitrary real distinct offsets, even-degree positivity only excludes real roots. Repeated nonreal roots can occur: a separate adversarial calculation supplies an exact algebraic-offset example with n=9,d=6. That example has multiplicity pattern (2,2,1,1), so it is not a proper power. Squarefreeness is stronger than the required absence of a common divisor of all multiplicities.

## 1. Elementary finite-difference lemma

Let p be a nonconstant polynomial all of whose roots lie on the vertical line Re z=c, let h>0, and let |lambda|=1. Set

    f(z)=p(z+h)-lambda p(z).

If f is nonconstant, every root is simple and lies on Re z=c-h/2.

Proof. Write p(z)=C product_j (z-c-i y_j), with y_j real, allowing repetitions. If Re z>c-h/2, each factor of p(z+h) has larger modulus than its corresponding factor of p(z). The inequality reverses on the other side of the line. Thus equality p(z+h)=lambda p(z) is possible only on the stated line. At such a root z=c-h/2+i t, neither p(z) nor p(z+h) is zero, and

    p'(z+h)/p(z+h)-p'(z)/p(z)
      = sum_j h/[h^2/4+(t-y_j)^2] > 0.

Consequently f'(z) is nonzero. If lambda=1 the degree drops by one; otherwise it is unchanged. This proves the lemma without needing any global zero-location assumption beyond the input line.

This is the vertical-line specialization of Katkova–Tyaglov–Vishnyakova's finite-difference simplicity argument, Theorem 2.4. See the provenance section.

## 2. Barycentric shift-symbol criterion

Let S={s_1,...,s_n} be distinct integers with min S=0 and max S=K, and let n>=2. Define

    g_S(t)=product_(s in S)(t-s),
    R_S(z)=sum_(s in S) z^s/g_S'(s).

Suppose every complex root of R_S lies on the unit circle. Then for every d>=1, every root of

    H_d(L)=h_d(L+b+h s_1,...,L+b+h s_n),  h>0,

is simple and lies on

    Re L=-b-h K/2.

In particular H_d is not a proper polynomial power for any d>=1.

Proof. Put N=n+d-1 and x=(L+b)/h. The divided-difference identity gives

    H_d(L)=h^d sum_(s in S) (x+s)^N/g_S'(s)
          =h^d R_S(E)x^N,

where E f(x)=f(x+1). One may verify the divided-difference identity directly from partial fractions of product_s(1-(x+s)t)^(-1).

The coefficient of z^K and the constant term of R_S are both nonzero. Its zero at z=1 has multiplicity exactly n-1: the barycentric moment identities are

    sum_s s^j/g_S'(s)=0  (0<=j<n-1),
    sum_s s^(n-1)/g_S'(s)=1,

so R_S(exp(t))=t^(n-1)/(n-1)!+O(t^n).

Factor R_S(z)=C product_(j=1)^K (z-lambda_j), with |lambda_j|=1. Apply the lemma successively to (E-lambda_j), starting from x^N. The n-1 factors with lambda_j=1 lower the degree to d, while all other factors preserve the degree. Since d>=1, none of these steps has a constant input or output. Each factor moves the root line left by 1/2 and gives simple roots. The final root line is Re x=-K/2, and all final roots are simple. Scaling back proves the claim.

The unit-circle condition is a sufficient hypothesis that must actually be checked. Arbitrary real or even arbitrary lattice offsets do not satisfy it automatically.

## 3. Two infinite offset families

### 3.1 Arithmetic-progression offsets

For S={0,1,...,n-1},

    R_S(z)=(z-1)^(n-1)/(n-1)!.

Thus all H_d have simple roots on the vertical line through the negative mean of the offsets. This recovers Proposition 2.5 of the cited paper after the divided-difference identification.

### 3.2 Even grid with its center deleted

For an integer r>=1, set

    S={0,1,...,2r} minus {r}.

There are n=2r offsets. For k != r,

    1/g_S'(k)=(k-r)(-1)^(2r-k)/[k!(2r-k)!].

The omitted k=r summand is zero, so

    R_S(z)
      =[(z d/dz)-r](z-1)^(2r)/(2r)!
      =r (z-1)^(2r-1)(z+1)/(2r)!.

All roots of this symbol are 1 or -1. Therefore, for every d>=1 and offsets

    b+h(-r,-r+1,...,-1,1,...,r),

all roots of H_d are simple and have real part -b. For r>=2 these offsets are not an arithmetic progression. The first example is (-2,-1,1,2).

The claim concerns the offsets, not the exponents of the one-outlier alternant. It gives the one-outlier independence theorem for all d on these offset families, with every allowed distinguished exponent k, by applying the already-established ODE reduction.

## 4. Generic consequence, without universality

For fixed n>=2 and d>=1, the discriminant in L of H_d is a polynomial in the offsets. It is nonzero at arithmetic-progression offsets by Section 3.1. Hence the discriminant is not identically zero. It follows that H_d is squarefree on a nonempty Zariski-open set of offset tuples, and in particular for Lebesgue-almost every distinct real tuple. This does not settle the exceptional tuples or the weaker universal no-proper-power statement.

## 5. Exact literature scope

Primary source:

Olga Katkova, Mikhail Tyaglov, Anna Vishnyakova, “Hermite–Poulain theorems for linear finite difference operators,” Constructive Approximation 52 (2020), 357–393, DOI https://doi.org/10.1007/s00365-020-09507-0. Author manuscript: https://arxiv.org/abs/1901.06398 ; PDF https://arxiv.org/pdf/1901.06398 .

Relevant locations in the 27-page arXiv version:

- Theorem 1.3, manuscript pages 2–3: line-preserving finite difference operators are characterized using a unit-circle symbol and perpendicular shift direction.
- Theorem 2.4, page 10: under those hypotheses the resulting roots are simple.
- Proposition 2.5, page 10: roots of Delta^m(z^N), 1<=m<=N-1, are simple on Re z=-m/2.

The proof above supplies the entire specialized argument, so applicability is explicit. The primary theorem does not assert simplicity for arbitrary divided-difference knots. The central-deletion corollary and the barycentric-symbol formulation are deductions here; no novelty claim is made for them.

Secondary search lead (not used to justify the theorem): https://mathoverflow.net/questions/514900/are-the-zeros-of-the-moment-polynomials-e-xx-n-always-simple . It points to the same primary source and records that positivity of a general measure does not suffice. The atomic law P(X=0)=8/9, P(X=±sqrt(3))=1/18 has E[(L+X)^4]=(L^2+1)^2. This is not a simplex/B-spline counterexample.

Additional primary source inspected: Albrecht Böttcher, Stephan Ramon Garcia, Mohamed Omar, Christopher O'Neill, “Weighted means of B-splines, positivity of divided differences, and complete homogeneous symmetric polynomials,” Linear Algebra and its Applications 608 (2021), 68–83, https://doi.org/10.1016/j.laa.2020.08.018; author manuscript https://arxiv.org/abs/2001.01658 . Its moment representation and positivity do not by themselves exclude proper powers.

## 6. Reproduction

Run check.py and python -O check.py. The checks verify exact barycentric symbols, the divided-difference identity, sample squarefreeness, and the missing-center formula. Their finite range is an implementation check; Sections 1–3 provide all-degree proofs.
