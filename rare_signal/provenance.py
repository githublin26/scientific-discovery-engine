import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


SOURCE = "https://storage.googleapis.com/gdm_materials_discovery/gnome_data/stable_materials_summary.csv"


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def manifest(path):
    return {
        "input_path": str(Path(path).resolve()),
        "sha256": digest(path),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "source": "user-provided; not authenticated by filename",
        "energy_unit": "eV/atom",
        "implementation": "v0.1",
    }

