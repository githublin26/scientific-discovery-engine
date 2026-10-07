import csv
import json
import tempfile
import unittest
from pathlib import Path

from rare_signal.evaluate import FEATURE, TARGET, load, rank, run


FIXTURE = Path(__file__).parent / "fixtures" / "materials.csv"


class WorkflowTests(unittest.TestCase):
    def test_labels_are_hidden(self):
        candidates, references = load(FIXTURE)
        self.assertTrue(references)
        self.assertTrue(all(TARGET not in candidate for candidate in candidates))
        contaminated = [dict(candidates[0], **{TARGET: 0})]
        with self.assertRaises(ValueError):
            rank(contaminated)

    def test_deterministic_ranking(self):
        candidates, _ = load(FIXTURE)
        self.assertEqual(rank(candidates), rank(list(reversed(candidates))))
        self.assertEqual(rank(candidates)[0]["id"], "synthetic-c")

    def test_run_metrics_and_trace(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "run"
            report = run(FIXTURE, output)
            self.assertEqual(report["precision_at_k"], 2 / 3)
            self.assertFalse(report["single_class"])
            self.assertEqual(report["stable_prevalence"], 0.5)
            self.assertEqual(len(report["prediction_sha256"]), 64)
            metadata = json.loads((output / "provenance.json").read_text())
            self.assertEqual(len(metadata["sha256"]), 64)
            with self.assertRaises(FileExistsError):
                run(FIXTURE, output)

    def test_invalid_data(self):
        for energy in ("nan", "inf", ""):
            with self.subTest(energy=energy), tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / "bad.csv"
                with path.open("w", newline="") as stream:
                    writer = csv.writer(stream)
                    writer.writerow(["MaterialId", "Composition", FEATURE, TARGET])
                    writer.writerow(["id", "Li", energy, "0"])
                with self.assertRaises(ValueError):
                    load(path)

    def test_missing_columns(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "bad.csv"
            path.write_text("MaterialId\nid\n")
            with self.assertRaises(ValueError):
                load(path)


if __name__ == "__main__":
    unittest.main()

