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
- The caller, not a helper agent, owns repo grounding, failure-history reading, baseline-contract recovery, and any Exa usage.
- Use Exa only when local evidence is still insufficient or when mechanism cross-check matters.
- Use the fixed helper-agent sequence for every discovery pass after local repo reading and baseline recovery:
  1. `paper-architect`
  2. `experiment-designer`
  3. `idea-critic`
- Keep helper-agent outputs transient in the turn context. Do not create repo files for intermediate drafts. Persist only the final `.codex/active_idea.md`.
- Ask at most one batched `request_user_input` round when critical baseline fields are missing or conflicting.
- Use that clarification round only after the caller has assembled baseline-contract candidates, and only for `baseline_commit`, main metric, baseline value, `reference_command`, and `result_locator` when the repo does not settle them cleanly.
- If any required helper agent fails, returns missing support, or leaves a required section underspecified, stop and list the blockers instead of writing `.codex/active_idea.md`.
- If `idea-critic` does not return `VERDICT: PASS`, stop and list the blockers instead of writing `.codex/active_idea.md`.
- Keep the final body minimal. Use only these top-level sections: `Baseline Contract`, `Method`, `Experiment Plan`, `Current Batch`, `Outcome Bar`, `Review Notes`.

## Helper Agents

Discovery always calls these helpers in this order:
- `paper-architect`: oral-grade thesis shaping and `Method`.
- `experiment-designer`: oral-grade `Experiment Plan`, repo-native `Current Batch`, and discovery-time runtime fields.
- `idea-critic`: reviewer-style pressure check plus final refinements for `Method`, `Experiment Plan`, `Current Batch`, `Outcome Bar`, and `Review Notes`.

## Process

1. Read all required local materials from `Read First`, then establish the baseline anchor from `.codex/baseline_commit.txt`.
2. The caller performs repo-first grounding so it returns:
   - one thesis seed,
   - one baseline-contract candidate,
   - code touchpoints,
   - measurable thesis phenomena,
   - overlap avoidance against `experience.md`.
   Use Exa only if local evidence is still insufficient.
3. Recover the locked baseline contract:
   - main metric name,
   - strongest known baseline value,
   - one repo-native reference command,
   - result locator.
4. If any of those fields are missing or conflicting after the caller grounding step, use one batched `request_user_input` round to confirm them.
5. Call `paper-architect` with the locked baseline contract, thesis seed, code touchpoints, thesis phenomena, and repo constraints. Require it to return the `Method` section plus any missing support.
6. If `paper-architect` returns missing support or fails to make the oral-grade case, stop and list the blockers.
7. Call `experiment-designer` with the locked baseline contract, thesis seed, `Method`, code touchpoints, thesis phenomena, and repo constraints. Require it to return `Experiment Plan`, `Current Batch`, and the frontmatter runtime fields needed for discovery writeback.
8. If `experiment-designer` leaves `Experiment Plan`, `Current Batch`, or any required runtime field underspecified, stop and list the blockers.
9. Call `idea-critic` on the combined proposal. Require `VERDICT: PASS`, reviewer-style refinements for `Method`, `Experiment Plan`, and `Current Batch`, plus final `Outcome Bar` and `Review Notes`.
10. If `idea-critic` returns revised section bodies, treat them as the final writeback values.
11. Overwrite `.codex/active_idea.md` only if all hard rules are satisfied and `idea-critic` returns `VERDICT: PASS`.
12. Present a concise summary to the user.

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
- `Method`
- `Experiment Plan`
- `Current Batch`
- `Outcome Bar`
- `Review Notes`

## Required Body Constraints

- `Baseline Contract` must include metric name, baseline value, target lift, reference command, and result locator.
- `Method` must include:
  - `Paper Thesis`
  - `Innovation Points`
  - `Method Sketch`
  - `Primary Hyperparameters`
  - `Theory Hook`
- `Innovation Points` inside `Method` must contain exactly three numbered items.
- `Primary Hyperparameters` inside `Method` must contain at most two items.
- `Experiment Plan` must include:
  - `Planned Code Changes`
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
- `Review Notes` must state the discovery-time reviewer assessment, key confounder controls, and why this idea differs from the failed ideas already recorded in `experience.md`.

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
