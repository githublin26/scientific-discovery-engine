# Single-record retrospective evidence check — 2026-10-07

Actual input: existing official GNoME snapshot, SHA256 c37bffb9dd6c51d38d259a2d340ecf796194729f656d474828512390db1ff0c9.
Retrieval manifest time: 2026-10-07T03:24:52.971637+00:00.
Candidate: 000006a8c4, composition Cs1S6Zr3, reduced formula Cs(ZrS2)3.
Published formation energy: -1.9058 eV/atom; published Decomposition Energy Per Atom All: 0.0 eV/atom; space group: C2/m.
Derived conversion: 0.0 meV/atom. Project tolerance check at 0.001 eV/atom: true.

The reference file was pinned from the raw record inspected before writing the new mapper. Five reference checks passed. This is a retrospective data-mapping regression, NOT independent thermodynamic recomputation and NOT a blinded prediction experiment. No method superiority or materials novelty is claimed.
12 software tests passed (five preserved original tests and seven new tests).
Missing-ID CLI check returned structured UNKNOWN. Python compilation passed. The optional system skill quick_validate.py could not run because its Python environment lacks PyYAML; no dependency was installed just for packaging. SKILL.md frontmatter and repository-relative links were inspected directly. This skill is not installed globally.
Local generated evidence: runs/materials-v01/000006a8c4.json, including the complete raw record and per-field provenance.

Reproduce from the project root:
```powershell
python -m skills.materials_discovery --snapshot data/gnome.csv --candidate-id 000006a8c4 --out runs/materials-v01/reproduced.json --reference skills/materials_discovery/examples/reference.json
```
Use a new output filename if it exists. The frozen reference deliberately rejects a different snapshot hash.
Remaining UNKNOWN: actual CIF coordinates, independent hull calculation, experimental synthesis, calibrated confidence, Mo5GeB2 detailed claims, Antigravity execution logs not attached here.
Next smallest experiment: check an independently retrieved computational reference for a small same-chemistry group, preserving calculation compatibility. Do not claim predictive discrimination until mixed classes and held-out input/label separation exist.
