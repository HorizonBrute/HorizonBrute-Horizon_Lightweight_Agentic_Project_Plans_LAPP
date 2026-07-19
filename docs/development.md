---
type: How-To
title: "Developing & Releasing LAPP"
description: The factory-canon → upstream → deployment model — where development happens, how it publishes, and how deployments track it as pull-only mirrors.
tags: [development, release, deployment, aios]
timestamp: 2026-07-19
status: draft
---

# Developing & Releasing LAPP

There are three roles in the lifecycle of this package. Keep them straight — they have different
permissions and different jobs.

| Role | Where | Git | Job |
|---|---|---|---|
| **Factory canon** | the development checkout (e.g. the `projects/…` repo) | origin = upstream, **push enabled** | where all changes are made and published |
| **Upstream** | the GitHub repo (`…LAPP`) | — | the distribution point; canon's `main` |
| **Deployment** | `$HORIZON_SYSTEM/deployed_packages/<name>/` on each install | origin = upstream, **push DISABLED (pull-only)** | a read-only mirror that runs the skill |

## The canon (single source of truth)

The **development checkout is the factory canon**. All edits — to `core/`, the skill, the installer,
the docs — happen there, and only there. It is a normal git repo with push enabled; you publish from it.
Do **not** develop in a deployment clone: `update` will overwrite it (see below).

## Publishing a change (canon → upstream)

From the canon checkout:

```bash
# edit core/ , aios/ , docs/ …
git add -A && git commit -s -m "…"
git push origin main            # publish to the upstream
```

That's the whole release: canon `main` → upstream `main`.

## Updating a deployment (upstream → deployment)

On a machine running a deployment, pull the new canon and re-deploy in one step:

```bash
python $HORIZON_SYSTEM/deployed_packages/<name>/aios/install/horizon_project_planning_package.py update
```

`update` is **upstream-authoritative**: it fetches and **hard-resets the deployment clone to upstream**
(local changes are overwritten — a deployment is a mirror, not a workspace), then re-runs
`install --force` to refresh the deployed skill/kit and the registry. Because the deployment is
configured **pull-only**, it can never accidentally push developer-side changes back to the upstream —
a `git push` from a deployment fails fast.

## Why deployments are pull-only

The developer is the only publisher. A deployment exists to *run* the skill and *receive* updates, never
to originate them. Making deployments pull-only (push URL pointed at a disabled sentinel) enforces the
one-way flow **canon → upstream → deployment** and removes any path for a deployment's incidental edits
(or an `update`'s reset) to reach the shared upstream. See ADR-0008.

## First-time deployment

```bash
git clone <upstream> "$HORIZON_SYSTEM/deployed_packages/horizon_agentic_project_planning"
python "$HORIZON_SYSTEM/deployed_packages/horizon_agentic_project_planning/aios/install/horizon_project_planning_package.py" install
```

`install` detects it is running under `deployed_packages/`, configures the clone pull-only, deploys the
skill, and registers the package (with `role: deployment`, `pull_only: true`). Running `install` from the
canon instead records `role: development-canon` and leaves push enabled.
