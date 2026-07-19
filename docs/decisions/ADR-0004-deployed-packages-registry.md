---
type: decision
title: "ADR-0004 — Deployed-packages registry + clone location"
status: Accepted
timestamp: 2026-07-19
tags: [adr, registry, aios, sync]
---

# ADR-0004 — Deployed-packages registry + clone location

## Status
Accepted (2026-07-19).

## Context
For a deployed package to receive updates it must be a git clone the admin can pull; for it to survive
and be backed up it must be tracked by the AIOS sync. The AIOS had **no** package/feature registry —
this was greenfield. Two things had to be decided: where a package clone lives, and how the system
records that it is installed. Constraints from the AIOS: the sync is lane-partitioned and file locality
(the `*.local.*` naming) decides which lane carries a file; the official lane overwrites canon from
upstream, so a canon-named state file would be discarded on sync.

## Decision
- **Registry:** a machine-local JSON file, `$HORIZON_ETC/horizon_deployed_packages.local.json` (schema
  `horizon_deployed_packages/v1`). Each entry records `name`, `version`, `clone_path` (relative to
  `$HORIZON_ROOT`), git `remotes[]` (so forks are captured), a `sync` flag, and a `payload` manifest of
  what was deployed (for exact uninstall). JSON because it is primarily machine-read; human-readable
  enough for inspection. The `.local.json` name makes it gitignored from OS canon yet carried by the
  hourly personal backup sync (its name matches the `*local*` re-include rule).
- **Clone location:** `$HORIZON_SYSTEM/deployed_packages/<name>/`. A dedicated home, separate from user
  `projects/` and OS tooling `usrbin/`. As a nested git repo it is auto-backed-up by the nightly
  nested-repo sync and pulled for updates on its own.

## Consequences
- The registry is the authoritative inventory and uninstall manifest.
- Because the clone lives under the official-owned `horizon_system/`, it needs explicit protection from
  the official overwrite lane — see ADR-0005.
- Per-machine state never enters OS canon and never conflicts on upstream sync.
- Recording `remotes[]` supports forked package sources.
