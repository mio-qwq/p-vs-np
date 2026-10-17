# Exact all-field matching support radius

For ordinary edge-incidence polynomial functions of degree at most d on perfect matchings of K_(2n), the exact universal testing radius in changed baseline pairs is min(n,2d+1) when n>=2 and d>=1. For n<=1 or d=0 it is zero. The signed-hafnian lower construction works over every field and every nonzero commutative unital ring. The unchanged [direct upper proof](../matching-polynomial-radius/support-upper/PROOF.md) uses only integral additions/subtractions and unit coefficients, so the same upper bound extends to those rings.

PROOF.md is the frozen separate AI-assisted audit and proof. It generalizes the older characteristic-two SUPPORT lower bound. It does not extend the older exact FLIP-radius theorem beyond characteristic two. Changed-pair support and flip distance are different metrics.

Run Python 3 standard-library verification from this directory:

    python check.py

Actual output is check.log: 45,852 integer matching evaluations and 14,852 expanded-term checks (6,230 involution inputs). These finite regressions check the construction; the written argument supplies the unrestricted theorem. The proof and checker are byte-identical to their reviewed sources. See [provenance](../matching-degree-two-flip/SOURCE_PROVENANCE.json) and [prior-art context](../matching-degree-two-flip/PRIOR_ART.md).

No historical novelty, runtime lower bound, P versus NP solution, human peer review, or Lean verification is claimed.
