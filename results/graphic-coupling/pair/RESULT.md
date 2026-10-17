# Pair-sum graphic recognition: choosing a useful graph representation

2026-10-17. Exact restricted-class recognition theorem and a certificate-backed solver. No historical novelty or general P=NP claim.

## Main result

Given an explicit binary matrix A and designated pairs of independent nonzero columns (a_e,a_f), append one column a_e+a_f per pair. Call the resulting matrix A+.

**There exists a graph representation of A in which every designated pair shares a vertex if and only if the binary column matroid of A+ is graphic.**

This turns simultaneous representation selection into one standard graphic-recognition call. It does not require enumerating Whitney flips or treating their choices as independent Boolean variables.

For disjoint NAND pairs, an accepting representation supplies a polynomial-time solver: remove the appended recognition-only edges, transport the affine target correctly, and use the incident-pair matching algorithm. Rejection means this representation class is unavailable, not that the original SAT instance is unsatisfiable.

## 1. Proof of the recognition equivalence

Forward: suppose B is a graph incidence representation of A in which e and f are incident. Since their columns are independent, they are distinct nonparallel nonloop edges. Their sum is the incidence column of an edge joining their other endpoints. Add this closing edge for every pair, allowing parallel copies if necessary. The extended representation has the same binary kernel as A+, so A+ is graphic.

Reverse: every designated triple {e,f,g_ef} in A+ is a three-element circuit: the three nonzero columns sum to zero and no pair is dependent. In any graph realizing A+, a three-element circuit is a triangle. Thus e and f share a vertex. Delete every added g_ef edge to obtain the required graph representation of A, with all designated incidences realized simultaneously.

This recognition statement itself allows overlapping designated pairs. The subsequent matching algorithm needs the local disjointness promise; our original domain supplies global pair disjointness automatically. One must not infer tractability for overlapping NAND constraints merely from graphicity of the extension.

## 2. Why the affine target transports correctly

Binary representations of the same labeled matroid have the same kernel. Indeed their minimal nonempty dependency supports are the same circuits, each with all coefficients one. Every kernel vector can be decomposed into circuit indicator vectors by repeatedly subtracting a circuit contained in its support. Thus equality of circuits implies equality of the entire kernels.

Let B be the incidence matrix of the recovered graph, restricted to the original columns. First solve Az=b by Gaussian elimination, ignoring NAND restrictions. If no such z exists, reject the SAT instance. Otherwise set

    b_graph = Bz.

This is independent of the selected linear solution, since another solution differs by a vector in ker A=ker B. For every x,

    Ax=b iff Bx=b_graph.

The graph target has even parity on each connected component automatically. There is no need to guess vertex parity bits or to keep the original row target after changing representations. Appended pair-sum columns are used ONLY for recognition; they are never additional selectable SAT variables.

## 3. Degenerate pairs and preprocessing scope

If a pair has rank below two, its feasible syndrome set {0,a_e,a_f} is its entire linear span (dimension zero or one). That span can be absorbed into a global quotient and the pair deleted; new degeneracies may then arise, so repeat. Unpaired free columns can similarly be absorbed. Gaussian bookkeeping reconstructs their choices after solving the quotient instance.

This optional preprocessing is an equivalent decision reduction and may enlarge the solvable subclass. It should not be confused with a statement that the original unquotiented matrix has a local graph representation. The main triangle theorem and current certificate solver explicitly assume rank-two designated pairs.

A nonzero parallel pair is already incident in every graph representation; its appended sum would be a loop. A single zero-column member of a disjoint NAND pair can simply be set to zero and its partner made unrestricted. These are alternative direct treatments, but the implementation rejects unprocessed degenerate pairs rather than silently mishandling them.

## 4. Polynomial recognition is an established algorithmic primitive

[Robert E. Bixby and Donald K. Wagner, An Almost Linear-Time Algorithm for Graph Realization, Mathematics of Operations Research 13(1), 99–123 (1988)](https://doi.org/10.1287/moor.13.1.99) solves the fundamental-circuit matrix graph-realization problem: represent each column as a path in a tree or certify failure. Its [author technical report](https://repository.rice.edu/bitstream/1911/101579/1/TR85-02.pdf) is also available.

To apply that result to A+, first choose an actual column basis by Gaussian elimination, remove redundant rows and transform to [I | D], retaining all column labels. Feed D to graph realization; the identity columns are the returned tree edges and the remaining columns give chords closing their tree paths. This normalization is polynomial in the explicit matrix bit size and must be included in the cost. The almost-linear claim applies to the normalized graph-realization input, not automatically to the entire pipeline.

The result here is an elementary reduction to this known recognition problem, not a claim to have invented a new graphic-recognition algorithm. The incidence-pair matching stage is also covered by the earlier cited Cannon–Ishaque–Tóth parity-orientation work.

## 5. Positive rescue and invariant obstruction

Take reduced four-cycle columns

    A = [3,6,4,1]

where integers denote three-bit vectors and omitted root is vertex 3. Pairs (0,2) and (1,3) are opposite edges and hence nonincident in this presentation. The invertible map with unit-vector images [1,2,6] gives

    B = [3,4,6,1],

where both designated pairs are incident. Thus representation search can genuinely enlarge the directly visible matching subclass. Every one of the 128 target/assignment combinations preserves its exact linear feasibility under this map.

In contrast, K4 has reduced columns [1,2,3,4,5,6]. The opposite pair with columns 3 and 4 appends 7, producing all seven nonzero vectors of GF(2)^3, the Fano matroid. It is not graphic. Independently, any graph representation of M(K4) is loopless and simple (there are no one- or two-element circuits), has rank three and six edges, and its edge-bearing component must be connected because the matroid is connected. Thus it is K4. Opposite edges are characterized by the absence of a triangle containing both, a circuit invariant, so cannot become incident in another representation. This does not imply that a single forbidden pair is computationally hard; branching twice handles one pair.

## 6. Executed implementation and checks

`test.py` enumerates all 168 invertible three-dimensional binary maps and checks 1,562 rank-three column/pair configurations. Direct simultaneous-incidence recognition agrees exactly with the pair-sum extension test. It includes the positive four-cycle rescue, all target fibers and the K4/Fano obstruction.

This exhaustive GL(3,2) code is a finite validation oracle, NOT a polynomial generic graphic recognizer.

`certificate_solver.py` is a polynomial certificate-backed implementation. Input includes a proposed graph representation of A+. It checks endpoint validity, equality of binary kernels and triangle incidences; transports the target by Gaussian elimination; invokes the independently implemented polynomial blossom-backed local matching solver; and rechecks the returned assignment against the original matrix and NAND pairs. It does not discover the graph representation.

`test_certificate.py` tests 500 random matrix instances created by arbitrary invertible row operations on graph incidences, with independently supplied extension certificates. Its decisions match exhaustive original-edge assignment search; all 153 returned witnesses pass original matrix and NAND checks.

The distinction is explicit: automatic polynomial recognition follows theoretically from the proved reduction and the cited graph-realization algorithm; the executed general prototype verifies supplied certificates and solves accepted instances. Full automatic graph-realization discovery has not been implemented here.

Run `python test.py` and `python test_certificate.py`. The certificate solver requires the sibling quota and blossom modules at the explicit paths recorded in its source. Results and hashes are included. No previous artifact was changed.

## Next substantive limitation

The pair-sum test gives a sharp recognizable structural class, but the Fano extension shows not every graphic input lies in it. Further progress must handle genuinely non-graphic pair-sum extensions or another representation entirely. It cannot be obtained merely by searching more Whitney flips after the exact recognition test rejects.
