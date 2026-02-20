# Testing Rules (Anthropic Pattern)

## CRITICAL: E2E Testing Requirement

**YOU MUST run E2E tests BEFORE marking ANY task as "done":**

### Testing Hierarchy (ALL required)

1. **Unit Tests** (narrow scope)
   - Test individual functions
   - Mock external dependencies
   - Fast execution (< 1 second)

2. **Integration Tests** (service interactions)
   - Test API endpoints
   - Real database (test DB)
   - Test service-to-service calls

3. **E2E Tests** (REAL user scenario) ⚠️ MANDATORY
   - Use Puppeteer/Playwright
   - Real browser automation
   - Full user flow (login → action → verification)

### E2E Test = Real Environment

**IMPORTANT**: E2E tests must use REAL conditions:

**✅ Acceptable E2E**:
```javascript
// Puppeteer browser automation
await page.goto('http://localhost:3000/login');
await page.fill('[name="email"]', 'test@example.com');
await page.click('button[type="submit"]');
await page.waitForNavigation();
expect(await page.url()).toBe('http://localhost:3000/dashboard');
```

**❌ NOT E2E**:
```javascript
// API-only test (missing UI verification)
const res = await fetch('/api/login', { method: 'POST', body: data });
expect(res.status).toBe(200);
```

**❌ NOT E2E**:
```javascript
// Jest/Vitest mocking (simulated, not real)
const mockFetch = jest.fn(() => Promise.resolve({ ok: true }));
```

## Common Rationalizations (ALL WRONG)

| Excuse | Reality |
|--------|---------|
| "Unit tests are sufficient" | Unit tests don't catch integration bugs |
| "I manually tested in browser" | Manual testing isn't reproducible |
| "API works, UI will work too" | API working ≠ UI working |
| "E2E tests are slow" | Bugs in production are slower |

## Test File Organization

**Structure**:
```
tests/
├── unit/          # Fast, isolated tests
├── integration/   # API + DB tests
└── e2e/           # Browser automation
    ├── auth.spec.ts
    ├── posts.spec.ts
    └── webhooks.spec.ts
```

## E2E Test Checklist (Instagram Bot)

**YOU MUST test these flows end-to-end:**

- [ ] OAuth flow: Login → Redirect → Token saved → Dashboard
- [ ] Post management: Fetch posts → Display → Add product
- [ ] Webhook: Comment posted → GPT-4o analysis → Auto-reply → Log saved
- [ ] Product CRUD: Add → Edit → Delete → Verify DB

**NEVER mark task "done" without E2E verification.**

## Test Coverage Targets

- **Minimum**: 80% line coverage
- **Critical paths** (auth, payments, webhooks): 95%+

## Before Marking Task Complete

**CRITICAL checklist**:

1. [ ] Unit tests pass (`npm test` or `pytest`)
2. [ ] Integration tests pass
3. [ ] **E2E tests pass** (Puppeteer/Playwright)
4. [ ] Manual verification in browser
5. [ ] No console errors
6. [ ] TaskMaster updated with test results

**Red Flag**: "I'll add tests later" → STOP. Tests first, or tests never.

## Test-Driven Development (TDD)

**IMPORTANT for new features**:

1. Write failing test (describe expected behavior)
2. Write minimum code to pass test
3. Refactor while keeping tests green

**Exception**: MVP timeline may skip TDD for speed, but E2E tests still mandatory.
