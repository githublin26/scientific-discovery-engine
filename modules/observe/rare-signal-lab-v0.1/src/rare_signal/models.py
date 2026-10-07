import numpy as np
from sklearn.ensemble import IsolationForest, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from .data import SENSORS, features


class Baselines:
    def fit(self, train, seed):
        # Phase I: first 50 lots of each training run precede every event/ramp.
        phase1 = train[train.lot_index < 50][SENSORS]
        self.mean = phase1.mean().to_numpy()
        self.std = phase1.std(ddof=1).to_numpy()
        use = train.eligible.to_numpy()
        x, y = features(train)[use], train.target.to_numpy()[use]
        if len(np.unique(y)) < 2:
            raise ValueError("Training split needs both classes; increase --runs")
        self.iforest = IsolationForest(n_estimators=100, random_state=seed, n_jobs=1)
        self.iforest.fit(x[y == 0])
        self.gb = GradientBoostingClassifier(n_estimators=70, max_depth=2,
                                            random_state=seed).fit(x, y)
        self.logistic = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(x, y)
        return self

    def scores(self, frame):
        z = (frame[SENSORS].to_numpy()-self.mean)/self.std
        ewma = np.zeros_like(z)
        for _, indices in frame.groupby("run_id", sort=False).indices.items():
            state = np.zeros(len(SENSORS))
            for i in indices:
                state = .2*z[i]+.8*state
                ewma[i] = state
        x = features(frame)
        return {
            "shewhart": np.abs(z).max(axis=1),
            "ewma": np.abs(ewma).max(axis=1)/np.sqrt(.2/(2-.2)),
            "isolation_forest": -self.iforest.score_samples(x),
            "gradient_boosting": self.gb.decision_function(x),
            "logistic": self.logistic.decision_function(x),
        }


def calibrate(scores, target):
    """Sigmoid calibration on a disjoint set; score is not itself a probability."""
    if len(np.unique(target)) < 2:
        raise ValueError("Calibration split needs both classes; increase --runs")
    return LogisticRegression(C=100., max_iter=1000).fit(np.asarray(scores).reshape(-1, 1), target)


def threshold(scores, y, false_alarm_budget=1.0):
    """Choose highest row recall under validation false-positive/normal-lot budget."""
    if not np.any(y == 0):
        raise ValueError("Validation split needs negative lots")
    order = np.argsort(-scores, kind="stable")
    ordered = scores[order]
    positives = np.cumsum(y[order] == 1)
    negatives = np.cumsum(y[order] == 0)
    ends = np.r_[np.flatnonzero(ordered[:-1] != ordered[1:]), len(ordered)-1]
    feasible = [(0., 0., np.nextafter(np.max(scores), np.inf))]
    for i in ends:
        rate = 100*negatives[i]/np.sum(y == 0)
        if rate <= false_alarm_budget:
            recall = positives[i]/np.sum(y == 1) if np.any(y == 1) else 0.
            feasible.append((recall, -rate, ordered[i]))
    return max(feasible)[2]
