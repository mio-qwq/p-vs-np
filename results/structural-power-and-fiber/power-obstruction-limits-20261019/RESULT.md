# Exact limits of global root arguments

19 October 2026. Local adversarial research certificate.

## Result

For distinct real offsets, the translated complete homogeneous polynomial

    H_d(L) = h_d(L+a_1,...,L+a_n)

need not be squarefree. Even when the offsets are symmetric, it need not have all its roots on the imaginary axis. In an exact symmetric example, both roots with maximal imaginary magnitude are double.

These statements block three stronger proposed routes to the no-proper-power conjecture. They do **not** refute the no-proper-power conjecture: the examples below retain simple roots. They also do not supply a Laplace-family kernel or any nonnegative/binary sparse cancellation. An actual kernel requires the additional shifted-power span condition, and its signs need a separate check.

## 1. A single one-parameter family

Take n=9, d=6 and the symmetric knots

    (-1,-3t,-2t,-t,0,t,2t,3t,1),       0<t<1/3.

Put u=t^2 and y=L^2. Then

    H_6(L)=F_u(L^2),
    F_u(y)=A y^3+B y^2+C y+D,
    A=3003,
    B=1001(14u+1),
    C=91(147u^2+14u+1),
    D=1408u^3+147u^2+14u+1.

To check this directly, symmetry gives

    sum h_j(a) z^j
      = 1/[(1-z^2)(1-u z^2)(1-4u z^2)(1-9u z^2)],

so h_2=1+14u, h_4=1+14u+147u^2, and h_6=D. The translation formula is

    h_6(L+a)=sum_(j=0)^6 binom(14,6-j) h_j(a) L^(6-j).

This is a structural one-parameter example, not an enumeration of low-degree power exclusions.

## 2. Exact algebraic repeated-root certificate

Define

    P(u)=12827754466u^6+6383624352u^5+1082672647u^4
         +114597802u^3+4936407u^2+164108u-236.

Exact symbolic calculation gives

    Disc_y(F_u)=364364 P(u).

Every nonconstant coefficient of P is positive, so P is strictly increasing on u>0. Moreover

    P(1/729)=-194787303798304118/150094635296999121 < 0,
    P(1/700)= 520770458873915433/58824500000000000 > 0.

Thus there is exactly one positive root u_0, and

    1/729 < u_0 < 1/700 < 1/9.

Let t=sqrt(u_0). This defines all nine offsets exactly as real algebraic numbers. The displayed interval proves that all nine are distinct.

Set

    W=833u^2+182u+2,
    r=-(74631u^3+13622u^2+1085u+32)/(91W),
    s=-(613456u^3+225939u^2+12600u-10)/(273W).

At u=u_0 there is the exact identity

    H_6(L)=3003(L^2-r)^2(L^2-s).                  (1)

For verification, r=(9AD-BC)/(2(B^2-3AC)) and s=-B/A-2r, while

    B^2-3AC=91091W>0.

Every coefficient of F_u(y)-3003(y-r)^2(y-s), after clearing denominators, is divisible by P(u). The checker verifies these polynomial identities exactly.

The formula gives r<0. The numerator defining -s is increasing for u>0 and is positive at u=1/729, hence s<0. Finally

    r-s=(389563u^3+185073u^2+9345u-106)/(273W)<0,

because its numerator is increasing and is negative at u=1/700. Thus

    r<s<0.

Consequently the roots +i sqrt(-r) and -i sqrt(-r) each have multiplicity two, while +i sqrt(-s) and -i sqrt(-s) each have multiplicity one. The double roots are the outer pair, with strictly largest absolute imaginary part. The simple roots are the inner pair.

No floating-point argument is used to establish the offsets, identity, multiplicities, or root ordering. For orientation only, u_0 is about 0.00137901867, r about -0.163536783, and s about -0.0126951876.

## 3. Rational symmetric offsets with off-axis roots

A separate exact member, after scaling, uses integer offsets

    (-30,-3,-2,-1,0,1,2,3,30).

It gives

    H_6(L)=3003L^6+914914L^4+74869977L^2+740473708.

The cubic in y=L^2 has discriminant

    -9179328219383127985355176 < 0.

Therefore it has precisely one real root and a conjugate nonreal pair. Its positive coefficients exclude nonnegative real roots. Thus H_6 has one simple imaginary conjugate pair and four roots off the imaginary axis. The discriminant is nonzero, and the constant term is positive, so H_6 itself is squarefree here.

## 4. Precise effect on proposed global routes

Refuted:

1. Every H_d with distinct real offsets is squarefree.
2. Symmetric offsets force every root of H_d to be imaginary.
3. Every H_d has a simple root of maximal absolute imaginary part, even under symmetric offsets.

Not refuted or proved:

1. Every H_d has at least one simple root.
2. Some root nearest the real axis is simple.
3. Every even-degree H_d is not a proper polynomial power.
4. The one-column nonnegative-kernel conjecture, the arbitrary-background conjecture, or any sparse noncancellation claim.

Equation (1) has root multiplicity gcd equal to one, so it is not a proper power. In the ODE reduction, the two simple roots already exclude every nonintegral exponent alpha. The example is therefore fully consistent with the existing d=6 theorem.

## 5. Reproduction

Run

    python check.py
    python -O check.py

Both modes check exact translation coefficients, discriminant, isolating signs, factorization modulo P, negativity and ordering of the y roots, integer-knot example, and its negative cubic discriminant. The checker uses explicit exceptions rather than Python assertions.
