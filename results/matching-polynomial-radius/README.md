# Matching-polynomial support and flip radii

Fix a baseline perfect matching on the complete simple graph with 2n vertices. Polynomials use ordinary unordered-edge incidence variables. A support radius counts missing baseline edges (changed baseline pairs), not individual moved vertices.

- support-upper/PROOF.md proves over **every field** that a nonzero degree-at-most-d function has a witness missing at most min(n,2d+1) baseline edges.
- support-char2/PROOF.md supplies matching lower examples **in characteristic two**, proving exact support radius min(n,2d+1) for n>=2 and d>=1 in that characteristic.
- flip-radius/PROOF.md proves flip distance equals m-c, where m is the number of changed baseline pairs and c the number of nontrivial alternating cycles. The universal radius is at most min(n-1,2d) over every field, and exactly that value in characteristic two.

For d=0 or n<=1, both radii are zero. A flip replaces two matching edges on four vertices by another pairing; intermediate matchings belong to the complete graph. No odd-characteristic sharp lower bound is claimed. No missing-edge-domain transfer, optimal algorithmic runtime, historical novelty or P versus NP consequence follows.

All three frozen proof files are preserved byte-for-byte. The neighboring check.py files contain independent finite controls and their .log files record actual packaged runs. From each subdirectory run python check.py, or use ../colorful-parity/run_checks.py to run the entire checkpoint. These tests support rather than formally verify the general field-uniform upper arguments or characteristic-two lower arguments.

The stronger direct upper bound is a separate mathematical result: the accompanying frozen undirected solver still uses its earlier valid 4(k+q)+1 bound. Implementation changes would need their own review.
