# Census 31 FWMT Gateway Version Tracker

This repository is the deployment source of truth for the FWMT suite.

## Layout

- `manifest.yaml`: summary of the last fully promoted suite.
- `environments/dev.yaml`: active desired state for `dev`.
- `environments/int.yaml`: active desired state for `int`.
- `candidates/`: immutable accepted RC suite snapshots.
- `releases/`: immutable promoted release suite snapshots.
- `scripts/validate_tracker.py`: validates tracker layout and manifest semantics.
- `scripts/restore_snapshot.py`: copies a release or candidate snapshot into an environment file.
- `scripts/write_candidate_snapshot.py`: writes an accepted candidate snapshot.
- `scripts/write_release_snapshot.py`: writes a promoted release snapshot.

## Validation

Run:

```bash
python3 scripts/validate_tracker.py
```

If `PyYAML` is missing locally, install it with:

```bash
python3 -m pip install pyyaml
```

## Restore hook

Restore a known snapshot into an environment file:

```bash
python3 scripts/restore_snapshot.py --source releases/27.0.1.yaml --environment dev
python3 scripts/restore_snapshot.py --source candidates/27.0.2-rc.4.yaml --environment int
```

The restore hook preserves explicit dev-only services already present in `environments/dev.yaml` when restoring into `dev`.

## Bootstrap note

The initial D-05 migration seeds the tracker with the current baseline from the FWMT repositories at the time of migration. The first seeded release snapshot uses `source_candidate: bootstrap-seed` because no accepted RC snapshot existed in this repo before the layout change.