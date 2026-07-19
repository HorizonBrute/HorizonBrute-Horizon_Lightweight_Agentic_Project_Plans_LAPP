---
type: decision
title: "ADR-0006 — Three-tier .local. guide override"
status: Accepted
timestamp: 2026-07-19
tags: [adr, configuration, override]
---

# ADR-0006 — Three-tier `.local.` guide override

## Status
Accepted (2026-07-19).

## Context
`PROJECT_PLAN_GUIDE.md` encodes how project plans are run. Different operators want different rules: an
admin wants machine-wide defaults; a single project sometimes needs its own tweaks; and the package
still ships a sensible baseline. Editing the shipped file to customize is wrong — updates would clobber
edits, and per-folder tweaks would leak globally. The AIOS already uses a `*.template` → `*.local.*`
convention where the local copy wins and is machine-specific.

## Decision
Layer the guide with three tiers, **most-specific wins**:
1. **Shipped default** — `core/templates/PROJECT_PLAN_GUIDE.md`.
2. **System-wide admin override** — `$HORIZON_ETC/horizon_project_planning_guide.local.md`, materialized
   once by the installer from the default, admin-editable, never clobbered. The `/project-plan` skill
   copies *this* into new projects when present. It is git-ignored via the containing repo's
   `.git/info/exclude` (not the tracked `.gitignore`, which the official lane would overwrite from
   upstream; `*.local.md` is not covered by the canon `*.local.json` rule).
3. **Project/folder-specific override** — a `PROJECT_PLAN_GUIDE.local.md` in a folder, referenced from
   that folder's `agents.md`, amending the base for that folder only. Needs no AIOS.

## Consequences
- Admins customize system-wide behavior without forking the package; edits survive updates and sync.
- A single project can diverge without affecting others.
- `.local.` is a uniform signal across the system: machine/folder-specific, git-ignored, wins over canon.
- Uninstall preserves the admin override (it is admin content, not package payload).
- Standalone (non-AIOS) users get tiers 1 and 3; the admin tier is AIOS-only (needs `$HORIZON_ETC`).
