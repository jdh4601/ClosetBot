---
name: session-checkpoint
description: Create structured session checkpoint for context preservation across sessions
---

You are creating a session checkpoint to preserve context for future sessions.

## Your Task

Analyze the current conversation and create a structured session log containing:

1. **✅ Verified Working Approaches**
   - What solutions worked successfully
   - Evidence/proof of success
   - Key implementation details

2. **❌ Failed Approaches**
   - What was tried but didn't work
   - Reasoning for failure
   - Lessons learned

3. **🔬 Unattempted Approaches**
   - Ideas not yet explored
   - Potential next experiments
   - Alternative strategies

4. **📋 Remaining Action Items**
   - Concrete next steps
   - Prioritized tasks
   - Blockers or dependencies

## Output Format

Save to `.claude/sessions/session_YYYYMMDD_HHMM.md` using this structure:

```markdown
# Session Log - YYYY-MM-DD HH:MM

## Context
[One paragraph: what was this session about?]

## ✅ Verified Working Approaches

### [Approach 1 Name]
- **What worked**: [description]
- **Evidence**: [proof/results]
- **Implementation**: [key details]

### [Approach 2 Name]
...

## ❌ Failed Approaches

### [Attempt 1 Name]
- **What was tried**: [description]
- **Why it failed**: [reasoning]
- **Lesson learned**: [insight]

### [Attempt 2 Name]
...

## 🔬 Unattempted Approaches

1. [Approach name]: [brief description and rationale]
2. [Approach name]: [brief description and rationale]
...

## 📋 Remaining Action Items

- [ ] [Actionable task 1]
- [ ] [Actionable task 2]
- [ ] [Actionable task 3]
...

## Notes
[Any additional observations, context, or important details]
```

## Process

1. Review the entire conversation history
2. Extract relevant information for each section
3. Be specific and evidence-based (not vague summaries)
4. Use Write tool to save the file with current timestamp
5. Confirm the saved file path

## Important

- Focus on **what** and **why**, not just descriptions
- Include concrete evidence (test results, error messages, successful outputs)
- Make action items specific and executable
- This file will be read by a future session with no prior context
- Use current date/time for filename: `session_YYYYMMDD_HHMM.md`

## Example Usage

**Manual trigger:**
```
/session-checkpoint
```

**To resume from a previous session:**
```
Continue work from session file: .claude/sessions/session_20260215_1430.md
```

The future Claude instance will read this file and have full context to continue work.
