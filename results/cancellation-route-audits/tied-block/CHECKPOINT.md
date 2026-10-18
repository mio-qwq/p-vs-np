# Checkpoint: tied square boundary resolved; rectangular top obstruction certified

18 October 2026. Local only; no publication or remote edits.

## Main findings

1. The n=2k−1 all-red k×k boundary has exact combined coefficient C z(z−1)^{k−1} at D=E−(k−1)². The two tied Laplace sizes have equal scalar coefficient C. Every feasible target 1,…,k has nonzero top coefficient. A Lagrange-interpolation identity proves the tied sum directly.
2. Exact fiber identities reduce every majority square block to its complementary smaller square block. Together with the earlier small-square theorem, this completes all all-red square blocks for arbitrary distinct real offsets and distinct nonnegative integer exponents. This is a structural addendum, not grounds for a release by itself.
3. For an underfull rectangular block r×s, r<s and r+s≤n, the maximal leading sum is a signed Vandermonde product times an explicit polynomial-remainder determinant. Saturated r+s=n rectangles reduce to square blocks by reversing counts.
4. A genuine source-standard multirow obstruction occurs at n=8, r=3, s=4, I={0,1,2}, J={0,1,6,7}, a_i=e_i=i. Candidate degree 15 cancels because the two exponent subsets have equal sum 14. The exact next coefficient is 967680(z−1)³ at degree 14. Thus every target remains nonzero; this is a counterexample only to the proposed leading-sum nonvanishing route.
5. The next coefficient has a structural proof using the difference of second elementary exponent sums and the difference of row-offset means. The n=8 coefficient is therefore independently derived rather than only experimentally observed.

## Files

- `PROOF.md`: tied square boundary, interpolation proof, standard-label coefficient, and complete-square corollary.
- `RECTANGULAR_OBSTRUCTION.md`: general remainder-matrix identity, saturated reduction, balanced-sum obstruction, and next-coefficient proof.
- `check.py`: complete exact bivariate determinant cross-checks by direct permutations and subset-state Laplace recurrence on ten fixed cases, including the single n=8 example.
- `results.json`: all exact polynomial coefficients for these ten cases.
- `check_identities.py`, `identity-results.json`: ten bounded structural algebra checks including unsorted labels; independently evaluate the remainder quotient and weighted column identities.
- `normal.sha256`, `optimized.sha256`: identical hashes after normal and optimized runs; checks use explicit exceptions.

`results.json` SHA-256:

    154e6ea35a52ef04c3e33f48931e606535bc07a087fcac653792e5a480928ad6

All checks completed successfully. The n=8 direct permutation and raw Laplace implementations agree on every bivariate coefficient. Neither a general rectangular nonvanishing theorem nor general ASNC is claimed. No all-colorings enumeration was performed.

## Audit and source freeze

The independent reviewer found no substantive discrepancy. Its separate checks covered 125 quotient cases, 55 weighted-identity cases, 15 translated-minor cases with unsorted rational offsets, and the complete n=8 polynomial through numeric determinant evaluation plus exact interpolation. See `AUDIT.md` and the `audit-results*.json` files. The sole clarification makes r≥1 explicit for the mean-based next-coefficient formula. Core proof and checker sources were frozen after that clarification on 18 October 2026 at 19:05 UTC; the checker files are unchanged.
