# ai-code-eval-harness

**Name:** Saina Kakkar

## Design and Implementation

I made this project to understand how coding websites and AI coding
benchmarks check whether a submitted solution is correct. The basic idea is
simple: pick a programming problem, give the tool a submitted Python file,
run that file against tests, and print a report that says what passed and
what failed. It is a small version of the kind of system used by coding
challenge sites, class autograders, or AI code evaluation tools.

```
submission.py ──► temp folder ──► copy in problem tests ──► pytest ──► JSON report
                  (as solution.py)
```

When the evaluator runs, it creates a temporary folder, copies the submitted
file into that folder as `solution.py`, copies the problem tests in next to
it, runs `pytest`, and saves the result as a report. I copied every
submission as `solution.py` because the tests can then always import the
same file name. Without that rename, every problem's tests would need to
know the submission's filename in advance, which gets messy fast.

## Files

The repo has three sample problems: `two_sum`, `normalize_event`, and
`dependency_order`. Each problem folder contains:

- a `README.md` explaining the problem
- `starter.py` with unfinished starter code
- `solution.py` with a correct solution
- a `tests/` folder with pytest tests

There is also `submissions/two_sum_buggy.py`, a deliberately wrong
submission you can use to see what a failing report looks like. The
evaluator code is in `src/eval_harness/` (`runner.py` does the work,
`cli.py` is the interface).

## Run

Setup:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
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

## CLI Reference

`eval-harness run` evaluates a single submission:

| Argument | Default | What it does |
|---|---|---|
| `--problem` | (required) | Problem directory |
| `--submission` | (required) | Candidate Python file |
| `--timeout` | `10` | Per-run timeout in seconds |
| `--out` | none | Write the JSON report to a file |

`eval-harness batch` evaluates jobs from a manifest:

| Argument | Default | What it does |
|---|---|---|
| `--manifest` | (required) | Batch manifest JSON |
| `--timeout` | `10` | Default per-run timeout |
| `--out` | none | Write the JSON report to a file |

The timeout matters more than it looks. A submission with an infinite loop
would otherwise hang the whole batch. Ten seconds is generous for these
problems, and a submission that hits it is reported as failed rather than
waited on forever.

The batch manifest can also include points for each job:

```json
{
  "id": "dependency-order-reference",
  "problem": "../problems/dependency_order",
  "submission": "../problems/dependency_order/solution.py",
  "points": 5
}
```

That makes the output more like a small autograder, because the final report
includes `earned_points`, `possible_points`, and `score_percent`.

## Example Report

Running the bundled buggy submission against `two_sum` produces this:

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

Three tests pass and one fails. That is what a partially-correct submission
looks like, and it is why the report counts individual tests instead of
giving a single yes/no. For batch runs, the report also shows the score:

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

## Verify

```bash
pytest
```

## Notes

At first the batch runner only reported pass/fail. Adding points-based
scoring made the output feel like a real autograder instead of a test
wrapper. I wanted a project that connects to testing,
coding challenges, and AI code evaluation, and it helped me practice writing
tests, building a command-line tool, using temporary folders, running
another command from Python, creating JSON reports, and organizing a project
so someone else can understand it.

## License

MIT. See the [LICENSE](LICENSE) file.
