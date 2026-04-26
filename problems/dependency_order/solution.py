def dependency_order(packages: list[str], dependencies: dict[str, list[str]]) -> list[str]:
    visiting: set[str] = set()
    visited: set[str] = set()
    ordered: list[str] = []
    package_set = set(packages)

    def visit(package: str) -> None:
        if package in visited:
            return
        if package in visiting:
            raise ValueError("dependency cycle detected")

        visiting.add(package)
        for dependency in dependencies.get(package, []):
            if dependency in package_set:
                visit(dependency)
        visiting.remove(package)
        visited.add(package)
        ordered.append(package)

    for package in packages:
        visit(package)

    return ordered

