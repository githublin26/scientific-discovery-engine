"""Reproducible four-way benchmark; no test-dependent fitting or threshold tuning."""
import argparse
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
import pandas as pd
import sklearn
from .data import generate
from .models import Baselines, calibrate, threshold
from .metrics import evaluate, reliability


def run(seed, runs, strength, budget, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    splits = {name: generate(seed*10+i, runs, strength)
              for i, name in enumerate(["train", "calibration", "validation", "test"])}
    model = Baselines().fit(splits["train"], seed)
    scores = {name: model.scores(f) for name, f in splits.items()}
    cal, val, test = (splits[k] for k in ["calibration", "validation", "test"])
    report, predictions, event_rows, calibration_rows = [], [], [], []
    reference = scores["test"]["shewhart"] >= 3
    for name in scores["test"]:
        c = cal.eligible.to_numpy()
        calibrator = calibrate(scores["calibration"][name][c], cal.target.to_numpy()[c])
        p = calibrator.predict_proba(scores["test"][name].reshape(-1, 1))[:, 1]
        v = val.eligible.to_numpy()
        tuned = threshold(scores["validation"][name][v], val.target.to_numpy()[v], budget)
        variants = [(name+"_budget", tuned)]
        if name in ["shewhart", "ewma"]:
            variants.insert(0, (name+"_3sigma", 3.))
        for label, limit in variants:
            alert = scores["test"][name] >= limit
            metrics, events = evaluate(test, alert, p, reference)
            prevalence = float(cal.target.to_numpy()[c].mean())
            metrics["constant_brier"] = float(np.mean((test.target.to_numpy()[test.eligible]-prevalence)**2))
            metrics.update(model=label, threshold=float(limit), seed=seed)
            report.append(metrics)
            event_rows.extend(dict(e, model=label, seed=seed) for e in events)
            for scenario in ["noise", "slow", "obvious"]:
                # Preserve positions for causal scores when taking a subgroup.
                mask = test.scenario.to_numpy() == scenario
                sub, _ = evaluate(test[mask].reset_index(drop=True), alert[mask], p[mask], reference[mask])
                report.append(dict(sub, model=label, threshold=float(limit), seed=seed, scenario=scenario))
            pred = test[["run_id", "lot_id", "lot_index", "scenario", "onset", "target", "eligible"]].copy()
            pred["model"], pred["score"], pred["probability"], pred["alert"] = label, scores["test"][name], p, alert
            predictions.append(pred)
        bins = reliability(test.target.to_numpy()[test.eligible], p[test.eligible])
        calibration_rows.extend(dict(b, model=name, seed=seed) for b in bins)
    csv = {}
    for name, f in splits.items():
        path = output/f"{name}.csv"
        f.to_csv(path, index=False)
        csv[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    pd.DataFrame(report).to_csv(output/"metrics.csv", index=False)
    pd.concat(predictions).to_csv(output/"predictions.csv", index=False)
    pd.DataFrame(event_rows).to_csv(output/"events.csv", index=False)
    pd.DataFrame(calibration_rows).to_csv(output/"reliability.csv", index=False)
    manifest = {"seed": seed, "runs_per_split": runs, "signal_strength": strength,
                "validation_false_alarm_budget": budget, "horizon_lots": 12,
                "split_seeds": {k: seed*10+i for i, k in enumerate(splits)},
                "python": platform.python_version(), "numpy": np.__version__,
                "pandas": pd.__version__, "sklearn": sklearn.__version__, "sha256": csv}
    (output/"manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return pd.DataFrame([r for r in report if "scenario" not in r])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 43, 44])
    parser.add_argument("--runs", type=int, default=120)
    parser.add_argument("--signal-strength", type=float, default=1.)
    parser.add_argument("--false-alarm-budget", type=float, default=1.)
    parser.add_argument("--output", type=Path, default=Path("results/default"))
    args = parser.parse_args()
    if args.runs < 40 or args.false_alarm_budget < 0 or args.signal_strength < 0 or any(s < 0 for s in args.seeds):
        parser.error("runs >= 40; seeds, strength and budget must be nonnegative")
    summary = pd.concat([run(s, args.runs, args.signal_strength, args.false_alarm_budget,
                            args.output/f"seed_{s}") for s in args.seeds], ignore_index=True)
    summary.to_csv(args.output/"summary.csv", index=False)
    print(summary[["seed", "model", "excursion_recall", "false_alarms_per_100_normal_lots",
                   "median_lead_lots_detected", "brier"]].to_string(index=False))


if __name__ == "__main__":
    main()
