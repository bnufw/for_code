---
name: idea-review
description: Review the active deep-learning run by reading .codex/active_idea.md, the latest log, and result files, then decide whether to continue the same idea, terminate it, or wait for more evidence.
metadata:
  short-description: "Review results and decide next step"
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
- the current log file recorded in `.codex/active_idea.md`
- the result files or result directory recorded in `.codex/active_idea.md`
- the commits recorded in `idea_commits`

## Hard rules

- Base the decision on file-backed evidence only.
- Compare against the stop rule in `.codex/active_idea.md`.
- Use `result-judge` when the evidence is spread across many files.
- Preserve `experience.md` before reverting code.
- Clean only the log and artifact paths that belong to the active idea.

## Decision logic

### wait
Use `wait` when:
- the `screen` session is still running,
- the log or result files are incomplete, or
- the evidence is contradictory.

### continue
Use `continue` when the current idea still has credible upside.
Two subcases are allowed:
1. If the next step only changes the formal command, update `.codex/active_idea.md` and relaunch with the execution script.
2. If the next step needs code or config edits, update `.codex/active_idea.md` with the next experiment design and route back to `idea-execution`.

### terminate
Use `terminate` when the idea has exhausted its plausible upside or clearly misses the target lift.
The order is fixed:
1. Append a structured entry to `experience.md`.
2. Reset `.codex/active_idea.md` to `status: idle`.
3. Create one note-only commit for the `experience.md` update and the state reset.
4. Show the baseline commit from `.codex/baseline_commit.txt`.
5. Revert every commit recorded in `idea_commits`, newest first.
6. Run the cleanup script on the recorded log and artifact paths.

## Cleanup command

Use the helper script in dry-run mode first, then execute mode:

```bash
python .codex/skills/idea-review/scripts/cleanup_failed_idea.py \
  --active-file .codex/active_idea.md

python .codex/skills/idea-review/scripts/cleanup_failed_idea.py \
  --active-file .codex/active_idea.md \
  --execute
```

## Experience entry format

Append to `experience.md` with these fields:
- idea id and short title
- date
- baseline commit
- related commits
- method summary
- code touchpoints
- key metrics
- termination reason

## Output contract

The user-facing summary should contain:
- the decision
- the best observed metric versus baseline
- the exact next step or termination reason
- the cleanup paths
- the rollback anchor when termination is chosen
