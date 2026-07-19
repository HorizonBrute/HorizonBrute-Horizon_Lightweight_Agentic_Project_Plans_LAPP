---
type: decision
title: "ADR-0005 — Gate the AIOS official sync lane on the deployed-packages registry"
status: Accepted
timestamp: 2026-07-19
tags: [adr, sync, aios, canon]
---

# ADR-0005 — Gate the AIOS official sync lane on the deployed-packages registry

## Status
Accepted (2026-07-19). Modifies AIOS canon (`horizon_system/sbin/horizon_aios_sync.py`).

## Context
A deployed package clone lives under `horizon_system/deployed_packages/<name>/` (ADR-0004), inside the
**official-owned** part of the tree. The two-lane sync's official lane overwrites everything except
`projects/usrbin/brains` from upstream via `official_pathspec()` (`git checkout <upstream> -- .` with
those excludes). A separately-versioned package in an official-owned dir is therefore at risk of being
clobbered by an upstream sync. The registry needed to be the authority for what is protected.

## Decision
Teach `official_pathspec()` to **also exclude every registered deployed-package clone with
`sync != false`**, read from `$HORIZON_ETC/horizon_deployed_packages.local.json`. Implementation is a
`deployed_package_excludes()` helper that is best-effort and fail-safe: a missing or malformed registry
yields no exclusions and never fails the sync; only in-tree relative paths are honored. The change is
additive (it can only *add* excludes, never cause an overwrite), and includes an INFO log line and a
`--status` report line. Landed in the devroot canon and pushed to `origin/master`.

## Consequences
- The registry genuinely gates the sync: an installed package is protected from the official overwrite
  lane; a package with `sync: false` opts out.
- Deployed packages are backed up by the nightly nested-repo sync (they are nested git repos) rather
  than by the root-repo lanes — the gate only *protects*, it does not push.
- This is a canon change owned by the OS core; it must ride the OS release process (devroot → upstream →
  pulled down by installs). Interim safety holds even without it: an untracked nested repo not present in
  the upstream ref is not deleted by a scoped `git checkout`.
