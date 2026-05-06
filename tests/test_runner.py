import json
from pathlib import Path

from eval_harness.runner import evaluate_batch, evaluate_submission, parse_pytest_summary


def test_parse_pytest_summary_counts_outcomes():
    summary = parse_pytest_summary("..F\n1 failed, 2 passed, 1 skipped in 0.04s")

    assert summary["failed"] == 1
    assert summary["passed"] == 2
    assert summary["skipped"] == 1


def test_evaluate_submission_passes_reference_problem():
    result = evaluate_submission(
        "problems/two_sum",
        "problems/two_sum/solution.py",
        timeout_seconds=5,
    )

    assert result.status == "passed"
    assert result.pytest["passed"] == 4


def test_evaluate_submission_reports_failure():
    result = evaluate_submission(
        "problems/two_sum",
        "submissions/two_sum_buggy.py",
        timeout_seconds=5,
    )

    assert result.status == "failed"
    assert result.pytest["failed"] >= 1


def test_evaluate_batch_aggregates_results(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "suite": "unit",
                "jobs": [
                    {
                        "id": "reference",
                        "problem": str(Path("problems/normalize_event").resolve()),
                        "submission": str(Path("problems/normalize_event/solution.py").resolve()),
                        "points": 3,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    report = evaluate_batch(manifest, timeout_seconds=5)

    assert report["suite"] == "unit"
    assert report["passed"] == 1
    assert report["failed"] == 0
    assert report["earned_points"] == 3
    assert report["possible_points"] == 3
    assert report["score_percent"] == 100.0
    assert report["results"][0]["earned_points"] == 3


def test_evaluate_batch_scores_failed_jobs_as_zero(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "suite": "mixed",
                "jobs": [
                    {
                        "id": "reference",
                        "problem": str(Path("problems/normalize_event").resolve()),
                        "submission": str(Path("problems/normalize_event/solution.py").resolve()),
                        "points": 4,
                    },
                    {
                        "id": "buggy",
                        "problem": str(Path("problems/two_sum").resolve()),
                        "submission": str(Path("submissions/two_sum_buggy.py").resolve()),
                        "points": 2,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    report = evaluate_batch(manifest, timeout_seconds=5)

    assert report["passed"] == 1
    assert report["failed"] == 1
    assert report["earned_points"] == 4
    assert report["possible_points"] == 6
    assert report["score_percent"] == 66.67
