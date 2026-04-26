"""Utilities for evaluating submitted code against pytest problem suites."""

from .runner import EvaluationResult, evaluate_submission, evaluate_batch

__all__ = ["EvaluationResult", "evaluate_submission", "evaluate_batch"]

