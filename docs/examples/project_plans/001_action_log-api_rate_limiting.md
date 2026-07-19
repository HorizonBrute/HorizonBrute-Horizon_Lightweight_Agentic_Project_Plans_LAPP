# Project 001 — Action Log

Serial, append-only postcard timeline. One line per action, appended to the END.
Format: `ISO8601-UTC,<postcard>`. Append with:
`echo "$(date -u +%Y-%m-%dT%H:%M:%SZ),<postcard>" >> <this file>`
Do not rewrite history; only append. This is a `log` doc — no YAML frontmatter by convention.

2026-06-02T14:10:00Z,project scaffold created (six files + index); planning-only session, no product code
2026-06-02T14:35:00Z,NOTE 001-1 RESOLVED: token bucket over sliding-window (O(1) state, natural burst)
2026-06-03T09:20:00Z,NOTE 001-2 RESOLVED: bucket store behind a BucketStore interface from day one so Redis is a store swap not a rewrite
2026-06-04T16:05:00Z,Section 1 landed (3 commits): pure TokenBucket + after-auth middleware + in-memory MapBucketStore; unit tests green
2026-06-05T11:00:00Z,Section 1 VERIFIED under single-instance load test (limit held exactly, p99 latency unchanged); block archived; next Section 2
2026-06-05T11:05:00Z,NOTE 001-3: Section 4 (Redis) BLOCKED on shared instance (INFRA-1421); shipping Sections 1-3 in-memory, documented as per-instance
2026-06-08T15:40:00Z,Section 2.1 DONE: per-route limits table with default + /search override (tests green, not yet load-verified)
2026-06-08T15:55:00Z,NOTE 001-4 OPEN: runtime-changeable limits decision (config-reload vs env vs admin endpoint) needs user input; hardcoded table interim -> DEBT-001-1
2026-06-09T10:15:00Z,BUG-001-1 observed: burst allows one extra request past capacity (off-by-one on refill rounding); logged, not yet fixed; next Section 3
