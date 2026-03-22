---
name: idea-review
description: Review one completed formal batch, then either improve the idea through multi-round clarification, abandon it, or finish it.
metadata:
  short-description: "Review one completed batch and choose improve, abandon, or finish"
---

<codex_skill_adapter>
## A. Skill Invocation
- This skill is invoked by mentioning `$idea-review`.
- Treat all user text after `$idea-review` as optional extra review focus, not as a replacement for file-backed evidence.
</codex_skill_adapter>

<objective>
Review one completed formal batch. If the run is still incomplete, stop and report that the batch is not ready. Otherwise choose exactly one of improve, abandon, or finish. For improve, continue into multi-round request_user_input clarification and rewrite the next batch in the same turn.
</objective>

<execution_context>
@/home/zhu/workflow/for_code/.codex/idea-workflow/workflows/idea-review.md
</execution_context>

<process>
Execute the review process from @/home/zhu/workflow/for_code/.codex/idea-workflow/workflows/idea-review.md end-to-end.
</process>

