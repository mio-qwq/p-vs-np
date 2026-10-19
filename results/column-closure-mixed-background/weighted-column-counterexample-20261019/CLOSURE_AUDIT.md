# Independent audit: three-row column-certificate closure

19 October 2026. Outcome: **PASS**. No correction to the audited proof is required.

## Audited artifact

- Proof: `/workspace/shared/column-certificate-closure-20261019/PROOF.md`
- Proof SHA-256: `ad583b0269795550bc008d28a9ed79cef1a8c621ae5a9e572d5ae9c6c27a0730`
- Exact checker: `/workspace/shared/column-certificate-closure-20261019/check.py`
- Recorded results: `/workspace/shared/column-certificate-closure-20261019/results.json`

## Independent derivation checks

1. Reconstructed the canonical three-by-three determinant with column-zero mask `(1,0,1)` and column-one weights `(2,1,2)`. Its determinant is identically zero. The three column-one contributions are `t^3-t^2`, `4t^2`, and `-t^3-t^2`, and the positive relation is exactly `2S_0+S_1+2S_2=0`. All three contributions are nonzero and supported by perfect matchings. This refutes existence of *any* strictly positive linear functional on that masked background, rather than merely invalidating a previously selected functional.

2. Checked all three full-background functional formulas. Each gives value one on every signed Laplace term of its own column. The two operations therefore each preserve noncancellation separately, as stated.

3. Independently checked the six matching signs and the complete nonnegative cone proof. For gaps `h,k>0`, evaluation at `t=0` gives `hk^2 C+h^2k D`; nonnegativity forces `C=D=0`. The remaining polynomial divided by t has equations

       k^2 A-h^2 F=0,
       2k A-k B-h E+2h F=0,
       A-B+E-F=0.

   Their full nonnegative solution set is exactly

       lambda(h^2,h(h+k),0,0,k(h+k),k^2), lambda>=0.

   This argument includes the zero ray and uses no numerical or generic-position assumption.

4. Checked all three maps from two-column weights to the six matching coefficients. For feasible support, the nonzero cone ray forces exactly the two asserted cancellation families:

       columns 0,1: u=p(h^2,0,k^2), v=q(h(h+k),hk,k(h+k));
       columns 0,2: u=p(h,0,k), v=q(k,h+k,h),

   with `p,q>0`. Substitution verifies sufficiency. Necessity uses only ratios of coordinates already proved strictly positive. The zero-ray case has no feasible support and is correctly excluded.

5. With column zero full, the nonzero ray would force `u_1,v_0,v_2>0`, then `u_0=u_2=0`, contradicting positivity of its B and E coordinates. Thus the claimed limited closure theorem for arbitrary nonnegative weights in columns one and two is valid.

6. A nonzero binary relation would require all four positive ray entries equal, but `B/A=(h+k)/h>1`. Consequently every nonempty matching subset is nonzero. This correctly covers binary supports and color-count fibers in this three-row consecutive-exponent setting; it does not promote the weighted relation to a binary counterexample.

7. Verified common consecutive-exponent shifts by the nonzero common row factor, and row/column permutation invariance. The two-row minimality argument is correct because the ratio of the two distinct translated-power matching terms is a nonconstant rational function whenever offsets and exponents are distinct.

## Executed checks

- `python /workspace/shared/column-certificate-closure-20261019/check.py`: PASS.
- `python -O /workspace/shared/column-certificate-closure-20261019/check.py`: PASS.
- Independently reconstructed the displayed zero determinant using the separate standard-library polynomial/permutation routine in this directory's `check.py`: PASS, in normal and optimized modes.
- The partner checker reports 6,561 bounded integer-weight cases, 315 nonempty binary matching subsets at exact rational gaps, exact named identities, and three corrupted-certificate controls. These tests support the proof; the universal conclusions rely on the cone derivation and ratio arguments above.

## Scope and disposition

The full-background arbitrary-exponent nonnegative one-column conjecture is unchanged. The audited result is a minimal weighted closure obstruction plus a complete three-row consecutive-exponent classification, not a general sparse noncancellation theorem. No P-versus-NP conclusion follows. No remote action was taken.
