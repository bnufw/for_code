#!/usr/bin/env python3
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def load_state(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"No YAML frontmatter found in {path}")
    data = yaml.safe_load(match.group(1)) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Frontmatter in {path} must be a mapping")
    return data


def resolve_target(repo_root: Path, raw: str) -> Path:
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = (repo_root / candidate).resolve()
    else:
        candidate = candidate.resolve()

    repo_root_resolved = repo_root.resolve()
    if repo_root_resolved not in candidate.parents and candidate != repo_root_resolved:
        raise ValueError(f"Refusing to touch path outside repo root: {candidate}")
    return candidate


def relabel(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def delete_target(path: Path) -> str:
    if not path.exists():
        return "missing"
    if path.is_dir():
        shutil.rmtree(path)
        return "removed-dir"
    path.unlink()
    return "removed-file"


def is_tracked(repo_root: Path, path: Path) -> bool:
    rel = relabel(path, repo_root)
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", rel],
        cwd=repo_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def restore_tracked(repo_root: Path, path: Path) -> str:
    rel = relabel(path, repo_root)
    result = subprocess.run(
        ["git", "restore", "--worktree", "--", rel],
        cwd=repo_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git restore failed for {rel}")
    return "restored-tracked"


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean failed idea artifacts recorded in .codex/active_idea.md")
    parser.add_argument("--active-file", default=".codex/active_idea.md", help="Path to the active idea markdown file")
    parser.add_argument("--execute", action="store_true", help="Actually delete paths instead of printing a dry run")
    args = parser.parse_args()

    active_file = Path(args.active_file)
    repo_root = Path.cwd().resolve()
    state = load_state(active_file)

    restore_targets = []
    code_touchpoints = state.get("code_touchpoints") or []
    if not isinstance(code_touchpoints, list):
        raise ValueError("code_touchpoints must be a list")
    restore_targets.extend(str(item).strip() for item in code_touchpoints if str(item).strip())

    experiment_script = state.get("experiment_script")
    if isinstance(experiment_script, str) and experiment_script.strip():
        restore_targets.append(experiment_script.strip())

    artifact_targets = []
    log_file = state.get("log_file")
    if isinstance(log_file, str) and log_file.strip():
        artifact_targets.append(log_file.strip())

    artifact_paths = state.get("artifact_paths") or []
    if not isinstance(artifact_paths, list):
        raise ValueError("artifact_paths must be a list")
    artifact_targets.extend(str(item).strip() for item in artifact_paths if str(item).strip())

    mode = "EXECUTE" if args.execute else "DRY_RUN"
    print(f"MODE={mode}")

    seen_restore = set()
    for raw in restore_targets:
        path = resolve_target(repo_root, raw)
        if path in seen_restore:
            continue
        seen_restore.add(path)
        tracked = is_tracked(repo_root, path)
        if args.execute:
            status = restore_tracked(repo_root, path) if tracked else delete_target(path)
        else:
            status = "would-restore-tracked" if tracked else ("would-remove" if path.exists() else "missing")
        print(f"{status}\t{raw}\t{path}")

    seen_artifacts = set()
    for raw in artifact_targets:
        path = resolve_target(repo_root, raw)
        if path in seen_artifacts:
            continue
        seen_artifacts.add(path)
        if args.execute:
            status = delete_target(path)
        else:
            status = "would-remove" if path.exists() else "missing"
        print(f"{status}\t{raw}\t{path}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR\t{exc}", file=sys.stderr)
        raise
