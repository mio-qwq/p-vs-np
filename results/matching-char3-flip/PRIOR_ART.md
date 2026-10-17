# Bounded prior-art check: characteristic-three degree-two flip radius

Search date: 2026-10-17 UTC. This is a bounded literature check, not an
exhaustive novelty search. Frozen proof and certificate files were not changed.
No external communication or publication was made.

## Conclusion

No inspected primary source states the exact classification proved in the
accompanying certificate package: radius four at n=5,6 and radius three at
n>=7 for degree-at-most-two functions over fields of characteristic three.
Nor did this check identify a theorem from which that classification is an
immediate corollary. This does NOT establish novelty or absence from the
literature. The closest papers use the same polynomial function space and
matching inclusion matrices, but generally over the real or complex numbers;
the closest local-recovery theorem has different assumptions and metric.

The generic methodology is standard: represent polynomial evaluations by an
incidence matrix, solve exact linear equations, exploit a stabilizer, and
transport a finite identity by relabeling/restriction. No novelty is claimed
for those methods. The specific finite characteristic-three ranks and
exceptional ambient sizes are what would need comparison with more specialized
modular inclusion-matrix or integral representation results.

## Primary sources inspected and overlap

### 1. Filmus and Lindzey, Harmonic Polynomials on Perfect Matchings (2022)

[Conference paper, SLC 86B.59](https://www.mat.univie.ac.at/~slc/wpapers/FPSAC2022/59.pdf)

Theorem 1.1 concerns unique succinct harmonic presentations of real-valued
functions on perfect matchings, compatible with the spectral decomposition.
Sections 2–3 define the relevant edge polynomials and matching inclusion
matrices. Theorem 3.3 is a global uniqueness theorem for harmonic polynomials.
The proof uses positive definiteness, while Theorem 1.2's presentation formula
inverts a product of upper hook lengths. These are close structural precedents,
but they do not by themselves establish characteristic-three local row spans:
real rank or invertibility cannot simply be reduced modulo three. The examined
statements are not sharp flip-ball interpolation claims.

### 2. Dafni, Filmus, Lifshitz, Lindzey, and Vinyals, Complexity Measures on the Symmetric Group and Beyond

[Author preprint, arXiv:2010.07405](https://arxiv.org/pdf/2010.07405)

The retrieved PDF is the October 2020 v1, 59 pages; the work also has an ITCS
2021 extended abstract and a 2026 journal listing. Theorem 3.2 and Section 3.2
prove a ball property for Boolean functions on composable domains, with
radius beta_c^{-1}(2s+1), where s is sensitivity. Its distance is |x\y|,
which on matchings counts changed matching edges, not two-edge-switch graph
distance. The proof uses majority recovery. This is genuine prior local
recovery work but has different range, parameter, metric, and quantitative
target. It is not a characteristic-three degree-two classification. Sections
5 and 6 also develop real spectral degree and classify Boolean degree-one
functions on perfect matchings.

### 3. Chase, Dafni, Filmus, and Lindzey, Uniqueness for 2-intersecting families of permutations and perfect matchings (2026 journal version)

[Algebraic Combinatorics 9(2), DOI 10.5802/alco.479](https://alco.centre-mersenne.org/item/10.5802/alco.479.pdf)

Section 2.2.1 defines degree of real-valued matching functions using the same
edge indicators. Theorem 2.7 places maximum-size 2-intersecting families in
degree two; Theorem 2.8 classifies Boolean degree-one functions. Theorem 1.4
classifies maximum 2-intersecting families. The hypotheses include Boolean
indicators and intersection restrictions, absent from our arbitrary
characteristic-three polynomial question. In particular, an F3-valued
polynomial need not lift to a real polynomial of the same degree. No direct
implication for the exact modular flip-testing radius was found in these
statements.

### 4. Srinivasan, The perfect matching association scheme (2020)

[Algebraic Combinatorics 3(3), 559–591, DOI 10.5802/alco.104](https://alco.centre-mersenne.org/item/10.5802/alco.104.pdf)

The introduction explicitly works with the complex permutation representation
C[M_{2n}]. The paper supplies algorithms and universal formulas for orbital
eigenvalues, and an inductive eigenvector construction. This is relevant
background for orbit-based evaluation matrices. Its complex eigenspaces and
spectral algorithms do not immediately determine the row span after reducing
a restricted evaluation matrix modulo three. No exact radius-three local
interpolation theorem was identified in the inspected material.

### 5. Bamberg and Klawuhn, On the association scheme of perfect matchings and their designs (v2, 18 March 2026)

[arXiv:2507.00813v2](https://arxiv.org/html/2507.00813v2)

This paper studies lambda-factorisations, designs and antidesigns using the
complex group algebra of S_{2n}. Hyperfactorisations control incidences with
pairs of disjoint edges, so they overlap directly with degree-two matching
monomials. Theorem 1.1 characterizes lambda-factorisations by excluded dual
degree sets. However, uniform-design incidence constraints are different
from expressing one evaluation by a flip-ball-supported linear combination
modulo three. The inspected framework is complex, not modular.

### 6. Aurko Roy, LP and SDP Extended Formulations: Lower Bounds and Approximation Algorithms (PhD dissertation, May 2017)

[Georgia Tech dissertation](https://aco25.gatech.edu/sites/default/files/documents/roy_aurko_thesis.pdf)

Section 2.2.3 proves low-degree certificates for the perfect-matching ideal.
Theorem 2.2.5 states a degree-(2 deg F−1) derivation for real polynomials F
vanishing globally on matchings. Lemma 2.2.6 reduces monomials to partial
matching monomials, exactly the standard reduction our checker uses. The
proof uses averaging by n! and other denominators. Global ideal-membership
certificates over R are not the same as local evaluation recovery over F3,
and the averaging is not automatically available modulo three. This source
therefore establishes methodological overlap, not the exact claimed result.

### 7. Bonamy et al., The Perfect Matching Reconfiguration Problem (MFCS 2019)

[Primary proceedings page, DOI 10.4230/LIPIcs.MFCS.2019.80](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2019.80)

The abstract uses precisely alternating four-cycle flips and studies
reachability complexity and graph classes. It concerns the underlying
reconfiguration operation, rather than low-degree polynomial evaluation or
modular interpolation. Only the primary abstract was inspected here.

## Exact search queries

Queries submitted to the web search tool, in order (quotes preserved):

1. perfect matchings low degree functions polynomial degree matching association scheme characteristic
2. perfect matching association scheme modular characteristic 3 rank
3. "perfect matchings" "low degree" functions Filmus
4. "perfect matchings" "characteristic" "local" polynomials
5. "perfect matching" "modular" "association scheme"
6. "perfect matchings" "interpolation" polynomial flip
7. "Complexity measures on" "beyond" perfect matchings
8. "perfect matching" "characteristic three"
9. "perfect matching association scheme" "modular"
10. "Uniqueness for 2-Intersecting Families" arxiv
11. "Harmonic Polynomials on Perfect Matchings"
12. "perfect matchings" "polynomial" "distance lemma"
13. "matching association scheme" "p-rank"
14. "perfect matchings" "local" "degree" "field"
15. "perfect matchings" "finite fields" polynomial degree
16. "matching inclusion matrices" rank characteristic
17. "perfect matchings" "vanishes" "ball"
18. "perfect matching" "2-switch" polynomial testing
19. "matching inclusion" "Smith"
20. "perfect matching" "local interpolation"
21. "perfect matching" "characteristic 3" polynomial

Primary PDFs/pages were opened and searched for theorem statements, field
assumptions, rank, ball, and distance. An attempted HTML retrieval of
arXiv:2010.07405v5 failed; the primary PDF succeeded. Some exact-word queries
returned unrelated counting, matching-existence, or medical “matching”
results. Those were not evidence for a literature absence. Search indexes,
abstracts, author publication pages, and secondary mirrors were used only to
locate primary material, not as proof of mathematical claims.

## Remaining uncertainty

This check does not exhaust modular representation theory, integral forms or
Smith normal forms of restricted matching inclusion matrices, theses,
unindexed manuscripts, or specialist folklore. Existing full-matrix rank
formulas, if found, would still need comparison to the BASELINE-BALL-RESTRICTED
row span and the exact switch metric. A specialist literature review could
identify a simpler derivation or a previously known equivalent statement.
Until then, describe the outcome as an independently checked exact
classification obtained here, with novelty unassessed.
