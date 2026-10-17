# Sharp permutation transposition-distance radius

For all fields, n>=2 and d>=1, the exact radius for detecting nonzero degree-at-most-d polynomial functions on all permutation matrices, measured by minimum number of arbitrary transpositions, is min(n-1,2d). For d=0 or n<=1 the radius is zero. This metric is different from the support radius min(n,2d+1).

transposition_radius_addendum.md is preserved byte-for-byte. Its reference to the earlier sharp_bound.md is historical: the audited dependency is now published as ../sharp-permutation-radius/PROOF.md with hash d46686373a10634f6976fa7c97cbdecf47b4876409ad7111829a821beab41f79. Use the row-image convention P_sigma[i,sigma(i)]=1. The new independent review is audit/REPORT.md.

Python 3, standard library only:

    python transposition_radius_test.py
    python audit/check.py

The independent checker measures distances by BFS and computes evaluation-space ranks over F2 and F3. Its results.json and adjacent logs are actual packaged output. The common runner ../colorful-parity/run_checks.py also executes these commands.

The theorem is about the full symmetric group and polynomial evaluation, not arbitrary allowed-edge domains or an algorithmic runtime lower bound. Historical novelty remains unverified; no P versus NP, human peer review or formal-verification claim is made. Original/packaged hashes are in ../colorful-parity/SOURCE_PROVENANCE.json.
