# Independent audit

19 October 2026. The adversarial noncancellation researcher independently reviewed PROOF.md Sections 1–4 and found no defect. The universal coefficient formula was checked algebraically rather than accepted from finite examples or another review.

Checks:

1. The omitted-exponent partition has size 5k and mean exponent k+2. Distinct integrality gives C2>=10; equality would make the omitted exponents consecutive starting at k, contradicting omission of k. Thus nu>0.
2. The confluent identity has the correct factor 24 and fourth power. In A(t), the first three nonconstant coefficients are h_1/5, h_2/30, h_3/210. Expanding log A gives variance C2/30 and third cumulant C3/105. The even hyperbolic-sine factor contributes variance -1/3 and zero third cumulant, while exp(-2t) only shifts the mean. Thus the stated variance 4nu and third centered moment tau are correct.
3. Factorial-moment conversion gives alpha, beta, and alpha3 exactly as stated. Differentiated Euler homogeneity gives 3alpha3+4beta21=(5k-2)alpha and 4beta21+3gamma=(5k-2)beta with the correct normalization factors.
4. For offsets (-v,-u,u,v,1), the mixed cubic sums are p3=1, sum_(i!=j) a_i^2 a_j=2Q, and e3=-Q. These reproduce the stated quadratic and cubic Taylor coefficients. Independent symbolic elimination of alpha3, beta21, and gamma and multiplication by (L-1)^k yield

       nu(Q-2)+(tau/6)(1-5Q/2),

   hence exactly formula (1) after tau=C3/105.
5. For the explicit exponents, sum e=70, C2=350, C3=-90, nu=17/6, and tau=-6/7. The resulting coefficient is (67Q-122)/21, which vanishes at the specified admissible Q=122/67. The two positive square roots satisfy 0<u<v<1, so offset distinctness and all three resonance conditions hold.
6. Endpoint reflection removes the even powers, exponent resonance removes degree 59, and the certificate removes degree 57. The full unmasked degree is 55. Thus the claimed upper bound degree(P)<=55 follows; actual degree or identical vanishing is not established.

The package correctly stops at an obstruction to universal survival of the D-3 coefficient. It is not a full-polynomial-zero certificate, and supplies no complexity-class conclusion.
