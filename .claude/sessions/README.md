# Session Memory System

세션 간 컨텍스트를 보존하는 LLM용 연구 노트북 시스템.

## 핵심 철학

**LLM은 장기 기억이 없다.**

따라서 세션을 파일로 외부화해야 한다:
- 세션 끝날 때 현재 상태 요약
- `.claude/sessions/` 에 저장
- 다음 날 그 파일 경로만 새 세션에 넣고 시작
- 매 세션마다 새 파일 생성 (이전 맥락 오염 방지)

## 사용법

### 1️⃣ 세션 체크포인트 생성

**수동 실행:**
```
/session-checkpoint
```

**자동 알림:**
- 세션 종료 시 자동으로 리마인더 표시됨 (SessionEnd hook)

Claude가 자동으로:
1. 대화 분석
2. 4가지 섹션으로 구조화 (검증된 접근, 실패, 미시도, 남은 작업)
3. `.claude/sessions/session_YYYYMMDD_HHMM.md` 저장

### 2️⃣ 이전 세션 불러오기

다음 날 새 세션에서:

```
Continue work from session file: .claude/sessions/session_20260215_1430.md
```

Claude가 파일을 읽고 전체 컨텍스트를 이해한 상태로 작업 재개.

## 세션 파일 구조

```markdown
# Session Log - YYYY-MM-DD HH:MM

## Context
[한 문단: 이 세션이 무엇에 대한 것이었는지]

## ✅ Verified Working Approaches

### [접근법 1 이름]
- **What worked**: [설명]
- **Evidence**: [증거/결과]
- **Implementation**: [핵심 디테일]

## ❌ Failed Approaches

### [시도 1 이름]
- **What was tried**: [설명]
- **Why it failed**: [이유]
- **Lesson learned**: [교훈]

## 🔬 Unattempted Approaches

1. [접근법 이름]: [간략한 설명과 근거]
2. [접근법 이름]: [간략한 설명과 근거]

## 📋 Remaining Action Items

- [ ] [실행 가능한 태스크 1]
- [ ] [실행 가능한 태스크 2]

## Notes
[추가 관찰, 컨텍스트, 중요한 디테일]
```

## 왜 이게 필요한가?

### 문제
- 100 세션, 2 커밋 = 작업 손실, 무거운 파일 읽기, 체크포인트 없음
- 컨텍스트 제한 초과 시 진행 상황 손실
- 무엇이 작동했는지 "증거 기반" 기록 불가능

### 해결책
- 장기 프로젝트 지속 가능
- 실험 히스토리 추적 가능
- 증거 기반 기록
- 컨텍스트 압축 가능

## 세션 파일에 반드시 포함되어야 할 것

이건 단순한 "오늘 뭐 했는지" 기록이 아니다.
**사고 기록(research notebook)**이다.

### 필수 4가지 섹션

1. **✅ Verified Working Approaches**
   → 검증된 결과와 근거 포함

2. **❌ Failed Approaches**
   → 왜 실패했는지 가설 포함

3. **🔬 Unattempted Approaches**
   → 다음 실험 후보

4. **📋 Remaining Action Items**
   → 실행 가능한 다음 액션

## 전략적 컨텍스트 리셋

**탐색(Exploration)과 실행(Execution)은 다르다.**

### 탐색 단계
- 아이디어 많음
- 가설 많음
- 노이즈 많음

### 실행 단계로 전환 시
1. 계획을 확정
2. 컨텍스트 초기화 (`/clear`)
3. 계획만 들고 실행

이게 **전략적 리셋**이다.
마치 GPU 메모리 비우고 다시 학습 돌리는 느낌.

## Auto Compact vs Manual Compact

### Auto Compact (자동 압축)
- Claude가 자동으로 대화 요약 압축
- 문제: 중요한 디테일도 같이 날아감, 논리적 구간과 무관하게 압축됨

### Manual Compact (수동 압축) - 권장
- 자동 압축 끄기
- 논리적 단계 끝날 때 수동 요약
- 또는 요약 Skill 만들어서 조건부 실행

**추천 기준:**
- 50 메시지 초과 시 요약
- 한 기능 완료 시 요약
- 빌드 성공 시 요약

이건 거의 **LLM용 GC(Garbage Collection) 설계**다.

## 사용 예시

### 세션 종료 시

```
/session-checkpoint
```

Claude가 자동으로:
1. 대화 분석
2. 검증된 접근, 실패, 미시도, 남은 작업 추출
3. `.claude/sessions/session_20260215_1430.md` 저장

### 다음 날 시작 시

```
Continue work from session file: .claude/sessions/session_20260215_1430.md
```

Claude가 파일을 읽고 전체 맥락을 이해한 상태로 작업 재개.

### 복잡한 작업에 특히 유용

- 복잡한 아키텍처 작업
- 디버깅 루프
- 리팩토링 중간 단계
- 장기 리서치 작업

## 파일 관리

### 디렉토리 구조
```
.claude/sessions/
├── session_20260215_1430.md
├── session_20260215_1800.md
├── session_20260216_0930.md
└── README.md (이 파일)
```

### 파일명 규칙
- `session_YYYYMMDD_HHMM.md`
- 예: `session_20260215_1430.md`

### 정리 전략
- 완료된 프로젝트 세션은 아카이브
- 또는 `.gitignore`에 추가 (프라이버시)

## 핵심 원칙

**"LLM을 IDE처럼 쓰는 게 아니라,
LLM을 연구 노트북처럼 쓰는 것이다."**

- 증거 기반 (evidence-based)
- 실험 히스토리 보존
- 사고 흐름 기록
- 장기 프로젝트 지속 가능성

## 관련 파일

- **스킬**: `.claude/skills/session-checkpoint.md`
- **Hook 설정**: `.claude/settings.local.json` (SessionEnd)
- **저장 위치**: `.claude/sessions/`
