# Exact degree-two flip radius outside characteristics two and three

For a field of characteristic different from 2 and 3, degree-at-most-two polynomial functions on perfect matchings of K_(2n) have exact universal flip testing radius min(n-1,3) for n>=2, and zero for n<=1. A flip replaces two matching edges with another pairing of the same four vertices. A polynomial must be nonzero as a function on the matching domain, not merely as a formal polynomial.

The proof and orbit_certificate.json are frozen byte-identically. The proof's original pending-review line is historical: audit/PROOF_AUDIT.md records the completed hash-specific independent AI-assisted review. Its references to exploratory rank files and discovery scripts describe provenance; those files are deliberately omitted because they are not needed to verify the theorem.

The exact integer identity has multiplier 48, 49 orbit terms and 346 weighted matchings. Its reduction gives the upper bound over the stated fields. Characteristic three is unresolved by this certificate. The older characteristic-two flip theorem is unchanged. The all-field support result in the sibling directory must not be read as an all-field flip theorem.

Run Python 3 standard-library verification from this directory:

    python check_certificate.py
    python audit/check.py

Both were actually run during packaging; outputs are check_certificate.log and audit/check.log. The supplied checker verifies 676 reduced monomials. The independent checker verifies all 1,081 formal monomials, reconstructs the 945-state flip graph, checks all 384 target-orbit matchings, rejects coefficient corruption, and performs 11,463 lower-bound evaluations. It reads only the frozen proof and certificate. Its sole code adaptation makes the source directory relative to its own location; SOURCE_PROVENANCE.json records both hashes. No SymPy or discovery elimination is required.

These exact certificate checks are one finite ingredient in the written uniform theorem, not a proof-assistant formalization. No P versus NP result, algorithmic lower bound, established historical novelty, human peer review, or Lean claim is made. See PRIOR_ART.md.
