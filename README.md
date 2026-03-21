# Deep Learning Idea Workflow Template

This repository packages a compact `.codex` workflow for deep-learning baseline projects.
It exposes a narrow three-skill loop for deep-learning idea exploration:

- `idea-discovery`
- `idea-execution`
- `idea-review`

## Quick Start

1. Copy this `.codex` directory, `AGENTS.md`, and `experience.md` into a target baseline repository.
2. Set the baseline anchor once:
   ```bash
   git rev-parse HEAD > .codex/baseline_commit.txt
   ```
3. Optionally create `direction.md` with the target task, dataset, hard constraints, and current hunch.
4. Run the skills in order:
   - `$idea-discovery`
   - `$idea-execution`
   - `$idea-review`

## Runtime State

- `.codex/baseline_commit.txt`: baseline rollback anchor.
- `.codex/active_idea.md`: active idea state and next action.
- `.codex/logs/`: current screen logs.
- `experience.md`: durable record of terminated ideas.

## Helper Agents

- `repo-exa-scout`: repo-first idea scouting with Exa-backed literature support.
- `result-judge`: result interpretation and continue/terminate decision support.
