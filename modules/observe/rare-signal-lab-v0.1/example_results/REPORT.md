# Verified experiment results

Executed locally with Python 3.12.10 and the dependency versions in requirements-verified.txt.

Verification: **9 tests passed**, including deterministic end-to-end runs and raw split hash preservation.

Commands: default benchmark and zero-precursor control, seeds 42/43/44, 120 runs per split; then the assessment command. All 24 raw split files were checked against their manifest SHA-256 hashes.

**H1 is not supported by the documented strict exploratory gate.** Neither logistic regression nor boosting beats both budget-matched SPC models on slow-event recall and lead in every seed while satisfying the realized test false-alarm budget. Both improve pooled Brier scores over a calibration-prevalence constant forecast, and control recall drops. This is evidence that the designed ramp is learnable, not a semiconductor discovery or a reason to add Transformers.

The table below is the unweighted mean of three per-seed pooled metrics. Lead values average conditional medians; they are not an overall median or confidence interval. Consult per-seed metrics and scenario rows before interpretation.

| Model | Event recall | Lot precision | False alerts / 100 normal lots | Detected median lead (lots) | Brier |
|---|---:|---:|---:|---:|---:|
| ewma_3sigma | 0.737 | 0.206 | 5.023 | 6.83 | 0.0288 |
| ewma_budget | 0.621 | 0.495 | 0.946 | 5.17 | 0.0288 |
| gradient_boosting_budget | 0.686 | 0.532 | 1.150 | 7.00 | 0.0251 |
| isolation_forest_budget | 0.683 | 0.460 | 1.051 | 5.67 | 0.0298 |
| logistic_budget | 0.668 | 0.609 | 0.911 | 7.67 | 0.0245 |
| shewhart_3sigma | 0.692 | 0.212 | 1.928 | 4.83 | 0.0329 |
| shewhart_budget | 0.595 | 0.279 | 0.933 | 3.50 | 0.0329 |

Important distinctions: the random false alarms of fixed charts can hit pre-event windows even without a precursor. Event recall is therefore never proof of predictive information by itself. The enriched simulation and detected-only lead metric can make warning performance look stronger than it would be in a real fab. Test-budget violations are retained rather than fixed by retuning on test data.

Compact CSVs, reliability bins, manifests, event leads and the machine-readable gate checks are retained here. Full data and predictions live in the ignored results directory and can be regenerated.
