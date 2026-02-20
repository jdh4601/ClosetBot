# Session Workflow Rules

## CRITICAL: Session Start Protocol (Anthropic Pattern)

**YOU MUST run these steps at EVERY session start:**

1. **Verify location**: `pwd` (confirm project root)
2. **Review history**: `git log --oneline -5`
3. **Read checkpoint**: `cat ~/.claude/sessions/session_*.md | tail -50`
4. **Get next task**: `task-master next`
5. **Run init script**: `./init.sh` (if exists)

**IMPORTANT**: Never skip session-start protocol. Skipping costs 15 minutes of context recovery.

## Session End Protocol

**YOU MUST before ending ANY session:**

1. **Commit changes**: All uncommitted work
2. **Create checkpoint**: `/session-checkpoint`
3. **Update TaskMaster**: Mark completed tasks as `done`

**Red Flag**: "I'll just close the terminal" → STOP and checkpoint first.

## One Session = One Feature

**IMPORTANT**: Focus on completing ONE feature per session.

**Why**: Context window management. Attempting multiple features = exhausted context = incomplete work.

**Exception**: Only combine if total work < 30 minutes.

## Commit Frequency

**YOU MUST commit in these situations:**

- Every 3-5 files changed
- Every 30 minutes of active work
- Before switching tasks
- Feature/fix complete (even 1-2 files)
- Before asking for user feedback
- End of session (ALWAYS)

**NEVER**:
- Skip committing because "it's not done yet"
- Combine unrelated changes into one commit
- Leave work uncommitted at session end

## Session Time Budget

- **Setup/Context**: 2-5 minutes (session-start protocol)
- **Implementation**: 30-90 minutes (one feature)
- **Testing**: 10-20 minutes (E2E tests)
- **Wrap-up**: 2-3 minutes (commit + checkpoint)

Total: ~1-2 hours per session optimal.
