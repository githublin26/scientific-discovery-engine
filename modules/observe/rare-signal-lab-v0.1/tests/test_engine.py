import numpy as np
import pandas as pd
import pytest
import hashlib
import json
from rare_signal.data import generate, features, SENSORS
from rare_signal.models import threshold, Baselines
from rare_signal.metrics import evaluate, reliability
from rare_signal.experiment import run


def test_seed_and_labels():
    a = generate(42, 50)
    pd.testing.assert_frame_equal(a, generate(42, 50))
    assert set(a.scenario) == {"slow", "obvious", "noise"}
    assert ((a.onset-a.lot_index).between(1, 12) == a.target.astype(bool)).all()
    assert not a.loc[a.eligible, "excursion_label"].any()
    assert not a.loc[a.lot_index < 50, "target"].any()


def test_features_are_causal_and_metadata_free():
    a = generate(3, 4)
    before = features(a)
    b = a.copy()
    b.loc[b.lot_index >= 60, SENSORS] = 1e9
    b["target"], b["scenario"], b["onset"] = 1, "fake", 0
    np.testing.assert_array_equal(before[a.lot_index < 60], features(b)[a.lot_index < 60])
    assert features(a).shape[1] == 21
    # Features reset at run boundaries.
    np.testing.assert_array_equal(features(a)[120], features(a.iloc[120:240])[0])


def test_threshold_budget_and_no_alert_solution():
    score = np.array([.9, .8, .7, .6])
    y = np.array([0, 1, 0, 1])
    t = threshold(score, y, 0)
    assert not np.any(score >= t)
    t = threshold(score, y, 50)
    assert 100*np.mean((score >= t)[y == 0]) <= 50


def test_lead_and_denominators():
    f = pd.DataFrame({"run_id": [0]*15+[1]*15, "lot_index": list(range(15))*2,
                      "onset": [14]*15+[-1]*15, "scenario": ["slow"]*15+["noise"]*15})
    f["eligible"] = (f.lot_index >= 2) & ((f.onset < 0) | (f.lot_index < f.onset))
    f["target"] = ((f.onset-f.lot_index).between(1, 12)).astype(int)
    a = np.zeros(30, bool); a[10] = True; a[20] = True
    ref = np.zeros(30, bool); ref[14] = True
    m, events = evaluate(f, a, reference=ref)
    assert m["excursion_recall"] == 1
    assert m["precision"] == .5
    assert m["false_alarms_per_100_normal_lots"] == pytest.approx(100/13)
    assert events[0]["lead_lots"] == events[0]["paired_gain_lots"] == 4


def test_calibration_edges():
    bins = reliability(np.array([0, 1]), np.array([0., 1.]))
    assert sum(b["count"] for b in bins) == 2


def test_negative_control_only_removes_ramp():
    a, b = generate(42, 40, 1), generate(42, 40, 0)
    outside = ~((a.scenario == "slow") & (a.target == 1))
    pd.testing.assert_frame_equal(a.loc[outside], b.loc[outside])
    assert not np.array_equal(a[SENSORS].to_numpy(), b[SENSORS].to_numpy())
    pd.testing.assert_series_equal(a.target, b.target)


def test_threshold_matches_brute_force_with_ties():
    score = np.array([.9, .9, .6, .5, .5, .1])
    y = np.array([1, 0, 1, 0, 1, 0])
    candidates = np.r_[np.unique(score), np.nextafter(score.max(), np.inf)]
    expected = max((np.mean((score >= t)[y == 1]), -100*np.mean((score >= t)[y == 0]), t)
                   for t in candidates if 100*np.mean((score >= t)[y == 0]) <= 34)[2]
    assert threshold(score, y, 34) == expected


def test_spc_is_train_only():
    train = generate(42, 40)
    model = Baselines().fit(train, 42)
    mean = model.mean.copy()
    test = generate(43, 5)
    model.scores(test)
    np.testing.assert_array_equal(mean, model.mean)
    assert model.scores(test)["shewhart"].shape == (600,)


def test_reproducible_end_to_end(tmp_path):
    a = run(42, 40, 1., 1., tmp_path/"a")
    b = run(42, 40, 1., 1., tmp_path/"b")
    pd.testing.assert_frame_equal(a, b)
    assert len(a) == 7
    assert (tmp_path/"a"/"manifest.json").exists()
    p = pd.read_csv(tmp_path/"a"/"predictions.csv")
    assert p.probability.between(0, 1).all()
    assert np.isfinite(a.brier).all()
    manifest = json.loads((tmp_path/"a"/"manifest.json").read_text())
    for split, expected in manifest["sha256"].items():
        assert hashlib.sha256((tmp_path/"a"/f"{split}.csv").read_bytes()).hexdigest() == expected
    assert (tmp_path/"a"/"reliability.csv").exists()
