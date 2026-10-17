# Cyclic parity gate-elimination recurrence

For finite monotone cyclic circuits with supplied input literals of both polarities, free ORs and binary AND cost under least-fixed-point semantics:

- r(m) >= r(m-1)+1 for m>=2.
- r(m) >= r(m-1)+2 for odd m>=3.
- Therefore r(m) >= m-1+floor((m-1)/2).
- The exact four-bit certificate in ../parity4-cover/ improves the base and implies r(5)=7, matched by an explicit seven-AND circuit.

PROOF.md contains the general mathematical argument. model-linkage.md proves the exact correspondence to unrestricted semifilter pair-cover cost and attributes the existing general equivalence to Cavalar–Oliveira. Independent AI-assisted audit reports accompany the proof. There is no Lean formalization of this new recurrence, no peer review, no claim of historical novelty, and no P-versus-NP separation. PRIOR_ART.md records unresolved historical checks.

Run with Python 3 standard library from this directory:

    python check_lfp_transforms.py
    python check_seed_cnf.py
    python check_upper_bound.py

These are finite regression and construction checks, not substitutes for the general proof. The four-bit lower certificate is separately reproducible in the sibling directory.
