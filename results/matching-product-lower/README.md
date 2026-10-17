# All-field product lower bound for flip testing

For d>=2 and n>=2d, the explicit degree-d product in PROOF.md has minimum nonzero flip distance ceil(3d/2) over every field. This gives a universal-radius lower bound, with no matching optimal upper bound asserted. The d=1 exception is stated in the proof.

The proof is byte-identical; its initial pending-review line is historical. audit/REPORT.md records completed independent AI-assisted review. Run standard-library checks:

    python check.py
    python audit/check.py

Both were actually run; corresponding .log files and audit/results.json record results. Only the independent checker's output path was adapted for portability. Cross-packet source hashes are in ../matching-char3-flip/SOURCE_PROVENANCE.json. No historical novelty, P versus NP result, runtime lower bound, human peer review or Lean claim is made.
