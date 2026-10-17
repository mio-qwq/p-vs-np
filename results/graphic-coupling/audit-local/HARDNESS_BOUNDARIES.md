# Audited sharpness boundaries for the graphic matching subclass

These are polynomial reductions and finite independent checks, not novelty claims. The distance-two transfer assumes the previously established NP-hardness of arbitrary remote globally disjoint conflict pairs. The local-overlap reduction directly starts from graph 3-colorability.

## Globally disjoint conflict pairs at line-graph distance at most two

Start with a simple graph G, parity vector b, and globally disjoint forbidden edge pairs. Subdivide every edge e=vw once, with new midpoint u_e of parity target zero, giving halves v-u_e and u_e-w. Mark either half; replace each old forbidden pair {e,f} by the pair of marked halves.

For each such pair, add connector c=u_e-u_f and a fresh pendant edge d=u_e-l. Set b_l=1 and toggle the midpoint target b_{u_e} from zero to one. Add the new forbidden pair {c,d}.

The leaf equation forces d=1. Its guard pair forces c=0. The target-one equation at u_e now cancels the pendant contribution and forces equality of its two old halves. At u_f the target-zero equation also forces equality of the two old halves. Thus every original solution has one and only one extension: copy each old edge's value to both halves, set all connectors to zero and all pendants to one. Conversely every transformed solution has exactly that form and restricts to an original solution.

Each pair of marked halves is at line-graph distance at most two via c. If its original edges were endpoint-disjoint, the distance is exactly two. Each guard pair is at distance one. The construction preserves simplicity: distinct original edges have distinct midpoints, connectors are between midpoints, and pendant leaves are fresh. It preserves global pair disjointness: only one half of each old paired edge is used, and every new c,d pair is fresh.

For n original vertices, m edges and p pairs, the output has n+m+p vertices, 2m+2p edges and 2p pairs. Targets may acquire two new odd vertices per guard; **fixed target-set size, including |T|=2, is not preserved**. Planarity or series-parallel structure is not asserted after the connectors are added.

Consequently hardness for arbitrary remote disjoint pairs transfers to the class where every pair has line-graph distance at most two, for unrestricted parity targets. This sharply differs from the common-endpoint, locally disjoint class reduced to matching.

## Overlapping conflicts all hosted at one vertex

Given a graph H with n vertices, create one center c. For each v in V(H), create an outer vertex v and three internally disjoint length-two paths c-u_{v,j}-v, j=1,2,3. Give outer vertices target one, intermediate vertices target zero, and c target n mod2.

Mark the center edge of every path. At c place all three pairwise conflicts between the three marked edges belonging to each v. Also, for each H-edge vw and each color j, forbid the two marked edges (v,j),(w,j). All conflicts are between incident edges at the **same center**, but an edge can participate in several conflicts.

The intermediate parity equations make each path's two edges equal. The odd outer equation permits either one or three selected paths. The three local conflicts forbid selecting two or more, leaving exactly one, which defines the color of v. Conflicts corresponding to H-edges prohibit equal colors. The center equation is automatically satisfied because exactly n marked edges are selected.

Thus proper 3-colorings of H and valid T-joins are in bijection. The host graph is simple and consists of n three-path branches sharing one center. This proves the necessity of a disjointness or comparable tractability restriction: “all conflicts have a common endpoint” alone does not make the problem polynomial unless P=NP.

There are 1+4n host vertices, 6n host edges, and 3n+3|E(H)| forbidden pairs. This statement concerns overlapping conflict pairs; it does not contradict the globally disjoint local-pair theorem.

## Independent finite verification

check_hardness_transforms.py implements Gaussian affine-solution enumeration for arbitrary graph parity equations, then filters all conflict pairs. It does not force the intended guard values as part of its solver.

- 1,200 random distance-two transformations passed exact whole-solution-set bijection checks, simplicity, global pair disjointness, and actual line-graph distance checks.
- Every simple source graph on n=0,1,2,3,4 vertices was tested for the 3-coloring reduction (76 graphs including the zero-vertex graph). Exhaustively enumerated proper colorings and gadget solutions agree bijectively, and every conflict's endpoints are hosted at c.

These tests support the implementations; the proofs establish the unbounded reductions.
