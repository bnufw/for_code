#!/usr/bin/env python3
import argparse
import re
import shutil
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


def delete_target(path: Path) -> str:
    if not path.exists():
        return "missing"
    if path.is_dir():
        shutil.rmtree(path)
        return "removed-dir"
    path.unlink()
    return "removed-file"


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean failed idea artifacts recorded in .codex/active_idea.md")
    parser.add_argument("--active-file", default=".codex/active_idea.md", help="Path to the active idea markdown file")
    parser.add_argument("--execute", action="store_true", help="Actually delete paths instead of printing a dry run")
    args = parser.parse_args()

    active_file = Path(args.active_file)
    repo_root = Path.cwd()
    state = load_state(active_file)

    raw_targets = []
    log_file = state.get("log_file")
    if isinstance(log_file, str) and log_file.strip():
        raw_targets.append(log_file.strip())

    artifact_paths = state.get("artifact_paths") or []
    if not isinstance(artifact_paths, list):
        raise ValueError("artifact_paths must be a list")
    raw_targets.extend(str(item).strip() for item in artifact_paths if str(item).strip())

    seen = set()
    targets = []
    for raw in raw_targets:
        resolved = resolve_target(repo_root, raw)
        if resolved not in seen:
            seen.add(resolved)
            targets.append((raw, resolved))

    mode = "EXECUTE" if args.execute else "DRY_RUN"
    print(f"MODE={mode}")
    if not targets:
        print("No cleanup targets recorded.")
        return 0

    for raw, resolved in targets:
        if args.execute:
            status = delete_target(resolved)
        else:
            status = "would-remove" if resolved.exists() else "missing"
        print(f"{status}\t{raw}\t{resolved}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR\t{exc}", file=sys.stderr)
        raise
