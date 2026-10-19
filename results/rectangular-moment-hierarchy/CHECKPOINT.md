# Frozen rectangular-moment checkpoint

18 October 2026. The theorem and local exact verification are complete. No remote writes or publication were performed. No assertion of novelty, general ASNC, or an ASNC counterexample is made.

## Main result

For n=2r+2, exactly I×J red with |I|=r, |J|=r+1, let k be the first differing positive power sum of the two exponent classes X=e_J and Y=e_Jᶜ. Then k≤r+1. Set

    D=Σe−binom(r,2)−binom(r+2,2),
    A=(−1)^ΣI Δ(a_I)Δ(a_Iᶜ)/(H_r H_{r+2}),
    K=(−1)^ΣJ Δ(X)Δ(Y),
    Δp_k=ΣY^k−ΣX^k,
    q_l=Σ_{u=0}^l (−1)^u e_u(a_I)/(r falling u)
                         · h_{l−u}(a_Iᶜ)/((r+2) rising (l−u)).

All coefficients above D−k+1 vanish and

    [λ^{D−k+1}]F = A K (Δp_k/k) q_{k−1}(z−1)^r.

If q_{k−1}≠0, every feasible fiber t=0,…,r has exact degree D−k+1. Separated row-offset blocks ensure q_{k−1}≠0. For standard rows a_i=i,I={0,…,r−1},

    q_l=(r+1)^l/l!,
    [λ^{D−k+1}]F=A K (r+1)^{k−1}Δp_k/k! ·(z−1)^r.

The proof includes a bound excluding all smaller Laplace layers: for s=r−j, correction orders t≤k−j−2 vanish. This follows from a remainder-matrix rank estimate, not from a mere leading-term comparison.

## Important limitations

Distinct offsets alone do not guarantee nonzero q. Both irrational and all-integer q_2=0 examples are recorded; their actual fibers remain nonzero and drop from D=11 to degree7. No all-colorings statement follows.

## Files

- `PROOF.md`: complete theorem, normalization, proof, separated-offset positivity, standard-row closed form, and counterexamples to unconditional candidate nonvanishing.
- `check.py`: exact standard-library Cauchy–Binet coefficient calculations and smaller-layer checks through k=5.
- `results.json`: seven finite cases through n=16, including k=3,4,5, unsorted rational offsets, and nonprincipal row sets.
- `check_cancellation.py`: independent signed sum of all 720 permutations over Q(√2), comparing every bivariate coefficient of the root's q_2=0 example.
- `cancellation_result.json`: complete nonzero coefficients of that example.
- Normal and optimized reruns are recorded by the publication-stage verification receipts; duplicate source logs are omitted.
- `SHA256SUMS` and `manifest.json`: canonical packaged inventory; source hashes and editorial changes are in `PROVENANCE.json`.

## Independent audit and provenance

The independent auditor checked all signs, factorial ratios, r=1 edge cases, remainder-rank cancellation, simplex positivity, and the formal-series proof of the standard-row closed form. It independently reconstructed complete determinants through n=10,k=5 and verified the integer q_2=0 examples. Its source and full data are in:

- `audit/check_independent.py`
- `audit/independent-results.json`
- `audit/check_qclosed.py`
- `audit/qclosed-results.json`

The earlier rectangular obstruction and the transition to this theorem are summarized in [STATUS.md](STATUS.md). The original n=8 diagnostic and Q(√2) determinant are fully covered by the included independent complete reconstruction and `check_cancellation.py`, respectively. The theorem and its checks require no files outside this package.

## Freeze rule

This source is frozen after the final audit. Do not edit proof or verification code without a coordinated, documented correction and a fresh hash manifest. Research dissemination, if requested, is a separate action.
