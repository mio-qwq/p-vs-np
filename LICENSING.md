# Licensing scope and third-party notices

The [MIT License](LICENSE) covers this repository's original code, research notes,
documentation, and data to the extent the repository copyright holder can
grant those rights. It does not claim ownership of or relicense third-party
quotations, referenced works, or external dependencies. Existing citations,
attribution, source receipts, and provenance records are retained.

## Quotations and research references

- `results/column-kernels-and-cost-audits/constructive-cost-audit-20261019/SOURCE-RECEIPT.md`
  contains explicitly marked short quotations from Yuefeng Du,
  *Bipartite Exact Matching in P*,
  [arXiv:2604.01571v3](https://arxiv.org/html/2604.01571v3), Proposition 2.3.
  Those quotations remain attributable to their original source and are not
  included in this repository's MIT grant.
- Papers and external source repositories cited throughout the research
  notes remain the works of their respective authors. Linking to, discussing,
  or independently implementing a result does not relicense its source.
  In particular, references to
  [SamuelSchlesinger/complexitylib2](https://github.com/SamuelSchlesinger/complexitylib2/tree/ffc377b51c1faac475b8cb5376d658fec457e70a)
  do not relicense that repository.
- The independent blossom implementation retains its attribution to Jack
  Edmonds's standard algorithm in `results/graphic-coupling/blossom/README.md`
  and `blossom.py`. Other historical and prior-art acknowledgments remain in
  their respective research notes.

## External dependencies

Some exact symbolic checkers require SymPy 1.14.0, as specified in the
corresponding requirements files. SymPy is an external dependency, not
vendored source in this repository. It and its bundled components retain
their upstream licenses and notices; see the
[SymPy 1.14 license file](https://github.com/sympy/sympy/blob/1.14/LICENSE).
This repository's MIT License does not replace those terms.
