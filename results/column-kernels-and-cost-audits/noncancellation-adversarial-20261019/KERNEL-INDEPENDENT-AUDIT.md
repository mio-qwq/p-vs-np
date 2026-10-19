# Independent audit of the one-gap kernel theorem

19 October 2026. The constructive structural worker independently reviewed KERNEL-THEOREM.md Sections 1--3 and found no defect.

Checked in detail:
- Factoring the common exponent shift preserves the constant kernel.
- The proposed cardinal polynomial interpolates correctly and its correction cancels the forbidden t^(n-1) coefficient.
- Extracting the coefficient of t yields the stated signed Laplace identity, including the factor (-1)^(n-2) and h'(b_s).
- The x^n coefficient of the weighted identity is exactly n(n-2)A0; n>=3 is used essentially here.
- A nonzero kernel must have A1 nonzero. A centered zero offset creates the claimed double pole, which cannot occur in the simple-pole expression H.
- For nonzero offsets, regularity at zero forces f'(0)=0, and residues determine the candidate kernel uniquely up to scale.
- The candidate satisfies the identity when sum 1/b_s=0; this is equivalent to f'(0)=0 because f(0) is nonzero.
- With distinct real centered nonzero offsets and n>=3, two adjacent offsets share a sign; their alternating derivative signs prove every nonzero kernel vector has both signs.

The argument proves the stated infinite family, rather than relying on finite rank checks. It does not prove nonnegative-kernel exclusion for arbitrary exponent sets or any arbitrary-graph noncancellation statement.
