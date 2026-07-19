---
type: project_plan
title: "Project 001 — Public API Rate Limiting (Status Archive)"
description: Archive of completed/verified work-item blocks retired out of the live status doc.
tags: [project-plan, status, archive, api, rate-limiting]
timestamp: 2026-06-02
status: draft
---

# Project 001 — Status Archive

When a Section (or a coherent group of items) in `001_status-api_rate_limiting.md` reaches `VERIFIED`,
its block is moved here verbatim under a dated `## Archived YYYY-MM-DD — <Section>` heading, and a
one-line stub is left in the live status doc. This keeps the live status doc short and context-cheap
while preserving the full record.

<!-- Archived blocks go below, newest first. -->

## Archived 2026-06-05 — Section 1: Token-bucket core + middleware wiring

**Status:** VERIFIED 2026-06-05 · Landed on `feat/rate-limiting` in 3 commits; verified under a
single-instance load test (limit held exactly; success-path p99 latency unchanged vs baseline).

### 1.1 Pure token-bucket implementation
**Status:** VERIFIED — `src/lib/token_bucket.ts`: `TokenBucket(capacity, refillPerSec)`, `tryConsume()`
returns `{ok, remaining, msToNextToken}`. Refill computed from elapsed time on read (no timer). 100%
branch-covered unit tests including burst-then-throttle and refill boundaries.

### 1.2 Middleware wiring after auth, before handlers
**Status:** VERIFIED — `src/middleware/rate_limit.ts` registered in `src/middleware/index.ts` directly
after auth; keys buckets on `resolveClientId(req)` (client id, else source IP). O(1) per request, no I/O.

### 1.3 Swappable bucket store interface
**Status:** VERIFIED — `BucketStore` interface (`read`/`write`) with an in-memory `MapBucketStore`
implementation. The middleware depends only on the interface; the Redis implementation (Section 4)
drops in without a middleware change. This is the seam NOTE 001-2 established.
