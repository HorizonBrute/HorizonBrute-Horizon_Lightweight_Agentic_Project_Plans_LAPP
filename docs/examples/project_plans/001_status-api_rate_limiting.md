---
type: project_plan
title: "Project 001 — Public API Rate Limiting (Status)"
description: Live per-item status for Project 001, plus serialized objective notes and mini-decisions.
tags: [project-plan, status, api, rate-limiting]
timestamp: 2026-06-02
status: draft
---

# Project 001 — Status

Plan detail: `001_detail-api_rate_limiting.md`.
Orientation (read this instead of a handoff): `001_current_orientation-api_rate_limiting.md`.

**Status legend:** `NOT STARTED` · `IN PROGRESS` · `BLOCKED` · `DONE` · `VERIFIED`.
Keep each item's status current as work lands. When a whole Section reaches `VERIFIED`, move its block
into `001_status_archive-api_rate_limiting.md` and leave a one-line stub pointing to the archive.

---

## Section 1 — Token-bucket core + middleware wiring
**Status:** ✅ VERIFIED 2026-06-05 — archived. Pure token bucket + after-auth middleware landed behind a
swappable store interface; unit tests green; verified under load on a single instance (limit held, p99
latency unchanged). Full block: `001_status_archive-…md` → "Archived 2026-06-05 — Section 1". Store
interface (NOTE 001-2) unblocks Section 4.

---

## Section 2 — Per-route limit configuration
**Status:** IN PROGRESS

### 2.1 Typed per-route limits table with a default
**Status:** DONE 2026-06-08 (tests green; not yet load-verified). `src/config/limits.ts` maps route
groups → {requests, window, burst}; unlisted routes use the default. `/search` override in place.

### 2.2 Runtime-overridable limits (no deploy)
**Status:** BLOCKED · **Open decision:** config-reload vs env vs admin endpoint — see NOTE 001-4.
Hardcoded table shipping as the interim; the "change without a deploy" requirement tracked as DEBT-001-1.

---

## Section 3 — Standards-compliant 429 responses
**Status:** NOT STARTED · **Depends:** 1 (bucket state), 2.1 (limit values)

---

## Section 4 — Distributed (Redis-backed) counters
**Status:** BLOCKED · **Depends:** shared Redis instance (NOTE 001-3); store interface from Section 1 (done)

---

# Objective Notes & Mini-Decisions (serialized)

Append-only, newest at the bottom. One `NOTE 001-K` per decision/update. Grep-able:
`grep "NOTE 001-"`. This project keeps its durable decisions as ADRs (see `../../decisions/`); a note
that reaches a durable decision sets its `ADR:` line.

Template:
```
## NOTE 001-K | YYYY-MM-DD | <short title>
- Status: OPEN | RESOLVED | SUPERSEDED-BY-NOTE-001-J
- ADR: none (self-contained) | ADR-00NN
- Sections: <e.g. 1, 2.2>
- Context: <the forces / situation>
- Decision/Update: <what was decided or what changed>
```

## NOTE 001-1 | 2026-06-02 | Token bucket over sliding-window log
- Status: RESOLVED
- ADR: none (self-contained)
- Sections: 1
- Context: Two common algorithms fit: a sliding-window request log (exact, but O(window) memory per
  client and more bookkeeping) or a token bucket (O(1) state per client, allows a configurable burst).
  The brief explicitly wants short bursts tolerated and cheap per-request cost.
- Decision/Update: Token bucket. Capacity = burst, refill rate = sustained limit. O(1) state and time
  per request, burst falls out naturally. Sliding-window rejected as heavier for no needed gain.

## NOTE 001-2 | 2026-06-03 | Bucket store sits behind an interface from day one
- Status: RESOLVED
- ADR: none (self-contained)
- Sections: 1, 4
- Context: The in-memory store ships first but must become Redis-backed without rewriting the
  middleware. If the middleware reaches into an in-memory map directly, Section 4 becomes a rewrite.
- Decision/Update: Define a minimal `BucketStore` interface (`read(clientId)`, `write(clientId, state)`)
  used by the middleware. In-memory implementation now; Redis implementation in Section 4. The swap is a
  store change only. This is the load-bearing seam of the whole project.

## NOTE 001-3 | 2026-06-05 | Section 4 blocked on shared Redis (infra)
- Status: OPEN (blocked)
- ADR: none (self-contained)
- Sections: 4
- Context: Fleet-wide enforcement needs a shared counter store. There is no shared Redis instance
  provisioned yet; infra ticket INFRA-1421 is open. Until then the limiter is per-instance, so behind
  the LB the effective limit is `N_instances × configured`.
- Decision/Update: Ship Sections 1–3 in-memory now (correct per instance, honestly documented as such).
  Hold Section 4 until Redis lands. Do not fake a distributed store. Re-evaluate when INFRA-1421 closes.

## NOTE 001-4 | 2026-06-08 | How limits become changeable without a deploy (OPEN)
- Status: OPEN
- ADR: none (self-contained)
- Sections: 2.2
- Context: The brief wants limits changeable without a deploy. Three options: (a) reload a config file on
  SIGHUP/watch, (b) read overrides from env at startup only (still needs a restart), (c) an authenticated
  admin endpoint that mutates the live table. (a) meets the requirement with least surface; (c) is most
  flexible but adds an auth-sensitive mutation path.
- Decision/Update: UNDECIDED — needs user input. Interim: hardcoded table (DEBT-001-1). Leaning (a)
  config-reload. Do not build (c) without an explicit ask (security surface).
