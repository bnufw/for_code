# Deep Learning Idea Repository

## Purpose

This repository packages a compact Codex setup for oral-grade deep-learning idea search on top of baseline projects.
Each active idea should stay on one main thesis, contain about three coordinated innovation points, use at most two primary hyperparameters, and support both a paper method section and a paper experiment-analysis section.

## Runtime Files

- `experience.md`: durable record for abandoned or exhausted ideas.
- `direction.md`: optional short user note for the next idea cycle.
- `.codex/baseline_commit.txt`: rollback anchor for the baseline project.
- `.codex/active_idea.md`: current state for exactly one active idea.
- `.codex/logs/`: screen logs for the current formal batch.

## Entry Skills

Use one entry skill for each stage:
- `$idea-discovery`: write one oral-grade idea plus the first formal batch.
- `$idea-execution`: implement the current formal batch and launch it in `screen`.
- `$idea-review`: review one completed formal batch and either improve, abandon, or finish the idea.

## Rule Files

Detailed idea-skill rules live under `.codex/idea-workflow/workflows/`:
- `.codex/idea-workflow/workflows/idea-discovery.md`
- `.codex/idea-workflow/workflows/idea-execution.md`
- `.codex/idea-workflow/workflows/idea-review.md`

When idea-related file edits are needed, start from one of the entry skills above instead of editing ad hoc.

## Project Constraints

- Every formal batch creates one new experiment script.
- Formal runs go through `screen` and write logs under `.codex/logs/`.
- `.codex/logs/` stays out of git history.
- Only `finish` in idea review allows a git commit.

