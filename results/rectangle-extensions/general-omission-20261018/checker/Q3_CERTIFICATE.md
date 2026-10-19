# Exact three-omission collision certificate

This compact example genuinely needs cancellation in a smaller Laplace layer: the maximal-layer cancellation loss is 9, whereas the next layer's raw degree gap is only 7.

## Input and polynomial identity

All indices are zero-based. Take

    n=12, r=3, q=3,
    offsets=(0,1,2,3,4,5,6,7,8,9,10,11),
    exponents=(0,1,2,5,6,10,12,16,17,20,21,22),
    I=(0,1,2), J=(0,3,4,7,8,11),
    X=(0,5,6,16,17,22), Y=(1,2,10,12,20,21).

With u=T−11, the root polynomials are

    f(T)=(u²−121)(u²−36)(u²−25),
    g(T)=(u²−100)(u²−81)(u²−1).

The first two elementary symmetric functions of the respective squared roots agree:

    121+36+25=100+81+1=182,
    121·36+121·25+36·25=100·81+100·1+81·1=8281.

Hence

    g(T)−f(T)=108900−8100=100800=:C.

The roots are pairwise distinct across both sets, and are nonnegative integers. The exact constant remainder is R=C.

## Exterior certificate and row factor

For 1≤k≤6, the first k moment rows have greedy pivot columns

    B_k={6−k,7−k,…,5}.

Indeed μ_0=⋯=μ_4=0 and μ_5=C. The corresponding first shape, degree, and value are

    λ^(k)=((6−k)^k), κ_k=k(6−k),
    E_k(s_λ)=(-1)^(k(k−1)/2) C^k.

The checker verifies every Schur value at every degree up to κ_k by summing directly over k-node subsets, for all six k. In particular κ_3=9, λ^(3)=(3,3,3), and γ=−C³.

For the rectangular target, the row factor has the explicit finite expression

    B=Σ_(η⊆(3³)) (−1)^|η| T_3(η′;(0,1,2))
                              T_9((3−η_3,3−η_2,3−η_1);(3,…,11)),

where

    T_b(α;A)=H_b s_α(A)/∏_(i=1)^b (α_i+b−i)!,
    H_b=∏_(i=0)^(b−1)i!.

The rectangular Littlewood–Richardson coefficient is one for the displayed complementary shapes and zero for all other pairs. Exact arithmetic gives

    B=590339/600,
    A=−1,
    K=−346784498681178488832000000,
    γ=−1024192512000000.

The omitted-set sign is (−1)^(q(n−q))=−1. Thus

    D=93, κ=9,
    [λ^84]F=349455192072211821543155615882280960000000000 (z−1)^3.

Every coefficient above degree 84 is zero. These are full-determinant statements, because the smaller-layer checks below rule out all competing contributions.

## Actual translated-minor checks

The checker computes each minor's loss-l coefficient directly as

    Σ_(d_0<⋯<d_(b−1), Σd=binom(b,2)+l)
       det[a_i^(d_j)] det[binom(e_j,d_i)],

then uses the signed generalized Laplace sum. It does not generate those coefficients from the Schur prediction.

For the maximal size-3 layer, the direct coefficients at losses 0 through 8 are zero, and the coefficient at loss 9 is exactly the integer displayed above.

For the size-2 layer, the raw gap is 7. Its direct own-loss coefficients at 0 through 7 are zero. Its first nonzero own-loss coefficient is at 8:

    20653517704839718344489387075450175488000000000000.

Its first global loss is therefore 7+8=15, strictly greater than 9. In particular the direct sums at global losses 7, 8, and 9 vanish; the raw bound alone would not establish this. The size-1 and size-0 layers have raw gaps 16 and 27, respectively, and already lie below the maximal leading term.

The checker also verifies all 42 original-index omitted-set weight identities for omission sizes 3 through 6, plus common-offset translation and reversal of the row factor. Translation by 7 preserves B; negation changes its sign because its degree is 9.

## Exact one- and two-omission regressions on the same nodes

Keep n=12, exponents, and J fixed. Change I to the initial r rows.

- q=1, r=5: κ=5, shape (5), B=324/5, D=101. Direct maximal losses 0,…,4 vanish and the loss-5 coefficient is 2265140859865668900492410880000000. The next layer's raw gap is 3, and its own-loss coefficients 0,1,2 all vanish.
- q=2, r=4: κ=8, shape (4,4), B=7944301/14400, D=98. Direct maximal losses 0,…,7 vanish and the loss-8 coefficient is 1943900086222250820724619162419200000000. The next layer's raw gap is 5, and its own-loss coefficients 0,…,3 all vanish.

The general pivot statement also reduces algebraically to the earlier formulas. For q=1, if t=deg R, then B_1={r−t}, giving κ=r−t and γ=lc(R). For q=2 and t≤r, the degree-echelon set is {t,t+1}, so B_2={r−t,r+1−t}; the shape is (r−t,r−t) and γ=−lc(R)². If t=r+1 and S=((T−c)R) mod f has degree s≤r, the echelon degrees are {r+1,s}, so B_2={0,r+1−s}; the shape is (r−s), and γ=lc(R)lc(S). These are precisely both branches of the two-omission theorem.

## A second q=3 shape with the opposite omitted-set sign

Use the eleven exponents

    e=(0,25,48,123,146,266,386,409,484,507,532),
    I=(0,1,2), J=(0,3,4,6,7,10), offsets=(0,…,10).

Here n=11,r=3,q=3. Write f for the six selected-node polynomial and R=g for the five complementary-node polynomial. The exact relation is

    (T−266)R=f+C, C=20835207993600.

Thus the first three remainder vectors span degrees {5,0,1}, the pivot columns are {0,4,5}, and the first shape is (3,3), of height two although q=3. The first loss is κ=6, γ=−C², and the omitted-set sign is (−1)^(3·8)=+1. The row factor is B=88589/480.

Direct translated-minor sums vanish at losses 0,…,5 and give

    [λ^2889]F=
      55627446086708070328745264456872708168270411745082952102861645639823652470831185920000
      ·(z−1)^3.

Here D=2895. The next layer has raw gap 6, and its direct own-loss-zero sum vanishes. All higher-loss smaller-layer coefficients are below the displayed degree; still smaller layers have larger raw gaps. Direct exterior subset sums separately verify that (3,3) is the only surviving Schur shape through degree 6. This checks a nonconstant remainder, a target shape with fewer than q rows, and the opposite parity sign from the compact sextic example.

## Reproduction and scope

Run either

    python checker/check_q3.py
    python -O checker/check_q3.py

The script uses only Python's standard library, exact integers and fractions, and explicit exceptions rather than assertions. It writes checker/q3_results.json. Runtime is under one second on the local environment. These structured certificates supplement the general proof; they are not a large finite catalog or a substitute for it.
