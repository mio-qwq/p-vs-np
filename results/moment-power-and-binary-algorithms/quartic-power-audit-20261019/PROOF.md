# Degree-eight complete homogeneous polynomials are not quartic squares

19 October 2026. Exact algebraic certificate; local research only.

## Theorem

Let n >= 2 and let a_1,...,a_n be real numbers that are not all equal. Then

    h_8(L+a_1,...,L+a_n)

is not a nonzero scalar multiple of the square of a quartic polynomial, even over C.
Every proper exponent of a degree-eight polynomial divides eight and is even, so every such power is a quartic square. Thus this excludes every proper power of H_8. Distinctness is unnecessary. This statement does not assert squarefreeness.

The proof below reduces to explicit rational polynomial positivity. The accompanying `check.py` derives the power sums from the quartic square, checks every identity, and verifies every coefficient certificate exactly. Its inequalities do not use floating-point arithmetic, numerical optimization, sampling, or unproved root isolation.

## 1. Center, scale, and recover knot power sums

Translate and positively rescale the offsets to arrange

    p_1=sum a_i=0,     p_2=sum a_i^2=1.

These changes preserve whether the monic normalization is a quartic square. With U uniform on the probability simplex and A=sum U_i a_i, the monic normalization is

    P(L)=E[(L+A)^8].

It is strictly positive for real L. If P=Q^2 for monic quartic Q over C, uniqueness of the monic square root and conjugation give real coefficients. The vanishing L^7 coefficient gives

    Q=L^4+bL^2+cL+d.

The coefficient identities give

    h_k(a) = [L^(8-k)](Q^2) (n)_k / (8)_[k],
    p_k = k h_k - sum_(j=1)^(k-1) p_j h_(k-j).

In particular b=14/[n(n+1)], c=56p_3/[n(n+1)(n+2)], and the p_4 identity determines d. Put

    x=p_3,    y=p_4,    z=x^2.

Substitution yields

    p_5=k x,
    p_6=e z+f y+g,
    p_8=h y^2+i y+j-l z,

where the following coefficients depend only on n:

    k=(n^2+22n+42)/(3n(n+1)),
    e=(3n^3+51n^2+216n+280)/(5n(n+1)(n+2)),
    f=(n^2+15n+35)/(n(n+1)),
    g=-(n^4+44n^3+491n^2+1624n+1470)/(15n^2(n+1)^2),
    h=(17n^4+382n^3+3127n^2+11162n+14700)
        /(2n(n+1)(n+2)(n+3)),
    i=-(n^6+105n^5+2236n^4+20121n^3+87205n^2+175056n+123480)
        /(3n^2(n+1)^2(n+2)(n+3)),
    j=(n^8+36n^7+1186n^6+22196n^5+212774n^4+1071874n^3
        +2822309n^2+3588564n+1728720)
        /(30n^3(n+1)^3(n+2)(n+3)),
    l=4(3n^3+44n^2+167n+196)/(15n(n+1)(n+2)).

All of k,e,f,l are positive, g<0, and h>1.

## 2. Necessary real-knot inequalities

Elementary Cauchy and expansion of squares give

    z=p_3^2 <= p_2 p_4=y,
    p_5^2 <= p_4 p_6,
    p_6^2 <= p_4 p_8,
    p_8 <= p_4^2=y^2.

For the last inequality, expand (sum a_i^4)^2; all cross terms are nonnegative. The preceding inequality is Cauchy applied to a_i^2 and a_i^4.

Define

    y0=-g/f,
    F(y)=(h-1)y^2+i y+j,
    J(y)=F(y)-l y,
    G(y)=F(y)(k^2-e y)-l(f y^2+g y),
    R(y)=e F(y)/l+f y+g.

One has

    k^2-e y0
      =(16n^7+976n^6+22726n^5+241759n^4+1212670n^3
         +3056998n^2+3783780n+1852200)
        /(225n^2(n+1)^2(n+2)(n^2+15n+35)) > 0.

The inequality p_5^2<=y p_6 becomes

    (k^2-e y)z <= y(f y+g).

If y<y0, the right side is negative and the left side is nonnegative. Thus

    y>=y0.                                                     (1)

Also p_8<=y^2 implies l z>=F(y), and z<=y then implies

    J(y)<=0.                                                   (2)

The same inequality gives p_6>=R(y). Meanwhile p_6^2<=y p_8<=y^3 and p_6>0, so

    R(y)<=p_6<=y^(3/2).                                        (3)

Finally, whenever k^2-e y>0, combining lz>=F(y) with the p_5 inequality gives

    G(y)<=0.                                                   (4)

## 3. Large-n certificate: n>=24

Let

    T(y)=R(y)^2-y^3.

The exact certificate is as follows. For each q=0,1,2,3,4, write the reduced rational function

    [u^q] T(y0+u)

as a numerator polynomial in n divided by a denominator polynomial. The denominators are positive for n>0. After substituting n=24+v, every coefficient of every numerator polynomial is strictly positive. The same holds for the numerator of R(y0).

The checker verifies these finite symbolic claims and writes the complete positive coefficient lists to `certificate.json`. Thus for every real n>=24 and every u>=0, T(y0+u)>0 and R(y0)>0. Since T has no zero on [y0,infinity), continuity shows R cannot change sign on that interval: R=0 there would give T=-y^3<0. Therefore

    R(y)>y^(3/2)  for all y>=y0,

contradicting (1) and (3).

## 4. Finite-n certificate: 4<=n<=23

For each of these twenty integer values, put

    U=3/n+1/10.

The checker verifies the following strict rational inequalities:

    U>y0,
    J(U)>0,
    J'(U)>0,
    k^2-e U>0.

Since the leading coefficient h-1 of J is positive, J is strictly increasing on [U,infinity) and positive there. Thus (2) forces y<U. Together with (1), this gives y0<=y<U and k^2-e y>0.

For each of the twenty n, the checker additionally verifies that all four coefficients of the cubic polynomial

    (1+t)^3 G((y0+U t)/(1+t))

are strictly positive rational numbers. They are listed in `certificate.json`. Every y in [y0,U) can be written as (y0+Ut)/(1+t) for a unique t>=0. Therefore G(y)>0 throughout this interval, contradicting (4).

## 5. n=2 and n=3

For two or three centered real knots, p_4=p_2^2/2=1/2. This follows from Newton's identities, with e_1=e_4=0 and e_2=-p_2/2. Direct substitution gives y0>1/2 for n=2 and n=3. This contradicts (1).

All n>=2 are now excluded. The sole degenerate exception excluded by hypothesis is when all offsets coincide; then H_8 is a scalar eighth power of a linear polynomial.
