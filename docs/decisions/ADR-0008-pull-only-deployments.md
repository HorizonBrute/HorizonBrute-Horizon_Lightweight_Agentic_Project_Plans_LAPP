---
type: decision
title: "ADR-0008 — Deployments are pull-only mirrors of the factory canon"
status: Accepted
timestamp: 2026-07-19
tags: [adr, deployment, release, git]
---

# ADR-0008 — Deployments are pull-only mirrors of the factory canon

## Status
Accepted (2026-07-19).

## Context
The package is developed in a factory-canon checkout (the `projects/…` repo) that publishes to the
upstream GitHub repo, and installed as a clone under `$HORIZON_SYSTEM/deployed_packages/<name>/` that
tracks the same upstream. Both clones have `origin` pointing at the upstream. Without a guard, a
deployment could push — sending incidental edits (or the result of an `update` reset) back to the shared
upstream and corrupting canon. The developer is the sole publisher.

## Decision
A deployment clone is **pull-only**: it may fetch/pull, but **push is disabled** (the installer points
the remote's push URL at a `DISABLED-pull-only-deployment` sentinel that fails fast). Updates are
**upstream-authoritative**: `update` does `git fetch` + `git reset --hard <upstream>` (local overwritten)
then re-deploys — a deployment is a mirror, not a workspace. The installer distinguishes the two roles by
path: a clone under `deployed_packages/` is a deployment (pull-only, `role: deployment`); anything else is
the development canon (push left enabled, `role: development-canon`). The registry records `role` and
`pull_only`.

## Consequences
- One-way flow is enforced: canon → upstream (push) → deployment (pull). No deployment can publish.
- `update` on a deployment is safe and idempotent: it can always take upstream cleanly because it never
  has to reconcile local commits.
- A developer must not treat a deployment clone as a workspace — `update` will discard local edits there.
  Develop in the canon.
- The heuristic is path-based (`deployed_packages/`). A canon checkout placed under that path would be
  misclassified; keep canon out of `deployed_packages/`.
