# An explicit degree-d matching polynomial with minimum flip support ceil(3d/2)

Parent derivation, pending independent audit and prior-art check. No P vs NP consequence asserted.

Fix baseline pairs (0,1),(2,3),... on 2n vertices. For d>=2 and n>=2d define

 f = product_{i=0}^{d-1} (x_{4i,4i+2} - x_{4i+1,4i+3}).

Over every field, the minimum flip distance of a matching at which f is nonzero is exactly ceil(3d/2). A flip replaces two matching edges with either other pairing of their four endpoints. In particular the universal degree-d testing radius is at least ceil(3d/2) in this range.

Proof of lower bound. Nonzero f means every factor is nonzero. Since indicators are 0 or 1, exactly one of its two edges is present. Hence the two baseline pairs belonging to that factor lie in the same alternating component of the matching against the baseline. That component cannot have only two baseline pairs: in such a component the two specified edges occur together or neither occurs, giving a zero factor. If a component contains t>=1 factors, it therefore has at least max(2t,3) baseline pairs and contributes at least max(2t,3)-1 to flip distance. This number is at least 3t/2: check t=1,2 separately and use 2t-1>=3t/2 for t>=2. Summing over components and rounding gives the claim. Components carrying no factors only increase distance.

Construction attaining the bound. If d is even, partition the factors into groups of size two. If d is odd (necessarily d>=3), use one group of size three and groups of size two. For a cyclically ordered group of t factors with indices i_1,...,i_t, include for each i_j the edge (4i_j,4i_j+2) and the connecting edge (4i_j+3,4i_{j+1}+1), indices j cyclic. These form a single alternating component on 2t baseline pairs. Since t>=2, none of the edges (4i_j+1,4i_j+3) occurs, so all factors equal 1. Leave every unused baseline pair fixed. Each group of size two costs three flips; the group of size three costs five. Total cost is 3d/2 if d is even, (3d+1)/2 if d is odd. The value is 1 over every field.

For d=1 the same product has minimum distance two when n>=3, attained by (0,2),(3,4),(5,1) and outside baseline edges. At n=2 it is identically zero. This exceptional small case is why the theorem states d>=2.

Scope: explicit all-field lower bound, not a matching upper bound or a claim of historical novelty. It reproduces the sharp generic d=2 lower bound three, while characteristic two has a stronger known radius 2d. Arbitrary ambient extension is covered directly by the component proof.
