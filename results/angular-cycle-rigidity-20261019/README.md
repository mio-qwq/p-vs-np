# Few cost-active cycle noncancellation

Source-only research archive, 19 October 2026.

## Accepted result and limits

For an entire additive-cost fiber of perfect matchings on a supported bipartite
graph consisting of independent alternating cycles and forced edges, its signed
translated-power polynomial is nonzero under either condition:

1. At most three cost-active cycles, with arbitrary flip parity.
2. At most four cost-active cycles, with every active flip odd.

There may be arbitrarily many inactive cycles of arbitrary length. Row offsets
are distinct real numbers, column exponents are distinct nonnegative integers,
and edge costs are arbitrary reals. The result also covers maximum-degree-two
support after edges unused by any perfect matching are discarded. Nonzero as a
polynomial does not mean every pointwise evaluation is nonzero.

The analytic proof uses exact product decomposition, distinct root multiplicities
and antichain arguments. Supplemental finite checks give the antichain census
2, 3, 6, 20, 168, and verify six sample graphs, 132 matchings and 42 entire fibers.
They do not replace the unbounded proof. Four active mixed-parity cycles,
unrestricted complete-fiber noncancellation, a general polynomial-time isolation
algorithm and P versus NP are not resolved. There is no formal proof-assistant
certification or external peer-review claim.

## Reproduce

Check `sha256sum -c SHA256SUMS`, extract the original ZIP and run in its directory
with Python 3.10 or later (standard library only):

    python -I -B verify_bundle.py
    python -I -B -O verify_bundle.py
    python -I -B rebuild.py ../rebuilt.zip

The verifier checks source and independent-review pins, both primary and audit
checkers in ordinary and optimized modes, byte-identical reference outputs and
11 required corruption rejections. Rebuilds use sorted paths and fixed metadata
with ZIP_STORED. No network access is needed.

Read primary/PROOF.md and audit/SHORT_AUDIT.md inside the ZIP for the proof
and scoped review. The package README records all file roles and limitations.

## Archive verification

VERIFICATION.json records the frozen checkpoint and a fresh independent archival
clean extraction, complete replay in both Python modes, and byte-identical rebuild.
The checkpoint's local-only/external-action fields describe packaging before this
additive archival commit. This directory adds only the exact original ZIP, this
README, SHA256SUMS and VERIFICATION.json. No existing source or archive is replaced.
No PR, merge, tag or release is created by this source archival operation.
