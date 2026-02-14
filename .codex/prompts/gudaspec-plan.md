---
name: GudaSpec: Plan
description: Refine proposals into zero-decision executable task flows via multi-model analysis.
category: GudaSpec
tags: [gudaspec, plan, multi-model, pbt]
allowed-tools: Bash(openspec:*)
argument-hint: [proposal_id]
---
<!-- GUDASPEC:START -->
**Guardrails**
- If the project is detected to lack `./openspec/` dir, prompt the user to initialize the project using `/gudaspec:init`.
- Strictly adhere to **OpenSpec** rules when writing **standardized spec-structured projects**.
- The goal of this phase is to eliminate ALL decision points from the task flow—implementation should be pure mechanical execution.
- Do not proceed to implementation until every ambiguity is resolved and every constraint is explicitly documented.
- Model collaboration is mandatory: use `gemini` to surface blind spots and conflicting assumptions.
- Every requirement must have Property-Based Testing (PBT) properties defined—focus on invariants, not just example-based tests.
- If constraints cannot be fully specified, escalate back to the user rather than making assumptions.

**Steps**
1. Run `openspec view` to display all **Active Changes**. If only one active proposal exists, automatically use it as `<proposal_id>`; otherwise, prompt the user to select one.

2. Run `/opsx:continue <proposal_id>` then follow it to review the current specs and improve quality of specs.

3. During the review progress, invoke `gemini` to detect remaining ambiguities:
   - With `gemini`: "Identify implicit assumptions in proposal <proposal_id>. For each assumption, specify: [ASSUMPTION] <description> → [EXPLICIT CONSTRAINT NEEDED] <concrete specification>."
   - **Anti-Pattern Detection** (flag and reject):
     - Information collection without decision boundaries (e.g., "JWT vs OAuth2 vs session—all viable")
     - Technical comparisons without selection criteria
     - Deferred decisions marked as "to be determined during implementation"
   - **Target Pattern** (required for approval):
     - Explicit technology choices with parameters (e.g., "JWT with accessToken TTL=15min, refreshToken TTL=7days")
     - Concrete algorithm selections with configurations (e.g., "bcrypt with cost factor=12")
     - Precise behavioral rules (e.g., "Lock account for 30min after 5 failed login attempts")
   - Use `interactive_feedback` tool for ANY ambiguity, NEVER assume or guess.
   - **Iterate** with user until ALL ambiguities are resolved into explicit constraints.

4. After clarifying requirements, modify the spec documents. For each change, you MUST run the command `openspec validate <proposal_id> --strict` to ensure the correct format.

5. When backend logic modification requirements are identified, Invoke `gemini` to derive testable invariants:
   - With `gemini`: "Analyze proposal <proposal_id> for system properties. Define: [PROPERTY] <name> | [DEFINITION] <formal description> | [BOUNDARY CONDITIONS] <edge cases to test> | [COUNTEREXAMPLE GENERATION] <approach>."
   - **PBT Property Categories to Extract**:
     - **Commutativity/Associativity**: Order-independent operations
     - **Idempotency**: Repeated operations yield same result
     - **Round-trip**: Encode→Decode returns original
     - **Invariant Preservation**: State constraints maintained across operations
     - **Monotonicity**: Ordering guarantees (e.g., timestamps always increase)
     - **Bounds**: Value ranges, size limits, rate constraints
   - After modify the spec documents with the PBT, MUST run the command `openspec validate <proposal_id> --strict` to ensure the correct format.

6. For complex proposals, consider running steps 2-4 iteratively on sub-components and remind the user rather than the entire proposal at once.

**Exit Criteria**
A proposal is ready to exit the Plan phase only when:
- [ ] All multi-model analyses completed and synthesized
- [ ] Zero ambiguities remain (verified by step 3 audit)
- [ ] All PBT properties documented with falsification strategies
- [ ] `openspec validate <id> --strict` returns zero issues
- [ ] User has explicitly approved all constraint decisions
<!-- GUDASPEC:END -->
