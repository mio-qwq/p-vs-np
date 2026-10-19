# Complete constant-kernel classification for one missing degree

19 October 2026. A scoped structural result for one-column noncancellation. This is not an arbitrary-graph theorem, a complexity conclusion, or a claim of historical novelty.

## Theorem

Let n>=3, let the offsets a_s be distinct real numbers, and let the sorted column exponents be

    e=(d,d+1,...,d+n-2,d+n), d>=0.

Fix the column c=1 (the second-smallest exponent). Let T_s(L) be its signed full-matrix Laplace term, including its entry. Center the offsets:

    b_s=a_s-(sum a)/n,
    h(t)=product_s(t-b_s), f(x)=product_s(x+b_s).

Then the real vector space of constant vectors w satisfying sum_s w_s T_s(L)=0 identically is:

- zero, unless every b_s is nonzero and f'(0)=0;
- exactly one-dimensional in that exceptional case, spanned by

      w_s=h'(b_s)/b_s.

Every nonzero vector in the exceptional kernel has both positive and negative coordinates. Consequently, replacing column c entry s by any fixed nonnegative weight w_s times its original value gives a nonzero polynomial determinant whenever at least one weight is positive. This includes every nonempty binary retained-row mask of that column.

In particular, symmetric distinct nonzero centered offsets in every even size n>=4 give an explicit one-dimensional signed dependence. Thus full cofactor linear independence fails in infinitely many sizes, while nonnegative-kernel exclusion remains true in this family.

## 1. Exact interpolation identity

The common exponent shift d contributes the same nonzero factor product_s(L+a_s)^d to every T_s, so it has no effect on the kernel. Translate L by the mean offset and reduce to d=0 and sum b_s=0. Put x=L+mean(a), t_s=x+b_s, and Delta(b)=product_(r<s)(b_s-b_r), using the actual row order.

The full alternant with powers 0,1,...,n-2,n has determinant

    det V = Delta(b) sum_s t_s = n x Delta(b).

For a generic x != 0, let F_x(t)=product_s(t-t_s). The polynomial space spanned by the columns omits t^(n-1). The cardinal polynomial at t_s in this space is

    q_s(t) = F_x(t)/[(t-t_s)h'(b_s)]
             + F_x(t)/[n x h'(b_s)].

It equals one at t_s and zero at the other nodes. The coefficient of t^(n-1) is zero, because that coefficient in F_x is -sum_s t_s=-n x. Thus its coefficient of t is (V^(-1))_(1,s).

The coefficient of t in the two summands gives

    T_s/[(-1)^(n-2) Delta(b)]
      = [((n-1)x-b_s) f'(x) - n x f(x)/(x+b_s)]/h'(b_s).    (1)

For example, before simplification its numerator is

    n x t_s e_(n-2)(t_except_s) - t_s e_(n-1)(t_all).

Use t_s e_(n-2)(t_except_s)=f'(x)-f(x)/(x+b_s) and e_(n-1)(t_all)=f'(x) to obtain (1). Each quotient f(x)/(x+b_s) is a polynomial. The derivation is valid for generic x and therefore proves the polynomial identity for every x, including x=0.

## 2. Necessary conditions and complete kernel

For a putative kernel vector define

    A0=sum_s w_s/h'(b_s),
    A1=sum_s w_s b_s/h'(b_s),
    H(x)=sum_s w_s/[h'(b_s)(x+b_s)].

Summing (1) gives the exact identity

    sum_s w_s T_s/[(-1)^(n-2) Delta(b)]
      = ((n-1)x A0-A1) f'(x) - n x f(x)H(x).       (2)

Its x^n coefficient is n(n-2)A0. Since n>=3, every kernel vector must satisfy A0=0. Equation (2) then requires

    H(x)=-(A1/n) f'(x)/[x f(x)].                   (3)

If A1=0, the distinct simple poles of H show every w_s=0. A nonzero kernel therefore has A1!=0.

If some b_s=0, f has a simple zero at x=0, and the right side of (3) has a double pole there; H has only simple poles. This is impossible. If no b_s=0, H is regular at x=0, so (3) forces f'(0)=0.

Taking residues of (3) at x=-b_s now gives

    w_s/h'(b_s)=A1/(n b_s).

Every kernel vector is therefore a multiple of the displayed candidate. Conversely, when all b_s!=0 and f'(0)=0, logarithmic differentiation at zero yields sum_s 1/b_s=0. For w_s=h'(b_s)/b_s,

    A0=0, A1=n,
    H(x)=sum_s 1/[b_s(x+b_s)]
        =(1/x)[sum_s 1/b_s-sum_s 1/(x+b_s)]
        =-f'(x)/[x f(x)].

Substitution into (2) proves the candidate is a kernel vector. This establishes the exact dimension and all necessity/sufficiency claims.

## 3. Why every nonzero kernel vector has mixed signs

Sort b_0<...<b_(n-1). Then h'(b_s) has alternating sign (-1)^(n-1-s). Centering ensures both negative and positive b_s occur. With n>=3, at least one of those two sign groups contains two adjacent offsets. For that adjacent pair the denominator b_s has the same sign while h'(b_s) has opposite signs. Their weights h'(b_s)/b_s therefore have opposite signs. Multiplication by a nonzero real scalar preserves mixedness.

This proves nonnegative-kernel exclusion without assuming full linear independence, positivity of signed cofactor coefficients, or a generic-offset specialization argument.

## 4. Explicit certificates and boundaries

- n=4, b=(-3,-1,1,3): the kernel is spanned by (1,-1,-1,1), matching the prior certificate.
- n=6, b=(-5,-3,-1,1,3,5): it is spanned by (6,-2,3,3,-2,6).
- n=8, b=(-7,-5,-3,-1,1,3,5,7): it is spanned by (45,-9,5,-9,-9,5,-9,45).
- Centered offsets containing zero necessarily give full rank in this exponent family, regardless of other symmetry.
- The theorem does not include arbitrary exponent sets or arbitrary multi-column masks. The broader no-nonnegative-constant-kernel conjecture is still unresolved here.

The checker verifies the rational polynomial identity by an independent raw-minor construction, the asserted exact ranks, both exceptional and nonexceptional cases, common exponent shifts, and a nonsymmetric algebraic exceptional n=5 example. The proof above, rather than the finite checks, establishes the infinite family.
