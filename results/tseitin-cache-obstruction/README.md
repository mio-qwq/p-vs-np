# Hidden Tseitin and formula-caching obstruction

See RESULT.md for the family, conditional CC+W simulation, failed context-clause reuse shortcut, and degree-four PC refutation. These do not establish an asymptotic runtime lower bound for the SCC-cached solver or a P-versus-NP result.

## Reproduce from the public repository

From the repository root:

    python results/tseitin-cache-obstruction/probe.py
    python results/tseitin-cache-obstruction/check_graphs.py
    python results/tseitin-cache-obstruction/check_specialization.py
    python results/tseitin-cache-obstruction/check_pc_degree.py

The default solver location is `results/affine-residual-pc/design/arb_pc.py`, resolved relative to the script rather than the current directory. For development outside that layout, set:

    export ARB_PC_SOURCE=/absolute/path/to/frozen/arb_pc.py

Only the exact frozen solver SHA256 `32ba57a17c8af1fc1045314fd89b849743bd6ba810fdfdb96f3a4ac9cde577c5` is accepted. A missing file or hash mismatch stops before importing the solver. The solver is never modified.

Each script writes its corresponding JSON beside the scripts and also prints it. Tests use the Python standard library only. `check_graphs.py` depends on the helper functions in `probe.py`; it does not certify graph expansion.

## Verification boundary

The parent independently reviewed the degree-four polynomial identity/vertex cancellation and the conditional CC+W proof against the primary 2003 rules. The documented test suite was rerun after portability changes. A deliberately different source file was rejected by the hash guard before execution. The polynomial-calculus checker is a symbolic sanity check of the given derivation identities, not a general formal PC proof checker.
