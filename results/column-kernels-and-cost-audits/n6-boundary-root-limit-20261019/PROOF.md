# An exact limit of the extreme-root test in the first residual size

19 October 2026. Separate continuation after freezing the structural theorem package. This gives an exact algebraic boundary-value zero on the residual resonance locus, and proves that the corresponding full polynomial is nevertheless nonzero. Thus it refutes a proposed proof shortcut, not the target nonvanishing statement.

## 1. A whole resonant one-parameter family

Take n=6, masked rows i=0,p=5, masked column c=3, and

    a=(0,t,1/3,2/3,1-t,1),  0<t<1/3,
    e=(0,1,2,3,4,18).

The offsets are distinct and increasing, with both masked rows extreme. The four interior offsets occur in pairs summing to 1, so

    R=1, sum a=3=6(a_0+a_5)/2.

Also sum e=28=6e_3+binom(5,2), since e_3=3. Thus every member of this family satisfies all three prior simultaneous-resonance conditions and lies in the first still-unclosed rank pattern.

## 2. The extreme-root value really can be zero

At L=0, expand the masked determinant P along its first row's exponent-zero entry, and factor x from each remaining row. The positive nodes are

    X=(t,1/3,2/3,1-t,1),

and the remaining exponent list is r=(0,1,2,3,17), with the entry at row 4,column 2 zeroed. Let B be the unmasked 5-square matrix, and C its signed row-4,column-2 Laplace term. The sign is positive.

For Y=(t,1/3,2/3,1-t), let h_j(Y) denote the complete homogeneous symmetric polynomial. Generalized Vandermonde/Schur identities give

    det B = Delta(Y) [product_(y in Y)(1-y)] h_13(Y,1),
    C = Delta(Y) [h_14(Y)h_1(Y)-h_15(Y)].

Here h_1(Y)=2 and product(1-y)=product y=2t(1-t)/9. Also h_13(Y,1)=sum_(j=0)^13 h_j(Y). Therefore, putting q=t(1-t),

    det B-C = Delta(Y) Z(q),
    Z(q)=(2q/9) sum_(j=0)^13 h_j(Y)-2h_14(Y)+h_15(Y).

The generating function for these h_j is

    sum_(j>=0) h_j(Y) z^j
      =1/[(1-z+q z^2)(1-z+(2/9)z^2)].

Consequently the exact degree-seven polynomial is

    Z(q) = -G(q)/4782969,

    G(q)=23914845 q^7 - 96722262 q^6 - 311660622 q^5
         +1403896536 q^4 -1763300097 q^3 +989902134 q^2
         -259912971 q +21435980.

Exact evaluations are

    Z(19/400) = -3650903964363584771691331
                  /1567283281920000000000000 < 0,
    Z(3/16) = 660577143130849/1283918464548864 > 0.

These are q=t(1-t) at t=1/20 and t=1/4. All factored quantities are positive throughout that interval. By continuity, there is a real algebraic t_* in (1/20,1/4) such that G(t_*(1-t_*))=0 and P(0)=0. This is an exact algebraic certificate that the extreme-root evaluation can vanish on the remaining resonance locus.

For comparison, independently computed raw minors give

    C/det B at t=1/20
      =21696409962886902545940437/3441890141068978687483782 >1,
    C/det B at t=1/4
      =32044941609589/70902420617286 <1.

No claim of a zero polynomial is made from this single evaluation.

## 3. The full polynomial has exact degree 15 throughout the family

In fact we can prove more: for the fixed exponent list (0,1,2,3,4,18), every symmetric six-offset configuration

    a=(-1,-v,-u,u,v,1), 0<u<v<1,

with endpoint holes in column 3 has a nonzero masked polynomial of exact degree 15. Translation and nonzero scaling preserve degree and nonvanishing, so this covers the algebraic t_* above.

Let

    C_0=(-1)^(0+3) Delta(a without a_0),
    H_0(L)=(L-1)^3 s_(14,1)(L+a_s:s!=0).

Thus the full column Laplace term is T_0=C_0 H_0. This C_0 is the raw Vandermonde prefactor; it is not the normalized leading coefficient used in the prior package. Symmetry gives C_5=-C_0 and H_5(L)=H_0(-L), since H_0 is homogeneous of total degree 18 in the shifted variables. Therefore

    T_0+T_5=C_0[H_0(L)-H_0(-L)].                   (1)

The Schur identity s_(14,1)=h_14 h_1-h_15 gives

    H_0(L)=(L-1)^3[(5L+1)h_14(L+A)-h_15(L+A)],
    A=(-v,-u,u,v,1).

Put Q=u^2+v^2. Then

    h_0(A)=1, h_1(A)=1,
    h_2(A)=1+Q, h_3(A)=1+Q.

For five variables the exact shift formula is

    h_r(L+A)=sum_(ell=0)^r binom(r+4,r-ell)
                            h_ell(A) L^(r-ell).

Writing B(L)=(5L+1)h_14(L+A)-h_15(L+A), its first four coefficients, in degrees 15,14,13,12, are respectively

    11424,
    34272,
    65688 Q+74256,
    127296 Q+127296.

Multiplication by (L-1)^3 now gives

    [L^17]H_0=34272-3*11424=0,
    [L^15]H_0=-69768 Q-4080 < 0.                   (2)

Equation (1) cancels every even degree. The possible degree 17 also vanishes by (2), while degree 15 survives. The complete unmasked alternant has degree

    sum e-binom(6,2)=28-15=13.

Since P=det V-T_0-T_5, it follows that

    deg P=15,
    [L^15]P=2 C_0(69768(u^2+v^2)+4080),            (3)

which is nonzero because C_0 is nonzero. This proves that the algebraic boundary zero from Section 2 is never a zero polynomial.

## 4. Exact failed lemma and resume condition

False lemma: in every remaining n=6 simultaneous-resonance case, the reduced extreme-root value is nonzero or has a fixed sign. Sections 1--2 give a rigorous counterexample to that lemma, with algebraic offsets specified by an explicit polynomial and a rational interval certified to contain a root.

The actual full-polynomial nonvanishing question remains open for arbitrary exponent lists in the remaining n>=6 odd off-diagonal rank regime. Section 3 settles only the displayed fixed exponent list over its entire symmetric offset family. A future proof must control later root coefficients, later asymptotic coefficients, the complete polynomial, or constant-kernel geometry; it cannot simply extend the already-proved root-value sign tests.
