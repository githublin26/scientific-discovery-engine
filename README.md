# Rare Signal Discovery Engine
Priority: Merck 2027 Science Agent preparation.

This project does not claim experimental discovery of new materials.
v0.1 evaluates whether an AI-assisted scientific workflow can reproducibly identify and rank candidates using public computational evidence, while preserving source provenance and uncertainty.
Research question: Can an AI-assisted workflow reproducibly retrieve, rank and trace materials candidates using public computational evidence?

## Actual project state
This is one Scientific Discovery Engine project. Semiconductor QA / process-excursion early warning is the intended observation module, but synthetic semiconductor generation, Shewhart, EWMA and ML benchmarks are NOT implemented. The existing rare_signal package is a materials CSV baseline. The new skills/materials_discovery submodule supports one exact public MaterialId; it is repository-local workflow packaging, not automatically installed into Codex or Antigravity.
User decisions and proposed architecture are preserved in [handoff](docs/HANDOFF.md).
Technical assets exist, but a competitive moat is not yet demonstrated. See [asset audit and evidence gates](docs/TECHNICAL_MOAT.md); provenance and mapping tests alone do not establish superiority over other agents.

## One real material (Python standard library only)
Run from this project directory. The current local official snapshot is already downloaded; do not fetch again unnecessarily. On another machine, first run the retrieve command below. No remote GitHub repository has been published, so there is no clone URL yet.
```powershell
python -m rare_signal retrieve --output data/gnome.csv
python -m skills.materials_discovery --snapshot data/gnome.csv --candidate-id 000006a8c4 --out runs/materials-example.json --reference skills/materials_discovery/examples/reference.json
python -m unittest discover -s tests -v
```
Skip retrieve when data/gnome.csv already exists. Output files are not overwritten; use a new output path on reruns. Reference is pinned to the 2026-10-07 snapshot hash; a newer download may fail reference validation intentionally. Without --reference, lookup still works for another snapshot or ID. Formula/system querying is not implemented; exact MaterialId satisfies the first vertical slice.
The example is Cs1S6Zr3, source ID 000006a8c4. JSON includes the complete raw record, field-level retrieved/unknown evidence, derived meV/atom conversion and tolerance comparison, interpretation and snapshot provenance. Atomic coordinates and experimental evidence remain UNKNOWN. Missing IDs produce structured UNKNOWN, not a guessed candidate.
PASS_REFERENCE_MAPPING means five pinned fields match the public record, not independent DFT validation, blinded prediction or scientific hypothesis acceptance. See [results](experiments/retrospective_validation/MATERIALS_V01.md).

## Run (Python 3.12+, no dependencies)
```powershell
python -m unittest discover -s tests -v
python -m rare_signal run --input tests/fixtures/materials.csv --out runs/demo
python -m rare_signal retrieve --output data/gnome.csv
python -m rare_signal run --input data/gnome.csv --out runs/gnome
```
The fixture is synthetic and tests software only. The retrieve command downloads the official GNoME stable-material summary; network access is required. Run outputs include candidates, frozen predictions, revealed references, metrics and provenance.

## Scientific boundaries
v0.1 is a deterministic tool foundation, NOT an autonomous AI co-scientist or trained stability model. Ranking uses negative formation energy as a deliberately weak baseline; negative formation energy does not imply convex-hull stability. Reference decomposition energy is never passed to the ranker. No independent formation-energy, hull or DFT calculations are performed.

The released GNoME stable-material dataset is selection-biased. Single-class results cannot establish general stability discrimination. Precision@3 and prevalence are descriptive; no scientific PASS is issued. Hashes and source-row numbers enable tracing. Uncertainty is uncalibrated, not a probability. Hiding labels in an artifact is not a security boundary against an agent allowed to read the raw file.

## Priorities
1. Reproducible public-data ingestion and leakage-resistant baseline.
2. Mixed stable/unstable, composition-grouped held-out benchmark; compare random and simple baselines.
3. Independent pymatgen hull reconstruction with compatible energy references.
4. Agent hypothesis/evidence loop, literature checks and human-approved next experiments.
5. Competition deliverables once 2027 rules and eligibility are verified.
These are materials-submodule milestones, not a replacement for the user's semiconductor observation-module priority. Semiconductor results will require their own synthetic benchmark; none are claimed here.

See [protocol](experiments/retrospective_validation/PROTOCOL.md) and [Merck preparation](docs/MERCK_2027.md).
