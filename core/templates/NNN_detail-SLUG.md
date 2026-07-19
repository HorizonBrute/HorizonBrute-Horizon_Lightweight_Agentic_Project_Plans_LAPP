---
type: project_plan
title: "Project NNN — [Project Title] (Plan Detail)"
description: [One-line description of the plan of record.]
tags: [project-plan, "[domain-tag]"]
timestamp: [YYYY-MM-DD]
status: draft
---

# Project NNN — [Project Title]

## Headline
[One line: the outcome this project delivers.]

## Executive summary
[One paragraph: the situation, the crux, the shape of the approach, and the load-bearing sequencing
decision if there is one.]

## Dependencies
1. **Upstream (this project depends on):** [none, or: Project MMM — <name> (<file>) — why.]
2. **Downstream (projects that depend on this one):** [none, or: Project PPP — <name> (<file>) — what
   state they need this project to reach first.]

## Relevant files
[Confirmed by trace on branch `[branch]` (`[YYYY-MM-DD]`). Name real files/functions; mark anything
unverified as (UNVERIFIED).]

- `[path/to/file]` — `[symbol]` ([what it does / why it matters here]).
- `[path/to/file]` — `[symbol]` ([…]).

## Relevant vocabulary / concepts
[Optional — keep if the domain has fixed meanings a reader must know. Point to where they're defined.]
- **[Term]** — [meaning / pointer].

---

## My Initial Brief
> Verbatim, as given by the user at project kickoff ([YYYY-MM-DD]). Not edited for grammar.

[PASTE THE USER'S BRIEF HERE, UNEDITED.]

---

## Your Initial Understanding From That Brief
> My reading after tracing the current code, grounded against [relevant decisions/docs].

1. [The crux, stated as one architectural fact.]
2. [How the pieces relate / what the fix mirrors.]
3. [Risks, invariants, sequencing constraints.]

---

## Plan

Each `### Section` below is a unit of work: the brief's items it covers plus the architectural context
that must shape the implementation. Status per item is tracked in `NNN_status-SLUG.md`.

### Section 1 — [Name]
- [Brief item this covers.]
- [Architectural context that must shape it.]
- Context: [why this is shaped the way it is; dependencies; sequencing.]

### Section 2 — [Name]
- [...]

## Cross-cutting invariants (do not violate)
[Optional — things no section may break.]
- [Invariant.]
