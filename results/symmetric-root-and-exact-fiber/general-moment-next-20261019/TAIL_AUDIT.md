# Independent rational-tail proof of the coefficient lemma

19 October 2026. This is an optional independent proof, not an assumption in the main manuscript.

Let C(y)=sum_(j=0)^m a_j y^j have positive coefficients, a_0=a_1=1, and assume a_j(2j)! is log-concave. Its first two normalized values are 1 and 2; nonincreasing ratios give

    0<a_j<=2^j/(2j)!,  j>=2.

At y=-2, bound all terms after the linear term by their absolute values:

    C(-2)<=-1+sum_(j=2)^infinity 4^j/(2j)!.

The first summand is 2/3. For j>=2 the next-to-current ratio is

    4/[(2j+1)(2j+2)]<=2/15.

Thus the entire positive tail is at most (2/3)/(1-2/15)=10/13, giving C(-2)<=-3/13<0.

For 0<=x<=2, similarly

    C'(-x)>=1-sum_(j=2)^infinity j 4^j/[2(2j)!].

Again the first summand is 2/3, and successive ratios are

    4(j+1)/[j(2j+1)(2j+2)]=2/[j(2j+1)]<=1/5.

The derivative tail is therefore at most (2/3)/(1-1/5)=5/6, giving C'(-x)>=1/6>0.

Consequently C has a unique simple real root on (-2,0). If an even polynomial A(z)=sum b_j z^(2j)/(2j)! has positive log-concave b_j, the rescaling

    C(y)=A(sqrt(2b_0 y/b_1))/b_0

is a polynomial (the square-root notation denotes substitution in an even polynomial), has a_0=a_1=1, and satisfies the required coefficient condition. Its negative simple root produces a simple imaginary pair of A.

This proof uses only exact rational estimates. The main alternating-pair proof is shorter and gives a sharper root-location bound; this independent argument confirms the simple-root/no-proper-power conclusion without depending on alternating-tail cancellations.
