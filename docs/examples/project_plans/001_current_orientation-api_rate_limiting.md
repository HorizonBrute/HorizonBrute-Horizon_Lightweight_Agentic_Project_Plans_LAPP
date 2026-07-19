---
type: project_plan
title: "Project 001 — Public API Rate Limiting (Current Orientation)"
description: The read-instead-of-a-handoff cold-start orientation for Project 001.
tags: [project-plan, orientation, api, rate-limiting]
timestamp: 2026-06-02
status: draft
---

# Project 001 — Current Orientation

> Read this instead of a handoff to resume Project 001 cold. It is short by design.

## What this project is
Add per-client, per-route rate limiting to the public API, with standards-compliant `429` responses,
and a path to fleet-wide enforcement. Full detail: `001_detail-api_rate_limiting.md`.

## The one thing to understand first
The **counter store is the crux**. The limiter ships in-memory first — correct on one instance, but
behind the load balancer it under-limits by the instance count. Section 1 put the store behind a
`BucketStore` interface (NOTE 001-2) so Section 4 can swap in Redis with no middleware change. Do not
let anything reach past that interface into the in-memory map.

## Where the project stands
Section 1 (token-bucket core + wiring) is **VERIFIED and archived**. Section 2.1 (per-route limits
table) is **DONE**; 2.2 (runtime-changeable limits) is **BLOCKED on an open decision** (NOTE 001-4).
Section 3 (429 responses) is next and unblocked. Section 4 (Redis) is **BLOCKED on infra** (NOTE 001-3,
INFRA-1421). Live per-item status: `001_status-api_rate_limiting.md`. **Next step:** Section 3, then
resolve NOTE 001-4 with the user.

## What to read, in order
1. This file.
2. `001_status-api_rate_limiting.md` — per-item status + `NOTE 001-K` decisions.
3. `001_detail-api_rate_limiting.md` — the full plan, the verbatim brief, and the traced file map.
4. `../../decisions/` — the package's ADRs (this example folder lives inside the project-planning package).

## Standing rules for keeping THIS project current (do these without being asked)
1. **Keep the status doc live** — update each item's status as work lands; add a `NOTE 001-K` for every
   decision/suspicion (`grep "NOTE 001-"`).
2. **Archive verified sections** — move `VERIFIED` blocks into `001_status_archive-…md` under a dated
   heading; leave a one-line stub. Keeps the live status doc short.
3. **Keep this orientation current** — a couple of plain lines when the shape or next step changes.
4. **Log every meaningful action as a postcard** — append ONE line to `001_action_log-…md`.

Full lifecycle rules for this folder live in `PROJECT_PLAN_GUIDE.md` (same folder).

## Related tracking
- Bugs & tech debt: `001_bugs_and_technical_debt-api_rate_limiting.md` — one open bug, one deferred debt
  item; both cleared before the project closes.
- Downstream: Project 002 (per-client quotas & billing) will build on this project's client-identity +
  counter store.
