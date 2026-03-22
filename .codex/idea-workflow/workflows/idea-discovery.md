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
- Ask at most one batched `request_user_input` round when critical baseline fields are missing or conflicting.
- Use that clarification round only for `baseline_commit`, main metric, baseline value, and `reference_command` when the repo does not settle them cleanly.
- If the oral-grade structure cannot be supported after repo reading and helper-agent pressure tests, stop and list the missing support instead of writing `.codex/active_idea.md`.

## Helper Agents

Use these helpers when the repository is non-trivial or when the draft would otherwise stay underspecified:
- `repo-exa-scout`: repo-first grounding, observable gap scan, baseline-contract recovery.
- `paper-architect`: single thesis, three innovation points, method sketch, theory hook, hyperparameter discipline.
- `analysis-planner`: full paper experiment program plus first-batch analysis layout.
- `experiment-designer`: repo-native current batch, new script plan, artifact layout.
- `idea-critic`: overlap review, confounder review, and the minimal threshold that separates improve, abandon, and finish.

## Process

1. Read `.codex/baseline_commit.txt` and establish the baseline anchor.
2. Recover the baseline contract:
   - main metric name,
   - strongest known baseline value,
   - one repo-native reference command,
   - result locator.
3. If any of those fields are missing or conflicting, use one batched `request_user_input` round to confirm them.
4. Read `experience.md` and exclude repeated directions.
5. Use `repo-exa-scout` when the repo needs help surfacing a thesis seed, an observable phenomenon, or missing baseline details.
6. Use `paper-architect` to turn that seed into an oral-grade paper skeleton.
7. Use `analysis-planner` to define the full experiment program. It must cover:
   - main results,
   - component ablations,
   - mechanism analysis,
   - boundary and cost analysis.
8. Use `experiment-designer` to define the first formal batch around one new experiment script such as `scripts/run_<idea-id>_b01.sh`.
9. Use `idea-critic` to sharpen confounders, overlap checks, and the outcome thresholds.
10. Overwrite `.codex/active_idea.md` only if all hard rules are satisfied.
11. Present a concise summary to the user.

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

