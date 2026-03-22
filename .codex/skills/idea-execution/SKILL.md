---
name: idea-execution
description: Implement the active formal batch from .codex/active_idea.md, disclose the batch with request_user_input, and launch the formal run in screen.
metadata:
  short-description: "Implement and launch one formal batch"
---

<codex_skill_adapter>
## A. Skill Invocation
- This skill is invoked by mentioning `$idea-execution`.
- Treat all user text after `$idea-execution` as optional extra constraints for the current batch.
</codex_skill_adapter>

<objective>
Implement the current formal batch, create or update exactly one new experiment script, disclose the batch with request_user_input, and launch the formal run in screen.
</objective>

<execution_context>
@/home/zhu/workflow/for_code/.codex/idea-workflow/workflows/idea-execution.md
</execution_context>

<process>
Execute the batch-implementation process from @/home/zhu/workflow/for_code/.codex/idea-workflow/workflows/idea-execution.md end-to-end.
</process>

