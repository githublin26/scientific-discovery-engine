import json
import platform
from datetime import datetime, timezone
from pathlib import Path

from rare_signal.provenance import SOURCE, digest


def snapshot_provenance(path):
    path = Path(path)
    metadata = {
        "source_url": None,
        "retrieved_at": None,
        "input_hash": digest(path),
        "snapshot_file": str(path),
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "software_version": "materials-discovery-v0.1",
        "python_version": platform.python_version(),
        "source_status": "UNKNOWN_USER_PROVIDED",
    }
    sidecar = path.with_suffix(".provenance.json")
    if sidecar.exists():
        original = json.loads(sidecar.read_text(encoding="utf-8"))
        if original.get("sha256") != metadata["input_hash"]:
            raise ValueError("Snapshot checksum mismatch")
        if original.get("source") != SOURCE or not original.get("recorded_at"):
            raise ValueError("Retrieval manifest is not for the supported official source")
        metadata.update(
            source_url=SOURCE,
            retrieved_at=original["recorded_at"],
            source_status="OFFICIAL_URL_IN_LOCAL_RETRIEVAL_MANIFEST",
        )
    return metadata


def evidence(value, raw_value, column, provenance, value_type="retrieved", notes=None):
    return {
        "value": value,
        "raw_value": raw_value,
        "value_type": value_type,
        "source_column": column,
        "source_id": provenance["source_identifier"],
        "source_url": provenance["source_url"],
        "retrieved_at": provenance["retrieved_at"],
        "input_hash": provenance["input_hash"],
        "software_version": provenance["software_version"],
        "notes": notes,
    }
