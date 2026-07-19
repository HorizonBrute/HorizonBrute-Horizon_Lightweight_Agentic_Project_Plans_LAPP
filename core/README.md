# Project-Plan Kit — Agent Entry Point

You are an agent. This folder is a self-contained kit for scaffolding and running a **project plan**:
a set of living documents that track a multi-session body of work from kickoff to a clean close. It
has **no dependencies** — you do not need Horizon AIOS or any other system to use it.

## How to use this kit

Read the lifecycle spec for what you're doing, then act on the target repository. You never need to
copy this kit's *reference* docs into the target project — but you MUST copy one file
(`templates/PROJECT_PLAN_GUIDE.md`) into the target so it becomes self-managing (see below).

| I want to… | Read | Then |
|---|---|---|
| Start a new project plan | [`lifecycle/01_setting_up_a_project.md`](lifecycle/01_setting_up_a_project.md) | Scaffold the six files + `index.md` + `PROJECT_PLAN_GUIDE.md` into the target. |
| Keep a project current | [`lifecycle/02_managing_a_project.md`](lifecycle/02_managing_a_project.md) | Apply the standing upkeep rules as work lands. |
| Wind a project down | [`lifecycle/03_closing_a_project.md`](lifecycle/03_closing_a_project.md) | Run the closing checklist to a clean rest state. |

The blank files you fill in live in [`templates/`](templates/). They use two literal placeholders you
substitute on every copy:

- `NNN` → the zero-padded project serial (`001`, `002`, …).
- `SLUG` → the lowercase underscore-joined topic slug (e.g. `look_here_primitives`).

Every `[SQUARE-BRACKET]` token inside a template is a fill-in you replace with real content.

## The self-containment rule (important)

A project plan must be **manageable from inside the target project alone** — once scaffolded, nobody
should have to come back and read *this* kit again. To guarantee that, setup copies
[`templates/PROJECT_PLAN_GUIDE.md`](templates/PROJECT_PLAN_GUIDE.md) into the target's project-plans
folder. That single file restates the upkeep and closing rules in project-local terms. From then on,
the target project's own `PROJECT_PLAN_GUIDE.md` + `index.md` are the source of truth for how its
plans are run; this kit is only needed to scaffold the *next* project.

## Overriding the guide per folder (`.local.`)

`PROJECT_PLAN_GUIDE.md` (copied into each project-plans folder) is the base rulebook. A folder can
override it for itself without editing the base: create a `PROJECT_PLAN_GUIDE.local.md` in the same
folder holding just the changed/added rules, and reference it from that folder's `agents.md` (e.g.
`@docs/project_plans/PROJECT_PLAN_GUIDE.local.md`) so agents working there load the folder-specific
rules on top of the base. `.local.` files are folder-specific and should be git-ignored by the host
repo. (Inside a Horizon AIOS install there is also a machine-wide admin override —
`$HORIZON_ETC/horizon_project_planning_guide.local.md` — but the folder-level override needs no AIOS.)

## Design principles (why the system is shaped this way)

1. **Doc-truth, not code-truth.** The plan records intent and the traced map of reality; it never
   competes with the code as the source of truth for behavior.
2. **Living, not narrative.** Status is updated in place as work lands. History is preserved by
   *archiving* verified blocks and *appending* to the action log — never by rewriting.
3. **Grep-able serialization.** Notes are `NOTE NNN-K`, bugs are `BUG-NNN-K` / `DEBT-NNN-K`. A single
   `grep` reconstructs any thread.
4. **Cold-start recoverable.** The orientation doc lets a fresh agent resume with zero prior context —
   it replaces reading a handoff.
5. **Nothing disappears silently.** Every bug/debt item is cleared or explicitly deferred-with-reason
   before a project closes.
6. **Optional integrations stay optional.** If the target repo has decision records (ADRs), issue
   trackers, objectives, or handoffs, the plan cross-references them. If it doesn't, the plan is fully
   self-contained (mini-decisions live inline as `NOTE` entries). Never hard-depend on a host system.
