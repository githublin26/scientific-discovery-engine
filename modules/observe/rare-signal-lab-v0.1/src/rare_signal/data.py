"""Independent synthetic tool runs; labels and event metadata are never features."""
import numpy as np
import pandas as pd

SENSORS = ["oxygen_ppm", "water_ppm", "particle_01um", "particle_02um",
           "pressure_drop", "assay", "temperature"]
MEAN = np.array([10., 5., 100., 40., 20., 99., 300.])
SCALE = np.array([1., .5, 10., 4., 2., .1, 2.])
HORIZON = 12


def generate(seed=42, runs=120, signal_strength=1.0):
    if runs < 1 or signal_strength < 0:
        raise ValueError("runs must be positive and signal_strength nonnegative")
    rng = np.random.default_rng(seed)
    frames = []
    for run in range(runs):
        n = 120
        scenario = rng.choice(["noise", "slow", "obvious"], p=[.7, .2, .1])
        onset = int(rng.integers(75, 106)) if scenario != "noise" else -1
        # Shared disturbances, serial correlation, and independent sensor noise.
        z = rng.normal(size=(n, 7)) * .85
        shared = rng.normal(size=n) * .25
        for t in range(1, n):
            z[t] += .15 * z[t - 1]
        z += shared[:, None]
        if scenario == "slow":
            ramp = np.linspace(.2, 1.8, HORIZON) * signal_strength
            z[onset-HORIZON:onset, :5] += ramp[:, None]
        if onset >= 0:
            z[onset:, 0] += 5  # externally scheduled event, not defined by SPC
        values = MEAN + z * SCALE
        f = pd.DataFrame(values, columns=SENSORS)
        f["run_id"] = run
        f["lot_id"] = [f"R{run:04d}-L{t:03d}" for t in range(n)]
        f["lot_index"] = np.arange(n)
        f["timestamp"] = pd.date_range("2025-01-01", periods=n, freq="h")
        f["tool_id"] = f"tool_{run % 3}"
        f["batch_age"] = np.arange(n)
        f["scenario"] = scenario
        f["onset"] = onset
        f["excursion_label"] = ((f.lot_index >= onset) & (onset >= 0)).astype(int)
        f["target"] = ((onset-f.lot_index >= 1) & (onset-f.lot_index <= HORIZON)).astype(int)
        f["eligible"] = (f.lot_index >= 10) & ((onset < 0) | (f.lot_index < onset))
        frames.append(f)
    return pd.concat(frames, ignore_index=True)


def features(frame):
    """Current measurements and trailing mean/change, reset at run boundaries."""
    current = frame[SENSORS]
    trailing = frame.groupby("run_id", sort=False)[SENSORS].transform(
        lambda s: s.rolling(5, min_periods=1).mean())
    lag = frame.groupby("run_id", sort=False)[SENSORS].shift(5)
    change = (current-lag).fillna(0)
    return np.hstack([current, trailing, change])
