import argparse
import json
from pathlib import Path

from rare_signal.provenance import write_json
from .evaluate import compare_reference, evaluate_record
from .retrieve import retrieve_record


def main():
    parser = argparse.ArgumentParser(description="Trace one exact GNoME MaterialId")
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--threshold", type=float, default=0.001)
    parser.add_argument("--reference")
    args = parser.parse_args()
    try:
        output = Path(args.out)
        if output.exists():
            raise ValueError("Refusing to overwrite an existing evidence artifact")
        row, provenance = retrieve_record(args.snapshot, args.candidate_id)
        result = (
            evaluate_record(row, provenance, args.threshold) if row is not None else
            {"status": "UNKNOWN", "candidate_id": args.candidate_id, "reason": "MaterialId not found in snapshot", "provenance": provenance}
        )
        if args.reference:
            reference = json.loads(Path(args.reference).read_text(encoding="utf-8"))
            result["validation"] = compare_reference(result, reference)
        output.parent.mkdir(parents=True, exist_ok=True)
        write_json(output, result)
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, f"Error: {error}\n")
    print(json.dumps({"status": result["status"], "output": str(output), "validation": result.get("validation")}, indent=2))
    if result.get("validation", {}).get("status") == "FAIL_REFERENCE_MAPPING":
        parser.exit(1)


if __name__ == "__main__":
    main()
