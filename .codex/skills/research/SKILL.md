---
name: "Research"
description: Transform user requirements into rigorous constraint sets, eliminate ambiguities, and generate a zero-decision OpenSpec proposal.
---

<!-- RESEARCH:START -->
**Core Philosophy**
- Transform requirements into constraint sets and verifiable success criteria.
- Eliminate all technical and business ambiguities so implementation requires zero decision-making.
- Strictly adhere to **OpenSpec** rules.

**Guardrails**
- **MANDATORY**: Use codebase retrieval tools instead of manual grep/search operations.
- Divide exploration tasks by context boundaries (e.g., auth, user domain), not by functional roles.
- **NEVER** leave decisions as "TBD during implementation" (e.g., must specify cache TTLs, algorithms).
- **ALWAYS** ask the user for any remaining ambiguities; never guess.

**Steps**

1. **Exploration & Constraints Gathering**
   - Run `/opsx:explore <user_question>` to begin.
   - Assess the codebase and identify natural context boundaries.
   - Aggregate findings into explicit hard/soft constraints, dependencies, and risks.

2. **Ambiguity Resolution & Deep Review**
   - Identify implicit assumptions in the gathered constraints.
   - Use `skill__collaborating-with-gemini-cli` to challenge technical decisions and force concrete selections (e.g., "Identify implicit assumptions. Specify: [ASSUMPTION] -> [EXPLICIT CONSTRAINT NEEDED]").
   - Interactively resolve all open questions with the user until zero ambiguities remain.

3. **Invariants Extraction (PBT)**
   - For backend/core logic, use `skill__collaborating-with-gemini-cli` to define Property-Based Testing (PBT) invariants (e.g., Idempotency, Round-trip, Bounds).

4. **Proposal Generation & Validation**
   - After finalizing all constraints, decisions, and PBT properties, run `/opsx:ff <requirement-description>` to generate the OpenSpec proposal.
   - Do NOT abbreviate user requirements or file paths in the proposal.
   - Finally, run `openspec validate <proposal_id> --strict` to ensure correctness.

**Exit Criteria**
- [ ] Zero ambiguities or implicit assumptions remain.
- [ ] All PBT properties documented with falsification strategies.
- [ ] `openspec validate <proposal_id> --strict` returns 0 issues.
- [ ] User explicitly approved all constraint decisions.
<!-- RESEARCH:END -->