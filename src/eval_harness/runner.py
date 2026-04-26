from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


SUMMARY_RE = re.compile(r"(?P<count>\d+) (?P<kind>passed|failed|error|errors|skipped)")


@dataclass(frozen=True)
class EvaluationResult:
    problem: str
    submission: str
    status: str
    exit_code: int | None
    duration_seconds: float
    pytest: dict[str, Any]
    stdout: str
    stderr: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_submission(
    problem_dir: str | Path,
    submission: str | Path,
    *,
    timeout_seconds: int = 10,
    python_executable: str = sys.executable,
) -> EvaluationResult:
    """Copy a candidate submission into an isolated workspace and run pytest."""

    problem_path = Path(problem_dir).resolve()
    submission_path = Path(submission).resolve()
    tests_path = problem_path / "tests"

    if not problem_path.exists():
        raise FileNotFoundError(f"Problem directory does not exist: {problem_path}")
    if not tests_path.is_dir():
        raise FileNotFoundError(f"Problem is missing a tests/ directory: {tests_path}")
    if not submission_path.is_file():
        raise FileNotFoundError(f"Submission file does not exist: {submission_path}")

    start = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="eval-harness-") as temp_name:
        workspace = Path(temp_name)
        shutil.copy2(submission_path, workspace / "solution.py")
        shutil.copytree(tests_path, workspace / "tests")

        env = os.environ.copy()
        env["PYTHONPATH"] = str(workspace)

        try:
            completed = subprocess.run(
                [python_executable, "-m", "pytest", "-q", "tests"],
                cwd=workspace,
                env=env,
                text=True,
                capture_output=True,
                timeout=timeout_seconds,
                check=False,
            )
            stdout = completed.stdout
            stderr = completed.stderr
            exit_code: int | None = completed.returncode
            status = "passed" if completed.returncode == 0 else "failed"
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout or ""
            stderr = exc.stderr or ""
            exit_code = None
            status = "timeout"

    duration = round(time.perf_counter() - start, 4)
    return EvaluationResult(
        problem=problem_path.name,
        submission=str(submission_path),
        status=status,
        exit_code=exit_code,
        duration_seconds=duration,
        pytest=parse_pytest_summary(stdout + "\n" + stderr),
        stdout=stdout,
        stderr=stderr,
    )


def evaluate_batch(
    manifest_path: str | Path,
    *,
    timeout_seconds: int = 10,
    python_executable: str = sys.executable,
) -> dict[str, Any]:
    manifest_file = Path(manifest_path).resolve()
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    base_dir = manifest_file.parent
    results = []

    for job in manifest["jobs"]:
        problem = _resolve_from_manifest(base_dir, job["problem"])
        submission = _resolve_from_manifest(base_dir, job["submission"])
        result = evaluate_submission(
            problem,
            submission,
            timeout_seconds=int(job.get("timeout_seconds", timeout_seconds)),
            python_executable=python_executable,
        )
        results.append(result.to_dict() | {"id": job.get("id", result.problem)})

    passed = sum(1 for result in results if result["status"] == "passed")
    return {
        "suite": manifest.get("suite", manifest_file.stem),
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "results": results,
    }


def parse_pytest_summary(output: str) -> dict[str, Any]:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    summary = lines[-1] if lines else ""
    counts = {"passed": 0, "failed": 0, "errors": 0, "skipped": 0}

    for match in SUMMARY_RE.finditer(summary):
        kind = match.group("kind")
        count = int(match.group("count"))
        if kind == "error":
            kind = "errors"
        counts[kind] = count

    counts["summary"] = summary
    return counts


def write_json_report(report: dict[str, Any], out_path: str | Path) -> None:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _resolve_from_manifest(base_dir: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base_dir / path).resolve()

