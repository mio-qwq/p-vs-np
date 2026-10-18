# Independent review of the arbitrary-depth obstruction

**Verdict: verified.** The supplied self-contained derivation is sound. It proves the stated obstruction for every integer `t ≥ 1` and every integer `m ≥ 2 ceil(log₂(2t))`. No oddness assumption on `m` is required.

The exact reviewed derivation is published as `general-theorem.md`, SHA-256:

    a02a5125b5905d9127cc698c64156572b53a20ab32243ffa6238859472fc957b

`general-theorem.md` is an exact copy, with that same SHA-256. The review checks the mathematical argument, rather than inferring correctness from the small computations.

## Checks of the general proof

1. **Zero-sum exclusion.** Vanishing odd power sums through `2t−1` implies vanishing of every positive power sum through `2t−1`, by repeatedly squaring. The zeroth power sum is zero because the number of distinct rows is even. Distinctness makes the square Vandermonde matrix invertible, contradicting its annihilation of the nonzero all-ones vector. This argument also applies when one of the selected field elements is zero: its zeroth-coordinate entry is defined as `1`.

2. **Trace representation, including even `m`.** The trace polynomial is nonzero of degree `2^(m−1) < 2^m`, so it is not identically zero on the field. Its values belong to `F₂`; therefore it is surjective. Multiplication by any nonzero coefficient is a bijection, establishing nondegeneracy of the trace pairing. Consequently every ambient binary affine functional has the stated unique coefficient representation. The shortcut `Tr(1)=1` would fail for even `m`; the reviewed proof does not use it.

3. **No hidden cyclotomic identifications.** Write `L=ceil(log₂(2t))`. Each allowed exponent is positive, odd, and less than `2^L`. A rotation by `1 ≤ r < m` that produces another such exponent would need a one at the original bit `a=m−r`. Hence `a≤L−1`. But the original bit zero becomes a one at `r=m−a≥L+1`, inconsistent with the rotated exponent being less than `2^L`. This rules out both shorter orbits and collisions between different allowed exponents. All reduced exponents lie between `1` and `N−2`, since no original bit string is zero or all ones. Therefore the expanded trace polynomial has no cross-term cancellation, has degree less than `N`, and is not the zero function. An added constant cannot cancel any of its positive-degree terms.

4. **Boolean degree and support.** In binary coordinates, Frobenius maps are linear. Expanding the product expression for `x^j` bounds each coordinate's Boolean algebraic degree by the number of ones in the binary expansion of `j`, at most `L`. Reducing coordinate powers by `z²=z` cannot increase degree. The stated induction proves that a nonzero Boolean function of degree at most `L` has weight at least `2^(m−L)`. The `P₁=0` branch doubles the support; the other branch contributes at least one nonzero evaluation for each nonzero evaluation of `P₁`. Thus every nonzero ambient affine functional has support at least `2t`.

5. **Conditioning is genuine matching conditioning.** A partial matching of at most `2t−1` edges removes that many rows and leaves at least one special column. The surviving labels retain full affine span by the support bound. The number `r` of unfilled special columns is strictly smaller than the number of surviving rows. For each two surviving indices, there are at least `r−1` other indices, so valid subset exchanges realize every pair difference. Every such `r`-subset can be assigned to the remaining special columns and extended over zero-label columns because the graph is complete. Thus the proof concerns exact perfect-matching extensions, not an independent-edge relaxation.

6. **Quantifiers and boundary.** For each fixed depth `d`, take `t=ceil((d+1)/2)` and arbitrarily large `m` satisfying the threshold. Then `k=tm=O_d(log N)`. At depth `2t`, fixing all special columns leaves a nonzero singleton hull; no failure at that depth is claimed. The result refutes completeness of the specified fixed-depth affine-hull tests, not stronger algorithms, fixed-dimension algorithms, or a complexity-class equality.

## Sharper optional bound using Weil

The self-contained proof is sufficient and does not depend on this paragraph. A standard additive-character estimate supplies the slightly sharper numerical hypothesis `N ≥ 4t²`, for any integer `m` with `N=2^m`.

If some coefficient is nonzero, the polynomial `f(X)=Σ a_j X^j` has positive odd degree `d≤2t−1`. For the nontrivial character `ψ(z)=(-1)^Tr(z)`, the Weil estimate is

    |Σ_(x∈F) ψ(f(x))| ≤ (d−1)√N ≤ (2t−2)√N.

The hypotheses are met because `gcd(d,2)=1`. This standard estimate is explicitly stated in the introduction of Ronald Cramer and Chaoping Xing, *An improvement to the Hasse–Weil bound and applications to character sums, cryptography and coding*, Advances in Mathematics 309 (2017), 238–253, [author-institution PDF, p. 239](https://ir.cwi.nl/pub/28867/28867.pdf#page=2), [DOI](https://doi.org/10.1016/j.aim.2017.01.011).

Therefore the support of either affine shift of the trace function is at least

    δ = [N−(2t−2)√N]/2.

When `√N≥2t`, write `y=√N`; the numerator is `y(y−2t+2)≥(2t)·2=4t`, so `δ≥2t`. This proves the same deletion and conditioning conclusions. An odd leading degree also rules out the formal polynomial exception `g²+g+c`, whose nonconstant degree is even. No separate assumption that the trace function is nonzero is being smuggled in: the strictly sub-`N` character-sum estimate itself proves this. For smaller fields genuine trace degeneracy is possible; the exact checker includes `Tr_(GF(16)/F₂)(x⁵)=0` as a negative control.

## Exact depth-five certificate

`check_depth_five.py` independently recomputes all 906,192 six-subset sums and all 65,536 ambient affine functional weights for `t=3, m=5`, with output in `certificate.json`. It passes. This parameter lies below both sufficient general thresholds; its stronger support bound is established by exact enumeration. Full details and the implication for every conditioned matching are in `README.md`.

The script also checks 192 finite parameter cases of the orbit lemma, covering `t=1,…,64` at three field degrees starting at the sufficient threshold. Those finite checks supplement the proof and are not offered as a proof for arbitrary parameters.

The construction uses standard finite-field parity-check and trace-code ingredients. There is no claim of novelty, and no claim about P versus NP.

## Publication editorial note

The original mathematical argument was independently reviewed by an AI reviewer. This public audit differs only in its provenance path and this note; a publication check confirmed that the mathematical text is unchanged. It is not human peer review. Original and published hashes are recorded in `PROVENANCE.json`.
