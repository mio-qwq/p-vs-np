# Verification and frozen-source record

All four README commands ran successfully on 17 October 2026 after portable packaging. The generated check_lower.log, test_solver.log, check.log and rank_check.log record their actual stdout.

- Root lower examples include exact Pfaffian and even-monomial sharpness, an extra fixed coordinate, and a deliberately wrong-sign negative control.
- Root solver tests: 1,440 exact target comparisons through n=7 and five malformed-input controls.
- Independent audit check: 420,903 toggle/descent cases, 137,790 integer Pfaffian evaluations, 2,352 alternating finite-difference monomials, and 6,200 solver calls compared with complete permutation enumeration.
- Independent rank checks: all twelve n=2,...,7, d=1,2 cases have full evaluation rank at the claimed radius and strictly smaller rank one radius below; even monomial controls through n=8 pass.

PROOF.md remains byte-identical, SHA256 d46686373a10634f6976fa7c97cbdecf47b4876409ad7111829a821beab41f79. solver.py, check_lower.py, test_solver.py and rank_check.py are unchanged. check.py changes only its solver import path to the packaged directory. REVIEW.md changes only scratch-path references and adds an explicit provenance banner; its original SHA256 is ac5066028f28c5f6eb55cb7a72d4a4f9329a7c78cc3718c1bd449e3acb9ee323. Source and packaged hashes are recorded in SOURCE_PROVENANCE.json. The review's listed original hashes remain historical evidence, while the repository manifest freezes these packaged files and rerun logs.

The frozen proof's final request for independent audit is a historical drafting statement; REVIEW.md supplies the subsequent independent audit. Its suggested row-image convention clarification is supplied explicitly in README.md without changing the frozen proof. Finite tests are not a formal proof of the theorem or a novelty search.
