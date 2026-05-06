# AI Code Evaluation Harness

I made this project to understand how coding websites and AI coding benchmarks check whether a submitted solution is correct.

The basic idea is simple:

1. Pick a programming problem.
2. Give the tool a submitted Python file.
3. Run that file against tests.
4. Print a report that says what passed and what failed.

This is a small version of the kind of system used by coding challenge sites, class autograders, or AI code evaluation tools.

## What I Built

This repo has three sample problems:

- `two_sum`
- `normalize_event`
- `dependency_order`

Each problem has:

- a `README.md` explaining the problem
- `starter.py` with unfinished starter code
- `solution.py` with a correct solution
- a `tests/` folder with pytest tests

The evaluator code is in `src/eval_harness/`.

## How It Works

When I run the evaluator, it:

1. Creates a temporary folder.
2. Copies the submitted file into that folder as `solution.py`.
3. Copies the problem tests into that folder.
4. Runs `pytest`.
5. Saves the result as a report.

I copied every submission as `solution.py` because the tests can then always import the same file name. That keeps the testing process simpler.

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

Run a batch of submissions:

```bash
eval-harness batch --manifest examples/batch_manifest.json --out reports/batch.json
```

The batch manifest can also include points for each job:

```json
{
  "id": "dependency-order-reference",
  "problem": "../problems/dependency_order",
  "submission": "../problems/dependency_order/solution.py",
  "points": 5
}
```

That makes the output more like a small autograder because the final report includes `earned_points`, `possible_points`, and `score_percent`.

## Example Report

The report is written in JSON. JSON is just a structured text format that programs can read easily.

```json
{
  "problem": "two_sum",
  "status": "failed",
  "pytest": {
    "passed": 3,
    "failed": 1
  }
}
```

This means the submission was tested on `two_sum`, but one test failed.

For batch runs, the report also shows the score:

```json
{
  "suite": "sample-agent-submissions",
  "passed": 2,
  "failed": 1,
  "earned_points": 8,
  "possible_points": 10,
  "score_percent": 80.0
}
```

This is useful when different problems are worth different amounts.

## Why I Made This

I wanted a project that connects to testing, coding challenges, and AI code evaluation. It helped me practice:

- writing tests
- building a command-line tool
- using temporary folders
- running another command from Python
- creating simple JSON reports
- adding points-based scoring
- organizing a project so someone else can understand it

## Running Tests

```bash
pytest
```
