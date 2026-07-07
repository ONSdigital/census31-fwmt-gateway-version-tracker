#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError as exc:
    raise SystemExit("PyYAML is required. Install with: python3 -m pip install pyyaml") from exc


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path):
    data = yaml.safe_load(path.read_text())
    return data or {}


def dump_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite-version", required=True)
    args = parser.parse_args()

    dev = load_yaml(ROOT / "environments" / "dev.yaml")
    manifest = load_yaml(ROOT / "manifest.yaml")
    candidate = {
        "suite_version": args.suite_version,
        "accepted_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "services": dev.get("services") or {},
        "libraries": manifest.get("libraries") or {},
    }

    output = ROOT / "candidates" / f"{args.suite_version}.yaml"
    dump_yaml(output, candidate)
    print(f"Wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()