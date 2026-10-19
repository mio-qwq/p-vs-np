# Adversarial audit: positive column certificates do not survive another column's deletion

19 October 2026. Local-only proof and exact checks. All indices below are zero-based.

## Results and scope

1. The explicit functional `[L]/768` in the existing four-row certificate fails after deleting just one entry in a different column. Every distinguished-column edge still lies in a perfect matching.
2. A stronger canonical three-row example, originally supplied by the parallel closure-testing worker and independently checked here, disproves existence of **any** strictly positive linear functional after one entry deletion in another column. A strictly positive rational kernel certifies the impossibility.
3. The three-row example belongs to an exact arithmetic-progression family. Within its prescribed three-row deletion pattern, arithmetic progression is necessary and sufficient for a constant-coefficient dependence.
4. Every nonempty binary mask of the distinguished column remains nonzero in this example. Thus neither construction is a binary sparse-ASNC counterexample, and neither settles P versus NP.

The target being disproved is a proof mechanism: iterating full-other-column positive-functional certificates through arbitrary sparse backgrounds. Full-other-column positivity itself is not disproved.

## 1. Failure of the supplied functional after one entry deletion

Start with

    a=(-3,-1,1,3), e=(0,1,2,4), c=1.

For the full translated-power matrix, the supplied functional

    lambda(f) = [L]f / 768

sends each distinguished-column Laplace polynomial to 1.

Delete only entry `(0,3)`, the top entry of the exponent-4 column. Keep all other entries. The new distinguished-column polynomials are

    T0 = 768L + 896L^2 - 128L^4,
    T1 = 648 - 420L - 612L^2 + 120L^3 + 224L^4 + 44L^5 - 4L^6,
    T2 = 648 + 1200L + 504L^2 - 96L^3 - 136L^4 - 80L^5 + 8L^6,
    T3 = -204L + 76L^2 - 216L^3 + 56L^4 + 36L^5 - 4L^6.

Consequently

    (lambda(T0),lambda(T1),lambda(T2),lambda(T3))
        = (1,-35/64,25/16,-17/64).

There are respectively `(6,4,4,4)` surviving perfect matchings using the four distinguished-column entries. In particular, the negative values do not come from edges that have ceased to be usable by a perfect matching. Even if the distinguished column is then restricted to just row 1 or just row 3, its determinant polynomial is nonzero while the old functional is negative.

This construction refutes reuse of the particular supplied functional. It does not by itself rule out finding a different functional, which motivates the stronger example next.

## 2. Canonical three-row obstruction to every positive functional

Take offsets and exponents

    a=e=(0,1,2).

Delete the middle entry of column 0, and distinguish column 1. The unweighted sparse matrix is

    [1, L,   L^2     ]
    [0, L+1, (L+1)^2 ]
    [1, L+2, (L+2)^2 ].

Write `q=(L+1)^2`. Its three column-1 Laplace polynomials are exactly

    T0 = Lq,
    T1 = 4q,
    T2 = -(L+2)q.

Each is nonzero. The matching counts through those entries are `(1,2,1)`. However,

    2T0 + T1 + 2T2 = 0.                                      (1)

Equivalently, the coefficient matrix has the normalized strictly positive rational kernel

    u=(2/5,1/5,2/5).

If a linear functional were strictly positive on all three polynomials, applying it to (1) would give a strictly positive number equal to zero. No such functional exists.

In explicit weighted-matrix form, the same identity is

    det [1, 2L,     L^2     ]
        [0, L+1,    (L+1)^2 ] = 0 identically.
        [1, 2(L+2), (L+2)^2 ]

The zero determinant retains four perfect matchings with nonzero edge weights. This is a nonnegative **weighted** two-column cancellation, not a binary deletion-mask cancellation.

### Both individual changes are harmless

The full canonical Vandermonde determinant is 2. The column-0 deletion alone gives

    2(L+1)^2 != 0.

The column-1 weight vector `(2,1,2)` alone, before the deletion, gives

    -4L(L+2) != 0.

Thus the combined obstruction is not a zero determinant already introduced by either of these two changes in isolation.

### A full-background certificate really exists

Before deleting `(1,0)`, the three column-1 polynomials are

    S0 = -L(2L+3),
    S1 = 4(L+1)^2,
    S2 = -(L+2)(2L+1).

The coefficient functional

    lambda_full(f) = 4[L^0]f - 4[L^1]f + 5[L^2]f

has values `(2,4,2)` on them, all strictly positive. On the deleted background it instead has values `(6,4,-8)`.

The fourth coefficient functional `[L^3]` is immaterial on the full background, but allowing an arbitrary extension to that higher coefficient cannot repair positivity: the exact relation (1) holds for every linear functional on the entire polynomial space.

### All binary second-column masks still work

The seven nonempty binary sums of `(T0,T1,T2)` equal q times

    L, 4, -L-2, L+4, -2, 2-L, 2.

None is the zero polynomial. Therefore the weighted-positive-functional property is strictly stronger than the binary nonvanishing property in this actual sparse translated-power family.

One cannot infer binary failure from the weighted kernel `(2,1,2)` or its normalized form. A direct binary-ASNC argument, a different kind of certificate, or a stronger invariant would be required to continue beyond this obstruction.

## 3. Exact family and resonance classification

Let offsets be distinct real numbers `(a,b,c)`, keep exponents `(0,1,2)`, delete `(1,0)`, and again distinguish column 1. Direct expansion gives

    T0=(L+a)(L+b)^2,
    T1=(c-a)(L+b)(2L+a+c),
    T2=-(L+c)(L+b)^2.

Suppose constant real weights satisfy

    u0 T0 + u1 T1 + u2 T2 = 0.

Divide by the nonzero polynomial `L+b`. The leading coefficient gives `u0=u2=t`. The remainder becomes

    (c-a) ((2u1-t)L + u1(a+c)-tb) = 0.

Since `c!=a`, we must have `u1=t/2`, and then

    t(a+c-2b)=0.

Consequently:

- If `a+c!=2b`, the three polynomials are linearly independent, so this particular deletion pattern has no constant kernel of any sign.
- If `a+c=2b`, the kernel is exactly the one-dimensional span of `(2,1,2)` and contains a strictly positive vector.

In arithmetic-progression notation `(a,b,c)=(b-h,b,b+h)`, `h!=0`, the formulas simplify to

    q=(L+b)^2,
    (T0,T1,T2)=q (L+b-h,4h,-L-b-h).

The seven nonempty binary sums are q times

    L+b-h, 4h, -L-b-h, L+b+3h, -2h, -L-b+3h, 2h.

They are all nonzero for `h!=0`. Thus the separation between weighted positivity and binary nonvanishing holds throughout this real two-parameter family. The canonical offsets `(0,1,2)` are its smallest ordinary instance.

## 4. Verification and provenance

The four-row example was independently found in this adversarial audit. The canonical three-row candidate was communicated by the parallel closure-testing worker; the derivation, exact coefficient checks, all binary-subset checks, and arithmetic-progression classification above were independently carried out here.

`check.py` is standard-library only. It:

- reconstructs all Laplace polynomials by signed permutation expansion;
- verifies the rational functional values and matching counts;
- independently evaluates isolated-column determinants by exact rational Gaussian elimination at degree-bound-plus-one points;
- checks the normalized strictly positive kernel and the seven nonempty binary sums;
- checks the arithmetic-progression formulas on 42 integer parameter pairs, supplementary to the symbolic proof above.

Run

    python check.py
    python -O check.py

Both pass. The checker uses explicit exceptions rather than optimization-removable assertions. `search.py` retains the elementary exact polynomial enumerator used in the initial search.

No remote files, repositories, pull requests, merges, or releases were changed.
