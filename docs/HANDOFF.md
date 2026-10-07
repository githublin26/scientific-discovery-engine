# Project handoff — 2026-10-07
This is a condensed durable record of the user's supplied 25-section handoff, not a verbatim transcript.

## User decisions
P0: Merck AI Agents Cup 2027 preparation (rules/eligibility remain unverified).
P1: Rare Signal Discovery Engine, originally semiconductor QA/process-excursion early warning, is the observation module of a broader Scientific Discovery Engine.
P2/current iteration: materials-discovery v0.1 inside this same project.
No parallel top-level projects. User has no wet lab; computational validation is the current scope.
Preserve: “重新回到『建造』” and “不要把構想寫成已完成成果。”

## Proposed architecture, not completed implementation
OBSERVE: weak-signal detection/reconstruction/uncertainty.
SEARCH: Generate → Screen → Validate → Learn.
EXECUTE: scientific tools. VALIDATE: provenance, computation, literature, future experiments.
ChatGPT directs research; Codex engineers artifacts; Antigravity operates scientific tools; GitHub is the intended durable store. No GitHub remote/publication is currently configured.

## Proposed semiconductor research, still unimplemented
H0: conventional SPC equals or outperforms uncertainty-aware multivariate methods.
H1: multivariate precursors yield earlier detection with acceptable false alarms.
Synthetic fixed-seed scenarios: obvious excursion, slow precursor, noise/no excursion.
Baselines: Shewhart 3σ, EWMA, ML baseline; Isolation Forest/Gradient Boosting/uncertainty-aware approaches are proposals.
Primary metrics: lead time, false alarms/100 lots, recall, precision/PPV, calibration.
Proposed columns: lot_id, timestamp, oxygen_ppm, water_ppm, particle_01um, particle_02um, pressure_drop, assay, temperature, tool_id, batch_age, excursion_label.
Do not imply these exist because specification exists.

## Current verified engineering state
rare_signal/ contains the earlier public-material CSV baseline, CLI and provenance, NOT semiconductor SPC.
tests/ contains five original software tests plus the new single-record tests.
data/gnome.csv and retrieval manifest already exist locally; reuse them, do not redownload without reason.
Prior full-data run: 554,054 records, single class; no predictive-skill evidence.
New single-record artifacts and their actual validation are described in README and the experiment result document.

## Evidence discipline
Separate retrieved/derived/inferred/unknown; preserve exact IDs, raw records, source URLs/times, hashes, code/version, units and assumptions.
Missing fields must remain UNKNOWN.
The handoff reports Antigravity Science Skills execution and materials-tool gaps; its referenced “貼上的文字 (1).txt” was not supplied here. Treat these as user-reported, not independently inspected logs.
Mo5GeB2 crystallographic sites, Tc ≈ 5.8 K and synthesis claims are unverified here; do not copy as ground truth.
IceCube/GNoME are inspirations, not proof that the proposed method will work.

## Exclusions
No GNN training, full GNoME reproduction, DFT/HPC infrastructure, transformer without evidence, agent swarm, plugin proliferation, proprietary company data or wet-lab discovery claims.
No model switching claimed. Model/client availability is separate from scientific acceptance.

## Remaining questions
Mixed-class blinded predictive benchmark; independent compatible hull reconstruction; CIF retrieval; literature/experimental confirmation; semiconductor benchmark implementation; 2027 rules and data-license applicability.
No Materials Project key or pymatgen is required for the current CSV retrieval/units slice.
