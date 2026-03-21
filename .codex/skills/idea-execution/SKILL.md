---
name: idea-execution
description: Implement the active deep-learning idea from .codex/active_idea.md, create one atomic code commit, and launch the formal training command in screen with log capture, without running tests or smoke runs.
metadata:
  short-description: "Implement and launch one DL idea"
---

# Idea Execution

## When to use

Use this skill after `idea-discovery` has written `.codex/active_idea.md`, or after `idea-review` has updated the same file with a follow-up refinement plan that requires code or config edits.

## Read first

Always inspect:
- `.codex/active_idea.md`
- `.codex/baseline_commit.txt`
- the files listed in `code_touchpoints`
- any existing result directory or log path already recorded for the active idea

## Hard rules

- Do not run tests.
- Do not run smoke runs, short benchmarks, or reduced-epoch probes.
- Modify only files required by the active thesis.
- Create exactly one atomic code commit for the current implementation pass.
- Keep `.codex/logs/` out of commits.
- Use the formal command from `.codex/active_idea.md`.
- If `train_command` is empty, stop and report the missing field.

## Commit discipline

1. Inspect `git status --short` before editing.
2. Stage only code and config files for the current implementation pass.
3. Do not stage `.codex/logs/*`.
4. Prefer leaving `.codex/active_idea.md` unstaged in the idea code commit.
5. Do not stage unrelated local modifications.
6. After committing, append the new commit hash to `idea_commits` and set `latest_idea_commit` in `.codex/active_idea.md`.

## Launch rule

After the code commit is created:
1. Set `status: running` in `.codex/active_idea.md`.
2. Set `log_file` to `.codex/logs/<idea-id>.log`.
3. Record every idea-specific artifact path that should be deleted if the idea is terminated.
4. Request sandbox-external permission.
5. Launch the formal run with:

```bash
bash .codex/skills/idea-execution/scripts/launch_screen_run.sh \
  "<idea-id>" \
  ".codex/logs/<idea-id>.log" \
  "<train_command>"
```

6. Copy the returned `SCREEN_SESSION` value into `.codex/active_idea.md`.

## Failure handling

- If the launch command fails before the detached session is created, remove the empty log file and leave the run state as `planned`.
- If the command starts successfully, leave result inspection to `idea-review`.
- If a stale `screen_session` is still alive for the same idea, stop and resolve it before launching a new run.

## Output contract

The user-facing summary should contain:
- touched files
- new commit hash
- screen session name
- log path
- artifact paths recorded for later cleanup
