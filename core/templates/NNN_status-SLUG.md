---
type: project_plan
title: "Project NNN — [Project Title] (Status)"
description: Live per-item status for Project NNN, plus serialized objective notes and mini-decisions.
tags: [project-plan, status, "[domain-tag]"]
timestamp: [YYYY-MM-DD]
status: draft
---

# Project NNN — Status

Plan detail: `NNN_detail-SLUG.md`.
Orientation (read this instead of a handoff): `NNN_current_orientation-SLUG.md`.

**Status legend:** `NOT STARTED` · `IN PROGRESS` · `BLOCKED` · `DONE` · `VERIFIED`.
Keep each item's status current as work lands. When a whole Section reaches `VERIFIED`, move its block
into `NNN_status_archive-SLUG.md` and leave a one-line stub pointing to the archive.

---

## Section 1 — [Name]
**Status:** NOT STARTED

### 1.1 [Item]
**Status:** NOT STARTED

### 1.2 [Item]
**Status:** NOT STARTED · **Depends:** [x.y]

---

## Section 2 — [Name]
**Status:** NOT STARTED

---

# Objective Notes & Mini-Decisions (serialized)

Append-only, newest at the bottom. One `NOTE NNN-K` per decision/update. Grep-able:
- Find all notes: `grep "NOTE NNN-"`.
- (If the repo uses ADRs) find notes tied to a real ADR: `grep "ADR: ADR-00"`.

Template:
```
## NOTE NNN-K | YYYY-MM-DD | <short title>
- Status: OPEN | RESOLVED | SUPERSEDED-BY-NOTE-NNN-J | SUPERSEDED-BY-ADR
- ADR: none (self-contained) | ADR-00NN
- Sections: <e.g. 1.1, 4.3>
- Context: <the forces / situation>
- Decision/Update: <what was decided or what changed>
```

## NOTE NNN-1 | [YYYY-MM-DD] | [Kickoff decision or open question]
- Status: OPEN
- ADR: none (self-contained)
- Sections: [x.y]
- Context: [...]
- Decision/Update: [...]
