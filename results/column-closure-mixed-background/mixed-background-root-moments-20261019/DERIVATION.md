# Root moment obstruction to proper powers for d=2,4,6

19 October 2026. Supporting proof independently audited and accepted. This supports the one-gap mixed-background ODE kernel criterion and is not a sparse noncancellation theorem.

Let a_1,...,a_n be distinct real offsets, n>=2, translated to mean zero. Put p_j=sum a_i^j, p_1=0,p_2>0, and H_d(L)=h_d(L+a_1,...,L+a_n). Uniform Dirichlet weights U on the simplex give X=sum U_i a_i and monic normalization
  H_d(L)/binom(n+d-1,d)=E(L+X)^d.
Indeed E X^j=j! h_j(a)/(n)_j. In particular
  mu2=p2/[n(n+1)],
  mu3=2p3/(n)_3,
  mu4=(3p2²+6p4)/(n)_4.
For even d, H_d(L)>0 at every real L, since X is nonconstant. Thus H_d has no real root. If the monic real polynomial H_d is a proper complex polynomial power, its monic root polynomial is real (unique monic root and conjugation), and its degree must be even; an odd-degree real root polynomial would have a real zero.

For d2 the only proper power would be square of a real linear polynomial, impossible. Equivalently the centered monic polynomial L²+mu2 has two simple complex roots.

For d4 the only possible proper power without real roots is the square of a monic real quadratic. Centering eliminates its linear coefficient. Thus E(L+X)^4=(L²+b)² implies mu3=0 and mu4=9mu2². But p4<=p2² implies
  mu4/mu2² <= 9n(n+1)/[(n+2)(n+3)] <9,
a contradiction.

For d6 a proper power without real roots must be the cube of a monic quadratic (the other divisors give odd-degree real polynomials). Centering again eliminates its linear coefficient. Thus E(L+X)^6=(L²+b)³ gives
  b=5mu2, mu3=mu5=0, mu4=5mu2², mu6=125mu2³.
As mu3=0, p3=0. Newton identities yield
  mu6=(15p2³+90p2p4+120p6)/(n)_6.
Set r4=p4/p2²,r6=p6/p2³. The required moment equalities force
  r4=(n²+11n+15)/(3n(n+1)),
  r6=(2n⁴+34n³+202n²+470n+375)/(3n²(n+1)²),
so
  r6-r4=(n⁴+22n³+176n²+455n+375)/(3n²(n+1)²)>0.
On the other hand p6<=p2*p4, since every a_i²<=p2 and sum a_i6<=p2 sum a_i4. This forces r6<=r4, contradiction.

Therefore H_d is not a proper polynomial power for d in {2,4,6}. This does not prove all its complex roots simple, and does not exclude individual multiple roots. It excludes a common divisor greater than one for all root multiplicities, exactly the property needed in the ODE criterion. Any degree8+ even extension remains open in this note.

Final review status: the constructive author and independent ODE auditor have both checked the moment formulas and proper-power exclusions. Root also reran the integrated exact checker in normal and optimized Python. The derivation is accepted as a supporting proof for the restricted one-outlier-background theorem; it remains separate from the already published frozen batch.
