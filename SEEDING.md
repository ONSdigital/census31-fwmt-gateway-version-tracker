# Census 31 FWMT tracker seeding

The original repository was seeded from 2021-era tracker files and used a flat per-component file layout.

This repo has now been modernized to the D-05 layout described in `pipeline-design.md`:

- `manifest.yaml`
- `environments/dev.yaml`
- `environments/int.yaml`
- `candidates/`
- `releases/`

Bootstrap seed details:

- Date: `2026-07-07`
- Seed source: current `version.txt` baselines in the active FWMT service and library repos.
- Seeded suite version: `27.0.1`
- Seeded release snapshot: `releases/27.0.1.yaml`
- Initial release snapshot uses `source_candidate: bootstrap-seed` because the legacy tracker did not store immutable candidate snapshots.

Use `python3 scripts/validate_tracker.py` after edits to verify manifest semantics.
