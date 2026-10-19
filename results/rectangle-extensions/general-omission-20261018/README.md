# General omitted-column rectangle theorem

This local package proves the all-red rectangle leading-coefficient theorem for every omission number q≥1, under n≥2r+q. It subsumes the earlier one- and two-omission formulas.

The key new point is an elementary flag argument. Greedy moment-column pivots determine the unique first surviving Schur shape. Pivot sets nest as moment rows are appended, giving κ_(q+h)−κ_q≥−qh. The raw lower-layer gap then leaves a strictly positive margin of at least h². General normalized-Schur translation and Pieri identities prove the surviving row factor strictly positive under separated offsets.

Files:

- PROOF.md: complete theorem, proof, signs, arbitrary-offset conditional formula, separated-offset nonvanishing, q=1 and q=2 reductions, and exact q=3 example.
- PIVOT_COMPARISON.md: standalone first-shape and lower-layer lemma, plus an independent quotient-polynomial degree proof.
- AUDIT.md: fresh independent mathematical audit, including the general omitted-set sign.
- checker/check_q3.py: exact standard-library translated-minor certificate and regressions.
- checker/q3_results.json: exact certificate data.
- checker/Q3_CERTIFICATE.md: derivation and detailed certificate notes.

Run the checker from this directory:

    python checker/check_q3.py
    python -O checker/check_q3.py

Scope: one all-red rectangle. The coefficient identity is valid for arbitrary distinct real offsets; unconditional nonvanishing requires strict separation. No arbitrary-coloring, complexity-lower-bound, novelty, or P-versus-NP conclusion is claimed. All work in this package is local.
