# For fixed real offsets, every sufficiently high degree has a simple root

Date: 2026-10-19. Local supplement. This statement is separate from the audited lattice-offset criterion in ROOT_GEOMETRY.md.

## Theorem and quantifiers

Fix n>=2 distinct real offsets a_0<...<a_m, m=n-1. There is a finite threshold d_0 depending on the offsets such that

    H_d(L)=h_d(L+a_0,...,L+a_m)

has a simple complex root for every integer d>=d_0. Hence H_d is not a proper polynomial power for every sufficiently large d with the offsets held fixed.

The order of quantifiers matters: this is not a proof for every offset tuple and every even d. The threshold is not asserted to depend only on n. All odd d already have a simple real root by the simplex-moment argument, so only even d need be considered.

## Endpoint scaling proof

Translate and scale the offsets so a_0=-1 and a_m=1. This only translates/scales roots and preserves multiplicities. Put

    g(t)=product_(s=0)^m(t-a_s),
    c_s=1/g'(a_s),
    A=|c_0|>0, B=c_m>0,
    N=d+m.

The endpoint signs are c_0=(-1)^m A and c_m=B. The divided-difference formula is

    H_d(L)=sum_(s=0)^m c_s(L+a_s)^N.

For even d, N and m have the same parity. Thus, with the scaled variable w=N L,

    H_d(w/N)
      =A(1-w/N)^N+B(1+w/N)^N
       +sum_(s=1)^(m-1)c_s(a_s+w/N)^N.             (1)

As d tends to infinity through even integers, the two endpoint terms tend locally uniformly in w to A exp(-w)+B exp(w). Every interior offset satisfies |a_s|<1, so every interior term tends locally uniformly to zero. Therefore

    H_d(w/N) -> F(w)=A exp(-w)+B exp(w)

locally uniformly on C along the even-degree subsequence.

The zeros of F are

    w_j=(log(A/B)+(2j+1)i*pi)/2, j in Z,

and are simple: at a zero, F'(w_j)=2B exp(w_j)!=0. Choose a closed disk of radius less than pi/2 around one w_j. Its boundary has no zeros of F and its interior has exactly one zero counted with multiplicity. Uniform convergence and Rouché's theorem imply that H_d(w/N) also has exactly one zero counted with multiplicity in this disk for every sufficiently large even d. That zero is therefore simple. Scaling w back to L preserves multiplicity.

The argument also shows that, for every fixed integer M, all sufficiently large even d have at least M simple roots, by applying Rouché on finitely many disjoint disks. Only one is needed to exclude a proper power.

## Root location asymptotic in the original coordinates

For the original, unnormalized offsets, write

    c=(a_0+a_m)/2, R=(a_m-a_0)/2,
    b_s=(a_s-c)/R,
    A=1/product_(s=1)^m(1+b_s),
    B=1/product_(s=0)^(m-1)(1-b_s).

One of the simple roots for sufficiently large even d obeys

    zeta_d=-c+R[log(A/B)+i*pi]/[2(d+m)]+o(1/d).

Its conjugate is another simple root. The ratio A/B is unchanged if the barycentric weights are computed before the common scaling, because both extreme weights acquire the same positive factor.

## An explicit sufficient threshold

The proof can be made effective without solving for polynomial roots. In the normalized coordinates, set

    w_0=(log(A/B)+i*pi)/2,
    r=pi/4,
    W=|w_0|+r,
    rho=max_(0<s<m)|a_s|<1,
    sigma=(1+rho)/2,
    C=sum_(0<s<m)|c_s|.

For n=2 there are no interior terms and the two-term polynomial has only simple roots at every degree; the following formula is for n>=3.

Take any integer N=d+m, d even, satisfying all of

    N>=2W/(1-rho),
    N>=W^2,
    N>=8(A+B)exp(W)W^2/sqrt(A B),
    N>=max(0,log(4C/sqrt(A B)))/(-log(sigma)).       (2)

These are sufficient, not optimized.

On |w-w_0|=r, write w=w_0+u. Since

    F(w)=2i sqrt(A B) sinh(u)

and |sinh(u)|^2=sinh(Re u)^2+sin(Im u)^2, the inequalities sinh(x)^2>=x^2 and |sin(y)|>=2|y|/pi for |y|<=pi/2 give

    |F(w)|>=sqrt(A B).

The first bound in (2) implies N>=2W and |a_s+w/N|<=sigma for every interior knot and every w in the disk. Hence the total interior error is at most C sigma^N<=sqrt(A B)/4.

For |w|<=W and N>=2W, the convergent logarithm series gives

    |N log(1±w/N) ∓ w|<=W^2/N.

Thus the endpoint approximation error is at most

    (A+B)exp(W)[exp(W^2/N)-1]
      <=2(A+B)exp(W)W^2/N
      <=sqrt(A B)/4,

where N>=W^2 permits exp(t)-1<=2t for 0<=t<=1. The total error is at most sqrt(A B)/2, strictly smaller than the boundary lower bound. Rouché therefore gives the claimed simple root at every even degree satisfying (2).

## Consequence and limitation for the one-gap family

For any fixed distinct real offset tuple, the existing ODE reduction proves complex linear independence in the one-gap family for all sufficiently large d and every allowed distinguished exponent. Combined with the already-proved odd-degree case, only finitely many even d remain for that fixed tuple.

This is not a uniform decision algorithm for arbitrary binary-encoded offsets or degrees, does not supply a bound independent of the offset geometry, and does not settle the remaining finite cases. It proves no arbitrary-background or complexity-theoretic claim. No publication novelty is asserted.
