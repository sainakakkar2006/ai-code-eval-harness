# Dependency Order

Return a valid installation order for packages with dependencies.

## Function

```python
def dependency_order(packages: list[str], dependencies: dict[str, list[str]]) -> list[str]:
    ...
```

## Requirements

- Every package in `packages` must appear exactly once.
- A dependency must appear before the package that needs it.
- Dependencies may mention packages that are already in `packages`.
- Raise `ValueError` when dependencies contain a cycle.

