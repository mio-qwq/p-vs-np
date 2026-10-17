# Packaged verification

2026-10-17 UTC. Python 3.12.14, standard library only. All six README commands actually ran with exit code zero. Their adjacent .log and JSON files contain actual output. The complete four-clique checker examined 53,226 compatible quadruples with zero covers; the rarest-witness checker made 184 calls; the ordered search made 1,904 calls. The upper gate table and closure were verified independently.

Two intentionally corrupted certificates and an incorrect output-gate mutant were rejected. Relative-path adaptations and explicit incomplete-search failure guards are packaging changes; the witness JSON bytes remain exactly the reviewed certificate (SHA256 733b9b267091d3e13443ceb511aa860af7f4d8e3191974cfa4f42e014cf096f5). No SciPy discovery result is trusted by these verifiers.
