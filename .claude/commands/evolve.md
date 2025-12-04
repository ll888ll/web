# Darwin Protocol: Self-Evolution

**Trigger:** User invokes `/evolve` or specifically asks for "improvement".

**Directive:**
You are authorized to modify your own operating instructions (`CLAUDE.md`) and toolset (`.claude/commands/*`) to become more efficient.

**Process:**
1.  **Analyze Session History:** Look at the mistakes, ambiguities, or repetitive clarifications in the recent conversation.
2.  **Identify Gaps:** What knowledge was missing? What tool would have solved this in 1 step instead of 3?
3.  **Mutate:**
    - If a rule was unclear, **REWRITE** the rule in `CLAUDE.md`.
    - If a manual process was repeated, **CREATE** a new slash command (e.g., `/fix-css`) to automate it.
    - If context was missing, **ADD** the file path to the "Knowledge Base" section.
4.  **Commit:** Save the changes to the configuration files.

**Constraint:** NEVER delete the "Visual Truth" or "Design System" core principles. Evolution must preserve the project's soul (Nocturne).
