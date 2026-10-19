# Independent audit of the three companion branches

19 October 2026. All checks in this branch were local. External source attribution was not re-browsed; the accepted mathematical arguments below are self-contained.

## Verdict

The following mathematical statements are approved with their stated scopes. None establishes the unresolved arbitrary-real-offset no-proper-power theorem for composite half-degrees with base degree at least four.

### 1. General quadratic-base obstruction

Reviewed `/workspace/shared/general-power-obstruction-20261019/PROOF.md`.

Approved:

- For n>=2 nonconstant real offsets and every s>=2, h_(2s)(L+a) is not a scalar multiple of a quadratic polynomial raised to the s-th power.
- Hence h_d has no proper polynomial power when d/2 is prime.
- The existing one-gap ODE reduction therefore proves full complex kernel exclusion in those degree families.

Independent derivation: the proposed coefficient ratio is exactly equivalent to

    ((s+1/2)theta-theta^2)B
      =c z[theta^2+(n+1/2)theta+n(n+1)/4]B
      modulo z^(s+1),

where theta=z d/dz. Dividing by B and setting R=theta B/B gives the displayed Riccati recurrence. Its top coefficient has a positive remainder and contradicts p_(2s)<=p_2 p_(2s-2). The s=2 and s>=3 factors of two in the written proof are correct. The odd-moment elimination, positivity c>0, finite truncation, and real-root argument for the prime-half-degree corollary are all justified.

Boundary: degree>=4 bases remain untreated; this is not a squarefreeness theorem. No span or sign claim is made for residual cases.

### 2. Unit-circle barycentric-symbol criterion

Reviewed Sections 1--4 of `/workspace/shared/translated-power-root-analysis-20261019/ROOT_GEOMETRY.md`.

Approved:

- If the integer-knot barycentric shift symbol has all roots on the unit circle, every translated H_d has only simple roots on the specified vertical line, for every d>=1.
- Arithmetic-progression knots and an even equally spaced grid with its center removed satisfy this criterion.
- The nonarithmetic central-deletion family is correctly derived.
- The generic squarefreeness consequence follows because the discriminant is polynomial in the offsets and is nonzero on the arithmetic-progression specialization.

The finite-difference modulus comparison is strict off the output line. On that line, the logarithmic-derivative difference is the strictly positive sum stated in the note, proving simplicity. The exact n-1 multiplicity of the symbol root at 1 follows from barycentric moments. There are exactly n-1 degree-lowering factors; d>=1 ensures no constant-input/output exceptional step. The scale factors h^d and the line location are correct.

Boundary: arbitrary lattice knots need not meet the unit-circle-symbol hypothesis. The proof does not show arbitrary symmetric knots have imaginary roots. Primary-source bibliographic details were not independently reverified in this local-only audit; the self-contained proof suffices for the theorem.

### 3. Exact root-geometry limits

Reviewed `/workspace/shared/power-obstruction-limits-20261019/RESULT.md` and its generic-moment supplement.

Approved:

- The n=9,d=6 algebraic-knot example has multiplicity pattern (2,2,1,1), with the outer imaginary pair double.
- The distinctness interval, discriminant polynomial, monotonicity, exact factorization modulo the defining polynomial, and strict ordering r<s<0 all check.
- The integer-knot example has four off-axis roots, established by a negative nonzero cubic discriminant in L^2.
- Neither example is a proper power or a kernel counterexample.
- The positive compact atomic measure in the supplement does give the degree-eight proper-power moment polynomial claimed; this only refutes generic-positive-measure/Hankel-positivity routes, not the simplex/B-spline statement.

Independent check in this directory recomputes the algebraic example's coefficients from its generating function, recomputes the discriminant rather than trusting a printed factorization, checks the isolating interval, and verifies coefficientwise divisibility by the defining polynomial. Exact signs imply the factorization has two double and two simple nonreal roots. Thus a generic squarefreeness or outer-root-simplicity proof is unavailable.

## New result and independent reviewers

`RESULT.md` in this directory proves a general multiplicity bound and the prime-(n-1) kernel corollary. The parent researcher and both constructive partners independently approved its circle/Vandermonde proof. The translated-root partner also independently approved the stronger bound mult_H(zeta)<=floor(n/2) for nonreal zeta.

The exact span criterion in Section 4 is an algebraic necessary-and-sufficient condition, checked against direct coefficient ranks. It is not advertised as a universal obstruction. Its automatic-membership case t=m is an important boundary for future work.

## Reproduction

The local `check.py` uses explicit exceptions and passes normal Python and python -O. The three companion checkers were also run in both modes. Finite implementation checks support algebraic identities; the universal quantifiers come from the proofs.

## Addendum: eventual simple roots for every fixed offset tuple

Reviewed the full `/workspace/shared/translated-power-root-analysis-20261019/EVENTUAL_SIMPLE_ROOT.md` after the core audit.

Approved: for every fixed n>=2 tuple of distinct real offsets, H_d has a simple root for every sufficiently large d. The proof's threshold depends on the offset geometry. It follows that, for that fixed tuple, only finitely many even d can remain in the one-gap kernel problem.

Independent derivation agrees with the written argument: after normalizing the extreme knots to -1 and 1 and taking N=m+d, H_d(w/N) converges locally uniformly along even d to A exp(-w)+B exp(w). Interior-knot terms vanish exponentially. Each chosen zero of that entire limit is simple and isolated; Rouche's theorem gives exactly one nearby zero counted with multiplicity for every sufficiently large even d. Odd d is already covered by the real simple root.

The effective threshold in the note is correct. For radius pi/4, |sinh(u)|>=2|u|/pi implies the boundary lower bound sqrt(AB). The first threshold gives both N>=2W and the interior contraction sigma. The logarithm-series tail is at most W^2/N, and exp(t)-1<=2t for 0<=t<=1 gives the endpoint error. The stated remaining bounds make each error at most sqrt(AB)/4, leaving a strict Rouche margin. The root asymptotic in the original coordinates uses the correct midpoint and half-range scaling. Nested disks imply convergence to the chosen limiting root, hence the stated o(1/d) remainder.

This is an all-sufficiently-large-degree theorem for each fixed tuple; it is not a uniform-in-offsets degree threshold, not a proof for all even d, and not a complexity-theoretic result.
