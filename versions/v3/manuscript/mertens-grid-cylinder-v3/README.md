# Boundary bounds for grid–cylinder domination growth

This note gives an alternative proof of the equality in Mertens (2024),
Section 5, page 19, immediately after equation (22). The equality already
follows from the grid-growth and selected-frame results of Gangloff and
Talon (2019/2020). The note gives an explicit same-size boundary comparison,
quantitative strip and rectangle bounds, and positive-activity extensions.

## Contents and build

- `note.tex` and `note.pdf`: statements, complete proofs, coverage table and references.
- `metadata.json`: bibliographic description and covered problem identifier.
- `coverage.json`: source locators, prior results and declaration-by-declaration scope.
- `verify.py` and `verification.json`: exact finite checks and their deterministic output.
- `SHA256SUMS`: checksums of these seven files.

Build with Tectonic 0.17.0 and Python 3.10 or later:

```sh
tectonic note.tex
python3 verify.py > verification.json
```

Alternatively run `pdflatex note.tex` twice. All bibliography entries are
included in the TeX source; BibTeX is unnecessary. There are no external
figures or data dependencies.

## Mathematical coverage

For ordinary dominating subsets on labelled vertices, the finite comparison is
`g(m,n) <= c(m,n) <= 4^n g(m,n)`, for `m >= 3, n >= 1`. The common
unrestricted joint per-vertex limit also equals the torus limit. With `h`
its natural logarithm, a rectangle gives
`0 <= h-log(g(a,b))/(ab) <= 2 log(2)(1/a+1/b)`, and the fixed-width strip
rate `h_m` satisfies `0 <= h-h_m <= 2 log(2)/m`.

For every fixed positive activity `z`, replace the counts by domination
polynomials evaluated at `z` and replace `2` in the boundary-error constant
by `1+1/z`. The same written proof covers king graphs and their periodic
versions. The ten-digit king-growth conjecture after Mertens (24), the
numerical estimates (21)–(23), and the assumed expansion (20) are not
consequences of these estimates.

The pinned
[MertensGridGrowth.lean](https://github.com/the-omega-institute/trureturing/blob/e277c80d045570daf43bd03b4e313f7ce457b4e2/D5/S3/Combinatorics/Graph/Domination/MertensGridGrowth.lean)
contains `finite_seam_bound`, `tiling_count` and `result`, for the seam
comparison, block inequality and common joint grid–cylinder limit.
Their namespace is `D5.S3.Combinatorics.Graph.Domination.MertensGridGrowth`.
The same revision's
[DominatingSetAverage.lean](https://github.com/the-omega-institute/trureturing/blob/e277c80d045570daf43bd03b4e313f7ce457b4e2/D5/S3/Combinatorics/Graph/DominatingSetAverage.lean)
defines `domSets` as all ordinary dominating subsets. The entropy, torus,
strip, positive-activity and king extensions have written proofs in the note.

The checker exhaustively enumerates subsets for `1 <= m,n <= 6` with
`mn <= 16`; periodic dimensions are at least three. A second direct
closed-neighborhood predicate agrees for graphs with at most 12 vertices.
It checks 87,808 cylinder repair pairs, 99,472 torus repair pairs and
270,892 king repair pairs. At activities `1/2`, `1`, `2`, exact fraction
arithmetic verifies 84 one-seam inequalities, 36 second-seam inequalities,
1,176 weighted block bounds and 648 weighted exact-partition bounds.
The output gives complete polynomial coefficients for all free rectangles
and eligible periodic versions in the stated finite range. The infinite
limits follow from the written proofs, rather than these finite checks.

## Authors and license

Haobo Ma — ChronoAI Pte Ltd, Singapore.

Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

CC BY 4.0 (Creative Commons Attribution 4.0 International).
