# Computer-assisted nonvanishing: five-row overlapping-pair mask

Status: root integration of exact mathematical reductions and two independent exhaustive computations; final review receipts are recorded separately. This is one restricted determinant model, not P vs NP or a general circuit lower bound. No priority or human peer-review claim.

## Statement

Let a,b,c,d,e be pairwise distinct nonnegative integers and r1,...,r5 pairwise distinct complex numbers. Let M(X) have entries (X+ri)^ej on a mask whose first two rows have supports {a,b} and {a,c}, and whose other three rows are full. Then det M(X) is not identically zero. Real offsets are included.

## 1. A proved finite exponent bound

The self-contained structural/PROOF.md and independent height-review/REVIEW.md prove that any counterexample has every consecutive exponent gap at most408, hence span at most1632. This is independent of low-coefficient elimination.

The proof considers the18 permitted determinant monomials, of equal total degree. In a minimal linear circuit ofk<=18 terms, divide their gcd to obtain equal-degreeD polynomials supported on at most5 roots. Forn=k−1 andC=binom(n,2), proportional omitted-column Wronskians yield degW>=kD−5C. Gaussian elimination to distinct leading degrees gives degW<=nD−2C. ThusD<=3C<=408. A gap larger than408 prevents circuits from crossing the associated row-assignment classes. Their spans form a direct sum. One class factors into nonzero proper minors, including only a specifically proved two-partial four-row minor, so its sum cannot vanish. No false general complex four-row assertion is imported.

Subtracting the least exponent preserves identity-zero by factoring nonzero row powers. The bound is on the span; subsequently subtracting the shared exponenta gives (0,B,C,D,E), with every entry in[−1632,1632] and total span<=1632. Swapping b,c together with the two partial rows and swapping d,e preserve identity-zero; therefore assume B<C andD<E. Normalize the two partial offsets to0,1 by an invertible affine change ofX.

## 2. Necessary algebraic coefficient equations

Write u=D+E,v=DE,x=u−B,y=u−C,L=x+y,A=xy,t=u−L,K=A+2L. Direct normalized determinant expansion first gives

    v=u(B+C)−B²−C²=tL+2A.                        (C3)

The normalization divides only the nonzero full-offset Vandermonde, E−D and a power-series unit. Coefficient vanishing is therefore preserved. The later equations are algebraic overC and require no real positivity. Independent direct power/binomial alternants in global-c8 regenerate the universal coefficients through8.

Let e1,e2,e3 be the elementary symmetric full offsets. The undivided C4 equation is BC(Le1−3x)=0, up to a nonzero constant. Thus L=0 would force x=y=0 andB=C, impossible. IfA=0, sayx=0, C3 forces one ofD,E to equalC; the other case is symmetric, also impossible. UnderC4, the undivided C5 equation is

    L²K(e1²−3e2)=9A(v+L).

IfK=0, thenv=−L andu=L+3. The integer equation(x+2)(y+2)=4 leaves, after x!=y andA!=0, the pairs(-1,2),(2,-1),(-3,-6),(-6,-3). The first pair types give(u,v)=(4,−1), whose discriminant20 is not an integer square. The others give(u,v)=(-6,9), forcingD=E. ThusL,A,K are nonzero in any candidate.

Set R=A/L,Z=t+2R+1,delta=x−y. Use the exact compact mu,eta,Q,N,Phi expressions of0654. After C3–C5, withg6=C6/(BC),g7=C7/(BC), exact elimination gives

    mu*g7 − [mu*(u−6)/2 + delta*Q/(2L)]*g6
      = −R*Phi/[240L(R+2)²].

This identity uses delta²=L(L−4R), but never divides bymu. Consequently identity-zero impliesPhi=0 even whenmu=0,Z=0 orR=−4. Define

    P7(L,A,t)=L^5 Phi(L,A/L,t+2A/L+1) in Z[L,A,t].

It is the112-term polynomial checked by both enumeration implementations and by a separately handwritten factored-Phi evaluator. Every candidate in the remaining L,A,K-nonzero domain must satisfy P7=0. No assumption on the six formerly open order types is needed below: all30 canonical orders are included.

## 3. Complete finite C3 parametrization

EquationC3 is equivalent to

    (D−B−C)(E−B−C)=2BC.

For every pair −1632<=B<C<=1632 with B,Cnonzero andmax(0,C)−min(0,B)<=1632, enumerate every signed divisorh of2BC, putk=2BC/h, and retainh<k. SetD=B+C+h,E=B+C+k. Retain exactly the tuples with all five entries distinct and span<=1632. Both positive and negative divisors are included. This is equivalent in both directions to all integer C3 candidates in the proved height domain; the D−B−C=0 case is impossible becauseBC!=0.

## 4. Exact exhaustive certificate

Two independently implemented C++ signed-divisor engines agree, and independent small-height direct B,C,D-to-E enumeration controls the coverage. The counts for the full proved domain are:

- B,C pairs:3,992,688.
- Distinct C3 tuples across all30 canonical orders:19,658,082.
- L=0:3,540; A=0 afterL exclusion:0; K=0 afterL,A exclusion:6.
- L,A,K-nonzero tuples:19,654,536.
- Survive exact P7 modulo101:220,631.
- Survive exact P7 modulo101 and103:2,432.
- Satisfy P7=0 under arbitrary-precision integer evaluation:0.

The second implementation also evaluates each of the2,432 survivors using a separately handwritten rational factoredPhi, obtaining exactly the same nonzero values after multiplying byL^5. Singular mu,Z,R+4 cases are not dropped. The root ordered survivor file has SHA256b008f2a7ec55b6156c355ff6d2c83b11cf4580a42b6046ba1a823e7757dc83c5; the independent file ordering differs but the tuple sets coincide exactly.

All modular filters are exact necessary conditions: a zero integer polynomial must vanish modulo both primes. All remaining cases are checked with unbounded Python integers. Fixed-width enumeration arithmetic has explicit bounds: |2BC|<=5,326,848, and every generated divisor/prime power and pre-filter offset fits signed32-bit; A uses64-bit; modular products and indices are far smaller. Compiler optimizations do not change the stated integer operations. Independent source audit and sanitizer/small-domain controls are documented in the review packet.

## 5. Conclusion and limits

The structural argument excludes every larger exponent span. The exhaustive certificate excludes every remaining regular integer C3/P7 candidate; the three low-denominator cases were excluded algebraically. This proves the stated nonvanishing theorem for the overlapping-pair mask, including complex distinct offsets. It replaces the earlier24/30 partial classification for this specific mask, not for arbitrary five-row masks.

The final theorem is computer-assisted, with explicit finite exact code and certificates. It is not a claim of Lean formalization, independent human review, general arithmetic circuit separation, or resolution of P vs NP.
