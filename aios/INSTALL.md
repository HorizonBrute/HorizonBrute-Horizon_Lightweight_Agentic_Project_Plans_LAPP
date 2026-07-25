# Installing the project-plan feature into Horizon.AIOS

This is the **optional** Horizon.AIOS wrapper. The kit in `core/` already works standalone with no install —
this layer deploys it as a discoverable `/project-plan` skill inside a Horizon.AIOS instance, and
registers the package so the Horizon.AIOS sync keeps it protected and backed up.

Installer: **`aios/install/horizon_project_planning_package.py`** — cross-platform, standard-library
only (Python 3.8+). Subcommands: `install`, `uninstall`, `status`.

## Deployment model

A deployed package is a **git clone under `$HORIZON_SYSTEM/deployed_packages/<name>/`** (so it can pull
its own updates) plus a machine-local registry entry that the Horizon.AIOS sync reads.

```
$HORIZON_SYSTEM/
  deployed_packages/
    horizon_agentic_project_planning/   ← git clone (this package)
  skills_bin/
    project-plan/                        ← deployed by the installer
      SKILL.md
      kit/                               ← a copy of core/ (lifecycle specs + templates)
    index.local.md                       ← +1 catalog row (machine-local, untracked)
  ai_os_etc/
    horizon_deployed_packages.local.json ← the deployed-packages registry (machine-local)
```

## What `install` does (idempotent)

1. **Copies the skill payload** to `$HORIZON_SYSTEM/skills_bin/project-plan/`: `SKILL.md` + `kit/` (a
   full copy of `core/`), so the skill is self-contained on the target machine.
2. **Registers a catalog row** in the machine-local `$HORIZON_SYSTEM/skills_bin/index.local.md` (created from the tracked `index.md` header if absent, so columns match exactly; skips if present). Being untracked, this row is never reverted by the OS official (overwrite) lane, so the registration survives AIOS updates — the tracked `index.md` carries core skills only.
3. **Migrates, then injects, a terse context pointer** — a marker-delimited block from
   `install/context_pointer.md`. It is written to
   `$HORIZON_ETC/horizon_aios_options_packages.local.md` (created with a short header if absent), a
   root-scope, machine-local file that the OS root `agents.md` imports — so every agent, not just
   project-scope ones, discovers the feature. Before injecting, `install`/`update` first strip any
   stale same-marker block left at the pre-retarget location, `$HORIZON_ROOT/projects/agents.md`, so
   an upgraded machine never carries the block twice (safe no-op if that file has no block). Kept to
   ~5 lines to respect the Horizon.AIOS terseness budget. The file is git-ignored via the containing
   repo's `.git/info/exclude` (never the tracked `.gitignore`), so the official sync lane never
   reverts it.
4. **Registers the package** in `$HORIZON_ETC/horizon_deployed_packages.local.json`: name, version,
   `clone_path` (relative to `$HORIZON_ROOT`), the git `remotes` (incl. forks), `sync: true`, and a
   `payload` manifest (what it deployed, including `context_block_file`) for exact uninstall.

`uninstall` reverses steps 1–4, including stripping any lingering legacy block for a machine that
never ran `install`/`update` after the retarget. `status` prints the registry and what is deployed,
including whether a stale legacy block is still present.

## Registry ↔ sync integration

The Horizon.AIOS two-lane sync (`horizon_aios_sync.py`) reads this registry. Its **official lane** overwrites
everything except `projects/usrbin/brains` from upstream — which would otherwise clobber a package
that lives under the official-owned `horizon_system/`. The sync's `official_pathspec()` now **also
excludes every registered clone with `sync != false`**, so a deployed package is protected from the
overwrite lane. Each package clone is a nested git repo, so the nightly nested-repo sync backs it up
to its own remote automatically. Verify protection with:

```
python horizon_system/sbin/horizon_aios_sync.py --status
#   Deployed pkgs   : 1 protected from official overwrite (horizon_system/deployed_packages/...)
```

Set a package's `sync` to `false` in the registry to opt it out of protection.

## Run it

Clone the package to its deployed home, then run the installer from there:

```bash
git clone <package-remote> "$HORIZON_SYSTEM/deployed_packages/horizon_agentic_project_planning"
python "$HORIZON_SYSTEM/deployed_packages/horizon_agentic_project_planning/aios/install/horizon_project_planning_package.py" install
```

Windows/PowerShell is identical — it's the same Python entry point:

```powershell
python "$env:HORIZON_SYSTEM\deployed_packages\horizon_agentic_project_planning\aios\install\horizon_project_planning_package.py" install
```

Options: `--horizon-root PATH` (default `$HORIZON_ROOT`), `--force` (overwrite an existing deploy).
Then **restart Claude Code** (skills load at session start) and type `/project-plan` in any project.

## Uninstall

```
python .../aios/install/horizon_project_planning_package.py uninstall
```

Removes the skill, the index row, the context block, and the registry entry. **The package clone and
any project plans already scaffolded into target repos are left untouched** — each scaffolded folder
carries its own `PROJECT_PLAN_GUIDE.md`, so removing the feature never orphans live plans.

## Notes

- The registry is `*.local.json` → machine-local: gitignored from OS canon (never rides the official
  lane) yet carried by the hourly personal backup sync (its name matches the `*local*` re-include).
- The installer writes only inside `$HORIZON_SYSTEM/skills_bin`, `$HORIZON_ETC` (including the managed
  block in `horizon_aios_options_packages.local.md`), and — migration cleanup only, stripping the
  package's own stale block — `$HORIZON_ROOT/projects/agents.md`. It does not touch privileged
  system dirs.
- `#midcost` is the skill's model-preference group. Adjust via `/model-prefs-assign` if your routing
  differs.
