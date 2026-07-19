---
type: project_plan
title: "Project 001 — Public API Rate Limiting (Plan Detail)"
description: The plan-of-record for adding per-client rate limiting to the public API — a token-bucket core, per-route limits, standards-compliant 429 responses, and a distributed backing store.
tags: [project-plan, api, rate-limiting, middleware]
timestamp: 2026-06-02
status: draft
---

# Project 001 — Public API Rate Limiting

## Headline
Add per-client rate limiting to the public API so no single caller can exhaust shared capacity, with
standards-compliant `429` responses and a path to enforcing limits across every server instance.

## Executive summary
The public API currently has no request throttling: a single client can saturate the request pool and
degrade the service for everyone. This project adds a token-bucket limiter as request middleware,
per-route limit configuration, and RFC-compliant `429 Too Many Requests` responses with `Retry-After`
and `RateLimit-*` headers. The load-bearing decision is the counter store: an in-memory bucket is
trivial but only limits *per instance*, so behind a load balancer the effective limit is
`N_instances × configured`. The plan lands the in-memory limiter first (immediate, correct on a single
instance) as a behavior-complete slice, then swaps the store for a shared Redis backing so the limit
holds fleet-wide — the middleware contract is designed up front so that swap is a store change, not a
rewrite.

## Dependencies
1. **Upstream (this project depends on):** none for Sections 1–3. Section 4 (distributed store) depends
   on a **shared Redis instance** being provisioned by infra — not yet available (see NOTE 001-3).
2. **Downstream (projects that depend on this one):** Project 002 — Per-Client API Quotas & Billing
   (planned) will build on the per-client identity + counter store this project establishes.

## Relevant files
Confirmed by trace on branch `feat/rate-limiting` (2026-06-02). Names marked (UNVERIFIED) are proposed,
not yet in the tree.

- `src/middleware/rate_limit.ts` — (UNVERIFIED) new middleware entry; the limiter runs here per request.
- `src/middleware/index.ts` — middleware registration order; the limiter must run AFTER auth (needs the
  resolved client id) and BEFORE route handlers.
- `src/lib/token_bucket.ts` — (UNVERIFIED) new pure token-bucket implementation (capacity, refill rate).
- `src/lib/client_identity.ts` — `resolveClientId(req)` — API key → client id; falls back to source IP
  for unauthenticated routes. The limiter keys buckets on this.
- `src/config/limits.ts` — (UNVERIFIED) new per-route limit table (requests/window, burst).
- `src/http/responses.ts` — `sendError(res, status, body)` — where the `429` + headers are emitted.
- `src/store/redis.ts` — existing Redis client wrapper (used elsewhere); the Section 4 backing store.

## Relevant vocabulary / concepts
- **Token bucket** — a bucket of `capacity` tokens refilled at `rate`/sec; each request costs one token;
  empty bucket → reject. Allows short bursts up to `capacity`, sustained rate = `rate`.
- **Client identity** — the key a bucket is scoped to: authenticated client id, else source IP.
- **Per-instance vs fleet-wide** — an in-memory bucket limits one server; a shared store limits the
  whole fleet. The equality that must eventually hold: *effective limit == configured limit*.

---

## My Initial Brief
> Verbatim, as given by the user at project kickoff (2026-06-02). Not edited for grammar.

we keep getting single clients hammering the api and taking it down for everyone. need rate limiting.
per client, and per route because /search is way more expensive than /health. return proper 429s with
retry-after so well behaved clients back off. it has to work across all our servers eventually not just
one box, but I'd rather ship something that works today than wait for the redis piece. limits should be
easy to change without a deploy ideally.

---

## Your Initial Understanding From That Brief
> My reading after tracing the middleware stack and the client-identity helper.

1. **The crux is the counter store, and it's a sequencing decision, not a blocker.** An in-memory
   token bucket is correct and shippable on a single instance today; behind the LB it under-limits by a
   factor of the instance count. Ship in-memory first (Sections 1–3), then swap to Redis (Section 4).
   Design the store behind an interface from the start so Section 4 is a store swap, not a rewrite.
2. **The limiter must key on resolved client identity**, so it runs after auth. `resolveClientId`
   already gives client-id-or-IP; reuse it. Do not re-implement identity.
3. **Per-route limits mean a config table**, not one global number. `/search` and `/health` get
   different buckets. The brief's "change without a deploy" wants this table loadable/overridable at
   runtime (env or config reload) — but a hardcoded table is an acceptable first step if flagged as debt.
4. **`429` must be standards-shaped**: `Retry-After` (seconds) plus the `RateLimit-Limit` /
   `RateLimit-Remaining` / `RateLimit-Reset` draft headers, so clients can self-pace.
5. **Nothing may change success-path latency measurably** — the limiter is O(1) per request (one bucket
   lookup + refill math); no I/O on the in-memory path.

---

## Plan

Each `### Section` is a unit of work. Status per item is tracked in
`001_status-api_rate_limiting.md`. Recommended order: 1 → 2 → 3 (shippable slice), then 4 when Redis is
available.

### Section 1 — Token-bucket core + middleware wiring
- Pure `token_bucket.ts` (capacity, refill rate, `tryConsume()`), unit-tested in isolation.
- `rate_limit.ts` middleware registered after auth, before handlers; keys buckets on `resolveClientId`.
- In-memory bucket registry (per client id), O(1) per request, no I/O.
- Context: this is the behavior-complete single-instance slice. The bucket store sits behind a small
  interface (`get/set` bucket state) so Section 4 can replace it without touching the middleware.

### Section 2 — Per-route limit configuration
- A limits table keyed by route (or route group) → {requests, window, burst}.
- Default limit for unlisted routes; explicit overrides for expensive routes (`/search`).
- Context: start with a typed table module; make it runtime-overridable if cheap, else file DEBT for the
  "change without a deploy" requirement (see DEBT-001-1).

### Section 3 — Standards-compliant 429 responses
- On empty bucket, emit `429` via `sendError` with `Retry-After` and `RateLimit-*` headers.
- Context: header math comes straight from the bucket state (remaining tokens, seconds to next token).

### Section 4 — Distributed (Redis-backed) counters
- Replace the in-memory bucket store with a Redis-backed store implementing the same interface, using an
  atomic token-bucket Lua script so concurrent instances don't race.
- Context: **blocked on a shared Redis instance (NOTE 001-3).** The interface from Section 1 is the seam;
  this section is a store implementation + wiring, not a middleware change. Verify effective limit ==
  configured limit across ≥2 instances.

## Cross-cutting invariants (do not violate)
- The limiter runs after auth (needs resolved client identity) and before route handlers.
- The in-memory success path does no I/O and stays O(1) per request.
- Limits are enforced by the same middleware regardless of store; the store is swappable behind its
  interface (in-memory ↔ Redis) with no middleware change.
