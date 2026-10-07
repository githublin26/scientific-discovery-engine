import csv
from pathlib import Path

from .provenance import snapshot_provenance


def retrieve_record(snapshot, candidate_id):
    if not candidate_id or not candidate_id.strip():
        raise ValueError("A nonempty exact MaterialId is required")
    provenance = snapshot_provenance(snapshot)
    found = None
    with Path(snapshot).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames or []
        if not {"MaterialId", "Composition"}.issubset(headers):
            raise ValueError("Missing MaterialId or Composition column")
        if len(headers) != len(set(headers)):
            raise ValueError("Duplicate column names")
        for record_number, row in enumerate(reader, 1):
            if row["MaterialId"] != candidate_id:
                continue
            if found is not None:
                raise ValueError("Ambiguous duplicate MaterialId")
            if None in row or any(value is None for value in row.values()):
                raise ValueError("Malformed source record")
            if not row["Composition"].strip():
                raise ValueError("Empty source composition")
            found = row
            provenance["source_identifier"] = candidate_id
            provenance["csv_record_number"] = record_number
    if found is None:
        return None, provenance
    return found, provenance
