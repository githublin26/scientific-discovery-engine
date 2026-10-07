import json
import tempfile
import unittest
from pathlib import Path

from rare_signal.provenance import SOURCE, digest
from skills.materials_discovery.evaluate import compare_reference, evaluate_record
from skills.materials_discovery.retrieve import retrieve_record


FIXTURE = Path(__file__).parent / "fixtures" / "materials.csv"


class MaterialsDiscoveryTests(unittest.TestCase):
    def test_retrieved_derived_and_unknown_are_separated(self):
        row, provenance = retrieve_record(FIXTURE, "synthetic-b")
        result = evaluate_record(row, provenance)
        energy = result["retrieved_values"]["Decomposition Energy Per Atom All"]
        self.assertEqual(energy["raw_value"], "0.2")
        self.assertEqual(energy["value_type"], "retrieved")
        self.assertEqual(result["derived_values"]["decomposition_all_mev_per_atom"]["value"], 200)
        self.assertFalse(result["derived_values"]["within_screening_tolerance"]["value"])
        self.assertEqual(result["retrieved_values"]["Space Group"]["value_type"], "unknown")
        self.assertIsNone(provenance["retrieved_at"])
        self.assertIsNone(provenance["source_url"])

    def test_not_found(self):
        row, _ = retrieve_record(FIXTURE, "absent")
        self.assertIsNone(row)

    def test_invalid_energy_is_unknown(self):
        row, provenance = retrieve_record(FIXTURE, "synthetic-a")
        for raw in ("nan", "inf", "", "garbage"):
            with self.subTest(raw=raw):
                row["Decomposition Energy Per Atom All"] = raw
                result = evaluate_record(row, provenance)
                self.assertFalse(result["derived_values"])
                self.assertIsNone(result["retrieved_values"]["Decomposition Energy Per Atom All"]["value"])

    def test_threshold_boundary_and_invalid_threshold(self):
        row, provenance = retrieve_record(FIXTURE, "synthetic-a")
        row["Decomposition Energy Per Atom All"] = "0.001"
        self.assertTrue(evaluate_record(row, provenance)["derived_values"]["within_screening_tolerance"]["value"])
        for threshold in (-1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                evaluate_record(row, provenance, threshold)

    def test_duplicate_id_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "duplicate.csv"
            path.write_text("MaterialId,Composition\nx,Li\nx,Li\n")
            with self.assertRaises(ValueError):
                retrieve_record(path, "x")

    def test_checksum_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "snapshot.csv"
            path.write_bytes(FIXTURE.read_bytes())
            path.with_suffix(".provenance.json").write_text(json.dumps({
                "source": SOURCE, "sha256": "wrong", "recorded_at": "2026-10-07T00:00:00Z",
            }))
            with self.assertRaises(ValueError):
                retrieve_record(path, "synthetic-a")

    def test_manifest_and_reference_checks(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "snapshot.csv"
            path.write_bytes(FIXTURE.read_bytes())
            path.with_suffix(".provenance.json").write_text(json.dumps({
                "source": SOURCE, "sha256": digest(path), "recorded_at": "2026-10-07T00:00:00Z",
            }))
            row, provenance = retrieve_record(path, "synthetic-a")
            self.assertEqual(provenance["source_url"], SOURCE)
            result = evaluate_record(row, provenance)
            reference = {"candidate_id": "synthetic-a", "input_hash": digest(path),
                         "retrieved_values": {"Formation Energy Per Atom": -2}}
            self.assertEqual(compare_reference(result, reference)["status"], "PASS_REFERENCE_MAPPING")
            reference["retrieved_values"]["Formation Energy Per Atom"] = 2
            self.assertEqual(compare_reference(result, reference)["status"], "FAIL_REFERENCE_MAPPING")
            reference["input_hash"] = "wrong"
            with self.assertRaises(ValueError):
                compare_reference(result, reference)


if __name__ == "__main__":
    unittest.main()
