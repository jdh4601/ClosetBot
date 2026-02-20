# Fashion SaaS Business Strategy Evaluator — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** `.claude/agents/fashion-saas-evaluator.yaml` — 패션 AI SaaS 비즈니스 전략을 트랙션/수익화 5개 항목으로 채점하고 Go/Hold/No-Go 판정을 반환하는 Claude Code 커스텀 에이전트

**Architecture:** 단일 에이전트 파일(YAML). 전략 문서 또는 아이디어 텍스트를 입력받아 5개 항목(BM 명확성, 가격 전략, CAC/LTV, 성장 경로, 수익 마일스톤)을 평가하고 마크다운 리포트를 반환. 선택적으로 `docs/reports/`에 저장.

**Tech Stack:** Claude Code agent YAML, model: opus

---

### Task 1: fashion-saas-evaluator 에이전트 파일 생성

**Files:**
- Create: `.claude/agents/fashion-saas-evaluator.yaml`

**Step 1: 에이전트 YAML 파일 작성**

```yaml
---
name: fashion-saas-evaluator
description: >
  패션 AI SaaS 스타트업 아이템의 비즈니스 전략을 평가하는 에이전트.
  트랙션/수익화 5개 항목(BM 명확성, 가격 전략·WTP, CAC/LTV 추정,
  성장 경로, 수익 마일스톤)을 각 10점 만점으로 채점하고
  Go/Hold/No-Go 판정을 포함한 구조화된 리포트를 반환한다.
  전략 문서, PRD, 아이디어 텍스트 모두 입력 가능.
model: opus
tools:
  - Read
  - Write
  - WebSearch
  - WebFetch
instructions: |
  [system prompt 내용]
```

**Step 2: 실제 파일 생성 확인**

```bash
cat .claude/agents/fashion-saas-evaluator.yaml | head -5
```
Expected: `name: fashion-saas-evaluator` 출력

**Step 3: Commit**

```bash
git add .claude/agents/fashion-saas-evaluator.yaml docs/plans/
git commit -m "feat(agent): add fashion-saas-evaluator business strategy evaluation agent"
```
