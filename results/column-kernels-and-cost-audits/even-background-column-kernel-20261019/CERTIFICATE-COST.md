# Exact coefficient realization and bit cost of the positive functional

19 October 2026. This supplements Section 6 of `PROOF.md`. It concerns rational offsets and the odd distinguished-power branch. The theorem itself allows arbitrary distinct real offsets.

## 1. A residue is an ordinary rational coefficient functional

Let `Q(z)=K B(z)` be the fixed denominator in equation (9). Fix a pole location alpha and let m be its multiplicity as a root of Q. Write

    Q(alpha+t)=t^m Q_0(t),    Q_0(0)!=0.

For every polynomial P,

    Res_(z=alpha) P(z/2)/Q(z)
      = [t^(m-1)] P((alpha+t)/2)/Q_0(t).          (11)

The reciprocal power series of Q_0 need only be computed through degree m-1. If `Q_0(t)=q_0+q_1 t+...` and its reciprocal coefficients are v_j, they satisfy

    v_0=1/q_0,
    v_j=-(1/q_0) sum_(i=1)^j q_i v_(j-i).

Thus (11) is a finite exact rational computation, linear in the coefficients of P. Evaluating it on the monomials gives a coefficient vector for the functional. It remains valid when multiple pairs have the same sum. The inadmissible shortcut `P(alpha)/Q'(alpha)` is not used for a repeated root.

For B, each equal-sum class consists of disjoint pairs, so m is at most floor(n/2). The individual quotients T_s(z/2)/Q(z) have only simple poles, but (11) correctly defines the functional on the whole polynomial space, including polynomials whose quotient has a higher-order pole.

## 2. Effective polynomial-size rational certificate

Suppose each offset numerator and positive denominator has at most b bits. Work first after removing the common exponent shift. Put

    S=(n-1)(n-2)+k,
    D=max(2,S,n^2).

Every T_s has degree at most S and Q has degree binomial(n,2). Rational coefficients of the raw T_s and Q have bit length bounded by a polynomial in n, D, and b. More explicitly, a common denominator for every translated monomial term is obtained from the offset denominators to power S. Raw determinant expansion bounds the numerator by a factor n! times products of binomial coefficients and translated-node powers. A conservative coefficient-height bound is

    H=O(n D (b+log(n+D))).

This bounds numerator and denominator bit lengths separately; cancellation can only reduce them. The pair locations have O(b) bits. The explicit beta residues in equation (4) have O((k+n^2)(b+log n)) bits, hence satisfy the same conservative H bound after enlarging its absolute constant.

For completeness, a general bound for constructing (11) is enough. If Q has degree at most D and coefficient bit lengths at most H, and alpha has A bits, translating Q and clearing a common coefficient denominator gives bit length

    O(D(H+A+log(D+2))).

Computing the first D reciprocal-series coefficients uses powers of the one nonzero constant coefficient, so their bit lengths are

    O(D^2(H+A+log(D+2))).

Evaluation on the degree-at-most-D monomials and normalization by beta are polynomial-size rational operations. Computing each value r_(j,s) by a coefficient dot product adds at most another factor O(D) to these conservative bit bounds. There are n(n-1) such values. Taking their exact maximum absolute value selects one of these rational values; it does not require numerical approximation.

The epsilon in equation (10) therefore has polynomial bit length. Raising it to powers at most n-2 multiplies this bound by at most n. Combining n-1 rational coefficient vectors multiplies it by at most another n, even if denominators are naively multiplied before reduction. In particular the final coefficient certificate has polynomial size in n, S, and b. One deliberately loose bound on each output numerator/denominator is

    O(n^3 D^4 (b+log(n+D))) bits.

All the displayed constructions use polynomially many additions, multiplications, exact divisions, and comparisons on integers of polynomially bounded length. Schoolbook integer arithmetic consequently gives a deterministic polynomial bit-cost algorithm. No polynomial-identity-testing oracle, floating-point positivity test, or unbounded-precision arithmetic model is assumed.

## 3. Common shifts and the broader parity theorem

If every exponent is shifted by d, first divide the input polynomial by the known common factor `product_s(L+a_s)^d` on its divisible subspace, then apply the functional above. This is a linear operation. Ordinary exact polynomial long division implements it with a cost polynomial in the enlarged degree and offset bit lengths. To define a functional on the whole ambient polynomial space, compose with the quotient map in division by that fixed monic polynomial; on the relevant divisible subspace the remainder is zero.

The same triangular construction works for the broader parity-background theorem when `ell=k-h>=0` is odd. Replace Q by its common factor `(-1)^(n-1+c) G(L) Delta(y)` and normalize each residue at `tau_0j` by `Res R_0`. Its Schur argument proves that this normalizing residue is nonzero. The ordering argument gives exactly the same triangular values and epsilon estimate. If Q has a repeated root, formula (11), with the appropriate variable scaling, again supplies the coefficient functional. The degree and coefficient-height reasoning remains polynomial in the numerical total exponent sum and offset bit lengths.

None of these bounds is a polynomial bound in the binary encoding length of arbitrarily large exponents. Degree-dependent expansion and output size can be exponential in that shorter input representation. The certificate remains for one weighted column with full other columns; it cannot be iterated under further masks without another theorem.
