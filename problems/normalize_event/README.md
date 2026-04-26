# Normalize Event

Normalize an event dictionary for downstream scoring.

## Function

```python
def normalize_event(event: dict) -> dict:
    ...
```

## Requirements

- Preserve the original input dictionary.
- Lowercase and strip `severity`.
- Strip `service`.
- Convert missing `tags` to an empty list.
- Deduplicate tags case-insensitively and return them sorted.
- Raise `ValueError` when `timestamp` is missing.

