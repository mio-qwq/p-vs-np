# Universal complex-offset guard and undivided C7 obstruction

2026-10-27. Independent critical signoff: **PASS**. This lemma uses only the restricted overlap mask, distinct integer exponents, and distinct complex offsets. It does not import real-offset positivity or any earlier order-type classification.

Write the exponents after subtracting the shared exponent as `(0,B,C,D,E)`, with all five values distinct integers. Normalize the partial offsets to `0,1`; this is an invertible affine change over C because those offsets differ. Set

```
u=D+E, v=DE, x=u-B, y=u-C,
L=x+y, A=xy, t=u-L, K=A+2L, delta=x-y.
```

All ordinary normalization factors, including `BC`, `D-E`, and the full-offset Vandermonde, are nonzero. The freshly independently derived C3–C7 identities are the coefficient input to this lemma. In particular identity-zero implies C3 balance `v=tL+2A`.

## 1. L, A, and K cannot vanish

**L=0.** The undivided C4 equation is `BC(LE1-3x)=0`, up to a nonzero factor. Because BC is nonzero, L=0 forces x=0 and then y=0. But `x-y=C-B` is nonzero. Contradiction.

**A=0.** Suppose x=0, so u=B. C3 gives `v=C(B-C)`. Therefore

`z^2-u z+v=(z-C)(z-(B-C))`.

Its roots D,E must include C, contrary to distinctness. The y=0 branch exchanges B and C and is identical. This argument does not need reality or a square-root choice.

**K=0.** With L and A nonzero, the undivided C5 equation, after the necessary C4 relation, is

`0 = BC/(36L^2) * [L^2 K(E1^2-3E2)-9A(v+L)]`.

Consequently `v=-L`. Because A=-2L, C3 gives

`-L = (u-L)L-4L`, hence `u=L+3`.

Also `(x+2)(y+2)=4`. The complete integer divisor list, imposing x!=y and A!=0, consists of

`(x,y)=(-1,2),(2,-1),(-3,-6),(-6,-3)`.

The first two have L=1, hence `(u,v)=(4,-1)` and quadratic discriminant 20, not an integer square. The last two have L=-9, hence `(u,v)=(-6,9)` and D=E=-3. Both possibilities are impossible. This finite divisor argument is global; it has no height cutoff.

Thus every identity-zero candidate has `LAK != 0`.

## 2. The C7 obstruction does not divide by mu

Put

`R=A/L, Z=t+2R+1`.

Let `mu,eta,Q,N` be the polynomial expressions recorded in the coefficient certificate, and define

`Phi = mu*N + 5(R+2)(L-4R)*eta*Q`.

The distinctness identity is `delta^2=L(L-4R)`. Denote the normalized C6 and C7 coefficients divided by BC by c6 and c7. Under the necessary C3–C5 equations, their certified identities are

```
c6 = L*mu*q/120 + R*delta*eta/[24L(R+2)],
c7 = (u-6)*c6/2 + delta*Q*q/240 - R*N/[240L(R+2)^2].
```

Here q is the remaining centered full-offset parameter; no assumption on q is required. Direct elimination gives

```
mu*c7 - [mu*(u-6)/2 + delta*Q/(2L)]*c6
  = -R*mu*N/[240L(R+2)^2]
    -R*delta^2*Q*eta/[48L^2(R+2)]
  = -R*Phi/[240L(R+2)^2].
```

This identity uses multiplication by mu, never division by it. The only canceled quantities are L, R, and R+2; these are nonzero because `LAK!=0`. Therefore c6=c7=0 implies Phi=0 even when any of `mu`, `M=L*mu`, `eta`, `Q`, `Z`, or `R+4` vanishes. No positivity is used.

Finally

`P(L,A,t)=L^5*Phi(L,A/L,t+2A/L+1)`

is the certified 112-term integer polynomial of coordinate degrees `(8,6,6)`. Since L!=0, identity-zero implies P=0. Evaluating P modulo primes 101 and 103 is a valid necessary filter even when either prime divides L: the integer polynomial is evaluated directly and no modular inverse or modular division occurs.

## 3. Independent exact implementation controls

`audit_complex_extension.py` freshly reconstructs the syzygy from the compact coefficient data and reduces its numerator modulo `delta^2-L(L-4R)`, obtaining zero. It independently checks the A=0 factorization and complete K=0 divisor list.

The all-30 C++ source was checked to differ from the already audited six-order source only in the complete canonical order list and its array/loop dimensions. That list is freshly regenerated from all permutations with b<c,d<e. Both H=80 binaries were compiled with undefined-behavior/bounds sanitizers and libstdc++ assertions. A separately written direct-E enumeration and exact arbitrary-precision P evaluation reproduce every aggregate count, per-order count, and modular survivor for the all-30 H=80 run. No duplicate full-height run was performed by this reviewer.

The whole all-30 proof therefore has no real-only order-classification dependency. Together with the independent finite-height proof and an independently certified complete all-30 exhaustion, the implication to the restricted complex-offset nonvanishing theorem is logically valid. This is not a theorem for arbitrary masks or arbitrary real exponents, and carries no general circuit lower-bound or P-versus-NP claim.
