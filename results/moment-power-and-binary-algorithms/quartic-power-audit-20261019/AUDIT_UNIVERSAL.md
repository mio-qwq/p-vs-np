# Independent audit of the universal separator certificate

The sibling derivation at `/workspace/shared/quartic-power-20261019` replaces this directory's split proof by a single rational separator. I independently reconstructed its eleven rational positivity expressions using this directory's separately derived p_5, p_6, p_8 identities. `audit_universal.py` passes normally and under `python -O`; the complete exact coefficient records are in `universal_audit_certificate.json`.

## Separator and logic

Retain the definitions k,e,f,g,h,i,j,l,y0,F,R from PROOF.md. Put

    r=(n+53)y0/(n+50),
    D(y)=k^2(fy+g)-y^2(k^2-ey),
    T(y)=R(y)^2-y^3.

The exact positive-coefficient certificate, valid for all real n>=2, establishes

    k^2-er>0,
    3ef-k^2>0,
    D(r)<0,
    all three coefficients of R(r+u) are positive,
    all five coefficients of T(r+u) are positive.

Every reduced denominator is verified as a nonzero polynomial with nonnegative coefficients in n, hence is positive for n>0. Every numerator, after n=2+v, is verified to have strictly positive coefficients. Degrees of the eleven shifted numerators are respectively 8,5,18,17,12,7,34,29,24,19,14.

For y<=r, k^2-ey>0. The necessary knot inequalities

    p_5^2<=p_4p_6,    p_4^2<=p_2p_6=p_6

and p_5=kx, p_6=e x^2+fy+g imply

    x^2 <= y(fy+g)/(k^2-ey),
    y^2 <= p_6 <= k^2(fy+g)/(k^2-ey),
    D(y)>=0.

But D'(y)=3ey^2-2k^2y+k^2f has positive leading coefficient and discriminant 4k^2(k^2-3ef)<0. Therefore D is strictly increasing on R, and y<=r implies D(y)<=D(r)<0. Contradiction.

For y>=r, positivity of the Taylor coefficients gives R(y)>0 and T(y)>0, hence R(y)>y^(3/2). The necessary inequalities p_8<=p_4^2=y^2 and p_6^2<=p_4p_8<=y^3 imply

    p_6>=R(y)>y^(3/2)>=p_6,

again a contradiction.

All inequalities follow from explicit Cauchy identities or expanding (sum a_i^4)^2. No log-concavity or distributional moment theorem is needed. The argument only needs real nonconstant knots, not distinctness or symmetry. It excludes the quartic-square form for degree eight; it does not assert squarefreeness or a general proper-power theorem in every degree. Every proper exponent in degree eight is even, so this already excludes every proper power in degree eight without a separate quadratic-base result.

Audit status: algebra, inequality direction, split coverage, denominator positivity, coefficient reconstruction, and exact certificates independently verified. The primary universal proof is preferable for presentation; this directory's distinct finite/large-n proof remains a redundant independent route.

The final sibling `PROOF.md` and standalone `check.py` were read in full after completion. Their displayed formulas match the independent reconstruction. The direct l_3<=l_2 argument for p_6<=y^(3/2), completed-square expression for D' and both exact Taylor identities are correct. Final manuscript approved within its stated degree-eight real-knot scope.
