import os
import tempfile
from pathlib import Path
from urllib.request import urlopen

from .provenance import SOURCE, manifest, write_json


def retrieve(output):
    output = Path(output)
    if output.exists():
        raise ValueError("Refusing to overwrite an existing snapshot")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            with urlopen(SOURCE, timeout=60) as response:
                while chunk := response.read(1024 * 1024):
                    stream.write(chunk)
        except BaseException:
            stream.close()
            temporary.unlink(missing_ok=True)
            raise
    os.replace(temporary, output)
    metadata = manifest(output)
    metadata["source"] = SOURCE
    write_json(output.with_suffix(".provenance.json"), metadata)
    return metadata

