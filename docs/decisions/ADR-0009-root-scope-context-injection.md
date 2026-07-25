---
type: decision
title: "ADR-0009 — Retarget context injection to a root-scope, machine-local file"
status: Accepted
timestamp: 2026-07-24
tags: [adr, context, installer, aios]
---

# ADR-0009 — Retarget context injection to a root-scope, machine-local file

## Status
Accepted (2026-07-24).

## Context
The installer advertised the package to agents by injecting a marker-delimited block into
`$HORIZON_ROOT/projects/agents.md`. `projects/agents.md` was originally chosen because the OS's
two-lane sync's official (overwrite) lane leaves `projects/`, `usrbin/`, and `brains/` alone — an OS
update cannot clobber a block parked there.

That target has a scope bug: `projects/agents.md` only loads for agents working under `projects/**`.
An agent operating on the OS itself (`horizon_system/`), in a brain, or anywhere outside `projects/`
never sees that this package is installed, even though its own deployment clone lives at
`horizon_system/deployed_packages/`. Root `agents.md` (the OS-source file loaded for every agent,
everywhere) is not a usable fix for this: it is OS-owned and overwritten wholesale by every OS update,
so an injected block there would be silently deleted the next time the OS syncs.

The OS side of this change (tracked separately, OS-source repo) adds a static orientation block to
root `agents.md` plus one `@`-import line pointing at a new machine-local file,
`horizon_system/ai_os_etc/horizon_aios_options_packages.local.md`. That file is never overwritten by
the official sync lane (`.local.` names are excluded the same way `horizon_deployed_packages.local.json`
and `skills_bin/index.local.md` already are) and, via the `@`-import, is loaded for every agent in
every scope — not just `projects/**`.

## Decision
Retarget this package's context injection from `$HORIZON_ROOT/projects/agents.md` to
`$HORIZON_ETC/horizon_aios_options_packages.local.md` (i.e.
`$HORIZON_ROOT/horizon_system/ai_os_etc/horizon_aios_options_packages.local.md`):
- `install` creates the file if absent (with a short "machine-local, managed by package installers,
  do not hand-edit" header), then injects the same marker-delimited block used before, guarded by the
  same `BEGIN_MARKER` idempotency check.
- The file is git-ignored via the containing repo's `.git/info/exclude` (never the tracked
  `.gitignore`, which the official sync lane would overwrite from upstream), following the same
  pattern already used for the admin guide override (ADR-0006).
- `install` and `update` both run a migration step first: strip this package's marker block from the
  OLD location, `projects/agents.md`, if present (safe no-op otherwise) — so a machine upgrading from
  an older installer never carries the block twice. `update` re-invokes `install`, so the migration
  runs on both paths automatically.
- `uninstall` strips the marker block from the new location, and — belt-and-suspenders, for a machine
  that skipped straight to `uninstall` without ever re-running `install`/`update` — also strips any
  lingering block at the old location.
- The registry's `payload.context_block_file` is updated to record the new path, so `uninstall` and
  tooling that reads the registry stay exact.
- The marker string itself, `horizon-agentic-project-planning`, is unchanged — uninstall on an
  already-installed machine (that has since migrated) still finds and removes exactly what it wrote.

## Consequences
- An agent working anywhere under `$HORIZON_ROOT` — not just inside `projects/`, — now discovers this
  package is installed, closing the scope gap that motivated this change.
- Package context and OS orientation are cleanly separated by ownership: OS core owns root
  `agents.md` and can overwrite it freely on every update; package installers own the `.local.` file
  and are never clobbered.
- A machine with zero packages installed costs nothing extra: the OS root `agents.md`'s `@`-import of
  a file that does not yet exist is the same proven no-op pattern already used for `@local.agents.md`.
- Every options package following this pattern (this package is the reference implementation other
  package authors are told to copy) must ship the same migration step, or an upgraded machine will
  carry a stale duplicate block at the old location indefinitely.
- This ADR's file target is coupled to the OS-source change that adds the `@`-import line to root
  `agents.md`; on a machine running an OS version that predates that import, the injected block is
  written correctly but not yet loaded anywhere until the OS is updated. That is expected and
  transient — the file still exists and is ready the moment the OS-side import lands.
