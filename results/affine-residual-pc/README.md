# Repaired affine branching: connected nonpure obstruction

The exact ARB-PC candidate adds safe pure-coordinate elimination and component decomposition. A connected, nonpure input family still forces at least 2^k distinct states on Theta(k log k)-bit inputs for this precise order-preserving cache. Stronger implication-SCC preprocessing defeats this family; arbitrary-isomorphism caching also escapes the proof. This is not an unrestricted SAT lower bound.

[Algorithm and proof](design/README.md), [proof details](design/PROOF.md), and [independent AI review](checker/REPORT.md). Python3 standard library. Run:

    python checker/check_arb_pc.py
    python checker/check_repairs.py
    python checker/check_family_invariants.py
    python checker/check_growth.py
    python design/run_experiments.py

Checker imports/results were made relative to their packaged files and rerun. Solver source remains frozen at SHA256 32ba57a17c8af1fc1045314fd89b849743bd6ba810fdfdb96f3a4ac9cde577c5. No historical novelty, human peer review or Lean verification is claimed.
