# Independent audit: universal +2 through the forbidden OR minor

Date: 2026-10-17. Mathematical audit only; no historical novelty or formal-verification claim.

## Source and verdict

Reviewed EVEN_CASE_OR_MINOR_CANDIDATE.md at SHA-256:

    ddedac566f2b4518c54486dee65d73cbe1b91f58d9c354134580274c9b491cf5

**PASS. No genuine gap found.** The proposed universal increment by two follows in the stated cyclic supplied-literal AND/OR model. Together with the elementary upper construction, it proves exact AND complexity 2m-3 for m>=2. The previous independently certified four-variable optimum is no longer needed as a premise.

Any corresponding fusion-cover statement still uses the separate exact model-linkage result. Historical status is outside this audit.

## 1. Fully explicit bottleneck lemma

Let l,h be independent Boolean input tokens. Their only direct occurrences are in respective opposite operands of one AND state g:

    g = (l OR A) AND (h OR B).

Neither appears in any other state equation or directly at output. Fix all other input tokens arbitrarily, even inconsistently with literal-pair encodings. Let u collect all other states. Their update is a monotone function F(u,q), where q is the value supplied for g; it is independent of l,h. Define

    w0 = lfp_u F(u,0),
    w1 = lfp_u F(u,1).

Monotonicity implies w0<=w1. Write a=A(0,w0), b=B(0,w0), and

    E(l,h) = (l OR a) AND (h OR b).

The following proves the global least fixed point directly, without relying on an informal scheduling argument or an unproved block-elimination formula.

If E=0, the vector (0,w0) is a fixed point of the full system. Its least fixed point is at most that vector, so its g coordinate is 0. Its remaining coordinates are a fixed point of F(u,0), hence at least w0. Thus the global least fixed point is exactly (0,w0).

If E=1, the global least fixed point cannot have g=0. Indeed, its remaining coordinates would be a fixed point of F(u,0), at least w0, which would force the g update to be at least E=1. Also, (1,w1) is a fixed point of the full system: by monotonicity the g update there is at least E=1, and the other equations are satisfied by definition. Therefore the global least fixed point is at most (1,w1). Its g coordinate is 1, so its remaining coordinates are fixed under F(u,1), at least w1. Consequently it equals (1,w1).

This argument even allows direct self references of g in A or B; preprocessing them away is not required for this lemma.

The output is an OR of fixed other inputs and state values and has no direct l,h occurrence. Its values O0 at (0,w0) and O1 at (1,w1) are constants satisfying O0<=O1. Therefore the two-token output is either constant 0, constant 1, or exactly E. Since a,b are constants, E is one of 1,l,h,l AND h. OR is not among these possibilities.

All feedback through g is accounted for by w0 and w1. No arbitrary fixed point is substituted for the least one.

## 2. Fully explicit parity OR minor

A finite monotone circuit's least output is monotone in its independently interpreted input tokens: compare the two least-point iteration sequences coordinatewise. Correctness is required only on consistent literal-pair inputs, but this monotonicity holds on the entire independent-token cube.

Let m>=3 and choose any two tokens l,h belonging to distinct coordinates. Fix their opposite tokens to 1. Fix the other m-2 coordinates consistently, choosing them so that the input with l=h=0 has negative parity. This is possible because at least one remaining coordinate is free.

The minor point 00 is a consistent negative input, so its output is 0.

Starting from this consistent input, flip only l's original coordinate. The resulting consistent input has positive parity, l=1, opposite(l)=0, and h=0, opposite(h)=1. It is coordinatewise below the minor point 10: the latter differs only by retaining opposite(l)=1. Hence the output at 10 is at least 1 and thus equals 1. The corresponding argument for h yields output 1 at 01. Monotonicity then gives output 1 at 11.

Thus every monotone extension of parity has an OR minor on every pair of different-coordinate literal tokens. This does not presume correctness on inconsistent inputs. Only monotonicity on those inputs is used. Signs of the selected tokens do not matter; changing either selected coordinate flips parity regardless of which polarity was chosen as its token.

## 3. Combining the lemmas with cleanup

The previously audited normal form and cleanup have the following consequences unless restriction already removes at least two gates:

- No literal occurs in two distinct charged states.
- Double-side occurrences of one literal can be factored and pushed until every literal occurs in at most one operand globally.
- Direct output literals and true output constants are impossible for parity on m>=2.
- Constant-one operands can be eliminated; a gate-saving equivalence by itself yields +2 when combined with the universal +1 recurrence.
- Two different-coordinate literals cannot share an operand: a positive finite activation proof can choose one and omit the uniquely occurring other coordinate, contradicting parity's implicant property.
- Complementary literals in one operand make that operand constantly true on consistent inputs, yielding the gate-saving case.

Now suppose an AND state has different-coordinate literals in its two opposite operands. Each is globally unique after cleanup. The bottleneck lemma says that after any fixing of other input tokens, the output cannot be OR on these two tokens. The parity extension lemma provides a fixing making it exactly OR. Contradiction.

Thus an AND state either has a literal-free operand, or the literals in its two operands are complementary tokens of the same coordinate. Equal tokens across operands were removed by double-side cleanup. At any consistent input and with all states initially zero, a literal-free operand is false, and complementary tokens cannot both be true. No AND state can activate. The all-zero state is a fixed point and hence the least one, so the output is identically false on consistent inputs. This contradicts parity.

The no-repeat alternative is therefore impossible for every m>=3, not merely odd m. A literal restriction eliminating two gates, or the already sufficient gate-saving case, must occur.

## 4. Exact consequences

For m>=3:

    r(m) >= r(m-1)+2.

Since r(2)=1, induction gives r(m)>=2m-3 for every m>=2. The explicit dual-rail construction from the earlier PROOF.md gives r(m)<=2m-3, so

    r(m)=2m-3 for every m>=2, and r(1)=0.

The upper construction is independently verified in final-audit.md. The new stronger argument removes the earlier dependence on a separate r(4)=5 optimum for deriving r(5)=7. It also gives r(6)=9 and all higher values, within this circuit model.

This exact linear bound has no P-versus-NP separation consequence.

## 5. Additional finite regression

I created and ran check_bottleneck_minor.py, SHA-256:

    42857f6e8e9d156d38a9de07827765c99688fd12a555527f039680d520b119da

The checker uses seed 17062026 and generates 20,000 random circuits with 1 through 8 charged states, arbitrary feedback including self loops, a randomly chosen unique distinguished bottleneck, six other fixed independent tokens, and outputs containing no direct distinguished token. It evaluates each circuit on all four l,h settings: 80,000 least-fixed-point evaluations.

Every resulting truth table was in {0,1,l,h,l AND h}. Counts, in input order 00,01,10,11:

- 0000: 2602
- 0001: 712
- 0011: 415
- 0101: 410
- 1111: 15861

Machine-readable results are in bottleneck_minor_result.json. This finite randomized regression supports implementation sanity only; the universal proof is the fixed-point argument above.

## 6. Acceptance audit of the unified final source

After writing the independent arguments above, I read the complete unified EXACT_PROOF.md and verified its SHA-256:

    7a247a5152549bc1e1ced2423b34bf5fc9bd8238d05173e4d72991c61680de7f

**ACCEPTED for the mathematical circuit-model theorem at these exact source bytes. No genuine gap found.** Sections 1-3 correctly supply the normalization and cleanup hypotheses required by the new lemmas, sections 4-5 correctly establish the bottleneck contradiction, section 6 obtains the universal +2 recurrence and base case without finite certification assumptions, and section 7 gives the matching construction.

In particular:

- Section 4's clamped-zero trajectory is dominated by actual monotone iteration; after g activates, the common g=1 closure gives the same possible accepting output. The direct fixed-point proof in section 1 of this audit independently justifies these steps.
- Section 5 validly uses inconsistent assignments only through monotonicity, not through an unwarranted extension of the parity correctness promise.
- Simplifications valid only on consistent inputs, such as replacing an operand containing both polarities by true, do not undermine the extension lemma. The simplified circuit is still monotone on the whole independent-token cube and correct on the consistent subdomain, which are exactly its hypotheses.
- Every gate-saving normalization is already sufficient through the separate +1 restriction bound. Thus these exits do not assume the +2 theorem being proved.
- The exact result no longer depends on r(4)=5, a SAT solver, or an enumeration.

This acceptance concerns the complete circuit proof. The transfer to unrestricted semifilter pair-cover cost uses the separate model-linkage result and audit; I have not independently reread that separate proof here. Likewise bibliographic details and the stated exhaustive two-state regression are supplied by other work, not independently verified by this reviewer. They are not premises of the circuit theorem.
