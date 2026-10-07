# Rare Signal Lab: moat thesis

This file separates what v0.1 demonstrates from what remains a hypothesis.
The experiment report, not this narrative, is authoritative for results.

## Demonstrated in v0.1

- A small, runnable benchmark turns an early-warning idea into a falsifiable
  comparison against fixed and budget-matched SPC baselines.
- The protocol separates training, calibration, validation, and test runs and
  freezes thresholds before test evaluation.
- Results retain event recall, detected-only lead, false alarms, calibration,
  per-scenario rows, per-seed rows, and a zero-precursor negative control.
- The machine-readable gate preserves a negative result: neither candidate
  supports H1 under the documented v0.1 convention.
- Deterministic generation, causal features, threshold behavior, metric
  denominators, calibration edges, train-only SPC fitting, and end-to-end
  reproducibility are covered by nine passing tests.

These are research-engineering strengths. They are not evidence of superior
semiconductor detection, proprietary advantage, or production readiness.

## Hypothesized moat — not yet demonstrated

- Combining weak multivariate evidence may warn earlier than conventional SPC
  at an operationally acceptable false-alarm rate in real process data.
- Evidence discipline, explicit negative controls, and durable provenance may
  make future scientific iterations more trustworthy and reusable.
- Domain knowledge may eventually improve simulator realism, label design, and
  validation choices in ways generic anomaly-detection demos do not.

## Evidence needed to strengthen the thesis

1. Stable candidate-versus-SPC gains across more independent seeds with
   uncertainty intervals and a pre-registered decision rule.
2. Robustness to realistic rarity, missing or delayed measurements, process
   drift, tool shifts, competing events, and uncertain labels.
3. Chronological or unseen-tool validation on appropriately governed real or
   credible public data.
4. Operational metrics based on alarm episodes and intervention costs, not
   only per-lot alerts.

Until then, the defensible asset is the reproducible evaluation framework and
its evidence discipline—not a claim that the proposed model wins.
