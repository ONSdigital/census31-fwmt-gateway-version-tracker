#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError as exc:
    raise SystemExit("PyYAML is required. Install with: python3 -m pip install pyyaml") from exc


ROOT = Path(__file__).resolve().parents[1]
RC_PATTERN = re.compile(r"-rc\.[0-9]+$")


def load_yaml(path: Path):
    data = yaml.safe_load(path.read_text())
    return data or {}


def dump_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Path to a candidate or release snapshot")
    parser.add_argument("--environment", required=True, choices=["dev", "int"])
    args = parser.parse_args()

    source = (ROOT / args.source).resolve() if not Path(args.source).is_absolute() else Path(args.source)
    snapshot = load_yaml(source)
    target = ROOT / "environments" / f"{args.environment}.yaml"
    current = load_yaml(target) if target.exists() else {}

    restored = {
        "suite_version": snapshot["suite_version"],
        "services": dict(snapshot.get("services") or {}),
    }

    if args.environment == "dev":
        current_services = current.get("services") or {}
        if "tm-mock" in current_services and "tm-mock" not in restored["services"]:
            restored["services"]["tm-mock"] = current_services["tm-mock"]
        restored["status"] = "accepted" if RC_PATTERN.search(str(snapshot["suite_version"])) else "promoted"

    dump_yaml(target, restored)
    print(f"Restored {source.name} into environments/{args.environment}.yaml")


if __name__ == "__main__":
    main()