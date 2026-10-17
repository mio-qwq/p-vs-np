# Independent audit of finite pair-state unrolling

Source inspected locally: Complexity/Computability/Circuit/Fusion/Cyclic/Compiler.lean at commit ffc377b51c1faac475b8cb5376d658fec457e70a, in the supplied complexitylib2 repository.

Let k be pairs.length and define F_j(S)=readState(S,a_j) intersect readState(S,b_j). The source's readState expression at a point u is an OR of a constant, membership bits of the fixed input sets, and selected S_j(u) bits. Selection depends on fixed global subset predicates, not on evolving states. Thus for each point u the pair update is a monotone Boolean map F_u:{0,1}^k->{0,1}^k.

Start S^0 at the empty sets and iterate S^(t+1)=F(S^t). For each u, the Boolean trajectory is increasing: bottom<=F(bottom), then monotonicity propagates the inequality. Every strict transition changes at least one of k bits from 0 to 1, permanently. Consequently at most k transitions are strict and F_u^k(0)=F_u^(k+1)(0). The same k works for every u, so set extensionality gives S^k=S^(k+1), including when the carrier is infinite. Iteration from bottom is below every prefixed point, hence this fixed point is the least one.

The pair state is independent of the additional output coordinate. After k pair-state updates, evaluate readState(S^k, empty) to obtain the intended output. If one instead iterates the full simultaneous map including the output coordinate, that output may lag the pair state by one round; k+1 full rounds are a safe bound. This is not a bound on individual internal-gate feedback propagation.

Unroll k layers of the k pair updates, retaining DAG sharing of preceding-layer state outputs. Each update contains exactly one charged AND, so the construction uses k^2 charged AND gates, followed by a free-OR output read. Read expressions have O(n+k) OR/constant/input occurrences, giving a conservative O(k^2(n+k)+(n+k)) total-gate bound for this straightforward construction. These are different cost measures. Recursive formula expansion without sharing need not satisfy the same size bound.

The resulting circuit's existence does not provide a uniform efficient compiler: the source chooses active seeds by classical subset tests over arbitrary sets. The statement is special to the pointwise set/Boolean interpretation; a general monotone self-map of an arbitrary complete lattice need not stabilize after k steps merely because it has k coordinates. It is not a P/NP lower bound and has not been formalized in Lean by this audit.

Independent finite sanity test: check_pointwise_unrolling.py exhausts every monotone Boolean network on k=1,2,3 coordinates (3,36,8000 networks respectively), verifies stabilization by k, and records tight examples at each k in pointwise_unrolling_result.json. The mathematical pointwise argument, not these finite checks, proves the arbitrary-k statement.
