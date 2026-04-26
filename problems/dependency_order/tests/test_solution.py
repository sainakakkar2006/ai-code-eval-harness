import pytest

from solution import dependency_order


def assert_valid_order(order, dependencies):
    positions = {package: index for index, package in enumerate(order)}
    for package, deps in dependencies.items():
        for dependency in deps:
            if dependency in positions:
                assert positions[dependency] < positions[package]


def test_returns_all_packages_once():
    packages = ["api", "db", "worker", "cache"]
    dependencies = {"api": ["db", "cache"], "worker": ["db"]}

    order = dependency_order(packages, dependencies)

    assert sorted(order) == sorted(packages)
    assert len(order) == len(set(order))
    assert_valid_order(order, dependencies)


def test_keeps_independent_packages():
    assert dependency_order(["a", "b"], {}) == ["a", "b"]


def test_detects_cycle():
    with pytest.raises(ValueError):
        dependency_order(["a", "b"], {"a": ["b"], "b": ["a"]})

