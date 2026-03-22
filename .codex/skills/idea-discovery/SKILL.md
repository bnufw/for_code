---
name: idea-discovery
description: Generate one repo-grounded oral-grade deep-learning idea by reading local code, results, experience.md, and optional direction.md, confirming missing baseline fields in one batched clarification round, and writing a paper-level method plus experiment-analysis program.
metadata:
  short-description: "Generate one oral-grade DL idea with method and experiment design"
---

# Idea Discovery

## When to use

Use this skill at the start of a new idea cycle for a deep-learning baseline project.
The goal is to produce exactly one actionable idea that is grounded in the local repository, does not repeat failed ideas already stored in `experience.md`, and already contains enough method and experiment-analysis structure to support an oral-level ICLR, ICML, or NeurIPS paper.

## Read first

Always inspect these sources before proposing anything:
- `experience.md`
- `direction.md` if it exists
- `.codex/baseline_commit.txt`
- `.codex/active_idea.md`
- local training scripts, configs, result folders, and README files

## Hard rules

- Produce one idea only.
- Target an oral-level paper, not a loose tweak.
- Keep the idea centered on one thesis.
- Require exactly three innovation points that all serve the same thesis.
- Allow at most two primary method hyperparameters.
- Require enough method detail to support a paper method section.
- Require enough experiment and analysis detail to support a paper experiment section.
- Require both a full experiment program and one current formal batch.
- Prefer local repo evidence over external search.
- Use Exa only when local evidence is incomplete or when mechanism cross-check matters.
- Ask at most one batched clarification round when critical baseline fields are missing or conflicting.
- Use that clarification round specifically for `baseline_commit`, main metric, baseline value, and `reference_command` when the repo does not settle them cleanly.
- If the main metric, baseline value, or reference command still cannot be identified after that round, stop and list the missing fields.
- If the oral-level structure cannot be supported after repo reading and helper-agent pressure tests, stop and list the missing support instead of writing `.codex/active_idea.md`.

## Helper agents

Use these helpers when the repository is non-trivial or when the discovery output would otherwise stay underspecified:
- `repo-exa-scout`: repo-first grounding, observable gap scan, and baseline-contract recovery.
- `paper-architect`: single thesis, three innovation points, method sketch, theory hook, and hyperparameter discipline.
- `analysis-planner`: full paper experiment program and first-batch analysis layout.
- `experiment-designer`: repo-native current batch, new script path, and artifact layout.
- `idea-critic`: overlap review, confounder review, value bar, and stop-rule pressure test.

`repo-exa-scout` may use `mcp__exa__get_code_context_exa` or `mcp__exa__web_search_exa` only after local evidence is exhausted.

## Workflow

1. Establish the baseline anchor.
   - Read `.codex/baseline_commit.txt`.
   - If it is `UNSET`, look for a clear baseline commit candidate or ask for it in the single clarification round.
2. Recover the baseline contract.
   - Find the main metric name.
   - Find the strongest known baseline value.
   - Find one repo-native reference command that represents the current baseline or strongest known formal run.
   - Find where result files are written.
3. If any of `baseline_commit`, metric name, baseline value, or `reference_command` are missing or conflicting, use one batched `request_user_input` round to confirm them.
4. Read `experience.md` and exclude repeated directions.
5. Use `repo-exa-scout` when the repo needs help surfacing a thesis seed, observable phenomenon, or missing baseline contract details.
6. Use `paper-architect` to turn the thesis seed into an oral-level paper skeleton:
   - one thesis,
   - three innovation points,
   - one method sketch,
   - one theory hook,
   - at most two primary hyperparameters.
7. Use `analysis-planner` to define the full experiment program. It must cover:
   - main results,
   - component ablations,
   - mechanism analysis,
   - boundary or cost analysis.
8. Use `experiment-designer` to define the current formal batch around one new experiment script, such as `scripts/run_<idea-id>_b01.sh`.
9. Use `idea-critic` to pressure-test overlap, confounders, value bar, and termination triggers.
10. Only write `.codex/active_idea.md` if all hard rules are satisfied.
11. Present a concise summary to the user.

## Required writeback

Overwrite `.codex/active_idea.md` and fill at least these frontmatter fields:
- `idea_id`
- `status: planned`
- `baseline_commit`
- `train_command`
- `experiment_script`
- `screen_session: ""`
- `log_file: ""`
- `artifact_paths`
- `code_touchpoints`
- `approved_commits`
- `value_status: unknown`
- `last_updated`

Also fill the body sections:
- `Baseline Contract`
- `Paper Thesis`
- `Innovation Points`
- `Method Sketch`
- `Primary Hyperparameters`
- `Planned Code Changes`
- `Full Experiment Program`
- `Current Batch`
- `Value Bar`
- `Review Notes`
- `Next Batch`

Required body constraints:
- `Baseline Contract` must include metric name, baseline value, target lift, reference command, and result locator.
- `Innovation Points` must contain exactly three numbered items.
- `Primary Hyperparameters` must contain at most two items.
- `Full Experiment Program` must include `Main Results`, `Component Ablations`, `Mechanism Analysis`, and `Boundary and Cost Analysis`.
- `Current Batch` must include `Script`, `Formal Experiments`, and `Batch Analysis`.
- `Value Bar` must state supported, unclear, and rejected conditions.

Set `train_command` to the planned launch command for the new experiment script, not to the old baseline command.

## Output contract

The user-facing summary should contain:
- one-line idea title
- baseline metric and target lift
- the three innovation points
- the exact code touchpoints
- the planned experiment script and formal run command, or the exact missing fields
- the current batch experiments and batch analysis items
- one sentence on why this differs from failed ideas in `experience.md`
