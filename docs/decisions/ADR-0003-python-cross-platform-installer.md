---
type: decision
title: "ADR-0003 — Cross-platform Python installer, package-scoped namespace"
status: Accepted
timestamp: 2026-07-19
tags: [adr, installer, tooling]
---

# ADR-0003 — Cross-platform Python installer, package-scoped namespace

## Status
Accepted (2026-07-19). Supersedes an earlier PowerShell + bash installer pair.

## Context
The first installer was a pair of shell scripts (`.ps1` + `.sh`). That splits maintenance across two
languages and two OS families and drifts out of sync. The Horizon.AIOS operational tooling is Python
(`horizon_aios_doctor.py`, `horizon_aios_backup_user_data.py`, …), so a Python installer matches house
style and runs anywhere Python does.

## Decision
Replace the shell scripts with a single **cross-platform, standard-library-only Python** tool,
`horizon_project_planning_package.py`, with `install` / `uninstall` / `status` subcommands. Namespace it
`horizon_project_planning_*` — **not** `horizon_aios_*`, which is reserved for the OS core. This package
is a separate deliverable; its filename prefix must say so.

## Consequences
- One implementation for Windows/macOS/Linux; no per-OS drift.
- Matches Horizon.AIOS Python tooling conventions while staying clearly outside the OS namespace.
- Idempotent operations (re-runnable install, marker-delimited context injection, upsert registry) make
  updates and repair safe.
- Requires Python 3.8+ on the target (already a given in a Horizon.AIOS environment).
