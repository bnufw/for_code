---
name: "Implement"
description: "Execute approved OpenSpec changes."
---
## guardrails:
  - "Never apply external model prototypes directly—all Codex/Gemini outputs serve as reference only and must be rewritten into readable, maintainable, production-grade code."
  - "Keep changes tightly scoped to the requested outcome; enforce side-effect review before applying any modification."
  - "Minimize documentation—avoid unnecessary comments; prefer self-explanatory code."
## steps:
  - "Run `openspec view` to inspect current project status and review `Active Changes`; Use `mcp__ask_user_questions` tool ask the user to confirm which proposal ID they want to implement and wait for explicit confirmation before proceeding."
  - "Run `/opsx:apply <proposal_id>` and then follow it."
  - "When performing a specific coding task, execute Gemini to obtain code prototypes:\n  - **Gemini Kernel** — `skill__collaborating-with-gemini-cli` tool for frontend/UI/styling tasks (CSS, React, Vue, HTML, component design).\n  - **Mandatory constraint**: When communicating with Gemini, the prompt **must explicitly require** returning a `Unified Diff Patch` only; external models are strictly forbidden from making any real file modifications."
  - "Upon receiving the diff patch from Gemini, **NEVER apply it directly**; rewrite the prototype by removing redundancy, ensuring clear naming and simple structure, aligning with project style, and eliminating unnecessary comments."
  - "For each completed task, conduct multi-model reviews using Gemini, requiring iterative reviews until receiving **LGTM approval**."
  - "MUST follow the `/opsx:apply <proposal_id>`."