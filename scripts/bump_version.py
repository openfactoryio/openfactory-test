"""
Bump OpenFactory versions across project configuration files.

This script updates:

1. The project version in `pyproject.toml`
2. The OpenFactory core Git dependency in `pyproject.toml`
3. The version tags of OpenFactory features in `.devcontainer/devcontainer.json`

Usage:
    python scripts/bump_version.py <new_version>

Arguments:
    <new_version> — A version string (e.g., 0.5.4 or 0.5.4rc2), or the special keyword "dev"

Behavior:
- If <new_version> is a version string:
    • Sets the project version in `pyproject.toml`
    • Updates the OpenFactory Git dependency to match the version (e.g., @v0.5.4rc2)
    • Updates OpenFactory feature image tags using semver format
      (e.g., 0.5.4rc2 → 0.5.4-rc.2)

- If <new_version> is "dev":
    • Transforms the current project version to "<base>-dev.1"
    • Updates the OpenFactory Git dependency to match the derived version
    • Sets feature image tags to "dev"

Notes:
    - Only dependencies pointing to the OpenFactory core Git repository are modified
    - Only features under `ghcr.io/openfactoryio/openfactory-sdk/` are updated
    - Will exit with an error if required fields are missing

Dependency:
    - tomlkit
"""

from pathlib import Path
import sys
import json
import re
from tomlkit import parse, dumps


def pep440_to_semver(version: str) -> str:
    """
    Convert a PEP 440 version string to a semver-compatible version.

    This is required for devcontainer feature publishing, which enforces
    strict semantic versioning. Python pre-release versions such as
    "rc", "a", and "b" are translated accordingly.

    Examples:
        0.5.4rc1 -> 0.5.4-rc.1
        0.5.4a2  -> 0.5.4-alpha.2
        0.5.4b3  -> 0.5.4-beta.3
        0.5.4    -> 0.5.4

    Args:
        version (str): A version string following PEP 440 conventions.

    Returns:
        str: A semver-compatible version string suitable for devcontainer features.
    """
    version_original = version

    patterns = [
        (r"^(\d+\.\d+\.\d+)rc(\d+)$", r"\1-rc.\2"),
        (r"^(\d+\.\d+\.\d+)a(\d+)$", r"\1-alpha.\2"),
        (r"^(\d+\.\d+\.\d+)b(\d+)$", r"\1-beta.\2"),
    ]

    for pattern, replacement in patterns:
        if re.fullmatch(pattern, version):
            converted = re.sub(pattern, replacement, version)
            print(f"[normalize] {version_original} → {converted}")
            return converted

    # No change
    print(f"[normalize] {version_original} → {version_original} (no change)")
    return version_original


def update_openfactory_dependency(toml_doc, version: str) -> None:
    """
    Update the OpenFactory Git dependency in pyproject.toml.

    This function ensures that the OpenFactory core dependency remains
    aligned with the project version by updating its Git reference tag.

    Specifically, it searches for dependencies matching the OpenFactory
    core repository and replaces the version suffix with the provided
    version string, prefixed with "v".

    Example:
        "OpenFactory @ git+https://github.com/openfactoryio/openfactory-core.git@v0.5.4rc4"
        → "OpenFactory @ git+https://github.com/openfactoryio/openfactory-core.git@v0.5.5rc1"

    Args:
        toml_doc: Parsed pyproject.toml document (tomlkit object).
        version (str): The target version string (PEP 440 format).

    Returns:
        None

    Notes:
        - Only dependencies pointing to the OpenFactory core Git repository are modified
        - Other dependencies are left unchanged
    """
    deps = toml_doc["project"].get("dependencies", [])

    new_deps = []
    pattern = r"^OpenFactory\s*@\s*git\+.*openfactory-core\.git@.*$"

    for dep in deps:
        if re.match(pattern, dep):
            new_dep = f"OpenFactory @ git+https://github.com/openfactoryio/openfactory-core.git@v{version}"
            print(f"[pyproject.toml] dependency updated: {dep} → {new_dep}")
            new_deps.append(new_dep)
        else:
            new_deps.append(dep)

    toml_doc["project"]["dependencies"] = new_deps


def bump_pyproject_version(version: str) -> None:
    """
    Update the version in pyproject.toml.

    If the version is "dev", it transforms the current version to "<base>-dev.1".
    Otherwise, sets the version to the provided semantic version.

    Args:
        version (str): The new version string, e.g., "0.4.0" or the special keyword "dev".

    Returns:
        str: The final version string written to pyproject.toml

    Raises:
        SystemExit: If the pyproject.toml file is missing or malformed.
    """
    pyproject_path = Path(__file__).resolve().parent.parent / "pyproject.toml"

    if not pyproject_path.exists():
        print("ERROR: pyproject.toml not found.")
        sys.exit(1)

    with pyproject_path.open("r", encoding="utf-8") as f:
        toml_doc = parse(f.read())

    if "project" not in toml_doc or "version" not in toml_doc["project"]:
        print("ERROR: [project] section or version field not found.")
        sys.exit(1)

    old_version = toml_doc["project"]["version"]

    if version == "dev":
        base_version = old_version.split("-")[0]
        new_version = f"{base_version}-dev.1"
    else:
        new_version = version

    toml_doc["project"]["version"] = new_version
    update_openfactory_dependency(toml_doc, new_version)

    with pyproject_path.open("w", encoding="utf-8") as f:
        f.write(dumps(toml_doc))

    print(f"[pyproject.toml] Version updated: {old_version} → {new_version}")


def update_devcontainer_image(data: dict, version: str) -> None:
    """
    Update the base image version in devcontainer.json.

    This function ensures that the devcontainer base image remains aligned
    with the project version by updating its tag.

    The image tag uses the original PEP 440 version string, prefixed with "v",
    unlike devcontainer features which use semver format.

    Example:
        "ghcr.io/openfactoryio/devcontainer-py3.14:v0.5.4rc4"
        → "ghcr.io/openfactoryio/devcontainer-py3.14:v0.5.5rc1"

    Args:
        data (dict): Parsed devcontainer.json content.
        version (str): The target version string (PEP 440 format).

    Returns:
        None

    Notes:
        - Only updates the "image" field if present
        - Preserves the original image name and replaces only the tag
    """
    if "image" not in data:
        return

    old_image = data["image"]

    if version == "dev":
        new_tag = "dev"
    else:
        new_tag = f"v{version}"

    base_image, _, _ = old_image.rpartition(":")
    new_image = f"{base_image}:{new_tag}"

    if old_image != new_image:
        print(f"[devcontainer.json] image updated: {old_image} → {new_image}")
        data["image"] = new_image


def bump_devcontainer_version(version: str) -> None:
    """
    Update version-related fields in devcontainer.json.

    This includes:
    - Updating the base image tag
    - Updating OpenFactory feature image tags

    If the version is "dev":
        • Sets image and feature tags to "dev"

    Otherwise:
        • Sets the image tag using the PEP 440 version (prefixed with "v")
        • Sets feature tags using semver-compatible format

    Args:
        version (str): The new version string, e.g., "0.4.0" or the special keyword "dev".

    Raises:
        SystemExit: If the JSON file is missing or required fields are not found.
    """
    json_path = (
        Path(__file__).resolve().parent.parent /
        ".devcontainer/devcontainer.json"
    )

    if not json_path.exists():
        print("ERROR: devcontainer.json not found.")
        sys.exit(1)

    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    update_devcontainer_image(data, version)

    if "features" not in data:
        print("ERROR: 'features' field not found in devcontainer.json.")
        sys.exit(1)

    old_features = list(data["features"].keys())

    if version == "dev":
        new_tag = "dev"
    else:
        new_tag = pep440_to_semver(version)

    updated_features = {}

    for feature, config in data["features"].items():
        if feature.startswith("ghcr.io/openfactoryio/openfactory-sdk/"):
            base = feature.split(":")[0]
            updated_features[f"{base}:{new_tag}"] = config
        else:
            updated_features[feature] = config

    data["features"] = updated_features
    for old, new in zip(old_features, updated_features.keys()):
        if old != new:
            print(f"[devcontainer.json] feature updated: {old} → {new}")

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: bump_version.py <new_version>")
        sys.exit(1)

    new_version = sys.argv[1]
    bump_pyproject_version(new_version)
    bump_devcontainer_version(new_version)
