# Deep Learning Idea Workflow

## Purpose

This repository provides a compact Codex workflow for deep-learning baseline projects.
The goal is to search for oral-level ideas that:
- clearly outperform the baseline,
- stay organized around one main thesis,
- include about three coordinated innovation points,
- keep the method controlled by at most two primary hyperparameters,
- produce useful observations from experiments, and
- retain theoretical value.

## Required Runtime Files

- `experience.md`: durable record of failed or exhausted ideas.
- `direction.md`: optional short direction note from the user.
- `.codex/baseline_commit.txt`: baseline git commit anchor for the current project.
- `.codex/active_idea.md`: current working state for one active idea.
- `.codex/logs/`: screen logs for the active run only.

## Skill Routing

Use exactly one of these entry skills for each stage:
- `$idea-discovery`: generate one repo-grounded oral-grade idea together with a paper-level method outline, a full experiment program, and the first formal batch.
- `$idea-execution`: implement the current batch, create one new experiment script, disclose the experiments and batch analysis with `request_user_input`, and launch the formal run in `screen`.
- `$idea-review`: inspect results, decide whether paper value is supported, and then choose commit, continue, or terminate.

## Discovery Rules

1. Read local code, scripts, configs, results, and `experience.md` before asking anything.
2. Read `direction.md` only when it exists.
3. Recover the baseline contract before proposing anything: `baseline_commit`, metric name, baseline value, reference command, and result locator.
4. If any of those fields are missing or conflicting, use one batched `request_user_input` round to confirm them.
5. Treat the target as an oral-level ICLR, ICML, or NeurIPS idea: one thesis, three innovation points, at most two primary hyperparameters, and enough method plus experiment-analysis content to support a paper.
6. Prefer local evidence first. Use `repo-exa-scout` for repo grounding, `paper-architect` for the paper method skeleton, `analysis-planner` for the full experiment program, `experiment-designer` for the current batch, and `idea-critic` for confounders and the value bar.
7. Prefer `mcp__exa__get_code_context_exa` and `mcp__exa__web_search_exa` for external search.
8. Produce one idea only. Do not output a ranked list.
9. Discovery output must include `Full Experiment Program`, `Current Batch`, and `Value Bar`.
10. If the oral-level structure cannot be supported, stop and list the missing evidence instead of writing a weak idea.

## Execution Rules

1. Read `.codex/active_idea.md` before editing code.
2. Use frontmatter for runtime fields and the body sections `Planned Code Changes` and `Current Batch` for implementation scope.
3. Touch only files needed for the active thesis.
4. Do not run tests, short smoke runs, or benchmark subsets.
5. Every new batch must create one new experiment script. The formal command must call that script.
6. Keep `.codex/logs/` out of commits.
7. Before launch, use `request_user_input` to disclose experiment count, experiment list, and batch analysis items, then wait for confirmation.
8. Launch the formal run in `screen` and redirect all output to `.codex/logs/<idea-id>.log`.
9. Record every unique artifact path for the run inside `.codex/active_idea.md` so failed runs can be cleaned safely.
10. Code changes remain uncommitted until `idea-review` marks the idea as valuable.
11. If the uncommitted batch is later rejected, revert tracked files from `code_touchpoints`, remove the batch experiment script when it is new, and then clear failed logs and artifacts.

## Review Rules

1. Read `.codex/active_idea.md`, especially `Baseline Contract`, `Full Experiment Program`, `Current Batch`, and `Value Bar`.
2. Read the screen log, result files, and relevant code diffs.
3. Use `result-judge` when result interpretation is non-trivial.
4. Decision must be one of: `continue`, `terminate`, or `wait`.
5. `wait`: keep the current batch unchanged and return to `$idea-review` later. Do not route to `$idea-execution` from `wait`.
6. `continue`: if value is supported, create one atomic code commit for the proven batch, record it in `approved_commits`, update the value evidence in the body, and then either stop with the approved state or define the next batch and route back to `$idea-execution`; if value is still unclear, update the next batch only and route back to `$idea-execution`.
7. `terminate`: append a structured entry to `experience.md`, commit the note, show the baseline commit, revert all approved commits, drop the remaining uncommitted code changes from `code_touchpoints`, remove the failed experiment script when needed, and clean failed artifacts.
8. Failed logs, failed experiment scripts, and failed artifacts should be removed after the experience entry is secured.

## Git Rules

1. `.codex/baseline_commit.txt` is the source of truth for the rollback anchor.
2. Only value-backed idea code enters git history.
3. Preserve `experience.md` updates in a note-only commit before reverting an idea.
4. Never rewrite unrelated history.

## Output Style

- User-facing responses should stay concise and in Chinese.
- Internal instructions, skill files, and agent files may stay in English for tool reliability.
