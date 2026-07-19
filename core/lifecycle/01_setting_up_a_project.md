# Setting Up a Project Plan

How to scaffold a new project-plan file set. A project plan tracks a body of work too large for a
single note across multiple sessions. It is doc-truth (roadmap/intent), not code-truth.

> **Scope check first.** A project plan is for multi-session, multi-part work. For a one-off change,
> use a single note or the target repo's normal issue/PR flow instead. If the work has a brief, will
> span sessions, and needs live status + a decision trail, scaffold a plan.

## 0. Locate the project-plans folder

Default: `docs/project_plans/` at the target repo root. If the repo has a different docs convention,
use it, but keep all files of every project together in one folder. Create the folder if absent.

## 1. Pick a project serial (`NNN`)

Projects are numbered serially, zero-padded to 3 digits (`001`, `002`, …). Take the next unused
number — check the `# Projects` list in the folder's `index.md` (if `index.md` doesn't exist yet,
this is `001` and you create the index from `templates/index.md`). The serial is stable for the life
of the project and prefixes every file in the set.

## 2. Pick a short slug (`SLUG`)

A lowercase, underscore-joined topic slug, e.g. `look_here_primitives_and_movement_simulation`. It
suffixes every file so the set greps and sorts together. Keep it stable.

## 3. Create the six living files

Copy each `templates/NNN_<role>-SLUG.md` into the project-plans folder, substituting the real `NNN`
and `SLUG` into both the filename and the contents, and filling every `[BRACKET]` token:

1. **`NNN_detail-SLUG.md`** — the plan of record. Sections, in order:
   1. `## Headline` — one line.
   2. `## Executive summary` — one paragraph.
   3. `## Dependencies` — upstream (what this needs first) / downstream (what waits on this). "none" is valid.
   4. `## Relevant files` — the traced code map. Name real files/functions; mark anything unverified.
   5. `## Relevant vocabulary / concepts` — pointers to domain terms (optional; keep if the domain has fixed meanings).
   6. `## My Initial Brief` — the originating brief, **verbatim** (unedited, even for grammar).
   7. `## Your Initial Understanding From That Brief` — your synthesis after tracing the code.
   8. `## Plan` — one `### Section` per unit of work; each is a bulleted list of the brief's items it
      covers plus the architectural context that must shape it.
   9. `## Cross-cutting invariants` — things no section may violate. Optional.
2. **`NNN_status-SLUG.md`** — live status. Every plan item becomes a header with a `**Status:**` line
   (`NOT STARTED` / `IN PROGRESS` / `BLOCKED` / `DONE` / `VERIFIED`), plus dependency/gate notes. Ends
   with an append-only **Objective Notes & Mini-Decisions** section: serialized `## NOTE NNN-K`
   entries, each grep-able (`grep "NOTE NNN-"`).
3. **`NNN_status_archive-SLUG.md`** — empty at creation. Completed/verified status blocks move here
   under dated headings to keep the live status doc short and context-cheap.
4. **`NNN_current_orientation-SLUG.md`** — the cold-start doc, read **instead of** a handoff. Short:
   what the project is, the one thing to understand first, where it stands, what to read in order, and
   the standing upkeep rules. A few plain lines longer than a postcard.
5. **`NNN_action_log-SLUG.md`** — append-only postcard timeline; a `log` doc, **no frontmatter**. One
   line per action, appended to the END:
   ```bash
   echo "$(date -u +%Y-%m-%dT%H:%M:%SZ),<postcard>" >> \
     "docs/project_plans/NNN_action_log-SLUG.md"
   ```
6. **`NNN_bugs_and_technical_debt-SLUG.md`** — running list. Each item a stable `BUG-NNN-K` /
   `DEBT-NNN-K` id. Every item must be cleared or explicitly deferred-with-reason before close.

## 4. Frontmatter

The detail/status/status_archive/current_orientation/bugs files carry a light YAML block:

```yaml
---
type: project_plan
title: "Project NNN — <Title> (<Role>)"
description: <one line>
tags: [project-plan, <domain tags>]
timestamp: YYYY-MM-DD
status: draft        # draft until the project ships/closes
---
```

The **action log** carries **no** frontmatter (log convention). If the target repo has a stricter
frontmatter schema (e.g. Diátaxis `doc_type`, `source_of_truth`, `category`), adopt it — this block is
the portable minimum, not a ceiling.

## 5. Register the project

1. If the folder has no `index.md`, create it from `templates/index.md`.
2. Add the project to the `# Projects` list in `index.md`, linking all six files.
3. Copy `templates/PROJECT_PLAN_GUIDE.md` into the folder (once per folder; skip if already present).
   This is what makes the target project self-managing — see the self-containment rule in
   `core/README.md`.
4. If the target repo has a top-level docs index, add a one-line pointer to the project-plans folder
   the first time you create one there.

## 6. Seed the initial content

- Paste the user's brief **verbatim** into the detail doc's `## My Initial Brief`.
- Trace the code before writing `## Your Initial Understanding` and `## Relevant files` — name real
  symbols; mark guesses as unverified.
- Break the brief into `### Section`s in the plan; mirror each as a status item.
- Write the first action-log postcard: `project scaffold created (six files + index); planning-only, no product code`.
- Record any kickoff decisions or open questions as `NOTE NNN-1`, `NOTE NNN-2`, … in the status doc.

## 7. Optional host integrations (include only if the target repo has them)

- **Decision records (ADRs)** — if the repo keeps ADRs, a `NOTE` that reaches a durable decision sets
  its `ADR:` line to the real id and status to `SUPERSEDED-BY-ADR`. If the repo has no ADRs, `NOTE`
  entries are the decision record — self-contained, nothing to graduate to.
- **Objectives / handoffs / branch-status docs** — if present, the orientation doc links to them; the
  plan is the deep, project-scoped record one strand of them points into.

Once scaffolded, manage the project with `02_managing_a_project.md`. When it's done, close it with
`03_closing_a_project.md`.
