---
type: Explanation
title: "Horizon Agentic Project Planning — Architecture"
description: How the package is structured — the standalone core, the optional AIOS wrapper, the installer, the deployed-packages registry, the sync gate, and the override layers.
tags: [architecture, package, project-planning, aios]
timestamp: 2026-07-19
status: draft
---

# Architecture

The package has two layers with a hard boundary between them, plus an installer that bridges them into
a Horizon AIOS instance. The governing decisions are recorded as ADRs in `../decisions/`.

## Layers

```
horizon_agentic_project_planning/
├── core/                      ← STANDALONE. Zero dependencies. The actual system.
│   ├── README.md              agent entry point
│   ├── lifecycle/             setup / manage / close specs
│   └── templates/             the six blank files + index + PROJECT_PLAN_GUIDE.md
├── aios/                      ← OPTIONAL wrapper. Thin. Adds discovery + install, not behavior.
│   ├── skill/project-plan/    the /project-plan skill (reads core/ as its "kit")
│   └── install/               the Python installer + the context pointer it injects
└── docs/                      ← this documentation + a worked example
```

**The boundary (ADR-0001):** everything the system *does* lives in `core/` and works with no AIOS. The
`aios/` layer only makes it discoverable and one-command installable inside a Horizon AIOS. Nothing in
`core/` imports or assumes `aios/`. This is what lets the package "stand alone completely away from
Horizon AIOS" and *also* be an optional AIOS feature.

## The document set (ADR-0002)

A project plan is six living files sharing an `NNN_role-slug` prefix (detail, status, status_archive,
current_orientation, action_log, bugs_and_technical_debt) plus a folder `index.md`. The design rests on:
doc-truth not code-truth; living (update-in-place) not narrative; grep-able serialization
(`NOTE NNN-K`, `BUG-NNN-K`); cold-start recoverability (the orientation replaces a handoff); and nothing
disappears silently (bugs/debt gate the close). Host integrations (ADRs, objectives, handoffs) are
optional — present when the target repo has them, absent otherwise.

## Install flow (ADR-0003, ADR-0004)

`aios/install/horizon_project_planning_package.py` (`install`/`uninstall`/`status`; cross-platform,
stdlib-only) is run from a clone placed at `$HORIZON_SYSTEM/deployed_packages/<name>/`. `install`:

1. copies `SKILL.md` + a copy of `core/` (as `kit/`) into `$HORIZON_SKILLS_BIN/project-plan/`;
2. adds a row to the skills index;
3. injects a marker-delimited terse context block into `projects/agents.md`;
4. materializes the admin `.local.` guide override (ADR-0006) and git-ignores it;
5. registers the package in `$HORIZON_ETC/horizon_deployed_packages.local.json` (ADR-0004) — name,
   version, `clone_path`, git `remotes[]`, `sync`, and a `payload` manifest for exact uninstall.

`uninstall` reverses 1–3 and 5; it leaves the clone, the admin override, and any scaffolded plans.

## Sync integration (ADR-0005)

The registry is machine-local (`*.local.json` → gitignored from OS canon, carried by the personal
backup sync). The AIOS official sync lane (`horizon_aios_sync.py`) overwrites everything except
`projects/usrbin/brains` from upstream — which would clobber a package living under the official-owned
`horizon_system/`. The sync's `official_pathspec()` was changed to also exclude every registered clone
with `sync != false`, so a deployed package is protected. Each clone is a nested git repo, so the
nightly nested-repo sync backs it up to its own remote automatically.

## Override layers (ADR-0006)

`PROJECT_PLAN_GUIDE.md` is the rulebook. Precedence, most-specific wins: shipped default → system-wide
admin override (`$HORIZON_ETC/horizon_project_planning_guide.local.md`, admin-editable, gitignored via
`.git/info/exclude`) → project/folder-specific override (`PROJECT_PLAN_GUIDE.local.md` referenced from
that folder's `agents.md`). `.local.` files are machine/folder-specific and never enter canon.

## Self-containment (ADR-0007)

Scaffolding copies the resolved `PROJECT_PLAN_GUIDE.md` into the target project's plans folder. From
then on the target manages its plans from that file + its own `index.md` — it never needs this package
again except to scaffold the next project. Uninstalling the package therefore never orphans a live plan.
