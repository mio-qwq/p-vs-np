# Packaging verification

The frozen solver is unchanged: SHA256 f949e6d749959a88e73f5516fd9dc0cca61fb17d55140265cb624538eaa4f941. Independent checker imports and result paths were changed only from temporary absolute directories to this file's directory, then the packaged checks were actually rerun. The proof uses the reviewed simplified first-core-branch argument.

Additional commands in this directory:

    python check_arb.py
    python check_resource_edges.py
    python check_marker_family.py

These include deliberately damaged implementations and exact original-definition oracles. See adjacent JSON and log files for actual run results.
