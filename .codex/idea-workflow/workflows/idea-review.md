# Idea Review Workflow

## Goal

Review one completed formal batch and produce exactly one of these outcomes:
- `improve`
- `abandon`
- `finish`

When the run is still incomplete, stop and report that the batch is not ready for review yet.
Do not write one of the three outcomes in that case.

## When To Use

Use this workflow after a formal run has started or finished.
The completed-batch review is the normal entry point.

## Read First

Always inspect:
- `.codex/active_idea.md`
- `.codex/baseline_commit.txt`
- `experience.md`
- the `Baseline Contract`, `Experiment Plan`, `Current Batch`, `Outcome Bar`, and `Review Notes` sections in `.codex/active_idea.md`
- the current log file recorded in `.codex/active_idea.md`
- the result files or result directory identified in `Baseline Contract`
- the current `experiment_script`
- the current `code_touchpoints`

## Hard Rules

- Base the outcome on file-backed evidence only.
- Compare the evidence against `Baseline Contract` and `Outcome Bar` in `.codex/active_idea.md`.
- Use `Experiment Plan` and `Current Batch` to judge whether the evidence is enough for the current stage.
- Use `result-judge` when the evidence is spread across many files.
- Use `improvement-planner` before improvement clarification when the next batch is not already obvious.
- `improve` must continue into multi-round `request_user_input` clarification in the same turn. Do not stop after merely naming `improve`.
- Improvement clarification must cover:
  - the main weakness or unexplained phenomenon,
  - the chosen improvement hypothesis,
  - why that hypothesis is worth formal testing,
  - the formal experiments to add,
  - the batch analysis items to add.
- Keep asking in additional `request_user_input` rounds until those fields are explicit enough to rewrite the next batch.
- Never create a git commit on `improve` or `abandon`.
- Create one atomic git commit only on `finish`.
- Clean only the log, artifact paths, experiment script, and code touched by the active idea.

## Incomplete-Run Gate

Check these conditions before outcome selection:
- the `screen` session is still alive,
- the log is still incomplete or still growing,
- the required result files are missing,
- the evidence is still contradictory because the batch has not settled.

If any of those conditions holds:
1. stop immediately,
2. report that the batch is not ready for review,
3. list the missing evidence,
4. leave `.codex/active_idea.md` unchanged,
5. tell the user to run `$idea-review` again later.

## Helper Agents

- `result-judge`: chooses `improve`, `abandon`, or `finish` from completed evidence and summarizes the scorecard.
- `improvement-planner`: turns completed evidence into 2-3 evidence-backed improvement directions, plus a clarification plan for multi-round `request_user_input`.
- `experiment-designer`: optional after the direction is chosen, to refresh `Experiment Plan`, `Current Batch`, and the runtime fields for the next formal batch.

## Outcome Logic

### improve

Use `improve` when the current idea still has credible upside but the full paper story is not ready yet.

Required sequence:
1. Summarize the best observed metric, its delta from the baseline, and the most important non-trivial observation from the completed batch.
2. Use `improvement-planner` to propose 2-3 evidence-backed improvement directions and a clarification order.
3. Run one or more `request_user_input` rounds to choose the next direction and record why it is worth formal testing.
4. If needed, use `experiment-designer` after the selected direction is fixed, so the next batch has a refreshed `Experiment Plan`, one concrete script, one formal experiment list, and one batch analysis list.
5. Rewrite `.codex/active_idea.md`:
   - keep the completed-batch evidence in `Review Notes`,
   - explain the chosen improvement direction and why it follows from the evidence,
   - rewrite `Experiment Plan` and `Current Batch` for the next formal step,
   - update `train_command`, `experiment_script`, and `code_touchpoints`,
   - set `status: planned`,
   - set `review_outcome: improve`,
   - clear `screen_session`.
6. Keep the latest completed `log_file` and `artifact_paths` until the next execution pass replaces them. This preserves cleanup coverage if the idea is abandoned before the new batch launches.
7. Route back to `$idea-execution`.

### abandon

Use `abandon` when the idea has exhausted its plausible upside or clearly misses the target threshold.

Required sequence:
1. Append a structured entry to `experience.md`.
2. Run the cleanup helper in dry-run mode and then execute mode:

```bash
python .codex/skills/idea-review/scripts/cleanup_failed_idea.py   --active-file .codex/active_idea.md

python .codex/skills/idea-review/scripts/cleanup_failed_idea.py   --active-file .codex/active_idea.md   --execute
```

3. Reset `.codex/active_idea.md` to the empty template:
   - `status: idle`
   - `review_outcome: pending`
4. Report the termination reason and the cleanup targets.
5. Route back to `$idea-discovery`.

### finish

Use `finish` when the current evidence is already strong enough to support an oral-grade paper story:
- strong effect versus the baseline,
- non-trivial and interpretable experimental observations,
- a method-and-analysis package that already reads like a paper rather than a loose tweak.

Required sequence:
1. Update `Review Notes` with:
   - the best observed metric,
   - the delta versus the baseline,
   - the non-trivial phenomenon,
   - why the idea is now strong enough to stop.
2. Set:
   - `status: finished`
   - `review_outcome: finish`
   - `screen_session: ""`
3. Create one atomic git commit for the proven code and the current formal experiment script.
4. Keep logs and artifacts as supporting evidence.

## Experience Entry Format

Append to `experience.md` with these fields:
- idea id and short title
- date
- baseline commit
- related commits
- method summary
- code touchpoints
- experiment scripts
- key metrics
- analysis summary
- observed insight
- termination reason

## Output Contract

The user-facing summary should contain:
- the outcome,
- the best observed metric versus baseline,
- the most important experimental observation,
- the exact next step or the termination reason,
- whether a git commit was created,
- the cleanup targets when `abandon` is chosen.
