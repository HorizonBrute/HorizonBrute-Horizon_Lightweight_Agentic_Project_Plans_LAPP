---
type: project_plan
title: "Project 001 — Public API Rate Limiting (Bugs & Technical Debt)"
description: Running list of open bugs and technical debt for Project 001; every item cleared or deferred-with-reason before close.
tags: [project-plan, bugs, technical-debt, api, rate-limiting]
timestamp: 2026-06-09
status: draft
---

# Project 001 — Bugs & Technical Debt

Running list for Project 001. Every item here must be triaged and cleared — either **FIXED** or
**explicitly DEFERRED with rationale and a destination** — BEFORE the project closes. Nothing on this
list disappears silently.

Companion docs: status (`001_status-…md`), detail (`001_detail-…md`), orientation
(`001_current_orientation-…md`).

Ids: `BUG-001-K` for defects, `DEBT-001-K` for technical debt.

---

## BUG-001-1 — Burst allows one request past capacity (off-by-one on refill rounding)
1. **Observed:** 2026-06-09, unit + manual test. A client that empties its bucket and hits again exactly
   at a refill boundary occasionally gets one extra token — effective burst is `capacity + 1`.
2. **Severity/priority:** low (one request over, not a flood); MUST be cleared before close.
3. **Status:** OPEN, unassigned.
4. **Likely area (untriaged hypothesis, not a diagnosis):** `TokenBucket.tryConsume()` refill math —
   suspect `Math.floor` vs `Math.round` on `elapsed * refillPerSec`, or refilling before the capacity
   clamp. To be confirmed against the boundary unit test, not asserted.

---

## DEBT-001-1 — Per-route limits are hardcoded; must be changeable without a deploy
1. **Decision/context:** the brief requires limits changeable without a deploy. Section 2.1 shipped a
   typed but **hardcoded** table as the interim; the runtime-override mechanism is an open decision
   (see `001_status-…md` → NOTE 001-4).
2. **Action needed:** implement the chosen mechanism (leaning config-file reload) so `src/config/limits.ts`
   can be updated live. Remove the hardcoded-only path.
3. **Impact:** medium — a product requirement, not just cleanup.
4. **Status:** DEFERRED → Section 2.2 (this project), pending NOTE 001-4 resolution. Not silently dropped;
   it gates project close.
