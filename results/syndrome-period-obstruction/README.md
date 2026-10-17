# Exact affine-slack SAT testbed

Read RESULT.md for proof, costs, and limitations. No general polynomial SAT algorithm or historical novelty is claimed. The candidate-independent result is a rank dichotomy showing that this particular local affine-slack quotient cannot compress standard repeated-variable strict-3CNF occurrence blocks.

Run with Python 3, standard library only:

    python test_syndrome_dp.py
    python test_stabilizer_dp.py
    python test_clause_dichotomy.py
    python check_anchor_control.py

Each script writes its JSON result beside itself. No imports depend on another research directory. The original frozen solver was read, not changed or executed by these new tests; its SHA-256 was verified as 32ba57a17c8af1fc1045314fd89b849743bd6ba810fdfdb96f3a4ac9cde577c5.

The APIs operate on explicit bit-vector columns and local literal lists; they are research prototypes, not a hardened adversarial-input CLI. `syndrome_dp.solve` checks basic input shapes and returns a witness or None plus stats; `stabilizer_dp.solve` returns a Boolean decision plus stats. The latter assumes valid inputs and does not reconstruct witnesses.
