# Independent addendum: sharp transposition-distance testing radius

Status: mathematically audited and exhaustively checked in small cases. This is separate from, and does not modify, the support-radius proof in sharp_bound.md. No claim of literature novelty is made. This addendum uses the already-audited support-radius theorem.

## Statement
Let F be any field, n≥2, and d≥1. For a permutation sigma∈S_n, let ell_T(sigma) be its minimum length as a product of arbitrary transpositions. The smallest integer R such that every degree-at-most-d polynomial nonzero on the n-by-n permutation matrices is nonzero at some P_sigma with ell_T(sigma)≤R is

R = min(n−1, 2d).

For d=0 or n≤1, radius zero suffices.

## Upper bound
The support-radius theorem gives a nonzero witness moving at most 2d+1 vertices. If it is not the identity, write m for its support size and c≥1 for its number of nontrivial cycles. Then ell_T(sigma)=m−c≤2d. Every permutation also satisfies ell_T(sigma)≤n−1.

## Two characteristic-independent facts
For every permutation matrix P,

P−P^T = (P−I)(I+P^T).

The kernel of P−I consists of vectors constant on each cycle, over any field, so

rank(P−I) = n − number_of_cycles(sigma) = ell_T(sigma).

The integral Pfaffian identity det(A)=Pf(A)^2 holds after reduction to every field for alternating matrices A, including characteristic two. Thus a nonzero Pfaffian of a principal 2d-by-2d minor implies rank(A)≥2d.

## Lower bound when n≥2d+1
Fix S⊆[n] with |S|=2d and set

q(X)=Pf((X−X^T)[S,S]).

It has degree d. If q(P_sigma)≠0, the two facts above give

2d ≤ rank(P_sigma−P_sigma^T) ≤ rank(P_sigma−I) = ell_T(sigma).

The polynomial is not identically zero: a (2d+1)-cycle on S and one extra vertex leaves an oriented even path after the extra vertex is deleted, so its Pfaffian is ±1. Therefore no radius below 2d suffices.

## Lower bound for odd n≤2d+1
Take S of size n−1 and the same Pfaffian. Its degree (n−1)/2 is at most d, and nonzero implies ell_T(sigma)≥n−1 by the same rank argument. An n-cycle gives ±1. This proves sharpness at n−1.

## Lower bound for even n=2r≤2d, n≥4
Choose distinct a,b∈[n], let S=[n]\{a,b}, and define

q(X)=(x_ab−x_ba) Pf((X−X^T)[S,S]).

Its degree is 1+(n−2)/2=r≤d. If q(P_sigma)≠0, exactly one of sigma(a)=b and sigma(b)=a holds. This remains true in characteristic two: if both hold their sum is zero. Therefore a,b lie in the same cycle, and that cycle has length at least three.

Suppose there were another cycle C. Then C⊆S. The vector supported on C and equal to one there lies in the kernel of (P_sigma−P_sigma^T)[S,S]: there are no matrix entries linking C to other cycles, and the rows within C sum to zero. The principal matrix would be singular and its Pfaffian zero, a contradiction.

Thus every nonzero witness is an n-cycle and has distance n−1. The polynomial is not identically zero: take any n-cycle with a,b consecutive. The first factor equals ±1; deleting a,b leaves an oriented path on n−2 vertices, with a unique perfect matching and Pfaffian ±1.

For n=2 use q(X)=x_12. The antisymmetric-factor construction must not be used at n=2 because x_12−x_21 vanishes on both permutation matrices.

## Independent exhaustive checker
transposition_radius_test.py uses exact integers and recursive Pfaffian expansion. It checks every permutation for n=2,...,8, verifying:
1. The small-n extremal polynomial is nonzero precisely on n-cycles, with a,b adjacent in the even case.
2. All its values are 0,+1,−1.
3. For every feasible 1≤d≤floor((n−1)/2), a nonzero principal 2d-minor Pfaffian implies transposition distance at least 2d.

Observed nonzero counts for n=2,...,8 were 1,2,4,24,48,720,1440. At n=8, all 40,320 permutations were tested, including 120,960 general-minor checks, with no failures. In the even cases n≥4, the nonzero count agrees with 2(n−2)!, the number of n-cycles with the designated vertices adjacent in either direction.

These finite checks are corroboration; the arguments above prove the result for every n,d and every field.
