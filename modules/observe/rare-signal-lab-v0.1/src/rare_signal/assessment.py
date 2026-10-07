"""Audit the documented exploratory gate without changing any model or threshold."""
import argparse
import json
from pathlib import Path
import pandas as pd


def assess(default, control):
    rows = []
    for seed_dir in sorted(Path(default).glob("seed_*")):
        seed = int(seed_dir.name.split("_")[-1])
        main_manifest = json.loads((seed_dir/"manifest.json").read_text())
        null_manifest = json.loads((Path(control)/seed_dir.name/"manifest.json").read_text())
        if (main_manifest["signal_strength"] <= 0 or null_manifest["signal_strength"] != 0 or
                main_manifest["runs_per_split"] != null_manifest["runs_per_split"] or
                main_manifest["seed"] != null_manifest["seed"] or
                main_manifest["validation_false_alarm_budget"] != 1 or
                null_manifest["validation_false_alarm_budget"] != 1):
            raise ValueError("Gate requires matched seeds/run counts, positive default signal, zero control signal and budget 1")
        default_metrics = pd.read_csv(seed_dir/"metrics.csv")
        control_metrics = pd.read_csv(Path(control)/seed_dir.name/"metrics.csv")
        for candidate in ["logistic_budget", "gradient_boosting_budget"]:
            slow = default_metrics[default_metrics.scenario == "slow"].set_index("model")
            pooled = default_metrics[default_metrics.scenario.isna()].set_index("model")
            null_slow = control_metrics[control_metrics.scenario == "slow"].set_index("model")
            c = slow.loc[candidate]
            wins = all(c.excursion_recall > slow.loc[baseline].excursion_recall and
                       c.median_lead_lots_detected > slow.loc[baseline].median_lead_lots_detected
                       for baseline in ["shewhart_budget", "ewma_budget"])
            rows.append({"seed": seed, "candidate": candidate,
                         "beats_both_spc_recall_and_lead": bool(wins),
                         "within_test_false_alarm_budget": bool(pooled.loc[candidate].false_alarms_per_100_normal_lots <= 1),
                         "beats_constant_brier": bool(pooled.loc[candidate].brier < pooled.loc[candidate].constant_brier),
                         "control_recall_lower": bool(null_slow.loc[candidate].excursion_recall < c.excursion_recall)})
    if not rows:
        raise ValueError("No seed results found")
    frame = pd.DataFrame(rows)
    gates = list(frame.columns[2:])
    supported = {candidate: bool(group[gates].to_numpy().all())
                 for candidate, group in frame.groupby("candidate")}
    return {"exploratory_gate_supported": supported, "checks": rows,
            "note": "Strict exploratory gate, not statistical significance or real-fab validation. Control check means lower recall, not a formal chance test."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--default", type=Path, default=Path("results/default"))
    parser.add_argument("--control", type=Path, default=Path("results/no_precursor"))
    parser.add_argument("--output", type=Path, default=Path("results/assessment.json"))
    args = parser.parse_args()
    result = assess(args.default, args.control)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
