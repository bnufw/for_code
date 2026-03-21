---
name: idea-discovery
description: Generate one repo-grounded deep-learning idea by reading local code, results, experience.md, and optional direction.md, asking at most one batched clarification round, and using Exa only when local evidence is insufficient.
metadata:
  short-description: "Generate one repo-grounded DL idea"
---

# Idea Discovery

## When to use

Use this skill at the start of a new idea cycle for a deep-learning baseline project.
The goal is to produce exactly one actionable idea that is grounded in the local repository and does not repeat failed ideas already stored in `experience.md`.

## Read first

Always inspect these sources before proposing anything:
- `experience.md`
- `direction.md` if it exists
- `.codex/baseline_commit.txt`
- `.codex/active_idea.md`
- local training scripts, configs, result folders, and README files

## Hard rules

- Produce one idea only.
- Keep the idea centered on one thesis.
- Prefer local repo evidence over external search.
- Use Exa only when local evidence is incomplete or when mechanism cross-check matters.
- Ask at most one batched clarification round when critical fields are missing.
- If the main metric, baseline value, or formal train command still cannot be identified after that round, stop and list the missing fields.

## Helper agent

When the repository is large or the literature angle is unclear, delegate the repo-and-literature scan to `repo-exa-scout`.
The helper should read local evidence first and only then use `mcp__exa__get_code_context_exa` or `mcp__exa__web_search_exa`.

## Workflow

1. Establish the baseline anchor.
   - Read `.codex/baseline_commit.txt`.
   - If it is `UNSET`, look for a clear baseline commit or ask for it in the single clarification round.
2. Recover the current project contract.
   - Find the main metric name.
   - Find the strongest known baseline value.
   - Find one formal training command.
   - Find where result files are written.
3. Read `experience.md` and exclude repeated directions.
4. If needed, use `repo-exa-scout` or Exa directly to validate the mechanism and novelty angle.
5. Write or overwrite `.codex/active_idea.md`.
6. Present a concise summary to the user.

## Required writeback

Overwrite `.codex/active_idea.md` and fill at least these fields:
- `idea_id`
- `status: planned`
- `baseline_commit`
- `baseline_metric_name`
- `baseline_metric_value`
- `target_lift`
- `train_command`
- `result_locator`
- `code_touchpoints`
- `last_updated`

Also fill the body sections:
- `Goal`
- `Hypothesis`
- `Why This Might Beat Baseline`
- `Planned Code Changes`
- `Stop Rule`

## Output contract

The user-facing summary should contain:
- one-line idea title
- baseline metric and target lift
- exact code touchpoints
- formal run command or the exact missing fields
- one sentence on why this differs from failed ideas in `experience.md`
