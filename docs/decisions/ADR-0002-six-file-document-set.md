---
type: decision
title: "ADR-0002 — Six-file living project-plan document set"
status: Accepted
timestamp: 2026-07-19
tags: [adr, document-model]
---

# ADR-0002 — Six-file living project-plan document set

## Status
Accepted (2026-07-19). Distilled from the SorceryPunk project-plan system.

## Context
A multi-session body of work needs more than one document: the plan of record drifts from live status,
which drifts from the decision trail, which drifts from the raw timeline. Folding all of that into one
file makes it unreadable and context-expensive; scattering it with no convention makes it
unreconstructable. The SorceryPunk system had already converged on a working shape; the task was to
generalize it and drop its host-specific couplings.

## Decision
Adopt a six-file set per project, sharing an `NNN_role-slug` prefix, plus a folder `index.md`:
**detail** (plan of record), **status** (live per-item + serialized `NOTE NNN-K`), **status_archive**
(retired verified blocks), **current_orientation** (cold-start, read instead of a handoff),
**action_log** (append-only postcard timeline, no frontmatter), **bugs_and_technical_debt** (cleared or
deferred-with-reason before close). Governing principles: doc-truth not code-truth; living
(update-in-place) not narrative; grep-able serialization; cold-start recoverability; nothing disappears
silently. Host integrations (ADRs, objectives, handoffs, branch-status docs) are **optional** — included
only when the target repo has them; otherwise `NOTE` entries are the self-contained decision record.

## Consequences
- Each concern has one home; the live status doc stays short because verified work is archived.
- One `grep` reconstructs any note/bug/decision thread.
- A resuming agent reads orientation → status → detail and needs no external handoff.
- More files per project than a single note — mitigated by scaffolding (the installer/skill or a copy)
  and by the folder `index.md`.
- Portability required stripping SorceryPunk's hard deps (its ADR dir, vocabulary file, governance) down
  to optional hooks (ADR-0001's "stands alone" requirement).
