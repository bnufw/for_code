---
name: idea-review
description: Review the active deep-learning run by reading .codex/active_idea.md, the latest log, and result files, then decide whether to continue the same idea, terminate it, or wait for more evidence, including whether the evidence justifies a git commit.
metadata:
  short-description: "Review results, judge paper value, and gate commits"
---

# Idea Review

## When to use

Use this skill after a formal run has started or finished.
The skill must return one decision: `continue`, `terminate`, or `wait`.

## Read first

Always inspect:
- `.codex/active_idea.md`
- `.codex/baseline_commit.txt`
- `experience.md`
- the `Baseline Contract`, `Full Experiment Program`, `Current Batch`, and `Value Bar` sections in `.codex/active_idea.md`
- the current log file recorded in `.codex/active_idea.md`
- the result files or result directory identified in `Baseline Contract`
- the commits recorded in `approved_commits`
- the current `experiment_script`
- the current `code_touchpoints`

## Hard rules

- Base the decision on file-backed evidence only.
- Compare the evidence against `Baseline Contract` and `Value Bar` in `.codex/active_idea.md`.
- Use `Full Experiment Program` and `Current Batch` to judge whether the observed evidence is enough for the current stage.
- Use `result-judge` when the evidence is spread across many files.
- Preserve `experience.md` before reverting code.
- Clean only the log, artifact paths, experiment script, and code touched by the active idea.
- Create a git commit only when the evidence already satisfies the supported bar.

## Decision logic

### wait
Use `wait` when:
- the `screen` session is still running,
- the log or result files are incomplete, or
- the evidence is contradictory.

After `wait`, keep the current batch unchanged and run `idea-review` again later.
Do not route to `idea-execution` from `wait`.

### continue
Use `continue` when the current idea still has credible upside.
Two subcases are allowed:
1. If `value_status` is `supported`, create one atomic commit for the proven code and experiment script, append the hash to `approved_commits`, update `Value Bar` and `Review Notes`, then either stop with the proven batch or, if the full paper program still needs more evidence, update `Current Batch` and `Next Batch` and route back to `idea-execution`.
2. If `value_status` is `unclear`, do not create a git commit. Update `Current Batch`, `Value Bar`, and `Next Batch` with one concrete follow-up batch, then route back to `idea-execution`.

### terminate
Use `terminate` when the idea has exhausted its plausible upside or clearly misses the target lift.
The order is fixed:
1. Append a structured entry to `experience.md`.
2. Reset `.codex/active_idea.md` to `status: idle`.
3. Create one note-only commit for the `experience.md` update and the state reset.
4. Show the baseline commit from `.codex/baseline_commit.txt`.
5. Revert every commit recorded in `approved_commits`, newest first.
6. Run the cleanup script so tracked files in `code_touchpoints` are restored, the current experiment script is removed when needed, and the failed artifacts are deleted.

## Cleanup command

Use the helper script in dry-run mode first, then execute mode:

```bash
python .codex/skills/idea-review/scripts/cleanup_failed_idea.py   --active-file .codex/active_idea.md

python .codex/skills/idea-review/scripts/cleanup_failed_idea.py   --active-file .codex/active_idea.md   --execute
```

## Experience entry format

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

## Output contract

The user-facing summary should contain:
- the decision
- the value status and whether a commit is justified
- the best observed metric versus baseline
- the exact next step or termination reason
- the cleanup paths
- the rollback anchor when termination is chosen
