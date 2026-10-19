# Degree-eight translated complete homogeneous polynomials are never proper powers

Date: 2026-10-19. Local research; no remote changes.

## Theorem

Let n>=2 and let a_1,...,a_n be real numbers that are not all equal. Then

    H_8(L)=h_8(L+a_1,...,L+a_n)

is not a proper polynomial power over C, even up to a nonzero scalar. Distinctness of the offsets is unnecessary.

The proof below is algebraic. Its only computer-assisted component is an exact polynomial-coefficient positivity certificate in one parameter. No numerical search, numerical root, finite sample of n, or asymptotic inference is used in the proof.

This settles degree eight. It does not settle arbitrary proper powers at other composite half-degrees.

## 1. Normalize and express the knot moments

Translate and rescale the offsets so that

    p_1=sum_i a_i=0,        p_2=sum_i a_i^2=1.

These changes preserve proper-power status. Uniform simplex coordinates U give the monic normalization

    P(L)=E[(L+sum_i U_i a_i)^8].

Because the offsets are nonconstant, P is strictly positive for real L. If P is a proper power, its monic base is real by conjugation and uniqueness, has no real roots, and therefore has even degree. Its exponent consequently divides 4. Every such representation makes P a square of a monic quartic. It suffices to exclude that case.

Suppose

    P(L)=(L^4+bL^2+cL+d)^2.                            (1)

The cubic coefficient of the quartic vanishes because [L^7]P=0. Write

    x=p_3,       y=p_4>0,       z=x^2>=0.

The generating-function identity

    sum_{m>=0} h_m(a)t^m=product_i(1-a_i t)^(-1)

and its logarithmic derivative give

    p_m=m h_m-sum_{j=1}^{m-1}p_j h_{m-j}.              (2)

Comparing the coefficients of (1) with the simplex-moment formula gives b=14/[n(n+1)], c=56x/[n(n+1)(n+2)], and determines d from p_4=y. Applying (2) yields

    p_5=k x,
    p_6=e z+f y+g,
    p_8=h y^2+i y+j-l z,                              (3)

where all the following rational functions depend only on n:

    k=(n^2+22n+42)/(3n(n+1)),

    e=(3n^3+51n^2+216n+280)/(5n(n+1)(n+2)),

    f=(n^2+15n+35)/(n(n+1)),

    g=-(n^4+44n^3+491n^2+1624n+1470)/(15n^2(n+1)^2),

    h=(17n^4+382n^3+3127n^2+11162n+14700)
         /(2n(n+1)(n+2)(n+3)),

    i=-(n^6+105n^5+2236n^4+20121n^3+87205n^2+175056n+123480)
         /(3n^2(n+1)^2(n+2)(n+3)),

    j=(n^8+36n^7+1186n^6+22196n^5+212774n^4
          +1071874n^3+2822309n^2+3588564n+1728720)
         /(30n^3(n+1)^3(n+2)(n+3)),

    l=4(3n^3+44n^2+167n+196)/(15n(n+1)(n+2)).

In particular k,e,f,l>0 and g<0 for n>=2. The checker independently reconstructs (2) from (1) and verifies every identity in (3).

## 2. Four necessary inequalities for real offsets

Cauchy–Schwarz gives

    p_5^2 <= p_4 p_6,             p_4^2 <= p_2 p_6=p_6.

Nonnegativity of a_i^4 gives

    p_8=sum_i(a_i^4)^2 <= (sum_i a_i^4)^2=y^2.

Finally, putting v_i=a_i^2>=0 gives v_i<=(sum_j v_j^2)^(1/2), and hence

    p_6=sum_i v_i^3 <= (sum_i v_i^2)^(3/2)=y^(3/2).

Thus every real-knot solution must satisfy

    k^2 z <= y p_6,       p_6>=y^2,
    p_8<=y^2,             p_6^2<=y^3.                 (4)

These inequalities do not require distinct offsets or any sign restrictions on them.

## 3. One separator works for every n>=2

Define

    F(y)=(h-1)y^2+i y+j,
    R(y)=e F(y)/l+f y+g,
    T(y)=R(y)^2-y^3,
    D(y)=k^2(f y+g)-y^2(k^2-e y),

and the positive rational separator

    r=((n+53)/(n+50))*(-g/f).                          (5)

The exact certificate in Section 4 proves all of the following for every real n>=2:

    k^2-e r>0,       3ef-k^2>0,       D(r)<0;           (6)

    every coefficient of R(r+u) is strictly positive;
    every coefficient of T(r+u) is strictly positive. (7)

We now show that neither y<=r nor y>=r is possible.

### Case 1: 0<y<=r

By (6), k^2-e y>0. Combining p_6=e z+f y+g and k^2 z<=y p_6 gives

    (k^2-e y)p_6 <= k^2(f y+g).

Using p_6>=y^2 and the positive multiplier k^2-e y then yields

    D(y)=k^2(f y+g)-y^2(k^2-e y)>=0.                 (8)

But

    D'(y)=3e y^2-2k^2 y+k^2 f
         =3e(y-k^2/(3e))^2 + k^2(3ef-k^2)/(3e)>0.

Hence D(y)<=D(r)<0 for y<=r, contradicting (8).

### Case 2: y>=r

The condition p_8<=y^2 and equation (3) give l z>=F(y). Since e,l>0, this implies

    p_6=e z+f y+g >= R(y).

Put u=y-r>=0. By (7), R(y)>0 and T(y)>0. Therefore

    p_6^2 >= R(y)^2 > y^3,

contradicting the last inequality in (4). The two cases cover every y>0, proving the theorem.

## 4. Exact positivity certificate

For each rational expression below, reduce it exactly and write it as N(n)/M(n), with the rational normalization used in check.py. Substitute n=v+2. The accompanying certificate.json records every coefficient of N(v+2) and M(v+2), in ascending order. Every coefficient is strictly positive. Therefore both N(n) and M(n) are strictly positive for every n>=2, proving all the needed signs without denominator ambiguity.

The expressions, numerator degrees, and least numerator coefficients are:

    k^2-e r                   degree 8:       16
    3ef-k^2                   degree 5:       76
    -D(r)                     degree 18:      16
    R(r)                      degree 17:      12
    R'(r)                     degree 12:      18
    R''(r)/2                  degree 7:      135
    T(r)                      degree 34:    1584
    T'(r)                     degree 29:     936
    T''(r)/2                  degree 24:    3492
    T'''(r)/6                 degree 19:    2286
    T''''(r)/24               degree 14:   18225

The exact factored denominators and the complete coefficient vectors are in certificate.json. All denominator factors are positive for n>=2; the checker additionally verifies positive coefficients for each expanded denominator after n=v+2.

The checker also verifies the exact Taylor identities for R(r+u) and T(r+u), the displayed identity for D', and all moment formulas (3). Run:

    python check.py
    python -O check.py

The proof relies on exact symbolic identities and coefficient signs, rather than any finite testing. The separator (5) is merely a convenient explicit choice; no optimality is claimed.

## 5. Status and scope

Independent audit approved the final manuscript, both case deductions, all moment identities, and the universal positivity certificate. The receipt is reproduced in AUDIT.md; its independent reconstruction and separate finite/large-n backup proof are retained in the companion audit package. The primary checker and independent universal checker both pass normally and under python -O. The real-offset degree-eight theorem is stronger than a symmetric-only result but remains degree-specific. No claim about arbitrary degrees, arbitrary backgrounds, or complexity-class separation follows from this theorem alone. No publication novelty is asserted.
