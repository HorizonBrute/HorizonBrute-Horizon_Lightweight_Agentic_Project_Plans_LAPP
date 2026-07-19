# Closing a Project Plan

How to wind a project down to a **clean, auditable rest state**. Closing is a deliberate act, not
"stopped touching it." A closed project must read, cold, as: every planned item resolved or
consciously dropped, every bug/debt item cleared or deferred-with-reason, and the record self-explains
why it ended where it did.

Run this checklist top to bottom. Do not skip the gates — a project that closes with silent loose ends
is the failure mode this whole system exists to prevent.

## Pre-close gates (all must pass, or be consciously waived in writing)

### Gate 1 — Every plan item is terminal
In `NNN_status-SLUG.md`, every Section and sub-item is in a terminal state:
- `VERIFIED` — done and confirmed, or
- `DONE` — landed, with the outstanding verification named and consciously accepted as post-close, or
- `DROPPED` — explicitly cut, with a one-line reason and a `NOTE` recording the decision.

No item may close as `NOT STARTED`, `IN PROGRESS`, or `BLOCKED` without a `NOTE` explaining why it's
being left that way and where the work goes (a follow-on project, an issue, or nowhere-by-choice).

### Gate 2 — Every bug/debt item is cleared or deferred-with-reason
In `NNN_bugs_and_technical_debt-SLUG.md`, every `BUG-NNN-K` / `DEBT-NNN-K` is either:
- `FIXED` (with the fixing commit/PR referenced), or
- `DEFERRED` — with a rationale AND a destination (a follow-on project id, a tracker issue, or an
  explicit "accepted as permanent" note). Nothing disappears silently.

### Gate 3 — Decisions are settled
Every `NOTE NNN-K` is `RESOLVED`, `SUPERSEDED-*`, or explicitly `OPEN (carried to <destination>)`. If
the repo uses ADRs, every note that reached a durable decision has graduated (its `ADR:` line points
at a real id). No decision is left dangling with no owner.

### Gate 4 — Dependencies are honored
If `## Dependencies` named downstream projects that required this one to land first, confirm this
project actually reached the state they depend on (and say so), or notify/annotate them. Do not close
a foundation out from under something that's waiting on it.

## Closing steps

Once the gates pass:

1. **Archive the remaining live status.** Move every remaining `VERIFIED`/`DONE` Section block into
   `NNN_status_archive-SLUG.md` under a final `## Archived YYYY-MM-DD — Project close` heading. The
   live status doc should end nearly empty — a header, the legend, and a pointer to the archive.

2. **Write the closeout note.** Append a final `## NOTE NNN-K | YYYY-MM-DD | Project close` to the
   status doc capturing:
   - **Outcome** — what shipped vs. what was planned (one honest paragraph).
   - **Dropped/deferred** — the consciously-cut items and where they went (cross-ref the bug/debt ids
     and any follow-on project).
   - **Final state** — branch/tag/commit or release the work landed in.
   - **Successors** — any follow-on project ids this seeds.

3. **Update the orientation to a closed banner.** Replace the top of
   `NNN_current_orientation-SLUG.md` with a short closed-state banner: `STATUS: CLOSED YYYY-MM-DD —
   <one-line outcome>. See the closeout NOTE NNN-K in the status doc.` Keep the rest as historical
   reference. A cold reader must learn in one line that this project is closed and how it ended.

4. **Flip frontmatter status.** Set `status: closed` (or the repo's equivalent, e.g. `shipped` /
   `verified`) in the frontmatter of the detail/status/status_archive/orientation/bugs files.

5. **Update the folder index.** In `index.md`, mark the project line `— CLOSED YYYY-MM-DD (<one-line
   outcome>)`. Keep all six file links; a closed project stays fully browsable.

6. **Final action-log postcard.** Append one closing line:
   ```bash
   echo "$(date -u +%Y-%m-%dT%H:%M:%SZ),PROJECT CLOSED — <one-line outcome>; N items verified, M deferred (see closeout NOTE NNN-K)" >> \
     "docs/project_plans/NNN_action_log-SLUG.md"
   ```

7. **Hand off successors.** If the closeout seeds a follow-on project, scaffold it now (per
   `01_setting_up_a_project.md`) so the dependency chain is live before this session ends, and record
   the reverse pointer in the new project's `## Dependencies` (upstream = this project).

## Reopening a closed project

Projects can reopen. To reopen: flip the frontmatter `status` back to `draft`, add a
`## NOTE NNN-K | YYYY-MM-DD | Reopened` explaining why, restore the affected status items from the
archive to the live doc, update the orientation banner, and log a `PROJECT REOPENED` postcard. Never
delete the closeout note — the reopen note supersedes it in sequence, preserving the full history.

## What "closed" is NOT
- Not "delete the files." Closed projects are permanent record; they stay in the folder and the index.
- Not "everything is perfect." A project can close honestly with deferred debt and dropped items — the
  requirement is that every one of them is *named and accounted for*, not that none exist.
- Not silent. If you stop work without running this checklist, the project is *abandoned*, not closed.
  Abandonment is itself a state worth a `NOTE` — but prefer a real close.
