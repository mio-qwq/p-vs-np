# Independent audit

19 October 2026. Audited the current `PROOF.md` against the actual statements and arguments of `../general-omission-20261018/PROOF.md`, and read and executed `checker/check.py`.

## Verdict

**Pass.** Theorem A, Theorem B, the one-row boundary ratio, and the displayed cancellation certificate are justified under the stated hypotheses. No unresolved mathematical error was found. This is a structural nonvanishing result for the specified coloring family; the equality case of the one-row boundary remains expressly unresolved beyond its leading coefficient.

## Main checks

- **Exact identity and feasibility.** Changing the single entry adds `(z−1)(Λ+a_p)^(e_c)` times its cofactor; the cofactor is precisely the retained-order deleted rectangle with sign `(−1)^(p+c)`. All feasible counts are exactly `0,…,r+1`. The current construction for `0≤t≤r` avoids the added edge and assigns `p` an unused column of `J`, which works also at the tight boundary.
- **Theorem A.** Deletion preserves row separation, leaves the same `r,q`, and gives size at least `2r+q`. The raw-degree identity `D_−=D+M−1−e_c` is correct. The prior pivot argument establishes annihilation of every symmetric polynomial of degree below `κ_−`, including inhomogeneous polynomials. Since `ρ_x=(x−y)ρ_x^−`, evaluating `s_θ∏(x−y)` gives the nonzero original exterior moment in degree at most `κ+q`. Thus `κ_−≤κ+q`, and the exact gap is at least `M−1−q=N−1≥r`. The edge contribution strictly dominates every original coefficient. The binomial coefficient signs in (4)–(5) are correct.
- **Boundary maximal layer.** The whole prior theorem is not applied outside its range. Its Sections 1–3 still apply: `M_−=r+q−1≥q`, all exponent nodes remain distinct, and the moment matrix retains full row rank. Interpolation gives `μ_l^−=0` for `l<q`, `μ_q^−=1`; consequently the pivots are `1,…,q`, the shape is `(1^q)`, and the exterior sign is `(−1)^(q(q−1)/2)`.
- **Boundary row factor and lower layers.** The prior Section 5 sign proof requires `M_−≥q` and shape width at most `r`, both satisfied here. Hence `C_*≠0`. The raw loss is exactly `h(q−1+h)`: only `h=1` can tie loss `q`, and all `h≥2` lie strictly below it. There can therefore be only `C_*w^r+C_1w^(r−1)` at the candidate degree. The minor has no zero-red matching, so evaluation at `z=0` forces `C_1=C_*`. This proves the nonzero top polynomial `C_*z(z−1)^(r−1)` without importing the prior lower-layer theorem below its threshold. For `r≥2`, the edge degree exceeds the original by `r−1`; the zero-red fiber is unchanged exactly. The signs and all degrees in (9)–(10) follow.
- **One-row boundary.** The same minor argument is valid when `r=1`; equivalently, every surviving column is in `J`, so the minor is `z` times an ordinary determinant. The row factor reduces to `∏_(s≠i,p)(a_s−a_i)/q!`. To check the compressed sign argument in the proof, put `k=p−1_(i<p)`, the position of `p` in the complementary row list. The combined cofactor/index/exterior sign ratio is `(−1)^k`, while `Δ(C')/Δ(C)=(−1)^k/∏_(s≠i,p)(a_s−a_p)`. These cancel, and `H_(q+1)/H_q=q!`, proving (15) in arbitrary original row/column order. All exponent factors cancel. Equation (14) and the stated scope of the equality obstruction are correct.

## Exact checks

- Read the standard-library checker: its determinant calculation is a direct signed-permutation expansion, not a use of the asserted cofactor or leading-term formulas. Integer/Fraction arithmetic is exact; its `require` checks remain active under optimization.
- Ran both `python checker/check.py` and `python -O checker/check.py`. Both passed all eight cases, including the positive-loss original rectangle, reordered row/column signs, reverse separation, both boundary ties, and the equality obstruction. Re-ran both after the reordered-column fixture changed to `[5,2,0,4,1,3]`, confirming the negative total row/column permutation-sign test.
- Independently reproduced the three `n=4` certificate fibers by symbolic determinant expansion: `−2Λ³`, `−18Λ²−54Λ−42`, and `2(Λ+3)³`.
- The independent signed-permutation checker is saved as `checker/audit_check.py`. It tests 32 deterministically sampled cases (seed 1019, sizes 3–6, varied row/column positions, sparse exponents, both separation directions), using only the standard library and explicit checks that remain active under optimization. Run `python checker/audit_check.py` or `python -O checker/audit_check.py` from this folder. Both commands passed: full cofactor identities and the applicable slack, boundary, and one-row-ratio predictions agreed. These finite checks supplement the arguments above; they do not establish universality by themselves.

## Issue resolved during audit

The initial feasibility paragraph used the added edge for `t=1`, which would require `r` rows to enter only `r−1` available blue columns at the tight boundary. The author replaced it with the valid no-added-edge construction described above. I reread the corrected paragraph and confirmed the fix. No further correction is required.
