# Horizon Agentic Project Planning

A portable, agent-driven **project-plan system**: a small set of living documents that let an AI
agent (or a human) run a body of work too large for a single note across many sessions, keeping a
traceable record of the brief, the plan, live status, decisions, an action-log timeline, and open
bugs/debt — from kickoff through a clean close.

This repository is a **Horizon AIOS Options Package**. It works two ways:

1. **Standalone — zero dependencies.** Point any agent at [`core/README.md`](core/README.md). It reads
   the three lifecycle specs and scaffolds/manages a project plan inside *any* repo. Nothing about
   Horizon.AIOS is required. This is the reference-folder mode: an agent reads this folder once and
   thereafter manages the plan entirely inside the target project.

2. **Optional Horizon AIOS Options Package.** Run the cross-platform Python installer in
   [`aios/`](aios/) to deploy a `/project-plan` skill into a Horizon.AIOS install (`$HORIZON_ROOT`), add
   a terse context pointer so agents discover it, and register the package in a machine-local
   deployed-packages registry the Horizon.AIOS sync reads (so an upstream sync never clobbers it). A matching
   uninstaller removes everything cleanly. The Horizon.AIOS layer is a thin wrapper over the same `core/` kit —
   it adds discovery, one-command scaffolding, and sync integration, not new behavior.

## What a "project plan" is

A doc-truth roadmap for a multi-session body of work. It is **intent/roadmap**, not source-of-truth
code. Each project is a set of files sharing a zero-padded serial prefix (`001_`, `002_`, …) and a
short slug, living together under one folder (default `docs/project_plans/`):

| Role | File | Purpose |
|---|---|---|
| Detail | `NNN_detail-slug.md` | Plan of record: headline, summary, traced file map, the verbatim brief, your synthesis, the sectioned plan. |
| Status | `NNN_status-slug.md` | Live per-item status + append-only serialized notes/mini-decisions. |
| Status archive | `NNN_status_archive-slug.md` | Completed/verified blocks retired out of the live status doc. |
| Orientation | `NNN_current_orientation-slug.md` | The cold-start doc — read *instead of* a handoff to resume. |
| Action log | `NNN_action_log-slug.md` | Append-only one-line-per-action timeline (no frontmatter). |
| Bugs & debt | `NNN_bugs_and_technical_debt-slug.md` | Running list; every item cleared or deferred-with-reason before close. |

Plus a folder `index.md` registering every project, and a project-resident
`PROJECT_PLAN_GUIDE.md` (copied in at scaffold time) that makes the target project self-managing.

## Lifecycle

The three specs in [`core/lifecycle/`](core/lifecycle/) cover the whole arc:

1. **[Setting up](core/lifecycle/01_setting_up_a_project.md)** — scaffold the file set, fill frontmatter, register it.
2. **[Managing](core/lifecycle/02_managing_a_project.md)** — the standing upkeep discipline (status stays live, archive verified work, log every action).
3. **[Closing](core/lifecycle/03_closing_a_project.md)** — the teardown checklist that winds a project down to a clean, auditable rest state.

## Customizing the guide (`.local.` overrides)

The rules that govern how project plans are run live in `PROJECT_PLAN_GUIDE.md`. You can override them
at three levels, most-specific wins:

1. **Shipped default** — `core/templates/PROJECT_PLAN_GUIDE.md`. The package's canonical guide.
2. **System-wide admin override** *(Horizon.AIOS installs)* — `$HORIZON_ETC/horizon_project_planning_guide.local.md`.
   The installer materializes this once from the shipped default; **admins edit it to change the
   project-plan rules for the whole machine**. It is machine-local: git-ignored (via the repo's
   `.git/info/exclude`, so it never enters OS canon and is never overwritten by a package update or an
   upstream sync). When the `/project-plan` skill scaffolds a new plan, it copies *this* guide if
   present, else the shipped default. Delete it to fall back to the default.
3. **Project/folder-specific override** *(any repo, Horizon.AIOS or not)* — a folder can override the rules just
   for itself by creating its own `PROJECT_PLAN_GUIDE.local.md` **in that folder** and **referencing it
   from that folder's `agents.md`** (e.g. `@docs/project_plans/PROJECT_PLAN_GUIDE.local.md`), so agents
   working in that folder load the folder-specific rules. The `.local.md` file is the local override; the
   scaffolded `PROJECT_PLAN_GUIDE.md` remains the base it amends.

The same `.local.` convention runs throughout: `.local.` files are machine/folder-specific, git-ignored,
and take precedence over the shipped canon.

## Layout

```
horizon_agentic_project_planning/
├── README.md                     ← you are here
├── VERSION
├── docs/                         ← package docs: design/, decisions/ (ADRs), examples/
│   ├── design/architecture.md
│   ├── decisions/                ← ADR-0001 … ADR-0007 + index
│   └── examples/project_plans/   ← a filled-in worked sample
├── core/                         ← STANDALONE kit (no AIOS dependency)
│   ├── README.md                 ← the entry point an agent reads
│   ├── lifecycle/                ← the three lifecycle specs
│   │   ├── 01_setting_up_a_project.md
│   │   ├── 02_managing_a_project.md
│   │   └── 03_closing_a_project.md
│   └── templates/                ← blank files with [PLACEHOLDERS]
│       ├── index.md
│       ├── PROJECT_PLAN_GUIDE.md ← copied into the target project (self-containment)
│       ├── NNN_detail-SLUG.md
│       ├── NNN_status-SLUG.md
│       ├── NNN_status_archive-SLUG.md
│       ├── NNN_current_orientation-SLUG.md
│       ├── NNN_action_log-SLUG.md
│       └── NNN_bugs_and_technical_debt-SLUG.md
└── aios/                         ← OPTIONAL Horizon AIOS wrapper
    ├── INSTALL.md
    ├── skill/project-plan/SKILL.md
    └── install/
        ├── horizon_project_planning_package.py   ← cross-platform installer (install/uninstall/status)
        └── context_pointer.md                    ← the terse context block injected on install
```

When installed, the package is a git clone at `$HORIZON_SYSTEM/deployed_packages/<name>/`, registered in
`$HORIZON_ETC/horizon_deployed_packages.local.json`. The Horizon.AIOS sync reads that registry to keep the
package protected from upstream overwrite and backed up. See [`aios/INSTALL.md`](aios/INSTALL.md).

## Quickstart

**Standalone:** tell your agent *"Read `core/README.md` and set up a project plan for `<slug>` in
this repo."*

**Horizon.AIOS:** clone this package to `$HORIZON_SYSTEM/deployed_packages/`, run
`python aios/install/horizon_project_planning_package.py install`, restart Claude Code, then
`/project-plan new <slug>` in any project.
