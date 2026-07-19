# Architecture Decision Records

Durable "why" behind the design of the Horizon Agentic Project Planning package. Each ADR is a single
decision: context, the decision, and its consequences. ADRs are append-only — a later ADR can supersede
an earlier one (note it in both).

These ADRs also dogfood the project-plan system's optional "ADR hook": a package that keeps decision
records, cross-referenced from its plans and notes.

| ADR | Title | Status |
|---|---|---|
| [0001](ADR-0001-dual-mode-package.md) | Dual-mode package: standalone core + optional AIOS wrapper | Accepted |
| [0002](ADR-0002-six-file-document-set.md) | Six-file living project-plan document set | Accepted |
| [0003](ADR-0003-python-cross-platform-installer.md) | Cross-platform Python installer, package-scoped namespace | Accepted |
| [0004](ADR-0004-deployed-packages-registry.md) | Deployed-packages registry + clone location | Accepted |
| [0005](ADR-0005-sync-gate-on-registry.md) | Gate the AIOS official sync lane on the registry | Accepted |
| [0006](ADR-0006-local-override-layers.md) | Three-tier `.local.` guide override | Accepted |
| [0007](ADR-0007-self-contained-projects.md) | Scaffolded projects are self-managing | Accepted |
