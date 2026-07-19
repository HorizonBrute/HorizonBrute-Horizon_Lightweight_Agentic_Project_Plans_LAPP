---
type: project_plan
title: "Project NNN — [Project Title] (Bugs & Technical Debt)"
description: Running list of open bugs and technical debt for Project NNN; every item cleared or deferred-with-reason before close.
tags: [project-plan, bugs, technical-debt, "[domain-tag]"]
timestamp: [YYYY-MM-DD]
status: draft
---

# Project NNN — Bugs & Technical Debt

Running list of bugs and technical debt for Project NNN. Every item here must be triaged and
cleared — either **FIXED** or **explicitly DEFERRED with rationale and a destination** — BEFORE the
project closes. Nothing on this list gets to disappear silently.

Companion docs: status (`NNN_status-SLUG.md`), detail (`NNN_detail-SLUG.md`), orientation
(`NNN_current_orientation-SLUG.md`).

Use stable ids: `BUG-NNN-K` for defects, `DEBT-NNN-K` for technical debt.

<!-- Items go below. Newest may go at top or bottom — be consistent. -->

## BUG-NNN-1 — [Short title]
1. **Observed:** [YYYY-MM-DD, context].
2. **Severity/priority:** [low / medium / high]; [any "clear before close" note].
3. **Status:** OPEN | FIXED (`[commit/PR]`) | DEFERRED (→ [destination], reason: [...]).
4. **Likely area (untriaged hypothesis, not a diagnosis):** [...].

## DEBT-NNN-1 — [Short title]
1. **Decision/context:** [...].
2. **Action needed:** [...].
3. **Impact:** [low / medium / high].
4. **Status:** OPEN | FIXED (`[commit/PR]`) | DEFERRED (→ [destination], reason: [...]).
