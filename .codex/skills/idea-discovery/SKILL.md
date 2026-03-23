---
name: idea-discovery
description: Generate one repo-grounded oral-grade deep-learning idea together with a paper-level method, a full experiment program, and the first formal batch.
metadata:
  short-description: "Generate one oral-grade DL idea plus the first formal batch"
---

<codex_skill_adapter>
## A. Skill Invocation
- This skill is invoked by mentioning `$idea-discovery`.
- Treat all user text after `$idea-discovery` as optional extra direction for the next idea cycle.
</codex_skill_adapter>

<objective>
Generate exactly one repo-grounded oral-grade deep-learning idea with a paper-level method, a full experiment program, and the first formal batch.
</objective>

<execution_context>
@/home/zhu/workflow/for_code/.codex/idea-workflow/workflows/idea-discovery.md
</execution_context>

<process>
Use actual registered child-agent delegation for the three discovery helpers.
Do not satisfy `paper-architect`, `experiment-designer`, or `idea-critic` locally in the parent rollout.
If child-agent support is unavailable, stop and report that discovery cannot continue with the required helper stack.

Execute the discovery process from @/home/zhu/workflow/for_code/.codex/idea-workflow/workflows/idea-discovery.md end-to-end.
</process>
