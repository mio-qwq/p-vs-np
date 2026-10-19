# Root independent derivation: two-column nonnegative closure fails

2026-10-19. Let a0<a1<a2, h=a1-a0>0, k=a2-a1>0, t=L+a1. Multiply columns 0 and 1 of [(L+ai)^j]_(i,j=0,1,2) by row weights u_i>=0 and v_i>=0, respectively. Column2 stays full. Root independently confirms the constructive worker's classification.

At t=0, determinant equals u1*h*k*(h*v2+k*v0). If it vanishes identically, either u1=0 or v0=v2=0. In the latter case the only potentially nonzero matching terms use v1; the polynomial is v1*t*[u0*(t+k)^2-u2*(t-h)^2]. Identity forces v1=0 or u0=u2=0, and support has no perfect matching. Therefore a support-feasible identity requires u1=0.

Then determinant is t times
  v1*[u0*(t+k)^2-u2*(t-h)^2]+t*[u2*v0*(t-h)-u0*v2*(t+k)].
If v1=0, the constant coefficient inside the remaining linear factor is -h*u2*v0-k*u0*v2. Its vanishing forces both available matching products zero. Thus feasible identity has v1>0, and constant coefficient after division by t requires u0*k²=u2*h²; both u0,u2>0. Write u0=p*h²,u2=p*k². The next two coefficient equations uniquely give v0=q*h*(h+k),v1=q*h*k,v2=q*k*(h+k), with p,q>0.

Conversely substitution cancels all three coefficients exactly. For equally spaced offsets h=k=1, u=(1,0,1),v=(2,1,2) gives a zero polynomial on a graph with perfect matchings. All full-background one-column results remain untouched. Since v0/v1=(h+k)/k>1 and v2/v1=(h+k)/h>1, this identity cannot occur when both masks are binary. The claim covers three rows, exponents0,1,2, masks on columns0,1 only; no arbitrary sparse binary ASNC counterexample is established.

Final review status: the full relation-cone classification and both weighted-column families are documented in the independently reviewed companion proof. Root read it and independently reran the adversarial exact checker in normal and optimized Python. These are exact restricted-model results, not a general binary noncancellation refutation.
