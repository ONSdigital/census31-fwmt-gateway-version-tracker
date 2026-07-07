#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError as exc:
    raise SystemExit("PyYAML is required. Install with: python3 -m pip install pyyaml") from exc


ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_ENVS = {"dev", "int"}
PROMOTABLE_STATUSES = {"acceptance-pending", "accepted", "promoted"}


def load_yaml(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    data = yaml.safe_load(path.read_text())
    return data or {}


def validate_manifest(manifest: dict) -> list[str]:
    errors = []
    services = manifest.get("services")
    if not isinstance(services, dict) or not services:
        errors.append("manifest.yaml must define non-empty services")
        return errors

    for service_name, service in services.items():
        if not isinstance(service, dict):
            errors.append(f"manifest.yaml service '{service_name}' must be a mapping")
            continue
        if not service.get("image"):
            errors.append(f"manifest.yaml service '{service_name}' is missing image")
        if not service.get("version"):
            errors.append(f"manifest.yaml service '{service_name}' is missing version")

        promote_to = service.get("promote_to")
        if promote_to in (None, [], ""):
            continue
        if not isinstance(promote_to, list):
            errors.append(f"manifest.yaml service '{service_name}' promote_to must be a list")
            continue
        invalid = [env for env in promote_to if env not in SUPPORTED_ENVS]
        if invalid:
            errors.append(
                f"manifest.yaml service '{service_name}' has invalid promote_to values: {', '.join(invalid)}"
            )

    libraries = manifest.get("libraries")
    if not isinstance(libraries, dict) or not libraries:
        errors.append("manifest.yaml must define non-empty libraries")
    return errors


def validate_environment(path: Path, allow_dev_only: bool) -> list[str]:
    errors = []
    env = load_yaml(path)
    services = env.get("services")
    if not env.get("suite_version"):
        errors.append(f"{path.name} is missing suite_version")
    if not isinstance(services, dict) or not services:
        errors.append(f"{path.name} must define non-empty services")
    if path.name == "dev.yaml":
        status = env.get("status")
        if status and status not in PROMOTABLE_STATUSES:
            errors.append(f"dev.yaml has invalid status '{status}'")
    if not allow_dev_only and "tm-mock" in (services or {}):
        errors.append("int.yaml must not contain dev-only service tm-mock")
    return errors


def validate_releases_dir(releases_dir: Path) -> list[str]:
    errors = []
    release_files = sorted(releases_dir.glob("*.yaml"))
    if not release_files:
        errors.append("releases/ must contain at least one seeded release snapshot")
    return errors


def main() -> None:
    errors: list[str] = []
    errors.extend(validate_manifest(load_yaml(ROOT / "manifest.yaml")))
    errors.extend(validate_environment(ROOT / "environments" / "dev.yaml", allow_dev_only=True))
    errors.extend(validate_environment(ROOT / "environments" / "int.yaml", allow_dev_only=False))
    errors.extend(validate_releases_dir(ROOT / "releases"))

    if errors:
        raise SystemExit("Tracker validation failed:\n- " + "\n- ".join(errors))

    print("Tracker validation passed")


if __name__ == "__main__":
    main()