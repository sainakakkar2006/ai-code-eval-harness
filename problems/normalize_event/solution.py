def normalize_event(event: dict) -> dict:
    if "timestamp" not in event:
        raise ValueError("timestamp is required")

    raw_tags = event.get("tags") or []
    tags = sorted({str(tag).strip().lower() for tag in raw_tags if str(tag).strip()})

    return {
        "timestamp": event["timestamp"],
        "service": str(event.get("service", "")).strip(),
        "severity": str(event.get("severity", "info")).strip().lower(),
        "message": str(event.get("message", "")).strip(),
        "tags": tags,
    }

