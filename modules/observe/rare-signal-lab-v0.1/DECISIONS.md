# Decision log

Only decisions supported by the v0.1 repository or necessary to preserve its
Project Truth are recorded here.

## 2026-10-07 — Treat v0.1 as a benchmark accepted with limitations

**Status:** accepted

**Decision:** Preserve v0.1 as a valid, reproducible synthetic research
benchmark. Record H1 as **not supported by the documented strict exploratory
gate**, rather than passed or partially passed.

**Why:** Both candidates show useful partial signals, but neither satisfies all
gate conditions across seeds. A partial metric improvement is evidence for a
follow-up question, not a partial hypothesis pass.

**Evidence:** `example_results/REPORT.md`, `example_results/assessment.json`,
per-seed `metrics.csv`, and nine passing tests.

**Revisit when:** A pre-registered follow-up meets its complete decision rule on
independent data.

## 2026-10-07 — Keep simple baselines; do not add a Transformer

**Status:** accepted for the next experiment

**Decision:** Continue with the existing SPC and simple ML models.

**Why:** v0.1 does not isolate model capacity as the cause of failure. The
observed problems are cross-seed consistency and false-alarm-budget
generalization. Adding architecture complexity would not answer either issue.

**Rejected for now:** Transformer or agent-swarm implementation.

**Revisit when:** A controlled benchmark shows a sequence dependency that the
current causal features and simple models cannot capture.

## 2026-10-07 — Next smallest experiment: threshold-generalization audit

**Status:** proposed; not yet run

**Decision:** Freeze the simulator, features, models, 12-lot horizon, and
one-per-100 validation budget. Run more independent seeds and report confidence
intervals for slow-event recall and lead plus pooled test false alarms. Do not
retune on test results.

**Why:** This is the smallest experiment that distinguishes a noisy three-seed
failure from a systematic inability to generalize the validation false-alarm
constraint. It directly targets the two reasons the v0.1 gate failed without
changing multiple variables at once.

**Completion rule:** Pre-register the seed count and interval method, retain the
zero-precursor control, and decide the result using the frozen gate or an
explicitly versioned replacement before examining results.

## 2026-10-07 — Use the repository as cross-client Project Truth

**Status:** accepted

**Decision:** Route operating rules to `AGENTS.md`, verified project state to
`README.md`, demonstrated versus hypothesized differentiation to `MOAT.md`,
decisions to this file, and experiment findings to
`example_results/REPORT.md`.

**Why:** Chat histories are fragmented across Mobile Codex, Desktop Codex,
Codex CLI, and GPT. Durable claims must remain discoverable without relying on
the user's memory of a conversation.
