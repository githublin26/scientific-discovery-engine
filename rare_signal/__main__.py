import argparse
import json

from .evaluate import run
from .retrieve import retrieve


def main():
    parser = argparse.ArgumentParser(description="Computational evidence baseline")
    commands = parser.add_subparsers(dest="command", required=True)
    download = commands.add_parser("retrieve")
    download.add_argument("--output", required=True)
    benchmark = commands.add_parser("run")
    benchmark.add_argument("--input", required=True)
    benchmark.add_argument("--out", required=True)
    args = parser.parse_args()
    try:
        result = retrieve(args.output) if args.command == "retrieve" else run(args.input, args.out)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Error: {error}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

