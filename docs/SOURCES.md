# Source record
Checked 2026-10-07.
GNoME official data definitions:
https://github.com/google-deepmind/materials_discovery/blob/main/DATASET.md
GNoME repository:
https://github.com/google-deepmind/materials_discovery
Use published values as computational references only. Full independent hull construction requires compatible external entries and correction conventions. Released stable entries are not an unbiased stability test set.
Raw data licensing remains upstream; do not redistribute snapshots before checking upstream terms.

## Rechecked for the single-record slice (2026-10-07)
Official README: https://github.com/google-deepmind/materials_discovery/blob/main/README.md
It identifies repository code/notebooks as Apache-2.0 and database data as CC BY-NC 4.0. Preserve attribution to Google DeepMind / Merchant et al.; commercial use and competition-license applicability are not cleared by this project. Full downloaded snapshots and generated runs remain local/ignored.
Paper: Merchant et al., Scaling deep learning for materials discovery, Nature (2023), DOI 10.1038/s41586-023-06735-9: https://www.nature.com/articles/s41586-023-06735-9
Official overview: https://deepmind.google/blog/millions-of-new-materials-discovered-with-deep-learning/
Visualization notebook path was accessible: https://github.com/google-deepmind/materials_discovery/blob/main/notebooks/Visualize_GNoME_Structures.ipynb
DATASET.md lists CIF archives separately from summary CSV metadata; those large archives and r2SCAN data were not downloaded or independently checked here.
Local CSV schema includes MaterialId, Composition, Reduced Formula, Formation Energy Per Atom, Decomposition Energy Per Atom and named All/Relative/MP/MP OQMD metrics. Actual fields, not model-generated crystallography, supply the example.
The 0.001 eV/atom threshold is explicit project configuration; official documents contain version-dependent tolerances, so no universal threshold is asserted.
