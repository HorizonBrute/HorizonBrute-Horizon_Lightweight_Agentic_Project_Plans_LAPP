---
name: project-plan
description: Scaffold and manage multi-session project plans (a set of living docs — detail, status, archive, orientation, action log, bugs/debt). Use when the user types /project-plan, asks to "start a project plan", "set up a project plan", "close a project", or wants a tracked multi-session body of work.
tools: Read, Write, Edit, Bash, Glob, Grep
---

# Skill: /project-plan

**Model preference:** `#midcost` (authoring/summarizing; per `horizon_aios_model_prefs.md`, overridable by a prompt directive).

Scaffold and run **project plans** — a set of living documents that track a body of work too large
for a single note across many sessions, from kickoff to a clean close. This skill is a thin wrapper
over a bundled, self-contained kit; all real behavior is defined there.

## The bundled kit

The lifecycle specs and blank templates ship alongside this skill at `<skill-dir>/kit/`, where
`<skill-dir>` is the directory containing this `SKILL.md` (typically
`$HORIZON_SKILLS_BIN/project-plan/` or `~/.claude/skills/project-plan/`). Read from there:

- `kit/README.md` — the kit overview and design principles.
- `kit/lifecycle/01_setting_up_a_project.md` — scaffolding a new plan.
- `kit/lifecycle/02_managing_a_project.md` — the standing upkeep discipline.
- `kit/lifecycle/03_closing_a_project.md` — the closing checklist.
- `kit/templates/` — the blank files (`NNN_*-SLUG.md`, `index.md`, `PROJECT_PLAN_GUIDE.md`).

## Invocation

`/project-plan <subcommand> [args]`. If no subcommand is given, infer from the user's words.

### `new [slug]` — scaffold a new project plan
1. Read `kit/lifecycle/01_setting_up_a_project.md` in full and follow it.
2. Locate the project-plans folder: default `docs/project_plans/` in the **current project** (the
   user's cwd, NOT the AIOS root). Create it if absent.
3. Pick the next serial `NNN` from that folder's `index.md` (or `001` if new).
4. Resolve the slug (from the arg, or ask for a short topic slug).
5. Copy every `kit/templates/NNN_*-SLUG.md` into the folder, substituting the real `NNN`/`SLUG` in
   filenames and contents; create `index.md` from the template if absent and copy the resolved
   **project-plan guide** into the folder as `PROJECT_PLAN_GUIDE.md` (once per folder). Resolve the
   guide by this precedence (first that exists wins):
   1. the **system-wide admin override**, `$HORIZON_ETC/horizon_project_planning_guide.local.md`
      (admin-editable, machine-local);
   2. the bundled default, `kit/templates/PROJECT_PLAN_GUIDE.md`.
   After scaffolding, a single project/folder may further override the rules by adding its own
   `PROJECT_PLAN_GUIDE.local.md` in the folder and referencing it from that folder's `agents.md`
   (see the kit README's override section).
6. Ask the user for the originating brief; paste it **verbatim** into the detail doc. Trace the code
   before writing the understanding and relevant-files sections.
7. Register the project in `index.md`; write the first action-log postcard.
8. **Self-containment:** confirm `PROJECT_PLAN_GUIDE.md` is present in the folder so the project is
   manageable without this skill from here on.

### `manage [NNN]` — upkeep an existing project
Read `kit/lifecycle/02_managing_a_project.md` and apply the standing rules to the named project (or
the most recently active one): update status, add `NOTE NNN-K` decisions, archive verified blocks,
append action-log postcards, keep the orientation current.

### `close [NNN]` — wind a project down
Read `kit/lifecycle/03_closing_a_project.md` and run the closing checklist: verify the four pre-close
gates, archive remaining status, write the closeout NOTE, flip frontmatter to `closed`, update the
orientation banner and the index line, and scaffold any successor project.

### `status [NNN]` — report where a project stands
Read the named project's `NNN_current_orientation-SLUG.md` and `NNN_status-SLUG.md` and give the user
a short orientation: what it is, where it stands, next step. Do not begin executing work.

### (no subcommand)
List the projects in the current project-plans folder (from `index.md`) and ask what the user wants
to do. If there's no folder yet, offer to `new`.

## Notes for the executing agent
- Project plans live in the **target project's** repo (the user's cwd), never in the AIOS system dirs.
  This skill only *reads* its kit from the skills path.
- Never invent a brief. The detail doc's `## My Initial Brief` is the user's words, verbatim.
- Keep `DONE` (landed) vs `VERIFIED` (confirmed in the running system) honest.
- The kit is self-contained and host-agnostic. Include optional integrations (ADRs, objectives,
  handoffs, branch-status docs) only if the target repo actually has them.
