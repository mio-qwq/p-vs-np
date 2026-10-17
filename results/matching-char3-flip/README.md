# Degree-two flip radius in characteristic three

For fields of characteristic three the exact radius is 4 at n=5,6, min(n-1,3) at every other n>=2, and zero at n<=1. In particular, radius need not be monotone with ambient size. CHARACTERISTIC_THREE_RADIUS.md and the JSON certificates are frozen unchanged. The existing [support upper proof](../matching-polynomial-radius/support-upper/PROOF.md) supplies the all-size reduction. Earlier characteristic-excluding proofs remain intact as historical results; this packet now settles the characteristic-three case for degree two.

Run from this directory, using Python's standard library:

    python check_certificates.py
    python audit/check_raw.py

Both commands actually passed during packaging. The independent checker is separately written and reads the same frozen certificates, with no discovery code or linear algebra. Its source/output locations were made relative to its file; original and packaged hashes are recorded in SOURCE_PROVENANCE.json. Actual logs accompany each checker and audit/results.json records the independent details. The retained extension_failure.json is an explicit negative control against extending the n=6 lower witness to arbitrary ambient n.

Discovery solvers, redundant certificate copies and exploratory ranks are excluded. PRIOR_ART.md records a bounded primary-source search with unresolved novelty. This is a polynomial-testing radius classification, not a P versus NP resolution or runtime lower bound. No human peer review or Lean verification is claimed.
