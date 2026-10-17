# Independent challenge of the grouped pair-difference lower bound

Verdict: valid. In fact the construction works over every nonzero commutative unital ring, since all factor values on matchings are 0 or +/-1 and the witness value is +1.

Let q_d be the product, for i=0,...,d-1, of (x_{4i,4i+2}-x_{4i+1,4i+3}). Its degree is d and it uses 2d disjoint baseline pairs. If q_d(M) is nonzero, each factor has exactly one indicated edge present. That edge places its two baseline pairs in one alternating component. That component cannot have size two: the other indicated edge would then be forced, making the factor zero.

Assign each factor to the component containing its present indicated edge. A component with t>=1 assigned factors uses s>=2t baseline pairs because the factors have disjoint pair supports. It also has s>=3. Its distance contribution s-1 is therefore at least max(2t,3)-1 >= 3t/2 (t=1 gives 2>=3/2; t>=2 gives 2t-1>=3t/2). Summing, and using integrality of distance, gives distance(M,B)>=ceil(3d/2). Components receiving no factor only increase distance. This includes arbitrarily large ambient sets; no extension assumption is needed.

For two factors on pairs 0,...,3, take actual matching edges {(0,2),(4,6),(3,5),(1,7)}. Its contracted graph is one four-pair cycle, distance three, and both factors equal +1.

For three factors on pairs 0,...,5, take {(0,2),(4,6),(8,10),(3,5),(7,9),(1,11)}. Its contracted graph is one six-pair cycle, distance five, and all factors equal +1.

For even d, concatenate disjoint copies of the two-factor block. For odd d>=3, use one three-factor block and (d-3)/2 two-factor blocks. All 2d pairs are used and every other baseline pair is unchanged. The product equals +1 and distance equals ceil(3d/2). Thus q_d has minimum nonzero distance exactly ceil(3d/2) for d>=2 and n>=2d. Consequently the universal degree-d testing radius is at least this value.

For d=1, n=2 the factor is identically zero. For n>=3, edges {(0,2),(1,4),(3,5)} give value +1 and distance two; this agrees with ceil(3/2). The third pair is essential. Degree zero is the separate constant case.

Independent exhaustive verification in check.py evaluates the integer product on every matching for n=2,...,7 and every d with 1<=d<=floor(n/2), totaling 12 parameter cases. The observed minimum nonzero distance is exactly the claimed value in every admissible case, and the n=2,d=1 case is identically zero. Results are in results.json.
