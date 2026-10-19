# Compact positive moment measures can produce a proper power

This supplement identifies another boundary of possible global arguments. It is **not** a counterexample for uniform-simplex projections or translated complete homogeneous polynomials.

Let y_1<y_2 be the two roots of

    47 y^2-1890 y+5390=0,
    y_1=(945-sqrt(639695))/47,
    y_2=(945+sqrt(639695))/47.

Direct sign checks show

    3<y_1<16/5<37<y_2<38.

Put v=16/5 and define

    w_1=(y_2-v)/(y_1(y_2-y_1)),
    w_2=(v-y_1)/(y_2(y_2-y_1)),
    w_0=1-w_1-w_2=9126/13475.

Every weight is strictly positive. Define a symmetric compactly supported probability law X with mass w_0 at zero, mass w_1/2 at each of +/-sqrt(y_1), and mass w_2/2 at each of +/-sqrt(y_2).

The first two squared-variable moments are E[X^2]=1 and E[X^4]=v by construction. Since each y_i satisfies y_i^2=(1890/47)y_i-5390/47, the higher even moments satisfy the same recurrence:

    E[X^6]=(1890/47)(16/5)-5390/47=14,
    E[X^8]=(1890/47)14-(5390/47)(16/5)=196.

All odd moments vanish. Therefore the exact identity is

    E[(L+X)^8]
      =L^8+28L^6+224L^4+392L^2+196
      =(L^4+14L^2+14)^2.

This example shows that bounded support, nondegeneracy, symmetry, positivity of the measure, and the corresponding positive-semidefinite moment matrices do not exclude a proper-power moment polynomial. Some specifically simplex/B-spline or sufficiently strong density-shape property is necessary for any such route. This atomic law is not a log-concave density and does not test the stronger log-concavity conjecture.

The identity is included in check.py and checked exactly. No claim of matching any real offset list is made.
