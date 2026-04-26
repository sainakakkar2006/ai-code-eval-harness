import pytest

from solution import normalize_event


def test_normalizes_fields_without_mutating_input():
    event = {
        "timestamp": "2026-04-26T10:30:00Z",
        "service": " api ",
        "severity": " WARN ",
        "message": " latency spike ",
        "tags": ["Prod", "prod", " API "],
    }

    normalized = normalize_event(event)

    assert normalized == {
        "timestamp": "2026-04-26T10:30:00Z",
        "service": "api",
        "severity": "warn",
        "message": "latency spike",
        "tags": ["api", "prod"],
    }
    assert event["severity"] == " WARN "


def test_defaults_missing_optional_fields():
    assert normalize_event({"timestamp": "t1"}) == {
        "timestamp": "t1",
        "service": "",
        "severity": "info",
        "message": "",
        "tags": [],
    }


def test_requires_timestamp():
    with pytest.raises(ValueError):
        normalize_event({"service": "worker"})

