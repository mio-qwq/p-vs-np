# Semifilter witnesses: exact small lower bound and an infinite-family obstruction

Date: 2026-10-17. Status: checked mathematical derivations and exact finite certificates. No P-versus-NP claim or historical novelty claim. The main negative result is against a proposed witness subclass, not against SAT algorithms.

## 1. Definitions and the intended lower-bound invariant

Use the pinned definitions in [complexitylib2 Semifilter.lean](https://github.com/SamuelSchlesinger/complexitylib2/blob/ffc377b51c1faac475b8cb5376d658fec457e70a/Complexity/Computability/Circuit/Fusion/Semifilter.lean), commit ffc377b51c1faac475b8cb5376d658fec457e70a.

For f:{0,1}^m->{0,1}, let T=f^{-1}(1), V=f^{-1}(0), with both input literals supplied. A semifilter F is an upward-closed predicate on subsets of V, accepting V and rejecting the empty set. It is above x in T if it accepts every restricted literal set {y in V:y_i=x_i}. A pair (A,B) defeats F if F(A)=F(B)=1 but F(A intersect B)=0. A pair cover must defeat every above-target semifilter.

The candidate invariant was a nonnegative weight w(F) on above-target semifilters, satisfying, for EVERY pair A,B subset V,

sum_{F defeated by (A,B)} w(F) <= 1.

Then every unrestricted pair cover has at least sum_F w(F) pairs. This is a genuine all-pair-list lower-bound method: summing the pair constraints over a cover counts every witness at least once. Its limitation is the selected witness class and weight construction, not a missing quantifier over pairs.

We tested three increasingly rich versions: hitting-set semifilters, a successful tiny parity certificate, and radial weighted threshold semifilters for growing parity functions.

## 2. First failed candidate: hitting-set semifilters

Let F_R(S) mean S intersects R, where R is a nonempty subset of V. If F_R is above x, R cannot be a singleton: a sole negative point differs from x in at least one coordinate and misses that target-matching literal.

Choose a uniformly random partition V=A disjoint-union B. For every such witness,

Pr[(A,B) defeats F_R] = 1 - 2^{1-|R|} >= 1/2.

Indeed, defeat means R meets both sides. Averaging shows that for ANY probability distribution on these witnesses, some pair defeats mass at least 1/2. Equivalently, any feasible weight invariant supported only on this class has total weight at most 2.

This is a limitation on fractional/weighted lower bounds from this subclass. It does not say two pairs cover the entire subclass. Integral covering can require more pairs.

## 3. Exact success on parity of three bits

Take T={1,2,4,7}, the odd-parity points, and V=[0,3,5,6] in this order. Encode subsets of V by four-bit masks. Encode a semifilter by a sixteen-bit truth table whose bit S is F(S).

There are exactly 166 nontrivial semifilters on this four-point carrier, and exactly 68 are above at least one target point. The following exact rational weights give total 3:

- F=65534, weight 1. This accepts every nonempty subset.
- F=59624, weight 1/2; minimal accepted subsets have masks 3,5,6.
- F=61064, weight 1/2; minimal accepted subsets have masks 3,9,10.
- F=64160, weight 1/2; minimal accepted subsets have masks 5,9,12.
- F=64704, weight 1/2; minimal accepted subsets have masks 6,10,12.

The four latter filters accept subsets containing at least two of the three negative Hamming neighbors of their corresponding target point. The exact verifier checks all 256 ordered pairs (A,B); the maximum defeated weight is 1. Hence every unrestricted pair cover has size at least 3.

Conversely, the three pairs of subset masks

(3,12), (13,14), (7,11)

defeat all 68 above-target semifilters. Thus the unrestricted pair-cover number of parity3, with both literals supplied, is EXACTLY 3.

This is a finite exact result, not an asymptotic lower bound. It does not depend on treating parity as a monotone function: both positive and negative input literals are included throughout.

The exploratory LP found this certificate, but the final verification uses only Python integers and Fraction arithmetic, and exhaustively enumerates every semifilter and pair. No floating-point optimization result is trusted in the proof.

## 4. Failed extension: radius-one threshold witnesses

For parity on m bits, a natural extension is F_x(S)=[S contains at least m-1 of the m negative Hamming neighbors of x]. This is above x: each target-matching literal contains exactly m-1 neighbors.

It fails dramatically when m=2^r. Label the m coordinates by all vectors in F_2^r, and define the syndrome of a Boolean string y as the XOR of labels of its one-coordinates. Partition V into m syndrome classes C_a.

For every positive x, the syndromes of its m Hamming neighbors are all distinct. Consequently each class C_a contains exactly one of these neighbors. Fix two distinct classes C_a,C_b and set

A=V minus C_a, B=V minus C_b.

Both A and B contain m-1 neighbors of every positive point, while their intersection contains only m-2. Thus this ONE pair defeats every radius-one threshold witness, simultaneously across all target points.

Explicit m=4 example, with odd target parity and even V:

V={0,3,5,6,9,10,12,15}; C_0={0,15}; C_1={3,12}.

The pair (V minus C_0, V minus C_1) defeats all eight radius-one witnesses. This is an infinite-family refutation of the intended extension, rather than extrapolation from one small instance.

## 5. Stronger obstruction: all radial weighted thresholds

One might repair the candidate by using larger Hamming spheres or mixtures of radii. The same syndrome structure prevents that repair from producing a large lower bound.

### Theorem

Let m=2^r with r>=1 and f be parity. For every target point x, let nu_x be ANY probability measure on V that is radially symmetric about x: its mass at y depends only on Hamming distance d(x,y). Different target points may use different radial profiles. Let

F_{x,nu,tau}(S) = [nu_x(S) >= tau],

where 0<tau and F is above x. There is a single list of r=log2(m) pairs of subsets of V defeating ALL such filters, simultaneously for every x, every radial profile, and every allowable threshold.

### Uniform syndrome lemma

For every odd radius d and every x, the sphere of radius d about x is uniformly distributed over the m syndrome classes.

To prove this, identify coordinate subsets D of size d with the points y=x XOR 1_D. Translating every coordinate label by h in F_2^r permutes the d-element subsets. Since d is odd, this translation changes the XOR of the labels in D by h. Hence all possible XOR values occur equally often. XOR with the fixed syndrome of x merely permutes them. Every syndrome class therefore contains binom(m,d)/m points of the sphere.

A radial measure is a mixture of the uniform measures on the odd-radius spheres, so nu_x(C_a)=1/m for every class a.

### The covering pairs

Fix an ordering of the syndrome classes. For each q in {1,2,4,...,m/2}, let A_q omit the first q classes and let B_q omit the next q classes. The omitted class groups are disjoint. Uniformity gives, for every radial profile and x,

nu_x(A_q)=nu_x(B_q)=1-q/m,
nu_x(A_q intersect B_q)=1-2q/m.

If the mean Hamming distance under nu_x is E[d], radial symmetry gives mass 1-E[d]/m to every target-matching literal. The above-target condition therefore implies

0<tau <= 1-E[d]/m <= 1-1/m.

Put h=m(1-tau). Then 1<=h<m. Choose q as the largest power of two not exceeding h, so q<=h<2q and q<=m/2. It follows that

1-q/m >= tau > 1-2q/m.

Thus A_q and B_q are accepted but their intersection is rejected. The SAME fixed list of log2(m) pairs covers every allowed filter. QED.

### Consequence and limits

Any lower-bound argument using only this radial weighted threshold subclass, including any feasible fractional witness weighting on it, can establish at most log2(m) pair-cover lower bounds at these lengths. This is an actual small integral cover of the subclass.

It is NOT a logarithmic cover of all semifilters. Unrestricted, nonradial, or non-threshold witnesses may survive all these pairs. Parity itself has small general circuits and is only a test family, not a proposed NP-hard witness. The obstruction does not imply that the same syndrome partition works for SAT targets.

## 6. Checks and reproduction

- The exploratory `search_covers.py` used SciPy to discover candidate weights; it is not required or included in this minimal exact-verification packet.
- Exploratory floating-point LP output is not used as proof and is omitted from this packet.
- `verify_certificates.py`: standalone exact verifier with no SciPy dependency.
- `certificate_results.json`: exact results.

The exact verifier checks all 65,536 sixteen-bit predicates to identify the semifilters, all 256 pairs for the rational dual, and the three-pair upper cover. It also enumerates odd coordinate subsets at m=2,4,8,16 to check syndrome uniformity. It checks all distinct integer threshold behaviours on each uniform sphere: respectively 1,4,64,16,384 thresholds. The general weighted-profile result follows from the proof by convex mixture, not from a finite random sample.

All exact checks passed. The independent auditor also verified the parity3 certificate separately in `negative-check/verify_parity3.py`.

## 7. Literature check and correction to round 2 context

The fusion-cover framework and its cyclic characterization are established literature. In particular, Cavalar and Oliveira, *Boolean Circuit Complexity and Two-Dimensional Cover Problems* (2025), [arXiv:2503.14117v1](https://arxiv.org/html/2503.14117v1), Theorem 24, already gives an O(rho^2) acyclic intersection bound. Their Section 4.2 gives a logarithmic canonical-filter bound for inequality graphs.

Therefore the preceding round's quadratic unrolling was an independently checked application/reproduction, not a historically new bound. Its note disclaimed novelty; this source now makes the prior result explicit. The present radial obstruction is reported as a derivation tested here, without claiming that nobody previously observed it.

## 8. Actual research state and next requirement

We obtained a valid all-pairs rational invariant at one finite instance, then falsified two plausible scalable witness classes: hitting-set weights and all radial threshold witnesses on parity at power-of-two dimensions. These attempts are stopped as routes to a strong lower bound.

A viable replacement must supply genuinely nonradial or non-threshold structure, or a direct integral adversary depending on the entire proposed pair list. It must defeat arbitrary pairs of arbitrary subsets, not just pairs obtainable from a chosen restricted circuit model. To reach the SAT/P/poly target, one ultimately needs a superpolynomial lower bound across input lengths. No such invariant is presently constructed here. Finite enumeration alone does not bridge this gap.
