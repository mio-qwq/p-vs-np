# Prior-art review: cyclic supplied-literal parity AND complexity

Review date: 17 October 2026. This is a bounded literature check, not a novelty certification or an independent mathematical audit of PROOF.md.

## Bottom line

The exact fusion-cover/cyclic-AND correspondence is established prior art. The searched primary sources did not supply the candidate odd-arity recurrence, its 1.5m−O(1) consequence, or the exact values rho(4)=5 and rho(5)=7 in the precise least-fixed-point, supplied-both-literals, OR-free model. That is a statement about this search, not evidence that these claims are new. In particular, an explicitly cited unpublished 2018 communication about AND lower bounds remains unresolved.

The appropriate provisional description is: “An independently audited candidate parity bound in the specified cyclic AND-cost model; historical novelty remains unverified.” Avoid “first bound beyond n,” “new circuit lower-bound method,” or “new fusion characterization.”

## 1. Cavalar–Oliveira: published version checked

Bruno P. Cavalar and Igor C. Oliveira, *Boolean Circuit Complexity and Two-Dimensional Cover Problems*, ACM Transactions on Computation Theory 17(2), article 13 (2025), DOI [10.1145/3718746](https://doi.org/10.1145/3718746). [Published-version PDF](https://wrap.warwick.ac.uk/id/eprint/191062/1/3718746.pdf); [institutional record](https://wrap.warwick.ac.uk/id/eprint/191062/); [arXiv v1](https://arxiv.org/html/2503.14117v1).

The published version retains Theorem 30, Section 3.4, printed page 15: rho(A,B)=D_cap^circ(A|B). The introduction calls this Theorem 3. Section 2.5 supplies the cyclic semantics. Their supplied positive/negative input generators describe DeMorgan circuits with negations at the inputs; intersection complexity counts ANDs while unions are free.

The introduction, printed page 3, explicitly says AND lower bounds Cn with C>1 follow from gate elimination, citing Golovnev, 2018, private communication (published bibliography [5]; arXiv bibliography [6]). It does not identify parity, a constant C, the recurrence, or a cyclic extension. The paper distinguishes its exact result from Nakayama–Maruoka's constant-factor characterization. Its parity mention in Proposition 40 is a two-input XOR identity in an inequality-function construction, not an n-input parity lower bound.

The arXiv submission history showed only v1 (18 March 2025). The institutional repository identifies the downloaded manuscript as the published version; its publication-date metadata is 11 June 2025.

## 2. Nakayama–Maruoka (1995): real overlap, incomplete access

Katsutoshi Nakayama and Akira Maruoka, *Loop Circuits and Their Relation to Razborov's Approximation Model*, Information and Computation 119(2), 154–159 (June 1995), DOI [10.1006/inco.1995.1083](https://doi.org/10.1006/inco.1995.1083). [Publisher abstract](https://www.sciencedirect.com/science/article/pii/S0890540185710838).

The publisher abstract introduces circuits whose underlying graphs may have cycles and establishes a Theta relationship between loop-circuit size and an approximation-model distance. Thus neither cyclic circuit models nor the general connection to approximation/fusion are new here. I could inspect the publisher-indexed abstract, but direct publisher opening failed and I did not retrieve the full six-page article. Consequently I have not independently ruled out a parity example, ancillary lemma, or stronger relevant statement in that article. Cavalar–Oliveira's explanation of the differences is informative but does not substitute for reading it.

## 3. Nearby parity results: different costs and semantics

### Classical XOR-free / DeMorgan total-gate complexity

Claus-Peter Schnorr, *Zwei lineare untere Schranken für die Komplexität Boolescher Funktionen*, Computing 13(2), 155–171 (1974), DOI [10.1007/BF02246615](https://link.springer.com/article/10.1007/BF02246615). The publisher page is accessible; the original full proof was not retrieved in this pass.

A directly inspected contemporary research source is Marco Carmosino, Ngu Dang, and Tim Jackman, *Convergent Gate Elimination and Constructive Circuit Lower Bounds*, [arXiv:2602.17942v1](https://arxiv.org/html/2602.17942v1) (20 February 2026). Its Section 2 explicitly uses acyclic circuits and counts binary gates, with NOT free. Its constructive parity result, Theorem 19, revisits the classical 3(n−1) DeMorgan bound. Appendix B compares bases; Appendix C reconstructs Schnorr's proof. This is relevant prior art for elimination, simplification, and constructive/formalizable parity arguments, but it is not the candidate cyclic, AND-only-cost theorem.

Crucial mathematical distinction: a lower bound on AND+OR count does not imply the same lower bound, or half of it without a separate conversion theorem, on AND count when arbitrarily many ORs are free. Allowing free internal NOT together with free OR would trivialize literal AND cost: a AND b = NOT(NOT a OR NOT b). Pushing internal negations to the inputs can change the AND/OR allocation, so the restriction on where NOT occurs is essential, even though ordinary total-size complexity often tolerates such transformations.

### Multiplicative complexity

The [NIST Circuit Complexity project](https://csrc.nist.gov/projects/circuit-complexity) explicitly uses the AND/XOR/NOT basis for its AND-optimization and multiplicative-complexity work. In that cost model parity has zero AND cost, because it is an XOR chain. Its small-variable optimal AND tables therefore do not certify rho(4) or rho(5) here. “XOR-free” means XOR is disallowed; it must not be confused with XOR being free of charge.

### Another meaning of cyclic circuits

Aleksandr Golovnev, *Circuit Complexity: New Techniques and Their Limitations*, NYU dissertation (May 2017), [author-hosted PDF](https://www.golovnev.org/theses/phd_nyu.pdf), especially Section 4.2 and its XOR-circuit subsections. The thesis develops cyclic circuit machinery with XOR-type gates in general gate-elimination arguments. It is not automatically the positive monotone least-fixed-point semantics of this candidate. Its parity discussion also records total-gate U2 bounds. The 2017 dissertation cannot itself resolve the contents of the unpublished 2018 communication.

### AND-versus-OR accounting

Uri Zwick, *On the number of ANDs versus the number of ORs in monotone Boolean circuits*, Information Processing Letters 59(1), 29–30 (1996), DOI [10.1016/0020-0190(96)00080-4](https://www.sciencedirect.com/science/article/abs/pii/0020019096000804). The publisher abstract concerns controlling OR counts while preserving AND count in monotone circuits. This is relevant accounting literature, but the abstract does not supply the proposed cyclic parity recurrence. The displayed mathematical bound in the abstract appears poorly rendered, so no numerical version is relied on here.

## 4. Search coverage and unresolved work

- Inspected the candidate PROOF.md, published Cavalar–Oliveira PDF and arXiv HTML, their citation trail, the Nakayama–Maruoka publisher abstract, Zwick publisher abstract, relevant Golovnev thesis sections/search hits, NIST's model description, and the 2026 convergent-elimination paper.
- Queried combinations of parity with AND complexity, AND-complexity, intersection complexity, free OR, cyclic circuits, loop circuits, 2n−3, and the named authors/titles. Many searches returned unrelated parity-games material; absence of useful hits is weak evidence.
- No full citation-graph sweep, non-English archival search, or author correspondence was performed. No contact with authors or other external write occurred.
- The most valuable next historical checks are the full 1995 article and the exact contents of Golovnev's 2018 communication, including whether its argument already gives this parity bound or extends to least-fixed-point circuits.
- The small finite values were not historically identified or independently certificate-checked in this task. Their correctness and the model linkage remain matters for the separate mathematical/certificate audit.
