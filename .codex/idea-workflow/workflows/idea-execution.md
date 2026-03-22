# Idea Execution Workflow

## Goal

Implement the current formal batch described in `.codex/active_idea.md`, create or update exactly one new experiment script for that batch, disclose the batch with `request_user_input`, and launch the formal run in `screen`.

## When To Use

Use this workflow after:
- `idea-discovery` has written the first batch, or
- `idea-review` has produced an `improve` result and rewritten the next batch.

## Read First

Always inspect:
- `.codex/active_idea.md`
- `.codex/baseline_commit.txt`
- the files listed in `code_touchpoints`
- the `Planned Code Changes` section
- the `Current Batch` section
- any existing result directory or log file already recorded for the active idea

## Hard Rules

- Do not run tests.
- Do not run smoke runs, short benchmarks, or reduced-epoch probes.
- Modify only files required by the active thesis.
- Create or update exactly one new experiment script for the current batch.
- Keep `.codex/logs/` out of commits.
- Keep `code_touchpoints`, `experiment_script`, and `artifact_paths` accurate enough to drop the batch cleanly if the idea later proves useless.
- Use the formal command from `.codex/active_idea.md`.
- Use `Current Batch` as the source of truth for the experiment list and batch analysis items.
- Do not create a git commit during implementation or launch.
- If `train_command` is empty, stop and report the missing field.
- If `experiment_script` is empty, stop and report the missing field.
- If `Current Batch` does not clearly specify the formal experiments or batch analysis items, stop and report the missing section.

## Batch Discipline

1. Inspect `git status --short` before editing.
2. Keep `code_touchpoints` current for every tracked file edited by the batch.
3. Put the batch logic into one new experiment script such as `scripts/run_<idea-id>_b01.sh`.
4. Keep `Current Batch` aligned with the script path, experiment list, and batch analysis items.
5. If the batch later fails before any commit, drop tracked code changes with `git restore -- <code_touchpoints>` and remove the new experiment script if it is untracked.

## Launch Rule

After the code and experiment script are ready:
1. Set `status: planned` in `.codex/active_idea.md`.
2. Set `review_outcome: pending` in `.codex/active_idea.md`.
3. Set `log_file` to `.codex/logs/<idea-id>.log`.
4. Record every idea-specific artifact path that should be deleted if the idea is later abandoned.
5. Use one `request_user_input` round to disclose:
   - how many formal experiments will run,
   - which experiment script will run,
   - the exact experiment list from `Current Batch`,
   - the batch analysis items from `Current Batch`.
6. If the user does not confirm the batch, stop and leave the idea in `planned`.
7. Request sandbox-external permission.
8. Launch the formal run with:

```bash
bash .codex/skills/idea-execution/scripts/launch_screen_run.sh   "<idea-id>"   ".codex/logs/<idea-id>.log"   "<train_command>"
```

9. Copy the returned `SCREEN_SESSION` value into `.codex/active_idea.md`.
10. Set `status: running` in `.codex/active_idea.md`.

## Failure Handling

- If the launch command fails before the detached session is created, remove the empty log file and leave the run state as `planned`.
- If the command starts successfully, leave result inspection to `idea-review`.
- If a stale `screen_session` is still alive for the same idea, stop and resolve it before launching a new run.
- If the batch is cancelled before launch, keep the code changes in place and revise them in the next execution pass, or drop them from `code_touchpoints` if the batch is abandoned.

## Output Contract

The user-facing summary should contain:
- touched files,
- experiment script path,
- disclosed experiments and batch analysis items,
- screen session name,
- log path,
- artifact paths recorded for later cleanup.

