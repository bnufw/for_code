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
- Use actual child-agent delegation for every helper role below. Describing those roles in the parent rollout without spawning the registered child agents does not satisfy the workflow.
- Use the fixed helper-agent sequence for every discovery pass after local repo reading and baseline recovery:
  1. `paper-architect`
  2. `theorem-architect`
  3. `experiment-designer`
- Accepted child-agent outputs must be written into `.codex/active_idea.md` immediately after each helper finishes. Do not leave accepted helper output only in transient turn context.
- Ask at most one batched `request_user_input` round when critical baseline fields are missing or conflicting.
- Use that clarification round only after the caller has assembled baseline-contract candidates, and only for `baseline_commit`, main metric, baseline value, `reference_command`, and `result_locator` when the repo does not settle them cleanly.
- If any required helper agent fails, returns missing support, or leaves a required section underspecified, stop and list the blockers instead of writing `.codex/active_idea.md`.
- Treat the theorem pass as a hard gate. Discovery stops when `theorem-architect` fails to produce exactly two non-trivial theorems or leaves any theorem without `Assumptions`, `Claim`, `Why non-trivial`, `Full proof`, or `Empirical consequence`.
- Treat the theorem pass as a method-stage formalization step. After `paper-architect` finishes, theorem content must serve the staged `Method` section rather than re-open repository code details.
- Keep the final body minimal. Use only these top-level sections: `Baseline Contract`, `Method`, `Experiment Plan`, `Current Batch`, `Outcome Bar`, `Review Notes`.
- If multi-agent support or any registered helper agent is unavailable, stop and report the exact missing child-agent capability.
- During staged writeback, keep `status: idle` until the caller finishes the final synthesis step. If discovery later stops with blockers, reset `.codex/active_idea.md` to the empty template before returning.

## Helper Agents

Discovery always calls these helpers in this order:
- `paper-architect`: oral-grade thesis shaping and `Method`.
- `theorem-architect`: two non-trivial theorems with full proofs that finalize `Method -> Theory hook` for the already-written method section.
- `experiment-designer`: oral-grade `Experiment Plan`, repo-native `Current Batch`, and discovery-time runtime fields, grounded in the finalized `Theory hook`.
After those three helpers finish, the caller writes `Outcome Bar` and `Review Notes` from the accepted proposal, the locked baseline contract, and `experience.md`.

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
5. Initialize `.codex/active_idea.md` with the empty template plus the locked `Baseline Contract`. Keep `status: idle`, keep runtime fields empty, and leave the unfinished sections blank.
6. Spawn the registered `paper-architect` child agent with the locked baseline contract, thesis seed, code touchpoints, thesis phenomena, and repo constraints. Wait for its final answer before continuing. Require it to return the `Method` section plus any missing support.
7. If `paper-architect` returns missing support or fails to make the oral-grade case, reset `.codex/active_idea.md` to the empty template and stop with blockers. Otherwise write the accepted `Method` section into `.codex/active_idea.md` immediately.
8. Spawn the registered `theorem-architect` child agent with the locked baseline contract, thesis seed, staged `Method`, and thesis phenomena. Wait for its final answer before continuing. Require it to return `THEORY_HOOK`, `THEOREM_CHECKLIST`, and any missing support.
9. If `theorem-architect` leaves fewer than two theorems, repeats the same theorem twice, leaves any required theorem field blank, or fails to tie the theorems back to the thesis, the staged `Method`, and measurable phenomena, reset `.codex/active_idea.md` to the empty template and stop with blockers. Otherwise overwrite `Method -> Theory hook` with the accepted theorem block immediately.
10. Spawn the registered `experiment-designer` child agent with the locked baseline contract, thesis seed, staged `Method`, code touchpoints, thesis phenomena, and repo constraints. Wait for its final answer before continuing. Require it to return `Experiment Plan`, `Current Batch`, and the frontmatter runtime fields needed for discovery writeback.
11. If `experiment-designer` leaves `Experiment Plan`, `Current Batch`, or any required runtime field underspecified, reset `.codex/active_idea.md` to the empty template and stop with blockers. Otherwise write the accepted `Experiment Plan`, `Current Batch`, and runtime fields into `.codex/active_idea.md` immediately.
12. The caller synthesizes `Outcome Bar` and `Review Notes` from the locked baseline contract, `experience.md`, and the accepted `Method`, `Experiment Plan`, and `Current Batch`. Keep the staged helper outputs unchanged unless a concrete contradiction must be corrected.
13. If the caller cannot state crisp thresholds for `Outcome Bar` or cannot explain overlap control and confounder control in `Review Notes`, reset `.codex/active_idea.md` to the empty template and stop with blockers.
14. Write `Outcome Bar`, `Review Notes`, and set `status: planned`.
15. Present a concise summary to the user.

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
- `Theory Hook` inside `Method Sketch` must contain exactly two theorem blocks named `Theorem 1` and `Theorem 2`.
- Each theorem block inside `Theory Hook` must contain:
  - `Assumptions`
  - `Claim`
  - `Why non-trivial`
  - `Full proof`
  - `Empirical consequence`
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
- `Review Notes` must state the discovery-time proposal assessment, key confounder controls, and why this idea differs from the failed ideas already recorded in `experience.md`.

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
