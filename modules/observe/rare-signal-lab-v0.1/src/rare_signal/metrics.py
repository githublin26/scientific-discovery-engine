import numpy as np
from sklearn.metrics import brier_score_loss, log_loss, precision_score
from .data import HORIZON


def reliability(y, p, bins=10):
    rows = []
    for i in range(bins):
        mask = (p >= i/bins) & ((p < (i+1)/bins) if i < bins-1 else (p <= 1))
        rows.append({"lower": i/bins, "upper": (i+1)/bins, "count": int(mask.sum()),
                     "mean_probability": float(p[mask].mean()) if mask.any() else None,
                     "event_fraction": float(y[mask].mean()) if mask.any() else None})
    return rows


def evaluate(frame, alert, probability=None, reference=None):
    use = frame.eligible.to_numpy()
    y = frame.target.to_numpy()[use]
    a = np.asarray(alert)[use]
    events = []
    for run, group in frame.groupby("run_id", sort=False):
        onset = int(group.onset.iloc[0])
        if onset < 0:
            continue
        ix = np.flatnonzero((frame.run_id.to_numpy() == run) &
                            (frame.lot_index.to_numpy() >= onset-HORIZON) &
                            (frame.lot_index.to_numpy() < onset))
        hits = ix[np.asarray(alert)[ix]]
        lead = int(onset-frame.lot_index.iloc[hits[0]]) if len(hits) else None
        # Reference includes onset, to distinguish a contemporaneous SPC alarm.
        ref_ix = np.flatnonzero((frame.run_id.to_numpy() == run) &
                               (frame.lot_index.to_numpy() >= onset-HORIZON) &
                               (frame.lot_index.to_numpy() <= onset))
        ref_hits = ref_ix[np.asarray(reference)[ref_ix]] if reference is not None else []
        ref_lead = int(onset-frame.lot_index.iloc[ref_hits[0]]) if len(ref_hits) else None
        events.append({"run_id": int(run), "scenario": group.scenario.iloc[0],
                       "lead_lots": lead, "spc_lead_lots": ref_lead,
                       "paired_gain_lots": lead-ref_lead if lead is not None and ref_lead is not None else None})
    leads = [e["lead_lots"] for e in events if e["lead_lots"] is not None]
    gains = [e["paired_gain_lots"] for e in events if e["paired_gain_lots"] is not None]
    result = {"eligible_lots": int(use.sum()), "positive_lots": int(y.sum()),
              "precision": float(precision_score(y, a, zero_division=0)),
              "lot_recall": float(np.sum(a & (y == 1))/y.sum()) if y.sum() else 0.,
              "false_alert_lots": int(np.sum(a & (y == 0))),
              "false_alarms_per_100_normal_lots": float(100*np.mean(a[y == 0])),
              "excursions": len(events), "early_detected_excursions": len(leads),
              "excursion_recall": len(leads)/len(events) if events else None,
              "median_lead_lots_detected": float(np.median(leads)) if leads else None,
              "paired_events": len(gains),
              "median_gain_vs_spc_lots_paired": float(np.median(gains)) if gains else None}
    if probability is not None:
        p = np.asarray(probability)[use]
        bins = reliability(y, p)
        result.update(brier=float(brier_score_loss(y, p)),
                      log_loss=float(log_loss(y, p, labels=[0, 1])),
                      ece=float(sum(b["count"]*abs(b["mean_probability"]-b["event_fraction"])
                                    for b in bins if b["count"])/len(y)))
    return result, events
