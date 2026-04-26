# AI Code Evaluation Harness

A small, practical harness for evaluating coding-agent or student submissions against problem-specific pytest suites. It is designed to show clean challenge design, reliable test execution, and machine-readable reports.

## Why This Project Exists

AI coding evaluations are only useful when the harness is clear, repeatable, and hard to accidentally game. This project demonstrates the building blocks:

- challenge folders with starter code, reference solutions, and tests
- isolated execution in a temporary workspace
- JSON reports with status, timing, stdout, stderr, and parsed pytest counts
- a batch mode for running multiple submissions at once
- sample problems across arrays, file/JSON processing, and graphs

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Run one submission:

```bash
eval-harness run \
  --problem problems/two_sum \
  --submission submissions/two_sum_buggy.py \
  --out reports/two_sum_buggy.json
```

Run a batch:

```bash
eval-harness batch --manifest examples/batch_manifest.json --out reports/batch.json
```

## Repository Layout

```text
.
├── problems/
│   ├── two_sum/
│   ├── normalize_event/
│   └── dependency_order/
├── submissions/
├── src/eval_harness/
├── tests/
└── examples/
```

Each problem contains:

- `README.md`: problem statement and constraints
- `starter.py`: candidate-facing starter code
- `solution.py`: reference implementation
- `tests/`: public pytest tests used by the harness

## JSON Report Shape

```json
{
  "problem": "two_sum",
  "submission": "submissions/two_sum_buggy.py",
  "status": "failed",
  "exit_code": 1,
  "duration_seconds": 0.42,
  "pytest": {
    "passed": 3,
    "failed": 1,
    "errors": 0,
    "skipped": 0,
    "summary": "1 failed, 3 passed in 0.04s"
  },
  "stdout": "...",
  "stderr": ""
}
```

## Design Choices

- The submitted file is copied to `solution.py` inside a temporary directory, so tests can use the same import path for every candidate.
- Tests are copied into the same temporary workspace to keep runs isolated from local files.
- The harness does not require a database or service. A CI runner can execute it with plain Python and pytest.
- Reports are structured for downstream dashboards, manual review, or model-comparison scripts.

## Commands

```bash
eval-harness run --problem problems/dependency_order --submission problems/dependency_order/solution.py
eval-harness batch --manifest examples/batch_manifest.json
pytest
```

## What This Shows

This repo is meant to signal readiness for work involving SWE-style evaluations, coding-agent benchmark infrastructure, test harness design, and careful failure reporting.

