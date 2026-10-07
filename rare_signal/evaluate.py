import csv
import math
from pathlib import Path

from .provenance import digest, manifest, write_json


TARGET = "Decomposition Energy Per Atom All"
FEATURE = "Formation Energy Per Atom"
TOLERANCE = 0.001


def finite(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("Non-finite energy")
    return number


def load(path):
    candidates, references, seen = [], {}, set()
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"MaterialId", "Composition", FEATURE, TARGET}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"Missing columns: {sorted(required - set(reader.fieldnames or []))}")
        for row_number, row in enumerate(reader, 2):
            identity = row["MaterialId"].strip()
            if not identity or identity in seen or not row["Composition"].strip():
                raise ValueError(f"Invalid identity/composition at row {row_number}")
            seen.add(identity)
            candidates.append({
                "id": identity, "composition": row["Composition"],
                "formation_energy": finite(row[FEATURE]), "source_row": row_number,
            })
            references[identity] = finite(row[TARGET])
    if not candidates:
        raise ValueError("Empty dataset")
    return candidates, references


def rank(candidates):
    allowed = {"id", "composition", "formation_energy", "source_row"}
    if any(set(candidate) != allowed for candidate in candidates):
        raise ValueError("Unexpected feature; possible label leakage")
    return [
        {**candidate, "score": -candidate["formation_energy"], "uncertainty": "uncalibrated"}
        for candidate in sorted(candidates, key=lambda item: (item["formation_energy"], item["id"]))
    ]


def run(path, output):
    candidates, references = load(path)
    predictions = rank(candidates)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    write_json(output / "candidates.json", candidates)
    write_json(output / "predictions.json", predictions)
    prediction_hash = digest(output / "predictions.json")
    write_json(output / "references.json", references)
    stable = {identity for identity, energy in references.items() if energy <= TOLERANCE}
    count = len(predictions)
    top_count = min(3, count)
    report = {
        "status": "WORKFLOW_COMPLETED_NOT_SCIENTIFIC_PASS",
        "n": count,
        "target": TARGET,
        "threshold_ev_per_atom": TOLERANCE,
        "precision_at_k": sum(item["id"] in stable for item in predictions[:top_count]) / top_count,
        "k": top_count,
        "stable_prevalence": len(stable) / count,
        "single_class": len(stable) in (0, count),
        "prediction_sha256": prediction_hash,
        "limitations": [
            "Formation-energy baseline is not a stability predictor.",
            "No independent hull or DFT calculation.",
            "Selected stable datasets cannot demonstrate general discrimination.",
            "No calibrated uncertainty or wet-lab evidence.",
        ],
        "next_validation": [
            {"id": item["id"], "action": "Check structure, compatible reference hull and independent literature; human review required."}
            for item in predictions[:top_count]
        ],
    }
    write_json(output / "metrics.json", report)
    metadata = manifest(path)
    sidecar = Path(path).with_suffix(".provenance.json")
    if sidecar.exists():
        import json
        source_metadata = json.loads(sidecar.read_text(encoding="utf-8"))
        if source_metadata.get("sha256") != metadata["sha256"]:
            raise ValueError("Snapshot checksum differs from retrieval manifest")
        metadata["retrieval"] = source_metadata
    write_json(output / "provenance.json", metadata)
    return report

