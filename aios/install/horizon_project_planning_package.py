#!/usr/bin/env python3
"""horizon_project_planning_package.py — install / uninstall / status for the
Horizon Agentic Project Planning package.

This is a SEPARATE package from the Horizon AIOS core. It deploys the /project-plan skill into a
Horizon AIOS instance and registers itself in the machine-local deployed-packages registry so the
AIOS sync can keep it backed up and updatable.

Cross-platform, standard-library only (Python 3.8+). Mirrors the horizon_aios_*.py tooling style but
uses the package-scoped horizon_project_planning_* name (it is not part of the OS core).

Subcommands:
  install     Deploy the skill + kit, inject the context pointer, and register the package.
  update      git-pull the deployment clone from its upstream, then re-deploy (install --force).
  uninstall   Reverse a deploy. Leaves the package clone and any scaffolded project plans in place.
  status      Print the registry and what is currently deployed.

Source model: the FACTORY CANON is the development checkout (the `projects/` repo), which publishes to
the upstream. A DEPLOYMENT is a clone of that upstream under $HORIZON_SYSTEM/deployed_packages/ that
tracks it. `update` is the deployment side of the loop: canon -> upstream (push) -> deployment (pull).

Locations (resolved from env, overridable with --horizon-root):
  HORIZON_ROOT         AIOS root
  HORIZON_SYSTEM       <root>/horizon_system         (expected clone home: <system>/deployed_packages/)
  HORIZON_ETC          <system>/ai_os_etc            (registry + packages context file live here)
  HORIZON_SKILLS_BIN   <system>/skills_bin           (skill deploy target)

Context injection target: `$HORIZON_ETC/horizon_aios_options_packages.local.md` — a root-scope,
machine-local file imported by the OS root `agents.md`, so every agent (not just project-scope ones)
sees this package is installed. On `install`/`update` the installer also migrates away a stale block
left by older versions at `$HORIZON_ROOT/projects/agents.md` (the previous injection target).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PACKAGE_NAME = "horizon_agentic_project_planning"
SKILL_NAME = "project-plan"
# Canonical upstream for this package — where deployments pull updates from and clone by default.
DEFAULT_UPSTREAM = "https://github.com/HorizonBrute/HorizonBrute-Horizon_Lightweight_Agentic_Project_Plans_LAPP"
REGISTRY_NAME = "horizon_deployed_packages.local.json"
REGISTRY_SCHEMA = "horizon_deployed_packages/v1"
ADMIN_GUIDE_NAME = "horizon_project_planning_guide.local.md"
PACKAGES_CONTEXT_NAME = "horizon_aios_options_packages.local.md"
PACKAGES_CONTEXT_HEADER = (
    "<!-- MACHINE-LOCAL — per-package context pointers, concatenated here by each installed\n"
    "     options package's installer. Managed by package installers; do not hand-edit. Imported\n"
    "     by the OS root agents.md so every agent, in every scope, sees what optional capability\n"
    "     this machine has installed. -->\n\n"
)
CONTEXT_MARKER = "horizon-agentic-project-planning"
BEGIN_MARKER = f"<!-- BEGIN {CONTEXT_MARKER}"
END_MARKER = f"<!-- END {CONTEXT_MARKER} -->"
INDEX_ROW = (
    f"| {SKILL_NAME} | `/{SKILL_NAME}` | `#midcost` | "
    "Scaffold and manage multi-session project plans (living docs: "
    "detail/status/archive/orientation/action-log/bugs); new / manage / close / status |"
)


# --------------------------------------------------------------------------- helpers
def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def die(msg: str) -> "None":
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def package_root() -> Path:
    # this file is <pkg>/aios/install/horizon_project_planning_package.py
    return Path(__file__).resolve().parents[2]


def resolve_paths(horizon_root: "str | None") -> dict:
    root = horizon_root or os.environ.get("HORIZON_ROOT")
    if not root:
        die("HORIZON_ROOT is not set and --horizon-root was not supplied.")
    root_p = Path(root).expanduser().resolve()
    if not root_p.is_dir():
        die(f"HORIZON_ROOT does not exist: {root_p}")
    system = Path(os.environ.get("HORIZON_SYSTEM") or root_p / "horizon_system").resolve()
    etc = Path(os.environ.get("HORIZON_ETC") or system / "ai_os_etc").resolve()
    skills_bin = Path(os.environ.get("HORIZON_SKILLS_BIN") or system / "skills_bin").resolve()
    return {
        "root": root_p,
        "system": system,
        "etc": etc,
        "skills_bin": skills_bin,
        "registry": etc / REGISTRY_NAME,
        "skills_index": skills_bin / "index.md",
        "skills_index_local": skills_bin / "index.local.md",
        "packages_context_file": etc / PACKAGES_CONTEXT_NAME,
        "legacy_agents_file": root_p / "projects" / "agents.md",
        "skill_dest": skills_bin / SKILL_NAME,
    }


def rel_to_root(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def git_remotes(repo: Path) -> list:
    """Return [{name,url}] for the package clone, or [] if not a git repo / git absent."""
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "remote", "-v"],
            capture_output=True, text=True, check=False,
        )
    except (OSError, FileNotFoundError):
        return []
    seen, remotes = set(), []
    for line in out.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0] not in seen:
            seen.add(parts[0])
            remotes.append({"name": parts[0], "url": parts[1]})
    return remotes


def ensure_gitignored(path: Path) -> str:
    """Make `path` git-ignored in its containing repo via .git/info/exclude (machine-local,
    never synced, never touches the tracked .gitignore that the official lane overwrites).

    Returns a short status string. No-op if git is absent, the path is outside a repo, or it is
    already ignored by an existing rule.
    """
    try:
        top = subprocess.run(
            ["git", "-C", str(path.parent), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=False,
        )
    except (OSError, FileNotFoundError):
        return "no-git"
    if top.returncode != 0 or not top.stdout.strip():
        return "not-in-repo"
    repo = Path(top.stdout.strip())
    already = subprocess.run(
        ["git", "-C", str(repo), "check-ignore", "-q", str(path)],
        capture_output=True, text=True, check=False,
    )
    if already.returncode == 0:
        return "already-ignored"
    try:
        rel = path.resolve().relative_to(repo.resolve()).as_posix()
    except ValueError:
        return "outside-repo"
    exclude = repo / ".git" / "info" / "exclude"
    exclude.parent.mkdir(parents=True, exist_ok=True)
    existing = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
    if rel in existing.splitlines():
        return "already-excluded"
    with exclude.open("a", encoding="utf-8", newline="\n") as fh:
        if existing and not existing.endswith("\n"):
            fh.write("\n")
        fh.write(f"# horizon_agentic_project_planning (machine-local .local. override)\n{rel}\n")
    return "excluded"


def strip_marker_block(path: Path) -> bool:
    """Remove this package's BEGIN/END marker block from `path` if present. Returns True if a block
    was stripped, False if `path` is absent or carries no block (safe no-op either way)."""
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    if BEGIN_MARKER not in text:
        return False
    out, skip = [], False
    for ln in text.splitlines():
        if BEGIN_MARKER in ln:
            skip = True
            continue
        if skip:
            if END_MARKER in ln:
                skip = False
            continue
        out.append(ln)
    while out and out[-1].strip() == "":
        out.pop()
    path.write_text("\n".join(out) + "\n" if out else "", encoding="utf-8")
    return True


def is_deployment_clone(pkg: Path, system: Path) -> bool:
    """True if this clone lives under $HORIZON_SYSTEM/deployed_packages/ (a DEPLOYMENT), as opposed
    to the development checkout (the FACTORY CANON, e.g. the projects/ repo)."""
    dp = (system / "deployed_packages").resolve()
    try:
        pkg.resolve().relative_to(dp)
        return True
    except ValueError:
        return False


def configure_pull_only(pkg: Path) -> str:
    """Make a deployment clone PULL-ONLY: it may fetch/pull from upstream but must never push.
    The developer publishes from the canon; a deployment is a read-only mirror. Implemented by
    pointing the push URL at a sentinel that fails fast with a clear message."""
    sentinel = "DISABLED-pull-only-deployment"
    remotes = git_remotes(pkg)
    if not remotes:
        return "no-remote"
    name = remotes[0]["name"]
    res = subprocess.run(
        ["git", "-C", str(pkg), "remote", "set-url", "--push", name, sentinel],
        capture_output=True, text=True, check=False,
    )
    return "pull-only" if res.returncode == 0 else f"failed:{res.stderr.strip()}"


def read_registry(registry: Path) -> dict:
    if registry.exists():
        try:
            data = json.loads(registry.read_text(encoding="utf-8"))
            data.setdefault("schema", REGISTRY_SCHEMA)
            data.setdefault("packages", [])
            return data
        except (json.JSONDecodeError, OSError) as exc:
            die(f"registry is present but unreadable ({exc}); fix or remove {registry}")
    return {"schema": REGISTRY_SCHEMA, "packages": []}


def write_registry(registry: Path, data: dict) -> None:
    data["updated_utc"] = now_utc()
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- install
def _source_index_header(index_md: Path):
    """Return [header_row, separator_row] from the tracked skills index so the machine-local
    index.local.md mirrors its columns EXACTLY. None if the index/header is unavailable."""
    if not index_md.exists():
        return None
    lines = index_md.read_text(encoding="utf-8").splitlines()
    for i, ln in enumerate(lines[:-1]):
        if ln.lstrip().startswith("|") and lines[i + 1].lstrip().startswith("|---"):
            return [ln, lines[i + 1]]
    return None


def cmd_install(args) -> None:
    p = resolve_paths(args.horizon_root)
    pkg = package_root()
    if not p["skills_bin"].is_dir():
        die(f"skills_bin not found: {p['skills_bin']}")

    print(f"Installing '{PACKAGE_NAME}' -> {p['skills_bin']}")

    # 1. skill payload (SKILL.md + kit/ = a copy of core/)
    dest = p["skill_dest"]
    if dest.exists() and not args.force:
        die(f"already deployed at {dest}; re-run with --force, or run uninstall first.")
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    shutil.copy2(pkg / "aios" / "skill" / SKILL_NAME / "SKILL.md", dest / "SKILL.md")
    shutil.copytree(pkg / "core", dest / "kit")
    print("  - copied SKILL.md and kit/ (core templates + lifecycle specs)")

    # 2. skills_bin catalog row -> machine-local index.local.md (untracked; the official
    #    (overwrite) lane never reverts it, so the registration survives OS updates). Its
    #    columns mirror the tracked skills_bin/index.md EXACTLY (header sourced from it).
    idx = p["skills_index"]
    local_idx = p["skills_index_local"]
    if not local_idx.exists():
        header = _source_index_header(idx)
        if header is None:
            print("  ! skills_bin/index.md header unavailable; skipped catalog registration")
        else:
            comment = (
                "<!-- MACHINE-LOCAL options-package skills catalog — admin-editable; "
                "not overwritten by AIOS sync (official lane). Columns mirror skills_bin/index.md. -->"
            )
            with local_idx.open("w", encoding="utf-8", newline="\n") as fh:
                fh.write(comment + "\n")
                fh.write(header[0] + "\n")
                fh.write(header[1] + "\n")
                fh.write(INDEX_ROW + "\n")
            print("  - created index.local.md and added catalog row")
    else:
        text = local_idx.read_text(encoding="utf-8")
        if f"| {SKILL_NAME} |" not in text:
            with local_idx.open("a", encoding="utf-8", newline="\n") as fh:
                if not text.endswith("\n"):
                    fh.write("\n")
                fh.write(INDEX_ROW + "\n")
            print("  - added row to index.local.md")
        else:
            print("  - index.local.md row already present (skipped)")
    if local_idx.exists():
        ensure_gitignored(local_idx)

    # 3. terse context pointer -> the machine-local, root-scope packages context file (idempotent,
    #    marker-delimited). This file is imported by the OS root agents.md, so every agent — not
    #    just project-scope ones — discovers the package.
    ctx_file = p["packages_context_file"]
    pointer = (pkg / "aios" / "install" / "context_pointer.md").read_text(encoding="utf-8")

    # 3a. migration: strip a stale same-marker block left by older versions at the OLD injection
    #     target (projects/agents.md) so an upgraded machine never carries the block twice. Runs on
    #     both install and update (cmd_update re-invokes cmd_install). Safe no-op if absent.
    if strip_marker_block(p["legacy_agents_file"]):
        print(f"  - migrated: stripped legacy context pointer from {p['legacy_agents_file']}")

    if not ctx_file.exists():
        ctx_file.parent.mkdir(parents=True, exist_ok=True)
        ctx_file.write_text(PACKAGES_CONTEXT_HEADER, encoding="utf-8")
        print(f"  - created {ctx_file.name}")

    text = ctx_file.read_text(encoding="utf-8")
    if BEGIN_MARKER not in text:
        with ctx_file.open("a", encoding="utf-8", newline="\n") as fh:
            if not text.endswith("\n"):
                fh.write("\n")
            fh.write("\n" + pointer.rstrip() + "\n")
        print(f"  - injected context pointer into {ctx_file.name}")
    else:
        print("  - context pointer already present (skipped)")
    ensure_gitignored(ctx_file)

    # 4. system-wide admin override guide (.local.) — materialized once, admin-editable.
    #    Used as the default guide when scaffolding new plans on this machine. Never clobbered
    #    by package updates or sync; delete it to fall back to the shipped default.
    admin_guide = p["etc"] / ADMIN_GUIDE_NAME
    canon_guide = pkg / "core" / "templates" / "PROJECT_PLAN_GUIDE.md"
    if not admin_guide.exists():
        banner = (
            "<!-- ADMIN-EDITABLE — SYSTEM-WIDE PROJECT-PLAN GUIDE (.local. override).\n"
            "     This machine-local copy is used as the default PROJECT_PLAN_GUIDE.md when\n"
            "     scaffolding new project plans on this machine. Edit freely to change the\n"
            "     system-wide project-plan rules; it is never overwritten by package updates\n"
            "     or by the AIOS sync. Delete it to fall back to the package's shipped default.\n"
            "     A single project/folder can override this further with its own\n"
            "     PROJECT_PLAN_GUIDE.local.md referenced from that folder's agents.md. -->\n\n"
        )
        admin_guide.parent.mkdir(parents=True, exist_ok=True)
        admin_guide.write_text(banner + canon_guide.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"  - materialized admin override guide: {admin_guide.name} (edit to customize system-wide)")
    else:
        print(f"  - admin override guide already present; left as-is ({admin_guide.name})")
    # keep the machine-local .local. override out of git (via .git/info/exclude, not tracked .gitignore)
    state = ensure_gitignored(admin_guide)
    print(f"  - gitignore ({admin_guide.name}): {state}")
    ensure_gitignored(p["registry"])  # registry too (already covered by *.local.json canon rule)

    # 4b. a DEPLOYMENT clone is a pull-only mirror of canon — allow fetch/pull, forbid push.
    #     The development checkout (factory canon) is left push-enabled.
    deployment = is_deployment_clone(pkg, p["system"])
    pull_only = False
    if deployment:
        st = configure_pull_only(pkg)
        pull_only = st == "pull-only"
        print(f"  - deployment clone: push {'DISABLED (pull-only)' if pull_only else st}")
    else:
        print("  - development checkout (factory canon): push left enabled")

    # 5. register in the machine-local deployed-packages registry
    data = read_registry(p["registry"])
    entry = {
        "name": PACKAGE_NAME,
        "version": (pkg / "VERSION").read_text(encoding="utf-8").strip()
        if (pkg / "VERSION").exists() else "unknown",
        "clone_path": rel_to_root(pkg, p["root"]),
        "upstream": DEFAULT_UPSTREAM,
        "remotes": git_remotes(pkg) or [{"name": "origin", "url": DEFAULT_UPSTREAM}],
        "role": "deployment" if deployment else "development-canon",
        "pull_only": pull_only,
        "sync": True,
        # Entrypoint the AIOS sync invokes to update this package: `python <clone>/<entrypoint> update`.
        # This is how registering a package ADDS it to the AIOS sync's options-package update pass.
        "install_entrypoint": Path(__file__).resolve().relative_to(pkg).as_posix(),
        "installed_utc": now_utc(),
        "updated_utc": now_utc(),
        "payload": {
            "skill_dir": rel_to_root(dest, p["root"]),
            "skills_index_file": rel_to_root(local_idx, p["root"]),
            "context_block_file": rel_to_root(ctx_file, p["root"]),
            "context_block_marker": CONTEXT_MARKER,
            "admin_guide_file": rel_to_root(admin_guide, p["root"]),
        },
    }
    others = [pk for pk in data["packages"] if pk.get("name") != PACKAGE_NAME]
    prior = next((pk for pk in data["packages"] if pk.get("name") == PACKAGE_NAME), None)
    if prior and prior.get("installed_utc"):
        entry["installed_utc"] = prior["installed_utc"]
    data["packages"] = others + [entry]
    write_registry(p["registry"], data)
    print(f"  - registered in {p['registry'].name}"
          f" (clone_path={entry['clone_path']}, remotes={len(entry['remotes'])})")

    print(f"Done. Restart Claude Code, then use /{SKILL_NAME} in any project.")
    if rel_to_root(pkg, p["root"]) == pkg.resolve().as_posix():
        print("  note: this package clone is OUTSIDE $HORIZON_ROOT; for sync coverage clone it to "
              f"$HORIZON_SYSTEM/deployed_packages/{PACKAGE_NAME}/ and re-run install.")


# --------------------------------------------------------------------------- uninstall
def cmd_uninstall(args) -> None:
    p = resolve_paths(args.horizon_root)
    print(f"Uninstalling '{PACKAGE_NAME}' from {p['skills_bin']}")

    if p["skill_dest"].exists():
        shutil.rmtree(p["skill_dest"])
        print(f"  - removed {p['skill_dest']}")
    else:
        print("  - skill payload not present (skipped)")

    idx = p["skills_index_local"]
    if idx.exists():
        lines = idx.read_text(encoding="utf-8").splitlines()
        kept = [ln for ln in lines if f"| {SKILL_NAME} |" not in ln]
        if len(kept) != len(lines):
            idx.write_text("\n".join(kept) + "\n", encoding="utf-8")
            print("  - removed row from index.local.md")
        else:
            print("  - no index.local.md row found (skipped)")

    ctx_file = p["packages_context_file"]
    if strip_marker_block(ctx_file):
        print(f"  - stripped context pointer from {ctx_file.name}")
    else:
        print("  - no context pointer block found (skipped)")
    # also clean up any stale block left at the pre-migration location, in case install/update was
    # never re-run on this machine after the retarget.
    if strip_marker_block(p["legacy_agents_file"]):
        print(f"  - stripped legacy context pointer from {p['legacy_agents_file']}")

    if p["registry"].exists():
        data = read_registry(p["registry"])
        before = len(data["packages"])
        data["packages"] = [pk for pk in data["packages"] if pk.get("name") != PACKAGE_NAME]
        if len(data["packages"]) != before:
            write_registry(p["registry"], data)
            print(f"  - deregistered from {p['registry'].name}")
        else:
            print("  - not in registry (skipped)")

    admin_guide = p["etc"] / ADMIN_GUIDE_NAME
    if admin_guide.exists():
        print(f"  - kept admin override guide {admin_guide.name} (admin content; delete manually if unwanted)")
    print("Done. The package clone and any scaffolded project plans are untouched (self-contained).")


# --------------------------------------------------------------------------- update
def cmd_update(args) -> None:
    """Pull the deployment clone from its upstream, then re-deploy. The deployment side of the
    canon -> upstream -> deployment loop. Run this from a deployed clone (has a git remote)."""
    pkg = package_root()
    remotes = git_remotes(pkg)
    if not remotes:
        die(f"{pkg} has no git remote to pull from. This command runs on a DEPLOYMENT clone "
            f"(cloned from the upstream), not a detached copy.")
    print(f"Updating deployment at {pkg} (upstream authoritative - local changes overwritten)")
    up = subprocess.run(
        ["git", "-C", str(pkg), "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
        capture_output=True, text=True, check=False,
    )
    upstream_ref = up.stdout.strip() if up.returncode == 0 else f"{remotes[0]['name']}/HEAD"
    fetch = subprocess.run(["git", "-C", str(pkg), "fetch", "--prune"],
                           capture_output=True, text=True, check=False)
    if fetch.returncode != 0:
        die(f"git fetch failed: {fetch.stderr.strip()}")
    reset = subprocess.run(["git", "-C", str(pkg), "reset", "--hard", upstream_ref],
                           capture_output=True, text=True, check=False)
    out = (reset.stdout + reset.stderr).strip()
    if out:
        print("  " + out.replace("\n", "\n  "))
    if reset.returncode != 0:
        die(f"git reset to {upstream_ref} failed: {reset.stderr.strip()}")
    print("  - overwritten from upstream; re-deploying ...")
    args.force = True
    cmd_install(args)


# --------------------------------------------------------------------------- status
def cmd_status(args) -> None:
    p = resolve_paths(args.horizon_root)
    print(f"HORIZON_ROOT : {p['root']}")
    print(f"registry     : {p['registry']}"
          + ("" if p["registry"].exists() else "  (absent)"))
    print(f"skill deploy : {p['skill_dest']}"
          + ("  [present]" if p["skill_dest"].exists() else "  [absent]"))
    admin_guide = p["etc"] / ADMIN_GUIDE_NAME
    print(f"admin guide  : {admin_guide}"
          + ("  [present]" if admin_guide.exists() else "  [absent]"))
    ctx_file = p["packages_context_file"]
    if not ctx_file.exists():
        ctx_state = "[absent]"
    elif BEGIN_MARKER in ctx_file.read_text(encoding="utf-8"):
        ctx_state = "[block present]"
    else:
        ctx_state = "[file present, no block]"
    print(f"context file : {ctx_file}  {ctx_state}")
    legacy = p["legacy_agents_file"]
    if legacy.exists() and BEGIN_MARKER in legacy.read_text(encoding="utf-8"):
        print(f"  ! stale legacy block still present at {legacy} — re-run install/update to migrate")
    if p["registry"].exists():
        data = read_registry(p["registry"])
        print(f"registry schema: {data.get('schema')}  updated: {data.get('updated_utc','?')}")
        if not data["packages"]:
            print("  (no packages registered)")
        for pk in data["packages"]:
            remotes = ", ".join(r.get("url", "?") for r in pk.get("remotes", [])) or "none"
            print(f"  - {pk['name']} v{pk.get('version','?')}  sync={pk.get('sync')}  "
                  f"role={pk.get('role','?')}  pull_only={pk.get('pull_only', '?')}")
            print(f"      clone   : {pk.get('clone_path')}")
            print(f"      upstream: {pk.get('upstream','(none)')}")
            print(f"      remotes : {remotes}")


# --------------------------------------------------------------------------- main
def main() -> None:
    ap = argparse.ArgumentParser(description="Install/uninstall the Horizon Agentic Project Planning package.")
    ap.add_argument("--horizon-root", help="AIOS root (default: $HORIZON_ROOT).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn, extra in (
        ("install", cmd_install, True),
        ("update", cmd_update, False),
        ("uninstall", cmd_uninstall, False),
        ("status", cmd_status, False),
    ):
        sp = sub.add_parser(name)
        sp.add_argument("--horizon-root", help="AIOS root (default: $HORIZON_ROOT).")
        if extra:
            sp.add_argument("--force", action="store_true",
                            help="overwrite an existing deploy in place.")
        sp.set_defaults(func=fn)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
