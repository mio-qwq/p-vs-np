# Independent audit: parity cover certificate and radial witness obstruction

Status: PASS for the precise restricted statements below. No public conjecture is claimed false; no P/NP separation follows.

## Definitions checked directly

Inspected complexitylib2 commit ffc377b51c1faac475b8cb5376d658fec457e70a, Complexity/Computability/Circuit/Fusion/Semifilter.lean. A semifilter is an upward-closed family accepting the full negative carrier V and rejecting the empty set; it need not be intersection-closed. A witness at a target point x accepts every supplied literal set that contains x, after restriction to V. A pair (A,B) defeats the witness precisely when F(A) and F(B) hold and F(A intersect B) fails. The pair-cover quantifier ranges over all such witnesses, with no assumed locality of pairs.

## Parity on three bits: exact unrestricted optimum 3

Target T={1,2,4,7}; negative carrier V=[0,3,5,6]. Independently enumerated all monotone truth tables on the sixteen subsets of V, with top true and bottom false, obtaining 166 semifilters. Exactly 68 are above at least one target point. Collapsing duplicate occurrences of the same filter at different target points is legitimate here: whether a pair defeats it depends only on the filter, not on the chosen point.

The dual gives weight 1 to the nonempty-set semifilter, and weight 1/2 to each of the four semifilters accepting sets that contain at least two of the three Hamming neighbors of a positive point. Their filter masks are 65534,59624,61064,64160,64704. Multiplying weights by two, all 256 ordered subset pairs have total defeated weight at most 2, while total witness weight is 6. Thus every fractional pair cover costs at least 3. The three pairs, in four-bit subset encoding, (3,12),(13,14),(7,11), defeat every one of the 68 filters. They give both fractional and integral upper bound 3. Both optima are therefore exactly 3, without relying on floating-point optimization.

Reproduction: verify_parity3.py; parity3_verified.json.

## Infinite family: neighbor-threshold witnesses all defeated by one pair

Let m=2^r, r>=1, and label the m coordinates by all elements of F2^r. Let target points have odd parity and V consist of even-parity strings. Define syndrome sigma(y) as the XOR of the labels of coordinates where y has value 1. For every positive x, its m negative Hamming neighbors have syndromes sigma(x) XOR i as i ranges over all labels. Hence each syndrome class contains exactly one neighbor.

Fix two distinct syndrome classes C0,C1 and set A=V minus C0, B=V minus C1. Every positive x has m-1 neighbors in A, m-1 in B, and m-2 in their intersection. Therefore the semifilter F_x(S)=[|S intersect N(x)|>=m-1] accepts A and B but rejects their intersection. It is a valid semifilter and above x: each matching-literal set contains exactly m-1 of x's neighbors. Consequently this entire witness family has a one-pair cover. It cannot certify growing unrestricted cover lower bounds via a weighted pair-load argument.

## Extension: all radial weighted threshold witnesses have a logarithmic pair cover

For each positive x, choose an arbitrary probability distribution nu_x on V whose point weights depend only on odd Hamming distance from x. Different x may have different radial profiles. For any fixed odd radius d, a negative y corresponds to a d-subset J of flipped coordinate labels, and sigma(y)=sigma(x) XOR XOR(J). Translating all labels in J by h permutes the d-subsets and changes XOR(J) by h, since d is odd. This establishes equal mass 1/m in each syndrome class for every sphere and hence every mixture.

Every matching-literal set has the same mass p=1-E[d]/m. The threshold family F(S)=[nu_x(S)>=tau] is a semifilter above x exactly when 0<tau<=p. In particular p<=1-1/m. Fix an ordering of the syndrome classes. For each q in {1,2,4,...,m/2}, let A_q exclude the first q classes and B_q exclude the next q classes. Their masses are 1-q/m individually and 1-2q/m at intersection.

Set t=m(1-tau). The seed constraint and positive threshold give 1<=t<m. Choose the unique dyadic q with q<=t<2q. Then 1-q/m>=tau while 1-2q/m<tau. Thus (A_q,B_q) defeats this witness. The same r=log2(m) pairs work for every x, every radial profile, and every permitted threshold. Equality at the individual-set threshold is handled correctly; rejection of the intersection remains strict.

This is only an upper cover for the radial-threshold subclass. Arbitrary semifilters need not be thresholds of radial measures. The result does not upper-bound unrestricted cover complexity.

Independent exact checks in verify_radial_attack.py verify neighbor-class uniqueness for every positive vertex at m=2,4,8, and test two mixtures over all odd spheres, including threshold boundaries, in 1344 cases using rational arithmetic. Output: radial_attack_verified.json. The symmetry and dyadic arguments, not finite checks, establish all powers of two.

## Scope

The finite exact optimum is a certificate for a toy target. The infinite construction refutes the proposed local/radial witness strategy as a source of large cover lower bounds. It neither refutes the repository's semifilter theorems nor proves that unrestricted witnesses cannot produce strong lower bounds. No publication or repository mutation was performed by this audit.
