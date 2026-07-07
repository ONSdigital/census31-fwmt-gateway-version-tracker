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
    parser.add_argument("--source-candidate", required=True)
    args = parser.parse_args()

    manifest = load_yaml(ROOT / "manifest.yaml")
    int_env = load_yaml(ROOT / "environments" / "int.yaml")
    release = {
        "suite_version": args.suite_version,
        "released_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_candidate": args.source_candidate,
        "services": int_env.get("services") or {},
        "libraries": manifest.get("libraries") or {},
    }

    output = ROOT / "releases" / f"{args.suite_version}.yaml"
    dump_yaml(output, release)
    print(f"Wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()