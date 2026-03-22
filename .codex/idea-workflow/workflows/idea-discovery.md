# Idea Discovery Workflow

## Goal

Generate exactly one repo-grounded oral-grade deep-learning idea.
The output must already contain:
- one main thesis,
- exactly three coordinated innovation points,
- at most two primary hyperparameters,
- enough method detail for a paper method section,
- enough experiment and analysis detail for a paper experiment section,
- one full experiment program,
- one current formal batch.

## Read First

Always inspect these sources before proposing anything:
- `experience.md`
- `direction.md` if it exists
- `.codex/baseline_commit.txt`
- `.codex/active_idea.md`
- local launch scripts, configs, result folders, and README files

## Hard Rules

- Produce one idea only.
- Prefer local repo evidence over external search.
- Use Exa only when local evidence is still insufficient or when mechanism cross-check matters.
- Use the fixed helper-agent sequence for every discovery pass after local repo reading:
  1. `repo-exa-scout`
  2. `paper-architect`
  3. `analysis-planner`
  4. `experiment-designer`
  5. `idea-critic`
- Keep helper-agent outputs transient in the turn context. Do not create repo files for intermediate drafts. Persist only the final `.codex/active_idea.md`.
- Ask at most one batched `request_user_input` round when critical baseline fields are missing or conflicting.
- Use that clarification round only after `repo-exa-scout` returns baseline-contract candidates, and only for `baseline_commit`, main metric, baseline value, and `reference_command` when the repo does not settle them cleanly.
- If any required helper agent fails, returns missing support, or leaves a required section underspecified, stop and list the blockers instead of writing `.codex/active_idea.md`.
- If `idea-critic` does not return `VERDICT: PASS`, stop and list the blockers instead of writing `.codex/active_idea.md`.

## Helper Agents

Discovery always calls these helpers in this order:
- `repo-exa-scout`: repo-first grounding, observable gap scan, baseline-contract recovery, thesis-seed proposal.
- `paper-architect`: oral-grade thesis shaping, three coordinated innovation points, method sketch, theory hook, hyperparameter discipline.
- `analysis-planner`: full paper experiment program with current-batch analysis layout.
- `experiment-designer`: repo-native current batch, one new script plan, artifact layout, and train-command shape.
- `idea-critic`: pass or reject pressure check on overlap, confounders, oral-grade support, and stop-rule sharpness.

## Process

1. Read all required local materials from `Read First`, then establish the baseline anchor from `.codex/baseline_commit.txt`.
2. Call `repo-exa-scout` with the local findings so it returns:
   - one thesis seed,
   - one baseline-contract candidate,
   - code touchpoints,
   - measurable thesis phenomena,
   - overlap avoidance against `experience.md`.
3. Recover the locked baseline contract:
   - main metric name,
   - strongest known baseline value,
   - one repo-native reference command,
   - result locator.
4. If any of those fields are missing or conflicting after `repo-exa-scout`, use one batched `request_user_input` round to confirm them.
5. Call `paper-architect` with the locked baseline contract, thesis seed, code touchpoints, and repo constraints. Require it to return an oral-grade method skeleton, exactly three innovation points, at most two primary hyperparameters, and an explicit oral-grade support argument.
6. If `paper-architect` returns missing support or fails to make the oral-grade case, stop and list the blockers.
7. Call `analysis-planner` to define the full experiment program. It must cover:
   - main results,
   - component ablations,
   - mechanism analysis,
   - boundary and cost analysis.
8. If `analysis-planner` cannot fill any required experiment family or current-batch analysis need, stop and list the blockers.
9. Call `experiment-designer` to define the first formal batch around one new experiment script such as `scripts/run_<idea-id>_b01.sh`. Require one script path, one formal experiment list, one batch analysis list, artifact layout, and planned train command.
10. If `experiment-designer` leaves the command shape, result locator, or batch contents underspecified, stop and list the blockers.
11. Call `idea-critic` on the combined proposal. Require `VERDICT: PASS` plus sharper confounder controls, paper-readiness gap checks, and stop-rule refinements.
12. Overwrite `.codex/active_idea.md` only if all hard rules are satisfied and `idea-critic` returns `VERDICT: PASS`.
13. Present a concise summary to the user.

## Required Writeback

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
- `review_outcome: pending`
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
- `Outcome Bar`
- `Review Notes`

## Required Body Constraints

- `Baseline Contract` must include metric name, baseline value, target lift, reference command, and result locator.
- `Innovation Points` must contain exactly three numbered items.
- `Primary Hyperparameters` must contain at most two items.
- `Full Experiment Program` must include:
  - `Main Results`
  - `Component Ablations`
  - `Mechanism Analysis`
  - `Boundary and Cost Analysis`
- `Current Batch` must include:
  - `Script`
  - `Formal Experiments`
  - `Batch Analysis`
- `Outcome Bar` must state:
  - `Improve when`
  - `Abandon when`
  - `Finish when`
  - `Current evidence`

Set `train_command` to the planned launch command for the new experiment script, not to the old baseline command.

## Output Contract

The user-facing summary should contain:
- one-line idea title,
- baseline metric and target lift,
- the three innovation points,
- exact code touchpoints,
- planned experiment script and formal run command, or the exact missing fields,
- current batch experiments and batch analysis items,
- one sentence on why this differs from failed ideas already recorded in `experience.md`.
