---
type: project_plan
title: "Project NNN — [Project Title] (Current Orientation)"
description: The read-instead-of-a-handoff cold-start orientation for Project NNN.
tags: [project-plan, orientation, "[domain-tag]"]
timestamp: [YYYY-MM-DD]
status: draft
---

# Project NNN — Current Orientation

> Read this instead of a handoff to resume Project NNN cold. It is short by design.

## What this project is
[Two or three sentences. Full detail: `NNN_detail-SLUG.md`.]

## The one thing to understand first
[The single load-bearing fact a fresh agent must grasp before touching anything. Point to the NOTE or
Section that expands it.]

## Where the project stands
[Current state in a few plain lines. Live per-item status: `NNN_status-SLUG.md`. Recommended next
step / build order. Any open user decisions that block a clean start.]

## What to read, in order
1. This file.
2. `NNN_status-SLUG.md` — per-item status + `NOTE NNN-K` objective notes / mini-decisions.
3. `NNN_detail-SLUG.md` — the full plan, the verbatim brief, and the traced code map.
4. [Governing decisions / docs, if any.]

## Standing rules for keeping THIS project current (do these without being asked)
1. **Keep the status doc live** — update each item's status as work lands; add a `NOTE NNN-K` for
   every decision/suspicion/mini-decision (`grep "NOTE NNN-"`).
2. **Archive verified sections** — move `VERIFIED` blocks into `NNN_status_archive-SLUG.md` under a
   dated heading; leave a one-line stub. Keeps the live status doc short.
3. **Keep this orientation current** — a couple of plain lines when the shape or next step changes.
4. **Log every meaningful action as a postcard** — append ONE line to `NNN_action_log-SLUG.md`:
   ```bash
   echo "$(date -u +%Y-%m-%dT%H:%M:%SZ),<postcard>" >> \
     "docs/project_plans/NNN_action_log-SLUG.md"
   ```

The full lifecycle rules for this project's folder live in `PROJECT_PLAN_GUIDE.md` (same folder).

## Related tracking
- Bugs & tech debt: `NNN_bugs_and_technical_debt-SLUG.md` — every item cleared before the project closes.
- [Optional: objective / branch-status doc / tracker this project is a strand of.]
