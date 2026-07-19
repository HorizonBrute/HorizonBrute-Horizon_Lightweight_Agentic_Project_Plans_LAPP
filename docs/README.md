# docs/

Documentation for the Horizon Agentic Project Planning package: the design, the decision record, and a
worked example.

## Contents

- **[`design/architecture.md`](design/architecture.md)** — how the package is structured: the standalone
  core, the optional AIOS wrapper, the installer, the deployed-packages registry, the sync gate, and the
  override layers.
- **[`decisions/`](decisions/index.md)** — Architecture Decision Records (ADRs) for the package itself:
  the "why" behind the dual-mode split, the document model, the Python installer, the registry, the sync
  gate, the `.local.` override layers, and self-containment. (These also dogfood the project-plan
  system's optional "ADR hook".)
- **[`examples/project_plans/`](examples/project_plans/)** — a filled-in sample project-plan folder.

## A worked example

[`examples/project_plans/`](examples/project_plans/) is a **filled-in sample project-plan folder** —
what a real `docs/project_plans/` looks like a few sessions into a project. It tracks a fictional
"add API rate limiting" effort and exercises every part of the system:

- **`index.md`** — the folder registry, listing project 001 and pointing at the guide.
- **`PROJECT_PLAN_GUIDE.md`** — the self-contained lifecycle guide copied in at scaffold time (this is
  what makes a scaffolded folder manageable without the package).
- **`001_detail-api_rate_limiting.md`** — the plan of record: headline, summary, dependencies, traced
  file map, the verbatim brief, the author's synthesis, and the sectioned plan.
- **`001_status-api_rate_limiting.md`** — live per-item status, a stubbed archived section, and
  serialized `NOTE 001-K` decisions (including an open decision).
- **`001_status_archive-api_rate_limiting.md`** — the verified Section 1 block, retired out of the
  live doc.
- **`001_current_orientation-api_rate_limiting.md`** — the cold-start "read instead of a handoff" doc.
- **`001_action_log-api_rate_limiting.md`** — the append-only postcard timeline.
- **`001_bugs_and_technical_debt-api_rate_limiting.md`** — one open bug and one deferred debt item.

Read it top-to-bottom the way a resuming agent would: orientation → status → detail. Then copy the
shape into your own `docs/project_plans/` (or let `/project-plan new` scaffold blank versions for you).

> The example is illustrative only — the file/function names in its "Relevant files" section refer to a
> fictional service, not this package.
