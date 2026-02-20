# .claude/rules Directory

## Purpose

This directory contains coding rules that Claude Code automatically loads at **every session start**.

Rules are separated by concern to keep each file focused and under 500 tokens for efficient loading.

---

## Available Rules

| File | Applies To | Purpose |
|------|-----------|---------|
| `session-workflow.md` | All sessions | Session start/end protocol (Anthropic pattern) |
| `backend-rules.md` | `backend/**/*.py` | FastAPI, async, security, Instagram API |
| `frontend-rules.md` | `frontend/**/*.{ts,tsx}` | Next.js, GiGi design, Zustand, TypeScript |
| `testing-rules.md` | `tests/**/*` | Unit + Integration + E2E testing requirements |
| `taskmaster-rules.md` | Task management | TaskMaster integrity, completion criteria |
| `security-rules.md` | All code | OWASP Top 10, input validation, secrets |

---

## How Rules Work

### Auto-Loading

- **Timing**: Rules load automatically at session start
- **Scope**: Global rules apply to all files, path-specific rules apply to matching files
- **Priority**: More specific rules override general rules

### Path-Based Rules (Future)

You can create path-specific rules:

```markdown
<!-- backend-rules.md -->
## Path: backend/**/*.py

[Rules here only apply to backend Python files]
```

### Rule Syntax

Use strong emphasis to ensure compliance:

- **"YOU MUST"** - Mandatory requirement
- **"NEVER"** - Absolute prohibition
- **"IMPORTANT"** - Critical guideline
- **"CRITICAL"** - Highest priority rule

Example:
```markdown
**YOU MUST run E2E tests BEFORE marking task "done".**
**NEVER commit .env files to git.**
```

---

## Adding New Rules

### 1. Create Rule File

```bash
# Create new rule file
touch .claude/rules/my-new-rules.md
```

### 2. Write Rule Content

```markdown
# My New Rules

## Path: src/specific/**/*.ts (optional)

**IMPORTANT**: [Your rule here]

**YOU MUST**: [Mandatory requirement]

**NEVER**: [Prohibition]
```

### 3. Keep It Concise

- **Target**: <500 tokens (~200-300 lines)
- **Focus**: One concern per file
- **Examples**: Include code examples for clarity

### 4. Test Rules

Start a new session and verify rules are applied:

```bash
# Start new session
/session-start

# Check if rules are followed
# (Claude should automatically apply them)
```

---

## Rule Hierarchy

### Precedence (highest to lowest)

1. **Explicit user instructions** (current conversation)
2. **Path-specific rules** (e.g., `backend/**/*.py`)
3. **General rules** (applies to all files)
4. **CLAUDE.md** (project overview)
5. **Default Claude behavior**

### When Rules Conflict

- More specific rules override general rules
- User instructions override all rules
- If unclear, ask user for clarification

---

## Best Practices

### ✅ Do

- Keep rules focused on one concern
- Use strong emphasis keywords ("YOU MUST", "NEVER")
- Include code examples
- Update rules as project evolves
- Keep files under 500 tokens

### ❌ Don't

- Create overlapping rules (causes confusion)
- Write vague rules (be specific)
- Ignore rule violations (enforce consistently)
- Let rules go stale (review regularly)

---

## Rule Templates

### Coding Standard Rule

```markdown
# [Language] Coding Standards

## Path: [path/**/*.ext]

**IMPORTANT**: Follow these standards for all [language] code.

## Naming Conventions

**YOU MUST use**:
- camelCase for variables
- PascalCase for classes
- SCREAMING_SNAKE_CASE for constants

**NEVER**:
- Use single-letter variable names (except loop counters)
- Abbreviate without comments
```

### Testing Rule

```markdown
# [Area] Testing Requirements

**YOU MUST write tests for**:
- All public API endpoints
- All business logic functions
- All UI components

**Test Coverage**: Minimum 80%, Critical paths 95%+

**NEVER mark "done" without**:
- Unit tests passing
- Integration tests passing
- E2E tests passing (MANDATORY)
```

### Security Rule

```markdown
# [Area] Security Requirements

**CRITICAL**: [Security concern]

**YOU MUST**:
- Validate all user input
- Sanitize before rendering
- Use parameterized queries

**NEVER**:
- Trust user input
- Expose secrets in code
- Use unsafe functions
```

---

## Maintenance

### Review Schedule

- **Weekly**: Check rules are still relevant
- **Monthly**: Update examples with new patterns
- **Per Feature**: Add rules for new concerns

### Version Control

- Commit rule changes with clear messages
- Document why rules were added/changed
- Keep changelog of major rule updates

---

## Integration with Other Systems

### session-checkpoint

Rules are referenced in checkpoints:

```markdown
## Key Decisions
- Followed backend-rules.md for FastAPI structure
- Applied testing-rules.md E2E requirement
```

### TaskMaster

Task completion criteria reference rules:

```markdown
## Definition of Done
- All rules in .claude/rules/ followed
- E2E tests pass (testing-rules.md)
- Security checklist complete (security-rules.md)
```

---

## Questions?

If rules are unclear or conflicting:

1. Check this README
2. Read the specific rule file
3. Ask user for clarification
4. Update rules to prevent future confusion

**Remember**: Rules exist to maintain consistency and quality. Follow them strictly.
