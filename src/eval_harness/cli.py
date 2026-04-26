from __future__ import annotations

import argparse
import json
from pathlib import Path

from .runner import evaluate_batch, evaluate_submission, write_json_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="eval-harness",
        description="Run coding submissions against pytest-based problem suites.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    run_parser = subcommands.add_parser("run", help="evaluate a single submission")
    run_parser.add_argument("--problem", required=True, help="problem directory")
    run_parser.add_argument("--submission", required=True, help="candidate Python file")
    run_parser.add_argument("--timeout", type=int, default=10, help="per-run timeout in seconds")
    run_parser.add_argument("--out", help="optional JSON report path")

    batch_parser = subcommands.add_parser("batch", help="evaluate jobs from a manifest")
    batch_parser.add_argument("--manifest", required=True, help="batch manifest JSON")
    batch_parser.add_argument("--timeout", type=int, default=10, help="default per-run timeout")
    batch_parser.add_argument("--out", help="optional JSON report path")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "run":
        result = evaluate_submission(args.problem, args.submission, timeout_seconds=args.timeout).to_dict()
        payload: dict = result
    else:
        payload = evaluate_batch(args.manifest, timeout_seconds=args.timeout)

    if args.out:
        write_json_report(payload, args.out)

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if _is_success(payload) else 1


def _is_success(payload: dict) -> bool:
    if "status" in payload:
        return payload["status"] == "passed"
    return payload.get("failed") == 0


if __name__ == "__main__":
    raise SystemExit(main())

