---
type: decision
title: "ADR-0007 — Scaffolded projects are self-managing"
status: Accepted
timestamp: 2026-07-19
tags: [adr, self-containment]
---

# ADR-0007 — Scaffolded projects are self-managing

## Status
Accepted (2026-07-19).

## Context
A project plan is scaffolded into a target repository and then lived in for weeks. If managing it
required continually re-reading this package (its lifecycle specs, its closing rules), the plan would be
hostage to the package's presence and location — and uninstalling the package, or using it on a machine
that never had it, would orphan the plan.

## Decision
At scaffold time, copy the resolved `PROJECT_PLAN_GUIDE.md` (a single self-contained doc covering setup
recap, standing upkeep rules, and the closing checklist) into the target project's plans folder. From
then on, the target manages its plans from that file plus its own `index.md`. The package is needed only
to scaffold the *next* project, never to run an existing one. Consequently, `uninstall` deliberately
leaves scaffolded plans (and the admin override) untouched.

## Consequences
- A project plan is portable and durable: it travels with its repo and survives package removal.
- The closing spec (a first-class part of the guide) means a project can be wound down to a clean,
  audited rest state from inside the target alone.
- One copy of the guide per folder is slight duplication across many projects — acceptable for the
  self-containment guarantee, and it lets a folder pin an older guide if it wants.
- The guide is itself overridable per folder (ADR-0006), so self-containment does not mean rigidity.
