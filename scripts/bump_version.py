"""
Bump OpenFactory versions in `.devcontainer/devcontainer.json`.

This script updates:

1. The version tags of OpenFactory features in `features`
   (e.g., infra and opcua-connector images)
2. The `OPENFACTORY_VERSION` variable in `containerEnv`

Usage:
    python scripts/bump_version.py <new_version>

Arguments:
    <new_version> — A version string (e.g., 0.5.4 or 0.5.4rc2), or the special keyword "dev"

Behavior:
- If <new_version> is a version string:
    • Updates OpenFactory feature image tags using semver format
      (e.g., 0.5.4rc2 → 0.5.4-rc.2)
    • Sets OPENFACTORY_VERSION using the original version string (PEP 440)

- If <new_version> is "dev":
    • Sets feature image tags to "dev"
    • Transforms OPENFACTORY_VERSION to "<base>-dev.1"

Notes:
    - Only features under `ghcr.io/openfactoryio/openfactory-sdk/` are modified
    - Will exit with an error if required fields are missing

Dependency:
    - None
"""

from pathlib import Path
import sys
import json
import re


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


def bump_devcontainer_version(version: str) -> None:
    """
    Update the version for the devcontainer.

    If the version is "dev", it transforms the current version to "<base>-dev.1"
    and sets openfactory-version.default to "main". Otherwise, it sets the version
    and default tag based on the semantic version provided.

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
    bump_devcontainer_version(new_version)
