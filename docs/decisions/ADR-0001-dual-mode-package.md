---
type: decision
title: "ADR-0001 — Dual-mode package: standalone core + optional AIOS wrapper"
status: Accepted
timestamp: 2026-07-19
tags: [adr, architecture, packaging]
---

# ADR-0001 — Dual-mode package: standalone core + optional AIOS wrapper

## Status
Accepted (2026-07-19).

## Context
The project-plan system needed to serve two audiences at once: a plain repository with no Horizon AIOS
(an agent just reads a folder and manages plans), and a Horizon AIOS install where it should be a
discoverable, one-command feature. Building two products would duplicate the actual system; building
only the AIOS version would strand every non-AIOS user.

## Decision
Split the package into a **standalone `core/`** (the entire system: lifecycle specs + templates, zero
dependencies) and a **thin optional `aios/` wrapper** (a `/project-plan` skill + installer that deploys
`core/` and wires discovery). The boundary is one-directional: `core/` never references `aios/`. The
AIOS layer adds discovery, one-command scaffolding, and sync integration — never new behavior. When
installed, the wrapper carries a verbatim copy of `core/` as its `kit/`.

## Consequences
- The same kit works in any repo and inside AIOS; no divergence.
- Any behavior change happens in `core/` once; the wrapper is mechanical.
- Slight duplication: the installer copies `core/` into the deployed skill dir (acceptable — it makes
  the deployed skill self-contained on the target machine).
- Docs must state both usage modes so neither audience is confused about dependencies.
