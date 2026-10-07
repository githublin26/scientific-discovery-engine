---
name: materials-discovery
description: Retrieve and trace one exact public GNoME MaterialId from a local CSV snapshot, separating published energies, derived screening values and unknown evidence. Use for single-record computational evidence, not synthesis claims or independent DFT.
---

# Materials discovery v0.1
Repository-local workflow; it has not been installed as a globally discoverable Codex or Antigravity skill.

## Inputs and execution
Run from the project root with Python 3.12+ and no external packages.
Input: exact MaterialId and snapshot path. Formula/system search is not implemented; obtain an exact ID from the public CSV rather than guessing a structure.
Reuse data/gnome.csv and its .provenance.json manifest if present. Otherwise use python -m rare_signal retrieve --output data/gnome.csv; external access remains subject to normal approval.

```powershell
python -m skills.materials_discovery --snapshot data/gnome.csv --candidate-id 000006a8c4 --out runs/materials-evidence.json --reference skills/materials_discovery/examples/reference.json
```
Omit --reference for arbitrary IDs. The optional --threshold is a finite nonnegative project screening tolerance in eV/atom (default 0.001), not a universal synthesis criterion.

## Output and evidence rules
JSON preserves raw_record, retrieved_values, derived_values, interpretation, unknown_fields and provenance. The snapshot hash, CSV record number and exact ID trace each field; the original manifest supplies retrieval time. Without a manifest, source URL/retrieval time remain unknown, never inferred from filename.
The derived properties are a unit conversion and explicit screening rule on the published All metric. Do not rename MP, MP OQMD or Relative values as All; their reference hulls differ.
CSV space-group metadata is not a CIF structure. Never infer missing atomic coordinates, synthesis success, superconducting Tc or calibrated confidence. Mo5GeB2 claims in prior discussions are not ground truth.
Source order: actual public record and official dataset definitions; paper for methods; literature for experimental evidence. Model interpretation is not a database fact.

## Validation and failure
Checksum mismatch, malformed matched rows, duplicate IDs or invalid thresholds stop with an error. Missing ID produces UNKNOWN; missing/invalid numeric fields preserve raw text and produce unknown typed values. Output paths cannot already exist.
The pinned reference comparison checks field mapping against the specified snapshot and exits nonzero on mismatch; it is not blinded prediction or independent hull validation. A newer snapshot requires review, not automatic reference replacement.
Tests: python -m unittest discover -s tests -v.

## Scope and lifecycle
Generate: external/manual candidate IDs; Screen: published evidence lookup and rule; Validate: reference mapping now, independent calculations/literature later; Learn: retain evidence artifacts, with no active-learning implementation yet.
No wet lab, DFT, pymatgen, Materials Project API, trained GNN or agent swarm is required for this slice.
Read [source record](../../docs/SOURCES.md) for attribution and data restrictions, and [results](../../experiments/retrospective_validation/MATERIALS_V01.md) for demonstrated behavior.
