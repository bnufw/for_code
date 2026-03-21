# Deep Learning Idea Workflow

## Purpose

This repository provides a compact Codex workflow for deep-learning baseline projects.
The goal is to search for oral-level ideas that:
- clearly outperform the baseline,
- stay organized around one main thesis,
- produce useful observations from experiments, and
- retain some theoretical value.

## Required Runtime Files

- `experience.md`: durable record of failed or exhausted ideas.
- `direction.md`: optional short direction note from the user.
- `.codex/baseline_commit.txt`: baseline git commit anchor for the current project.
- `.codex/active_idea.md`: current working state for one active idea.
- `.codex/logs/`: screen logs for the active run only.

## Skill Routing

Use exactly one of these entry skills for each stage:
- `$idea-discovery`: generate one repo-grounded idea.
- `$idea-execution`: implement the active idea, create one atomic code commit, and launch the formal run in `screen`.
- `$idea-review`: inspect results and decide whether to continue the same idea or terminate it and move on.

## Discovery Rules

1. Read local code, scripts, configs, results, and `experience.md` before asking anything.
2. Read `direction.md` only when it exists.
3. Prefer local evidence first. Use `repo-exa-scout` only when repo evidence is insufficient or when literature cross-check matters.
4. Prefer `mcp__exa__get_code_context_exa` and `mcp__exa__web_search_exa` for external search.
5. Ask at most one batched clarification round when mandatory inputs are missing.
6. Produce one idea only. Do not output a ranked list.

## Execution Rules

1. Read `.codex/active_idea.md` before editing code.
2. Touch only files needed for the active thesis.
3. Do not run tests, short smoke runs, or benchmark subsets.
4. Create one atomic code commit for each implementation pass.
5. Keep `.codex/logs/` out of commits.
6. Launch the formal run in `screen` and redirect all output to `.codex/logs/<idea-id>.log`.
7. Record every unique artifact path for the run inside `.codex/active_idea.md` so failed runs can be cleaned safely.

## Review Rules

1. Read `.codex/active_idea.md`, the screen log, result files, and relevant code diffs.
2. Use `result-judge` when result interpretation is non-trivial.
3. Decision must be one of: `continue`, `terminate`, or `wait`.
4. `continue`: update `.codex/active_idea.md`, define the next experiment, then either relaunch directly or route back to `$idea-execution` when code or config edits are required.
5. `terminate`: append a structured entry to `experience.md`, commit the experience note, show the baseline commit, revert all idea commits, and clean failed artifacts.
6. Failed logs and failed artifacts should be removed after the experience entry is secured.

## Git Rules

1. `.codex/baseline_commit.txt` is the source of truth for the rollback anchor.
2. Keep idea code changes in atomic commits.
3. Preserve `experience.md` updates in a note-only commit before reverting an idea.
4. Never rewrite unrelated history.

## Output Style

- User-facing responses should stay concise and in Chinese.
- Internal instructions, skill files, and agent files may stay in English for tool reliability.
