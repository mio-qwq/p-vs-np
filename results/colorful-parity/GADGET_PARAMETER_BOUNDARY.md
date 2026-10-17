# Why the cover parameter does not disappear in the NAND matching gadget

The previously published local disjoint-pair gadget introduces one private
auxiliary vertex for each forbidden pair. Each auxiliary is adjacent only to
the two ports of its own pair. Port cliques and external port-to-port matching
edges never add edges between auxiliary vertices.

If there are m such auxiliaries, they form an independent set in the allowed
matching graph. They therefore induce a complete graph K_m in its forbidden-edge
graph. Every vertex cover of that forbidden-edge graph must contain at least
m-1 of those auxiliary vertices: leaving two unselected would leave their
forbidden edge uncovered. Hence the minimum forbidden-edge cover parameter
satisfies q>=m-1.

Thus the newly audited FPT-in-(k+q) algorithm does not, through this gadget alone,
give FPT in only the k additional parity bits for arbitrarily many local NAND
constraints. Its guaranteed parameter bound may grow with the number of
constraints. This is a precise limitation of this composition of reductions,
not a complexity lower bound for the original problem or for other algorithms.

The ordinary no-extra-parity gadget remains polynomial-time solvable by matching.
The argument here concerns the attempted transfer of the new parameterized
algorithm, not that existing tractability theorem.
