# Managing a Project Plan

The standing upkeep discipline. Do these **without being asked** for the life of the project. Keeping
the docs live is what makes a project plan worth having — a stale plan is worse than none.

## The four standing rules

### 1. Status doc stays live
Update each item's `**Status:**` in `NNN_status-SLUG.md` as work lands. The legend:

- `NOT STARTED` — no code yet.
- `IN PROGRESS` — actively being built.
- `BLOCKED` — waiting on a dependency or a user decision (name it).
- `DONE` — code landed and parse/build-clean, but not yet confirmed in the running system.
- `VERIFIED` — confirmed working in the real system (in-app / in-test / by the user). Only `VERIFIED`
  work is archivable.

Add dependency and gate notes inline (`**Depends:** 2.2`, `**Open decision:** … — see NOTE NNN-K`).

### 2. Record every decision as a serialized NOTE
Append a `## NOTE NNN-K` to the **Objective Notes & Mini-Decisions** section for every decision,
suspicion, correction, or mini-decision. Newest at the bottom; never rewrite an existing note (add a
follow-up note that supersedes it and say so). The format is grep-able:

```
## NOTE NNN-K | YYYY-MM-DD | <short title>
- Status: OPEN | RESOLVED | SUPERSEDED-BY-NOTE-NNN-J | SUPERSEDED-BY-ADR
- ADR: none (self-contained) | ADR-00NN        # only if the repo uses ADRs
- Sections: <e.g. 1.1, 4.3>
- Context: <the forces / situation>
- Decision/Update: <what was decided or what changed>
```

Find all notes with `grep "NOTE NNN-"`. A `NOTE` is the durable "why" behind a change — write it even
when the change is small, because the reasoning is what a future session can't reconstruct from the
diff.

### 3. Archive verified work
When a Section (or a coherent group of items) reaches `VERIFIED`, **move** its block verbatim into
`NNN_status_archive-SLUG.md` under a dated `## Archived YYYY-MM-DD — <Section>` heading (newest
first), and leave a **one-line stub** in the live status doc pointing to the archive. This keeps the
live status doc short and context-cheap while preserving the full record.

### 4. Log every meaningful action
Append ONE postcard line to `NNN_action_log-SLUG.md` for each meaningful action — a landing, a
verify, a revert, a decision, a pause. The action log is the fast timeline; the status doc is the
structured state; the orientation is the cold-start entry point.

```bash
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ),<postcard: what just happened / next step>" >> \
  "docs/project_plans/NNN_action_log-SLUG.md"
```

Postcards are terse — one line, comma after the timestamp, present-tense fact. Never rewrite history;
only append.

## Keep the orientation current
When the project's **shape or next step** changes, update `NNN_current_orientation-SLUG.md` — a
couple of plain lines. It must always answer, for a cold agent: what is this, what's the one thing to
understand, where does it stand, what do I read in order. It replaces reading a handoff.

## Track bugs and debt as they surface
Anything observed-but-not-fixed goes into `NNN_bugs_and_technical_debt-SLUG.md` with a stable
`BUG-NNN-K` / `DEBT-NNN-K` id, an `Observed:` date, a severity, a status, and — for anything
non-trivial — a likely-area or postmortem note. Nothing gets to disappear silently; every item is
cleared or explicitly deferred before the project closes (enforced by the closing checklist).

## When a note graduates to a durable decision record (optional)
Only if the target repo keeps ADRs / decision records: when a mini-decision in a `NOTE` becomes a real
architectural decision, write the ADR in the repo's decisions folder and set the note's `ADR:` line to
the real id and `Status:` to `SUPERSEDED-BY-ADR`. If the repo has no ADR system, the `NOTE` *is* the
decision record — leave `ADR: none (self-contained)`.

## Verification honesty
Distinguish `DONE` (landed, parse/build-clean) from `VERIFIED` (confirmed in the running system). Do
not mark `VERIFIED` on your own say-so when the check requires running the system or the user's eyes —
mark it `DONE` and note the exact check still owed. Record what a verify run actually showed, including
anomalies, in a `NOTE`. Honest state is the whole point of a living plan.
