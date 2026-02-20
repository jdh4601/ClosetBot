# TaskMaster Integration Rules

## CRITICAL: Feature List Integrity (Anthropic Pattern)

**Iron Law**: Once a task is created, you may NOT:

- ❌ Delete tasks because "we don't need this anymore"
- ❌ Edit descriptions to reduce scope
- ❌ Mark as "cancelled" to avoid implementation
- ❌ Combine multiple tasks to "simplify"

**Why**: This prevents premature project completion declarations.

**IMPORTANT**: Agents tend to rationalize away difficult tasks. The feature list prevents this.

## Acceptable Status Changes

**✅ Allowed**:
- `pending` → `in-progress` → `done` (normal flow)
- `pending` → `blocked` (with clear blocker reason)
- `pending` → `deferred` (with target date)

**🚫 Requires user permission**:
- Deleting tasks
- Marking as cancelled
- Major scope reductions

## Task Workflow

**EVERY coding session**:

```bash
# 1. Start session
task-master next                    # Get highest priority task

# 2. Read full details
task-master show <id>               # Understand requirements

# 3. Mark in-progress
task-master set-status --id=<id> --status=in-progress

# 4. Implement (one feature only)
# ... code ...

# 5. Test (E2E required!)
# ... tests ...

# 6. Log implementation notes
task-master update-subtask --id=<id> --prompt="Implemented OAuth with FastAPI OAuth2PasswordBearer. Tests pass."

# 7. Mark complete
task-master set-status --id=<id> --status=done
```

## Task Completion Criteria

**IMPORTANT**: Task is "done" ONLY when:

- ✅ All acceptance criteria met
- ✅ Unit + Integration + **E2E** tests pass
- ✅ Code committed to git
- ✅ Manual verification in browser/API
- ✅ No console errors or warnings
- ✅ Implementation notes logged in subtask

**NEVER mark "done" if**:
- Tests failing
- Partial implementation
- "It mostly works"
- No E2E tests

## Blocked Tasks

**When blocking a task**:

```bash
task-master set-status --id=<id> --status=blocked
task-master update-subtask --id=<id> --prompt="Blocked: Waiting for Instagram API approval (applied 2026-02-15)"
```

**YOU MUST specify**:
- What is blocking (dependency, external approval, etc.)
- When you expect unblock (date or condition)
- What you tried to unblock

## Task Expansion

**For complex tasks** (>4 hours estimate):

```bash
task-master expand --id=<id> --research
```

This creates subtasks. Work on subtasks sequentially.

**NEVER**: Start implementing complex task without breaking it down first.

## TaskMaster + session-checkpoint Integration

**At session end**:

```bash
/session-checkpoint
# → Automatically includes:
#    - Completed tasks (done status)
#    - In-progress tasks (with % complete)
#    - Blocked tasks (with blocker reason)
```

Next session reads checkpoint to restore context.

## Common Rationalizations (ALL WRONG)

| Excuse | Reality |
|--------|---------|
| "This task is unnecessary now" | User decides, not you. Mark blocked, don't delete. |
| "I'll combine these for efficiency" | Scope changes require user approval. |
| "Feature mostly works, good enough" | "Done" means 100% complete with E2E tests. |
| "Tests will fail anyway" | Fix code or mark blocked. Don't mark done. |

**Red Flag**: Any thought about modifying/deleting tasks → ASK USER FIRST.
