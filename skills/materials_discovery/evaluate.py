import math

from .provenance import evidence


ENERGIES = (
    "Formation Energy Per Atom",
    "Decomposition Energy Per Atom",
    "Decomposition Energy Per Atom All",
    "Decomposition Energy Per Atom Relative",
    "Decomposition Energy Per Atom MP",
    "Decomposition Energy Per Atom MP OQMD",
)
STRUCTURE = ("NSites", "Space Group", "Space Group Number", "Crystal System")


def numeric(raw):
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def evaluate_record(row, provenance, threshold=0.001):
    if not math.isfinite(threshold) or threshold < 0:
        raise ValueError("Threshold must be finite and nonnegative")
    retrieved, unknown = {}, []
    for column in ("Composition", "Reduced Formula", *ENERGIES, *STRUCTURE):
        raw = row.get(column)
        value = numeric(raw) if column in ENERGIES else raw
        missing = value is None or (isinstance(value, str) and not value.strip())
        if missing:
            unknown.append(column)
        entry = evidence(
            None if missing else value, raw, column, provenance,
            "unknown" if missing else "retrieved",
            "Absent, empty or invalid; no value inferred." if missing else None,
        )
        if column in ENERGIES:
            entry["unit"] = "eV/atom"
        retrieved[column] = entry
    metric = retrieved["Decomposition Energy Per Atom All"]["value"]
    derived = {}
    if metric is not None:
        converted = evidence(metric * 1000, None, "Decomposition Energy Per Atom All", provenance, "derived")
        converted.update(
            unit="meV/atom", calculation_method="source eV/atom * 1000",
            assumptions=["Unit conversion only; original reference hull is unchanged."],
        )
        derived["decomposition_all_mev_per_atom"] = converted
        decision = evidence(metric <= threshold, None, "Decomposition Energy Per Atom All", provenance, "derived")
        decision.update(
            calculation_method="published decomposition_all <= project screening tolerance",
            threshold_ev_per_atom=threshold,
            assumptions=["Project tolerance, not synthesis feasibility or independent hull validation."],
        )
        derived["within_screening_tolerance"] = decision
    unknown.extend(["atomic_coordinates", "independent_hull_energy", "experimental_synthesis", "calibrated_confidence"])
    return {
        "status": "RECORD_RETRIEVED",
        "candidate_id": row["MaterialId"],
        "formula": row.get("Reduced Formula") or row["Composition"],
        "raw_record": row,
        "retrieved_values": retrieved,
        "derived_values": derived,
        "interpretation": {
            "value_type": "inferred",
            "value": "Published computational evidence only; no independent calculation or synthesis claim.",
        },
        "unknown_fields": unknown,
        "provenance": provenance,
        "limitations": [
            "CSV metadata is not a retrieved CIF structure.",
            "Distinct decomposition reference hulls are not interchangeable.",
            "Formation energy alone does not establish stability.",
            "Local manifest plus checksum provides traceability, not cryptographic source authentication.",
            "This lookup is not blinded prediction; reference comparison tests mapping only.",
        ],
    }


def compare_reference(result, reference):
    if result["status"] != "RECORD_RETRIEVED":
        return {"status": "UNKNOWN", "reason": "No record"}
    if reference["candidate_id"] != result["candidate_id"]:
        raise ValueError("Reference candidate mismatch")
    if reference["input_hash"] != result["provenance"]["input_hash"]:
        raise ValueError("Reference snapshot mismatch; do not silently update frozen reference")
    checks = {}
    for column, expected in reference["retrieved_values"].items():
        if column not in result["retrieved_values"]:
            raise ValueError(f"Unsupported reference field: {column}")
        actual = result["retrieved_values"][column]["value"]
        checks[column] = (
            actual is not None and math.isclose(actual, expected, rel_tol=0, abs_tol=1e-10)
            if isinstance(expected, (int, float))
            else actual == expected
        )
    if not checks:
        raise ValueError("Empty reference checks")
    return {
        "status": "PASS_REFERENCE_MAPPING" if all(checks.values()) else "FAIL_REFERENCE_MAPPING",
        "checks": checks,
        "scope": "Pinned public-record regression only, not independent stability validation or predictive skill.",
    }
