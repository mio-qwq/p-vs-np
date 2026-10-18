# Candidate theorem: arbitrary integer exponent gaps in order four

18 October 2026. Scope: the auxiliary uncolored masked determinant only. This is a candidate proof, accompanied by exact symbolic identity checks, awaiting independent audit. No ASNC, complexity, novelty, or P-versus-NP claim is made.

## Theorem

Let `eta` be a binary 4 by 4 matrix whose support has a perfect matching. Let `a_0,...,a_3` be distinct real numbers and let `e_0,...,e_3` be distinct nonnegative integers. Then

`det[eta_ij (x+a_i)^(e_j)]`

is not the zero polynomial.

The argument is a finite classification of support graphs with symbolic exponents and offsets, not a finite enumeration of exponent sets or offset values. Apart from the already proved one-partial-row lemma, the only real-offset argument is in Section 7. Integer exponents are essential to several of the exclusions below.

## 1. Normalizations and the 23 support types

A nonzero determinant of the binary mask is the leading polynomial coefficient and settles that mask. Remove edges that belong to no perfect matching, which cannot change any determinant term. If the resulting bipartite graph is disconnected, every component is balanced and the determinant factors into smaller masked determinants. Components of size at most three are nonzero for distinct offsets and arbitrary distinct integer exponents after factoring a common row power; the existing order-at-most-three proof works over any characteristic-zero field.

For the remaining connected singular masks, row permutation and column permutation give exactly the 23 representatives listed below. A row code has bit j equal to one exactly when column j is retained. Exhaustively enumerating the 3,060 sorted multisets of nonzero four-bit row codes yields 1,062 masks without a matching, 940 with nonzero binary determinant, 851 singular masks with disconnected allowed-edge graph, and 207 connected singular masks. The 207 become 23 column-permutation orbits. The accompanying checker reconstructs this classification and verifies each orbit map.

Column permutations permute the associated exponents; **we impose no exponent ordering in Sections 2–6**. Subtract the exponent attached to column zero by factoring a nonzero power of each row base. Thus the exponents become `(0,p,q,r)`, where p,q,r are arbitrary pairwise distinct nonzero integers, possibly negative. The determinant is now a rational function; zero versus nonzero is unchanged. At the roots of a row base, all other bases are units, so ordinary integer valuations remain valid.

Normalize offsets to `(0,1,b,c)` by an invertible affine change of x and nonzero column scalings. Distinctness means

`b c (b-1)(c-1)(b-c) != 0`.

Put `z=1/x`. Factoring the powers of x from columns leaves the formal power series

`H(z)=det[eta_ij (1+a_i z)^(e_j)] = sum C_k z^k`.

For negative integer exponents the binomial expansions are formal infinite series, but each C_k is a finite polynomial in p,q,r,b,c. For a supported permutation pi, its contribution is its sign times

`sum_{i+j+h=k} binom(e_pi(1),i) binom(e_pi(2),j) binom(e_pi(3),h) b^j c^h`.

This formula is the source of every coefficient identity below. Vanishing of the determinant implies vanishing of every C_k.

## 2. Immediate cases

The following coefficients are nonzero under the distinctness conditions. All earlier coefficients vanish identically when k exceeds one.

| Row codes | k | C_k |
|---|---:|---|
| (3,7,12,15) | 1 | cp |
| (3,7,13,13) | 1 | -r(b-c) |
| (3,7,15,15) | 1 | -p(b-c) |
| (3,12,15,15) | 2 | -p(b-c)(q-r) |
| (3,13,13,14) | 1 | -2(b-1)(q-r) |
| (3,13,13,15) | 1 | -(b-1)(q-r) |
| (3,13,15,15) | 1 | -(b-c)(q-r) |
| (7,7,11,11) | 2 | -p(b-c)(q-r) |
| (7,7,11,15) | 1 | -p |
| (7,11,15,15) | 1 | p(b-c) |
| (7,15,15,15) | 3 | pq(b-1)(b-c)(c-1)(p-q)/2 |

The representative `(3,5,10,12)` has exactly two matchings. Their signed monic products cannot cancel: if their signs oppose, equality would require the same multiplicity at each of the four distinct roots, hence the same exponent assignment, contrary to the permutations being different.

The full mask `(15,15,15,15)` has its nonzero coefficient C_6 equal to the product of the offset and exponent Vandermondes divided by `0!1!2!3!=12`.

The representative `(3,15,15,15)` is covered by the previously proved arbitrary-gap one-partial-row theorem. For completeness, that theorem is recalled in Section 8; it handles every exponent permutation and uses realness only in a sum-of-squares exclusion.

These account for 14 of the 23 representatives. The nine remaining types are treated next.

## 3. The two sparse four-matching types

### A simple-zero fact

At a point away from the roots of distinct linear polynomials A and B, a nonzero binomial `A^u B^v - A^v B^u`, with distinct integers u,v, has only simple zeros. After dividing by a unit, it is `A^(u-v)-B^(u-v)`. At a zero, its logarithmic derivative is a nonzero multiple of `1/A-1/B`, which is nonzero. The same applies to `A^u-B^u` for u nonzero. A monomial times either binomial therefore has valuation zero or one at such a point.

### (3,5,11,13)

The number of matching terms assigned to each retained entry, row by row, is

`(1,3,0,0), (1,0,3,0), (1,1,0,2), (1,0,1,2)`.

At row zero's root, the cofactor of exponent zero is a single nonzero monomial. If p were positive, this term would be the unique lowest valuation. Hence an identically zero determinant requires p<0. Similarly q<0. At row two's root, if r>p, the exponent-p term is a unique lowest nonzero monomial, so r<p; similarly row three forces r<q.

The exponent-r cofactor at row two is a monomial times the difference of the exponent-q powers of the bases of rows one and three. Its valuation is at most one by the simple-zero fact. The next exponent is p, whose cofactor is a monomial. Cancellation therefore forces p-r=1. The exponent-r cofactor at row three is analogously a monomial times the difference of the exponent-p powers of the bases of rows zero and two, forcing q-r=1. This contradicts p!=q.

### (3,5,10,15)

The entry matching counts are

`(2,2,0,0), (1,0,3,0), (0,1,0,3), (1,1,1,1)`.

The single-monomial cofactors in rows one and two force q<0 and r<p, respectively. Both cofactors of row zero are monomials times the simple binomials just described. Equality of their valuations forces `p=1` or `p=-1`.

For the Laurent coefficients define

`A=p+q-r, B=2p(p-r)-A, E=2pq+A`.

The first coefficient is `C_1=b(r-p)+cA-q`. If A=0 this equals q(b-1), nonzero; hence A!=0 and

`c=[b(p-r)+q]/A`.

Under this relation,

`C_2=-q(b-1)(p-r)(bB+E)/(2A^2)`.

If B=0, then E=B+E=2pA!=0; hence C_2=0 requires B!=0 and b=-E/B. Substituting both relations gives

`C_3=-p^2 q(p-r) A T/(3B^3)`,

where

`T=6p^2q+5p^2-6pqr-5pq-5pr-3p-3q+3r`.

Thus T=0. For p=1 this is equivalent to `(3q+1)(3r+1)=4`. Here q<=-1 and r<=-1, so both factors are at most -2, and equality forces q=r=-1. For p=-1 it is equivalent to `(3q+4)(3r+4)=4`. Now r<=-2; q=-1 gives a negative product, and q<=-2 forces q=r=-2. Both contradict exponent distinctness.

## 4. Four direct coefficient branches

### (3,5,14,14)

`C_1=-(b-c)(p+q-2r)` forces `r=(p+q)/2`. Then

`C_2=-(b-c)(p-q)[(b+c)(p-q)+2q]/4`.

Hence `c=-b-2q/(p-q)`. Put `u=b(p-q)+q`, so

`b=(u-q)/(p-q), c=(-u-q)/(p-q)`.

Distinctness gives u!=0. The next coefficient is

`C_3=u(u^2+pq)/(2(p-q))`.

Under its necessary relation u^2=-pq, the next is

`C_4=-pqu(p+q)/(3(p-q)^2)`.

This is nonzero because p,q,u,p-q are nonzero and p+q=2r!=0.

### (3,5,15,15)

`C_1=-(b-c)(p+q-r)` forces r=p+q. Then `C_2=pq(b-c)(b+c-1)` forces c=1-b. Now

`C_3=-bpq(b-1)(2b-1)(p+q+2)/2`.

Distinctness forces p+q=-2, so r=-2 and q=-p-2. Under these relations,

`C_4=bp(b-1)(2b-1)(p+1)(p+2)/6`.

Every factor is nonzero: p+2=-q, and p=-1 would make q=p. Contradiction.

### (3,7,11,12)

`C_1=-p(b+1)` forces b=-1. Next

`C_2=-p[c(q-r)+p-q-r-1]`

forces `c=(q+r+1-p)/(q-r)`. Then

`C_3=p(p-2q-1)(p-2r-1)/(2(q-r))`.

Its first possible zero factor makes c=-1=b; the other makes c=1. Both violate distinctness.

### (3,7,11,15)

`C_1=-p(b-c+1)` forces c=b+1. Then `C_2=bp(p-q-r-1)` forces p=q+r+1. The next coefficient is

`C_3=bp[br(q+1)+q(r+1)]/2`.

q=-1 would make p=r, so q+1!=0, and r!=0. Thus C_3=0 forces

`b=-q(r+1)/(r(q+1))`,

and b!=0 forces r+1!=0. At this point

`C_4=q^2(r+1)^2 p [q^2+q+r^2+r]/[6r^2(q+1)^2]`.

For every integer n, n(n+1)>=0, with equality only at n=0 or n=-1. Since q is neither, the bracket is strictly positive. Contradiction.

## 5. The orbit (3,13,14,15)

`C_1=-(q-r)(b-2c+1)` forces c=(b+1)/2. Put T=q+r-1. Then

`C_2=-(b-1)(q-r)[T(b-1)+2p]/4`.

T=0 would leave a nonzero coefficient, so T!=0 and

`b=1-2p/T, c=1-p/T`.

The necessary next relation C_3=0 is

`[T+p(p-1)]^2=p^2(p^2-1)`.

(The exact coefficient is `p^2(q-r)([T+p(p-1)]^2-p^2(p^2-1))/(2T^3)`.)

Since p is a nonzero integer, an integer solution requires p^2-1 to be a perfect square. For |p|>=2 it lies strictly between (|p|-1)^2 and |p|^2. Thus p=1 or p=-1. If p=1 the relation gives T=0, already excluded. If p=-1 it gives T=-2, whence b=0, also excluded.

## 6. The orbit (7,7,11,13)

`C_1=-p-q` forces q=-p. Next

`C_2=p[b(p+r)+c(p-r)-p]`

forces `c=[p-b(p+r)]/(p-r)`. Define

`L=4p^2r+p^2-r^2`,

`N=2p^2r+pr-r^2`,

`F=2L(b^2-b)+N`.

The next coefficient is `C_3=-p^2 F/(2(p-r)^2)`.

If L=0, vanishing C_3 gives N=0. Subtraction gives `r(1-2p)=p`. Since p is a nonzero integer, 1-2p!=0; substituting gives `L=-4p^4/(2p-1)^2`, a contradiction. Thus L!=0.

Reducing C_4 modulo F, its value on F=0 is

`p^2 r(2b-1) G/[6(p-r)L]`,

where

`G=(3p^2-1)(p^2-r^2)+6p^2(p^2-1)r`.

The factor 2b-1 cannot vanish: b=1/2 would give c=1/2. All remaining factors and denominators outside G are nonzero. Therefore G=0 is necessary.

As a quadratic in the integer r, G has discriminant

`4p^2 T_p`, where `T_p=9p^6-9p^4+3p^2+1`.

An integer root requires T_p to be an integer square. For n=|p|>=2 this is impossible. If n is even, let `m=3n^3-3n/2`, an integer. Then

`T_p-m^2=3n^2/4+1>0`,

`(m+1)^2-T_p=6n^3-3n^2/4-3n>0`.

If n is odd, hence n>=3, let `m=3n^3-(3n+1)/2`, again an integer. Then

`T_p-m^2=3n^3+3n^2/4-3n/2+3/4>0`,

`(m+1)^2-T_p=3(n-1)(4n^2+3n+1)/4>0`.

Thus T_p lies strictly between consecutive squares. Finally, |p|=1 makes `G=2(1-r^2)`, whose only integer zeros r=1,-1 collide with p or q=-p. This finishes the orbit.

## 7. The last orbit: (7,7,15,15)

The first three columns have exactly the same support. Permute them and subtract their smallest exponent. We may now assume **0<p<q** are integers. The exponent r of the fourth column is initially an arbitrary distinct integer. This additional ordering is valid specifically because these three columns are interchangeable; it was not assumed in the preceding orbit arguments.

The first nonzero coefficient is

`C_3=-pq(b-c)(p-q)(b+c-1)/2`,

so c=1-b. Under this relation,

`C_4=-bpq(b-1)(2b-1)(p-q)(p+q-3r-3)/6`.

Hence `r=(p+q-3)/3`. Since p+q>=3 and r!=0, we have r>0; also r<q. Set

`J=p^2-pq+q^2`,

`K=(p+q)(2p-q)(p-2q)`,

`A=K-45J+135`.

After both necessary substitutions, the sixth coefficient is

`C_6=-bpq(b-1)(2b-1)(p-q)[A b(b-1)-2K]/3240`.

Every displayed prefactor is nonzero. Let `s=(2b-1)^2`. Realness and distinctness give s>0 and s!=1. Vanishing C_6 therefore requires

`A(s-1)=8K`.                                          (1)

Also J>3: J=(q-p)^2+pq>=3, with equality only at p=1,q=2, which would give r=0.

Center and rescale the offsets, and permute the full rows if needed. They become `(-1,1,-t,t)`, where t=sqrt(s)>0 and t!=1. Write D(x) for this normalized masked determinant. If it were identically zero, D'(0) would vanish. Its derivative can be computed directly from the four rows; the following expressions omit only nonzero factors.

The exponent relation gives `r congruent p+q-1 modulo 2`.

- If p,q are both even, the relevant expression is `p(t^q-1)-q(t^p-1)`. It is strictly positive for t!=1: for positive e, `(t^e-1)/e=integral_1^t u^(e-1) du` strictly increases with e whenever t!=1.
- If p is even and q is odd, the expression is `(r-p)t^p+p t^(q+1)-r`. Its coefficients in increasing powers have exactly one sign change, since r,p>0 and q+1>p, regardless of the sign of r-p. Descartes' rule gives at most one positive root, and that root is t=1.
- If p,q are both odd, after dividing by t the expression is `(r-p)t^(p-1)+(q-r)t^(q-1)-(q-p)`. For p=1 it reduces to `(q-r)(t^(q-1)-1)`. For p>1 its coefficients again have exactly one sign change because q-r>0, so its only positive root is t=1.

It remains that p is odd and q is even; r is then even. Put

`U=(p+1)/2`, `V=q/2`.

The required derivative expression is

`F(s)=q s^U-(q-r)s^V-r`.                              (2)

Here F(1)=0, r>0, q-r>0. Since p+q-3 is divisible by three, and p is odd while q is even, q-2p is a multiple of six.

### If q=2p

K=0 and A=135(1-p^2). If p=1 then r=0, excluded; otherwise A!=0. Equation (1) forces s=1, excluded.

### If q>2p

Write h=q-2p>=6. Direct expansion gives

`K-5J+15=(9h-15)p(p+h)+(2h-5)h^2+15>0`.

K>0 as well. Equation (1) is equivalently

`A s = 9(K-5J+15)`.

A=0 is impossible, and s>0 requires A>0. Equation (1) then implies s>1. But V>U and

`F'(1)=q(2p-q)/3<0`.

For s>=1, the ratio of the positive term to the negative term in F'(s) is no larger than its value at one. Thus F'(s)<0 throughout s>=1, and F(s)<0 for s>1. Contradiction.

### If q<2p

Write h=2p-q>=6 and H=-K>0. Since q>p, p>=h+1. A=-H-45J+135<0, and equation (1) gives

`s=1+8H/(H+45J-135)`.

The exact identity

`H-15J+45=9(h-5)(p-h-1)(p+1)+2h(h-6)(h+3)>=0`

shows s>=3. If q=p+1, U=V and `F(s)=r(s^U-1)`, which is nonzero. Otherwise q>=p+3, so V-U>=1. Furthermore

`q/(q-r)=3q/(2q-p+3)<3`.

For s>=3, this gives `(q-r)s^V>q s^U`, and hence F(s)<0. Contradiction.

All parity possibilities are excluded. This finishes the last support orbit.

## 8. Recalled one-partial-row lemma

When one row retains a nonempty subset S of columns and the other three rows are full, translate the partial row's offset to zero and reorder exponents as `(0,p,q,r)` with 0<p<q<r. Let the three remaining offsets be a,b,c. Cauchy–Binet expands the normalized determinant into offset alternants times binomial minors. The first possible coefficient is degree three. Twice its binomial factor is the sum over S of

`w_0=(q-p)(r-p)(r-q), w_1=-qr(r-q), w_2=pr(r-p), w_3=-pq(q-p)`.

These sum to zero. For a proper nonempty S, their partial sum is nonzero except for the complementary pairs S={1,2} and S={0,3} when r=p+q. (Single and triple subsets are immediate; same-sign pairs are immediate; the other two opposite-sign pairings are excluded by strict inequalities.) The full subset is the ordinary generalized Vandermonde case.

For the exceptional pair S={1,2}, put V=Vandermonde(a,b,c) and B=pq(p-q)(p+q), both nonzero. The degree-four coefficient is `VB(a+b+c)/6`. If it vanishes, a+b+c=0, and the degree-five coefficient becomes `VB(ab+ac+bc)/6`. But then `ab+ac+bc=-(a^2+b^2+c^2)/2<0` for distinct real a,b,c. The complementary pair has opposite coefficients below degree six, since their sum is the full determinant. Thus neither pair can vanish identically.

## Verification and status

The companion checker recomputes support coverage, every displayed coefficient identity, the center derivatives, and the polynomial identities in the integer inequalities. It uses exact SymPy algebra and no sampled parameters. A proof of the inequalities and integer exclusions is given explicitly above. The independent-audit status must be reported separately; successful symbolic execution alone is not an independent audit or a formal proof-assistant verification.

No public write, network request, or unknown code was used. The research is bounded to this order-four auxiliary lemma; this theorem, even if confirmed, does not establish larger matching-covered components or the color-conditioned ASNC claim.
