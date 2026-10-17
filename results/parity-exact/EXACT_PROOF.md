# Exact cyclic supplied-literal AND complexity of parity

Date: 2026-10-17. Mathematical proof for independent audit. Historical novelty is unverified. No Lean formalization or human peer review is claimed.

## Theorem and model

For m>=2 the odd-parity function on m coordinates has minimum binary AND cost exactly 2m-3 in finite monotone cyclic circuits supplied with both literals of each input coordinate, with free OR gates and constants, under least-fixed-point semantics. For m=1 the cost is zero. By the cost-preserving correspondence proved in model-linkage.md, the unrestricted semifilter pair-cover cost is the same.

Every gate is monotone in its inputs. The 2m supplied literal tokens are evaluated consistently for computing parity, but the same circuit defines a monotone function on all independent token assignments. Negations of internal states and XOR gates are not allowed. Only AND gates are counted. Cycles are interpreted by iteration from the all-zero internal state. Arbitrary finite OR expressions are shorthand for free binary OR networks.

Let r_m be the minimum AND cost. Complemented parity has the same cost: exchange the two supplied tokens of one coordinate.

## 1. Normal form and the basic restriction bound

Collapse the OR-only subsystem by reachability, preserving its least solution. The k charged states then satisfy

    y_j = (OR A_j) AND (OR B_j),

where operands are finite sets of literal tokens, charged-state references and constants. The output is an OR of these sources. OR cycles without a seed stay false. Delete states with no directed path to output.

A constant-one operand makes the AND free OR; a constant-zero operand makes the state zero. Eliminate these states, absorbing any resulting OR cycles by least semantics. Direct self references can be deleted: replacing (y OR A) AND B by A AND B, or (y OR A) AND (y OR B) by A AND B, preserves the simultaneous least fixed point. Indeed the new map G is at most F, and any fixed point v of G also fixes F by absorption. Thus their least fixed points agree. This remains true with feedback through other states.

For m>=2 the output cannot contain a literal directly or a true constant, because parity is not identically one on a literal half-cube. A nonconstant parity computation must have some literal feeding an AND state. Setting that literal true converts at least one charged state to free OR, leaving parity or complemented parity on m-1 coordinates. Therefore

    r_m >= r_(m-1)+1,  m>=2.

If a literal occurs in two distinct charged states, the same restriction eliminates both, giving the stronger lower bound r_(m-1)+2.

Fix any circuit with k ANDs computing parity on m>=3. Any equivalent circuit with <=k-1 ANDs also yields k>=r_(m-1)+2 by the basic bound. Thus any gate-saving simplification is already a success for the stronger inequality. For the remaining case assume gate count is unchanged and each literal occurs in at most one charged state.

## 2. Remove double-operand occurrences

If a literal l appears in both operands of state y, write

    y = (l OR A) AND (l OR B) = l OR (A AND B).

Replace y everywhere by l OR z and use the single charged equation z=A AND B. There is no direct self reference after the preceding cleanup. This changes no other literal's direct locations and preserves the state-dependency graph, with z replacing y.

For least-fixed-point preservation, let phi replace z by l OR z at that coordinate and leave the others unchanged. If F' is the new map, F(phi(z))=phi(F'(z)), and 0<=phi(0)<=F(0). Thus iteration of F from phi(0) has the same finite limit as iteration from zero; the output substitutions preserve its value.

Now l occurs at the consumers of y. If two different states consume y, the repeated-state restriction applies. If the output consumes y, a direct output literal contradicts parity. Otherwise there is one state consumer. If l occurs in only one of its operands, the cleanup for l is finished; if in both, repeat.

This process follows a unique-outdegree walk in a fixed directed state graph. Every retained state has a path to output. Such a walk cannot enter a cycle, since a closed unique-outdegree cycle has no path to output. Hence the cleanup terminates. If a constant operand or another gate-saving reduction arises, the stronger inequality already follows. Repeating over the finitely many literal tokens leaves each token in at most one operand globally, unless an earlier success occurred.

## 3. Two literals cannot share one operand

Suppose an operand contains literals l,h of different coordinates. Since m>=3, some consistent positive-parity assignment makes both true. The positive output at that assignment has a finite first-activation derivation, which can be unrolled as a proof tree: choose one true predecessor at each OR and both at each AND.

Whenever this operand is used, choose l as its OR witness. Then h never appears as a leaf, because this is its only direct occurrence. Its opposite token also never appears, since it is false at the chosen consistent assignment. Thus the derivation omits that coordinate entirely. Flipping this coordinate preserves all its true proof leaves and hence the output, but flips parity, a contradiction.

Complementary literals in a single operand make that operand constantly true on consistent inputs and permit a gate-saving simplification. Hence in the remaining case each operand contains at most one input literal.

## 4. A unique opposite-operand bottleneck forbids an OR minor

Consider any finite monotone cyclic circuit with independent tokens l,h whose only direct occurrences are in opposite operands of one AND state g:

    g = (l OR A) AND (h OR B).

No other equation or the output directly contains l or h. Fix every other token arbitrarily. Clamp g=0 and let W_0 be the least closure of all other states. The values A_0,B_0 and output O_0 there are independent of l,h.

If O_0=1, every setting of l,h accepts, so the output is not OR. Suppose O_0=0. Any accepting computation must eventually activate g. Before its first activation all other states are bounded above by W_0. Therefore acceptance at (l,h)=(1,0) forces B_0=1, and acceptance at (0,1) forces A_0=1.

If both settings accept, then at (0,0) the actual monotone iteration dominates the g-clamped-zero iteration, so it reaches or dominates W_0 and activates g. Once g is active it stays active. The remaining state equations contain neither l nor h, so their least closure with g=1 is the same for all four settings and contains the accepting output from either setting. Thus (0,0) also accepts. This contradicts OR.

Equivalently the possible two-token functions are only 0,1,l,h,l AND h: the least activation of g is (l OR A_0) AND (h OR B_0), followed by a monotone unary output function. The argument does not require the whole circuit to be acyclic.

## 5. Every monotone extension of parity has the forbidden OR minor

Let l,h belong to different coordinates. Fix their opposite tokens to 1. Fix all other coordinates consistently so that the consistent assignment with l=h=0 has negative parity. There is at least one remaining coordinate because m>=3, so this choice is always possible.

At (l,h)=(0,0), the circuit outputs zero by correctness on consistent inputs. At (1,0), the independent-token assignment dominates the consistent positive input obtained by flipping l's coordinate: its opposite token is still one, rather than zero. Monotonicity therefore forces output one. Likewise the output at (0,1) is one, and monotonicity also gives one at (1,1).

This is an OR minor. Correctness on inconsistent inputs is not assumed; only monotonicity of the circuit on those inputs is used. By the bottleneck lemma, two different-coordinate tokens cannot be the unique literal seeds in opposite operands of the same state.

## 6. No initial seed remains: contradiction and recurrence

In the cleaned case a state with a literal-free operand cannot activate from the all-zero charged state. If both operands contain a literal, the literals cannot be equal by double-operand cleanup, nor from different coordinates by the OR-minor argument. They must be complementary literals of the same coordinate. These are never simultaneously true on a consistent input, so this state cannot initially activate either.

Thus no state activates at any consistent input. There is no direct output literal or true constant, so the output is always zero, contradicting positive parity inputs. The cleaned no-repeat case is impossible. An earlier success must therefore occur, proving

    r_m >= r_(m-1)+2 for every m>=3.

The two-bit XOR CNF uses one AND, and the basic restriction bound with r_1=0 proves r_2=1. Induction gives r_m>=2m-3 for m>=2.

## 7. Matching upper construction

For prefix odd parity p and its complement q, adjoining coordinate x uses

    p_new = (p OR x) AND (q OR NOT x),
    q_new = (p OR NOT x) AND (q OR x).

Start with the free input rails for one coordinate. Build both rails at every intermediate coordinate, costing two ANDs each, and only the odd rail at the final coordinate, costing one. For m>=2 the total is 2(m-2)+1=2m-3. This is acyclic, hence valid in the cyclic model. The lower and upper bounds agree.

## Scope, provenance and checks

The exact cover/cyclic characterization is established prior work: Cavalar–Oliveira, arXiv:2503.14117v1, Theorem30, adapting Nakayama–Maruoka (1995). model-linkage.md supplies both cost-preserving reductions for these precise conventions. The gate-elimination and monotone-extension ideas require further historical comparison; no first-discovery claim is made.

The earlier odd-seed argument is retained separately as a weaker independently audited route. This proof removes its even-cycle limitation through the OR minor. It no longer requires the finite four-bit lower certificate as a base; that independently verified certificate remains a useful independent consistency check.

Finite regression checks include least-fixed-point cleanup, exhaustive two-state bottleneck tables, odd-seed CNFs and explicit dual-rail circuits. They do not replace the general proof. Parity already has linear-size circuits, so this exact linear cost theorem does not separate P from NP or furnish a superpolynomial lower bound.
