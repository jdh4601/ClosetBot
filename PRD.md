---
title: "Fashion Brand Influencer Matcher - PRD"
type: "prd"
status: "draft"
date: 2026-02-17
version: "1.0"
category: "Fashion"
subcategory: "SaaS"
tags:
  - prd
  - influencer-marketing
  - fashion-tech
  - saas
  - instagram-api
---
# Fashion Brand Influencer Matcher - PRD v1.0

---

## 1. Executive Summary

Fashion Brand Influencer Matcher는 소규모 패션 디자이너 브랜드와 패션/인플루언서 마케팅 에이전시가 인플루언서 시딩 파트너를 선정할 때 데이터 기반 의사결정을 할 수 있도록 돕는 SaaS 제품이다.

사용자가 자신의 브랜드 Instagram username과 분석 대상 인플루언서 5명의 username을 입력하면, Instagram Graph API(Business Discovery)를 통해 각 인플루언서의 공개 데이터를 수집하고, 브랜드와의 적합도를 0-100 점수로 산정하여 대시보드로 제공한다.

핵심 제약: Instagram Graph API 정책을 100% 준수하며, 공식적으로 접근 가능한 데이터만 사용한다.

---

## 2. Problem Statement

### 현재 상황
소규모 패션 브랜드 및 패션 마케팅 에이전시의 담당자가 인플루언서를 선정할 때:
- 후보 인플루언서의 프로필을 하나씩 수동으로 방문하여 확인한다
- 참여율을 직접 계산하거나 감으로 추정한다
- 과거 협업 이력을 일일이 게시물을 넘겨가며 찾는다
- 브랜드와의 스타일 적합성을 주관적으로 판단한다
- 모든 정보를 스프레드시트에 수동 정리한다

### 결과
- 5명 분석에 반나절~하루 소요
- 주관적 판단으로 인해 미스매칭 발생
- 비교 기준이 없어 의사결정 근거 부족
- 동일 작업을 매번 반복

### 목표 상태
5명의 인플루언서 후보를 입력하면, 5분 이내에 객관적 데이터 기반의 비교 분석 결과와 적합도 점수를 받는다.

---

## 3. Goals & Metrics

### 제품 목표
1. 인플루언서 분석 시간을 반나절에서 5분으로 단축
2. 주관적 판단을 데이터 기반 점수로 전환
3. Instagram API 정책 준수 범위 내에서 최대한의 분석 제공

### 핵심 지표 (KPIs)

| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| 분석 완료 시간 | 5분 이내 (rate limit 미충돌 시 2분) | 작업 시작~완료 타임스탬프 |
| 분석 완료율 | 95% 이상 | 성공 작업 / 전체 작업 |
| API 오류율 | 2% 이하 | 실패 API 콜 / 전체 API 콜 |
| 월간 재사용률 | 50% 이상 | 월 3회+ 분석 사용자 / 전체 사용자 |
| 사용자 만족도 | 80% 이상 | 분석 후 피드백 설문 |

---

## 3.5 비즈니스 모델 및 수익화 전략

### 3.5.1 가격 정책

**월 구독 모델** (분석 횟수 기반)

| 플랜 | 월 분석 횟수 | 가격 | 타깃 |
|------|-------------|------|------|
| **Free** | 1회 | 무료 | 개인/스타트업 테스트 |
| **Pro** | 15회 | ₩29,000/월 | 소규모 브랜드, 1-2인 에이전시 |
| **Enterprise** | 50회 | ₩49,000/월 | 중견 브랜드, 패션/인플루언서 에이전시 |

**추가 규칙:**
- 횟수 초과 시: 5회 추가 패키지 ₩10,000
- 연간 결제 시: 2개월 무료 (월 요금 × 10)
- 에이전시 볼륨 계약: 월 200회+ 사용 시 별도 협의

### 3.5.2 타깃 고객 세그먼트

**세그먼트 A: 소규모 패션 브랜드 (Direct B2B)**
- 대상: 연 매출 10억 이하 패션 디자이너 브랜드, 스트리트웨어 브랜드
- 담당자: 브랜드 대표(1인) 또는 마케팅 담당자
- Pain Point: 인플루언서 선정에 반나절~하루 소요, 데이터 기반 의사결정 부재
- 채널: 무신사 스토어 입점 브랜드, 대동대 상가 직접 영업, 패션 커뮤니티

**세그먼트 B: 패션 마케팅 에이전시 (B2B2C)**
- 대상: 인플루언서 캠페인을 대행하는 5-20인 규모 에이전시
- 사용 패턴: 한 브랜드에 여러 인플루언서 분석, 월 20-50회 사용
- Pain Point: 다수 인플루언서 비교 분석 시 수작업 부담, 리포트 작성 시간
- 채널: 에이전시 컨소시엄, 업계 박람회, 콜드아웃바운드

**세그먼트 C: 인플루언서 에이전시/매니지먼트 (B2B2C)**
- 대상: 인플루언서를 매니지먼트하는 에이전시
- 사용 패턴: 소속 인플루언서의 브랜드 적합도 분석, 역제안 시 활용
- Pain Point: 브랜드와의 매칭 적합성을 객관적으로 제시할 도구 부재
- 채널: 인플루언서 협회, 매니지먼트사 네트워크

### 3.5.3 CAC 및 고객 확보 전략 (GTM)

**채널별 CAC 추정 및 전략**

| 채널 | 예상 CAC | 전략 | 우선순위 |
|------|----------|------|----------|
| **패션 박람회/전시회** | ₩50,000-100,000 | SFW(서울패션위크), 대동대 패션페어 참가 | High |
| **무신사 스토어 입점사** | ₩30,000-50,000 | 입점사 리스트 확보 → 이메일/전화 영업 | High |
| **에이전시 콜드아웃바운드** | ₩100,000-200,000 | 50개 에이전시 리스트 확보 → 묶�료 체험 제안 | Medium |
| **패션 커뮤니티/카페** | ₩20,000-40,000 | 인플루언서 마케팅 관련 글 게시, 댓글 참여 | Medium |
| **구글/메타 광고** | ₩150,000-300,000 | "인플루언서 분석 툴" 키워드 검색광고 (v2 이후) | Low |

**0→10 고객 확보 플랜 (Month 1-2)**
1. Week 1-2: 무신사 스토어 입점사 100개 리스트 확보 → 콜드메일 발송
2. Week 2-3: 대동대/성수동 상가 직접 방문 (10개 브랜드)
3. Week 3-4: 패션 마케팅 에이전시 20개 리스트 확보 → 링크드인/이메일 접촉
4. Week 4-6: 묶�료 체험 후 전환 캠페인 (10개 브랜드/에이전시)

**10→100 스케일 전략 (Month 3-6)**
- 입소문/레퍼럴: 사용 브랜드의 리포트 공유 유도 (워터마크/공유 기능)
- 콘텐츠 마케팅: "인플루언서 선정 가이드" 등 밸류 콘텐츠 발행
- 에이전시 파트너십: 3-5개 에이전시와 협약, 리셀러/소개 수수료 구조

---

## 4. User Stories

### US-01: 브랜드 분석
브랜드 담당자로서, 우리 브랜드의 인스타 username을 입력하면 브랜드의 컨셉, 최근 게시물들을 읽고 분위기를 분석한 결과, 핵심 해시태그, 캡션 키워드, 콘텐츠 카테고리가 자동 추출되어야 한다.

**인수 조건:**
- 프로페셔널 계정 여부 자동 확인
- 최근 게시물 20개의 캡션/해시태그 분석
- 상위 해시태그 20개와 카테고리 분류 결과 표시
- 비프로 계정 입력 시 명확한 안내 메시지

### US-02: 인플루언서 입력 및 검증
브랜드 담당자로서, 분석하고 싶은 인플루언서 5명의 username을 입력하면, 각각의 계정이 분석 가능한지 즉시 확인되어야 한다.

**인수 조건:**
- 5명 username 입력 필드
- 비즈니스/크리에이터 계정 여부 사전 확인
- 비공개/개인 계정은 "분석 불가" 표시 및 대체 입력 유도
- 중복 username 방지

### US-03: 비교 대시보드
브랜드 담당자로서, 5명의 인플루언서를 한 화면에서 점수순으로 비교할 수 있어야 한다.

**인수 조건:**
- 테이블 뷰로 5명 표시 (점수 내림차순)
- 컬럼: username, 종합 점수, 팔로워 수, 참여율, 브랜드 유사도
- 점수/참여율/팔로워 기준 정렬 가능
- CSV 내보내기

### US-04: 상세 분석 페이지
브랜드 담당자로서, 특정 인플루언서를 클릭하면 과거 협업 브랜드, 고참여 게시물, 해시태그 분포 등 상세 정보를 확인할 수 있어야 한다.

**인수 조건:**
- 프로필 요약 (팔로워, 게시물 수, 바이오)
- 과거 협업 브랜드 목록 (캡션 내 @멘션 + #ad/#협찬 해시태그 기반)
- 최근 고참여 게시물 Top 3 (permalink 포함)
- 콘텐츠 카테고리 분포 (해시태그 기반)
- 브랜드와의 유사도 상세 (공통 해시태그, 캡션 톤 유사도, 카테고리 겹침)

### US-05: 분석 진행 상태 확인
브랜드 담당자로서, API rate limit으로 대기 중일 때 진행 상태와 예상 완료 시간을 확인할 수 있어야 한다.

**인수 조건:**
- 큐 대기/분석 중/완료 상태 표시
- 예상 완료 시간(ETA) 표시
- 부분 완료 시 완료된 인플루언서부터 결과 표시

---

## 5. Functional Requirements

### FR-01: 계정 입력 및 검증
- 브랜드 username 1개 입력
- 인플루언서 username 최대 5개 입력
- Business Discovery API로 계정 유형 확인
- 비즈니스/크리에이터가 아닌 경우 "분석 불가" 처리 및 사유 안내

### FR-02: 데이터 수집 (Business Discovery API)
수집 대상: 브랜드 1명 + 인플루언서 최대 5명

**프로필 데이터:**
- username, name, followers_count, follows_count, media_count
- biography, website, profile_picture_url, is_verified

**미디어 데이터 (최근 20개):**
- id, caption, comments_count, media_type, timestamp, permalink
- like_count (Business Discovery에서 제공 시 활용, 미제공 시 comments 기반 대체)

### FR-03: 브랜드 분석 엔진
- 캡션 텍스트에서 해시태그 추출 및 정규화 (소문자 변환, 스톱워드 제거)
- 바이오 텍스트 키워드 추출
- 해시태그 빈도 기반 카테고리 프로필 생성
- 카테고리 분류: 사전 정의된 태그 사전 (패션 카테고리 룰셋) 활용

### FR-04: 인플루언서 분석 엔진

**참여율 계산:**
- 기본: (comments_count + like_count) / followers_count (게시물당)
- like_count 미제공 시: comments_count 기반 추정 참여율 사용
- 최근 20개 게시물 평균

**과거 협업 탐지:**
- 캡션 내 @멘션 추출 (브랜드 username 패턴)
- 협업 관련 해시태그 탐지: #ad, #협찬, #gifted, #sponsored, #파트너십 등
- 해당 게시물의 timestamp으로 협업 시점 추정
- 멘션된 브랜드의 간략한 프로필 정보 (가능 시)

**콘텐츠 카테고리:**
- 최근 20개 게시물의 해시태그 수집
- 카테고리 태그 사전과 매칭하여 다중 라벨링
- 카테고리별 비율 산출

**고참여 게시물 Top 3:**
- 참여 지표 기준 상위 3개 선정
- 각 게시물의 permalink, 캡션 일부, 참여 수치, 게시일 제공

### FR-05: 점수 산정 알고리즘

**최종 적합도 점수 (0-100):**

| 구성 요소 | 가중치 | 산정 방식 |
|-----------|--------|----------|
| 브랜드 유사도 | 40% | 가중 Jaccard 유사도 (브랜드 해시태그/키워드 vs 인플루언서 해시태그/키워드) |
| 참여율 품질 | 35% | 팔로워 구간별 표준화 점수 (동일 구간 내 백분위 변환) |
| 카테고리 적합성 | 25% | 브랜드 카테고리 vs 인플루언서 카테고리 매칭 점수 |

**팔로워 구간:**
- Nano: 1K-10K
- Micro: 10K-50K
- Mid: 50K-200K
- Macro: 200K+

**등급 부여:**
- A등급: 80-100점
- B등급: 60-79점
- C등급: 40-59점
- D등급: 0-39점

**점수 투명성:** 상세 페이지에서 각 구성 점수와 산정 근거를 공개한다.

### FR-06: 대시보드 (테이블 뷰)
- 5명을 종합 점수 내림차순으로 표시
- 컬럼: 프로필 썸네일, username, 팔로워 수, 참여율, 브랜드 유사도, 카테고리 적합성, 과거 협업 신호(횟수), 종합 점수, 등급
- 정렬: 점수/참여율/팔로워 기준
- CSV 날짜 기준 범위: **가공된 분석 결과만 포함** (원시 캡션 텍스트, 게시물 permalink, biography 원문 제외)
  - 포함 항목: 종합 점수, 등급, 참여율, 팔로워 수, 게시물 수, 브랜드 유사도 점수
  - 제외 항목: 캡션 원문, 미디어 URL, profile_picture_url (Meta 정책 준수)

### FR-07: 상세 페이지
- 프로필 섹션: 기본 정보 + 데이터 수집 시점 표시
- 점수 분해: 각 구성 점수 (유사도/참여율/카테고리) 개별 표시
- 과거 협업 브랜드 목록 (시점 포함)
- 고참여 게시물 Top 3 (썸네일/캡션 일부/참여 수치/permalink 외부 링크)
- 해시태그 분포: 상위 20개, 브랜드와의 교집합 하이라이트
- 데이터 제한 안내 배지 (like_count 미제공 시 등)

### FR-08: 큐잉 및 상태 관리
- 분석 요청 시 작업을 큐에 등록
- 시간당 200콜 제한 내에서 순차 처리
- 작업 상태: queued -> running -> done / failed
- 429 응답 시 대기열로 복귀, reset_at 기반 지연 후 재시도
- 5xx 응답 시 지수 백오프 (최대 3회 재시도)
- 부분 완료 시 완료된 인플루언서부터 결과 노출

---

## 6. Non-Functional Requirements

### NFR-01: 성능
- 5명 분석 평균 완료 시간: 5분 이내 (rate limit 미충돌 시 2분 목표)
- 대시보드 페이지 로딩: 2초 이내
- API 응답 시간: 500ms 이내 (캐시 히트 시)

### NFR-02: 안정성
- 작업 실패율: 2% 이하
- 재시도 최대 3회 후 실패 기록
- 서비스 가용성: 99.5%

### NFR-03: 보안
- Instagram 액세스 토큰: KMS 또는 안전 저장소에 보관
- 전송 구간 TLS 1.2+
- 최소 데이터 수집 원칙 (필요한 공개 데이터만 수집)
- 사용자 인증: JWT 기반

### NFR-04: 확장성
- 동시 50 작업 큐 처리 가능 (워커 수 수평 확장)
- PostgreSQL 인덱싱 최적화

### NFR-05: 관측성
- 구조화 로그 (JSON format)
- 메트릭 대시보드: API 콜수, 에러율, 큐 대기시간, 캐시 히트율
- 알림: rate limit 임박, 작업 실패 연속 발생 시

### NFR-06: 컴플라이언스
- Instagram Graph API 이용약관 100% 준수
- 비즈니스/크리에이터 계정만 분석
- 사용자에게 데이터 출처 및 제한사항 명시
- **데이터 삭제 정책**: 사용자가 서비스 탈퇴하거나 데이터 삭제를 요청할 경우, 수집된 모든 인플루언서 데이터를 즉시 삭제 (Meta Developer Policy 2024-11 강화)
- **데이터 보유 기간**: 분석 결과 및 원시 데이터는 최대 90일 보관 후 자동 삭제
- **profile_picture_url**: Meta CDN URL 만료로 인해 DB에 영구 저장하지 않고 실시간 조회
- **Privacy Policy**: 데이터 수집/보관/삭제 정책을 명시한 개인정보처리방침 필수 (App Review 제출 서류)
- **데이터 삭제 정책**: 사용자가 서비스 탈퇴하거나 데이터 삭제를 요청할 경우, 수집된 모든 인플루언서 데이터를 즉시 삭제 (Meta Developer Policy 2024-11 강화)
- **데이터 보유 기간**: 분석 결과 및 원시 데이터는 최대 90일 보관 후 자동 삭제
- **profile_picture_url**: Meta CDN URL 만료로 인해 DB에 영구 저장하지 않고 실시간 조회
- **Privacy Policy**: 데이터 수집/보관/삭제 정책을 명시한 개인정보처리방침 필수 (App Review 제출 서류)

---

## 7. Technical Architecture

### 시스템 구성

```
┌─────────────┐     ┌──────────────┐     ┌──────────────────┐
│   Frontend   │────>│   Backend    │────>│ Instagram Graph  │
│ React + TS   │     │   FastAPI    │     │      API         │
│ TanStack     │     │              │     │ (Business Disc.) │
│ Tailwind     │     │   Workers    │     └──────────────────┘
└─────────────┘     │   (Celery)   │
                    │              │     ┌──────────────────┐
                    │   Rate Limit │────>│   PostgreSQL     │
                    │   Manager    │     │   (영구 저장)     │
                    │              │     └──────────────────┘
                    │              │
                    │              │────>┌──────────────────┐
                    └──────────────┘     │   Redis          │
                                        │   (큐 + 캐시)     │
                                        └──────────────────┘
```

### Frontend
- React + TypeScript
- TanStack Table (대시보드 테이블)
- Tailwind CSS (UI 스타일링)
- React Router (페이지 라우팅)
- TanStack Query (서버 상태 관리)

### Backend
- FastAPI (REST API 서버)
- Celery + Redis (비동기 작업 큐)
- Rate Limit Manager (토큰 버킷 패턴, 200콜/시간 준수)
- httpx (비동기 HTTP 클라이언트)

### Database
- PostgreSQL (영구 저장: 프로필, 미디어 스냅샷, 분석 결과)
- Redis (작업 큐 + API 응답 캐시)

### 배포
- Docker (컨테이너화)
- 서비스 분리: Frontend / API Server / Worker / Redis / PostgreSQL

---

## 8. Data Model

### users
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | UUID | PK |
| email | VARCHAR | 사용자 이메일 |
| created_at | TIMESTAMP | 가입일 |

### brand_profiles
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | UUID | PK |
| user_id | UUID | FK -> users |
| ig_username | VARCHAR | 인스타 username |
| followers_count | INTEGER | 팔로워 수 |
| media_count | INTEGER | 게시물 수 |
| biography | TEXT | 바이오 |
| categories | JSONB | 카테고리 분류 결과 |
| last_fetched_at | TIMESTAMP | 마지막 수집 시점 |

### influencer_profiles
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | UUID | PK |
| ig_username | VARCHAR | 인스타 username |
| followers_count | INTEGER | 팔로워 수 |
| media_count | INTEGER | 게시물 수 |
| biography | TEXT | 바이오 |
| is_verified | BOOLEAN | 인증 여부 |
| categories | JSONB | 카테고리 분류 결과 |
| last_fetched_at | TIMESTAMP | 마지막 수집 시점 |

### media_snapshots
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | UUID | PK |
| profile_id | UUID | FK -> brand_profiles or influencer_profiles |
| profile_type | ENUM | 'brand' or 'influencer' |
| ig_media_id | VARCHAR | Instagram 미디어 ID |
| caption | TEXT | 캡션 텍스트 |
| comments_count | INTEGER | 댓글 수 |
| like_count | INTEGER (nullable) | 좋아요 수 (미제공 시 NULL) |
| media_type | VARCHAR | IMAGE/VIDEO/CAROUSEL |
| permalink | VARCHAR | 게시물 URL |
| posted_at | TIMESTAMP | 게시 시점 |
| fetched_at | TIMESTAMP | 수집 시점 |

### hashtag_aggregates
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | UUID | PK |
| profile_id | UUID | FK |
| profile_type | ENUM | 'brand' or 'influencer' |
| hashtag | VARCHAR | 해시태그 (정규화) |
| count | INTEGER | 출현 횟수 |

### analysis_jobs
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | UUID | PK |
| user_id | UUID | FK -> users |
| brand_profile_id | UUID | FK -> brand_profiles |
| influencer_usernames | JSONB | 입력된 5명 username 목록 |
| status | ENUM | queued / running / done / failed |
| api_calls_used | INTEGER | 사용된 API 콜 수 |
| started_at | TIMESTAMP | 시작 시점 |
| finished_at | TIMESTAMP | 완료 시점 |
| error | TEXT (nullable) | 에러 메시지 |

### analysis_results
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | UUID | PK |
| job_id | UUID | FK -> analysis_jobs |
| influencer_profile_id | UUID | FK -> influencer_profiles |
| similarity_score | FLOAT | 브랜드 유사도 점수 (0-100) |
| engagement_score | FLOAT | 참여율 품질 점수 (0-100) |
| category_score | FLOAT | 카테고리 적합성 점수 (0-100) |
| final_score | FLOAT | 최종 적합도 점수 (0-100) |
| grade | CHAR(1) | A/B/C/D |
| top_posts | JSONB | 고참여 게시물 Top 3 |
| collab_signals | JSONB | 과거 협업 탐지 결과 |

### category_taxonomy
| 컬럼 | 타입 | 설명 |
|------|------|------|
| slug | VARCHAR | PK (예: 'minimal', 'luxury') |
| keywords | JSONB | 관련 키워드/해시태그 목록 |
| weight | FLOAT | 카테고리 가중치 |

### 데이터 모델 주의사항
- **profile_picture_url**: Meta CDN URL 만료로 인해 DB에 영구 저장하지 않음. 필요시 Business Discovery API에서 실시간 조회
- **데이터 보유 기간**: 모든 프로필/미디어 데이터는 90일 후 자동 삭제 (Meta Developer Policy 준수)

---

## 9. API Integration Details

### 전제 조건
- 앱은 Facebook Page에 연결된 Instagram Business 계정으로 동작
- Meta App Review 통과 필요 (프로덕션 배포 시)
- 필요 권한: instagram_basic, pages_show_list
  - ⚠️ **App Review 전 재확인 필요**: `pages_read_engagement`, `instagram_manage_insights` 권한이 실제로 필요한지 Meta 공식 문서 확인 (Business Discovery API 권한 요건 변경 가능성)

### Business Discovery API 호출

**엔드포인트 (예시):**
```
GET /{ig-user-id}?fields=business_discovery.username({target_username}){
  id,
  username,
  name,
  followers_count,
  follows_count,
  media_count,
  is_verified,
  biography,
  website,
  profile_picture_url,
  media.limit(20){
    id,
    caption,
    comments_count,
    like_count,
    media_type,
    media_url,
    thumbnail_url,
    timestamp,
    permalink
  }
}
```

주의: like_count 필드는 Business Discovery에서 반환되지 않을 수 있음. 미제공 시 comments 기반 대체 지표 사용.

### API 호출량 추정 (1회 분석)

| 대상 | 호출 수 | 내역 |
|------|---------|------|
| 브랜드 | 약 26회 | 프로필 1 + 미디어 페이징 ~25 |
| 인플루언서 5명 | 약 130회 | 5 x (프로필 1 + 미디어 페이징 ~25) |
| 합계 | 약 156회 | 시간당 200회 한도 내 |

### 캐시 전략

| 데이터 유형 | TTL | 캐시 키 패턴 |
|------------|-----|-------------|
| 프로필 데이터 | 6시간 | bd:{username}:profile |
| 미디어 데이터 | 1시간 | bd:{username}:media |

### 에러 처리

| 상황 | 대응 |
|------|------|
| 429 (Rate Limit) | 대기열로 복귀, reset_at 기반 지연 후 재시도 |
| 400 (비프로 계정/비공개) | "분석 불가" 표시 + 사유 안내 |
| 5xx (서버 오류) | 지수 백오프, 최대 3회 재시도 후 실패 기록 |

---

## 10. UI/UX Specifications

### 10-1. 입력 화면
- 브랜드 username 입력 필드 (1개)
- 인플루언서 username 입력 필드 (5개)
- 입력 시 유효성 검증: 빈 값, 중복, 특수문자
- 프로 계정 여부 사전 확인 (가능 시)
- "분석 시작" 버튼
- 제출 후 "분석 대기/진행 중" 상태 표시 + ETA

### 10-2. 대시보드 (테이블 뷰)

```
┌──────────────────────────────────────────────────────────────┐
│ 분석 결과: @your_brand vs 5명 인플루언서                       │
├──────────┬──────┬────────┬────────┬────────┬──────┬────────┤
│ 인플루언서│ 등급 │ 점수   │ 팔로워 │ 참여율 │유사도│ 상세  │
├──────────┼──────┼────────┼────────┼────────┼──────┼────────┤
│ @inf_a   │  A   │ 87/100 │ 45K    │ 6.2%   │ 92%  │ 보기  │
│ @inf_b   │  B   │ 76/100 │ 32K    │ 4.8%   │ 81%  │ 보기  │
│ @inf_c   │  B   │ 73/100 │ 28K    │ 5.1%   │ 78%  │ 보기  │
│ @inf_d   │  B   │ 65/100 │ 22K    │ 3.9%   │ 72%  │ 보기  │
│ @inf_e   │  C   │ 58/100 │ 18K    │ 4.2%   │ 65%  │ 보기  │
└──────────┴──────┴────────┴────────┴────────┴──────┴────────┘
```

- 정렬: 점수/참여율/팔로워 기준 전환
- CSV 내보내기 버튼
- 데이터 수집 시점 표시

### 10-3. 상세 페이지

```
┌────────────────────────────────────────────┐
│ @influencer_a 상세 분석                     │
├────────────────────────────────────────────┤
│                                            │
│ 프로필 요약                                 │
│  팔로워: 45K | 게시물: 1,230개              │
│  바이오: "Minimal fashion / Seoul based"    │
│  데이터 수집: 2026-02-17 14:30 KST         │
│                                            │
│ 점수 분해                                   │
│  브랜드 유사도: 92/100 (40%)               │
│  참여율 품질: 85/100 (35%)                 │
│  카테고리 적합성: 78/100 (25%)             │
│  종합: 87/100 (A등급)                      │
│                                            │
│ 과거 협업 브랜드                            │
│  @luxury_brand_a (2025.12) #ad             │
│  @indie_designer_b (2025.09) #협찬          │
│  @fashion_store_c (2025.06) #gifted        │
│                                            │
│ 고참여 게시물 Top 3                         │
│  [1] 참여율 9.2% (댓글 156) - 2025.12.03  │
│  [2] 참여율 8.7% (댓글 142) - 2025.11.28  │
│  [3] 참여율 7.4% (댓글 128) - 2025.11.15  │
│                                            │
│ 해시태그 분포                               │
│  #fashion 45% | #minimal 22% | #ootd 18%  │
│  #luxury 10% | #lifestyle 5%              │
│  브랜드 교집합: #minimal #fashion #seoul    │
│                                            │
│ 브랜드 유사도 상세                          │
│  공통 해시태그: 12개 일치                   │
│  캡션 톤 유사도: 81%                       │
│  카테고리 겹침: 78%                        │
│                                            │
└────────────────────────────────────────────┘
```

### 10-4. 상태 및 오류 표시
- 큐 대기/진행률/재시도 배지
- 비프로 계정, 비공개 계정 시 명확한 사유와 해결 가이드
- like_count 미제공 시 "comments 기반 추정" 배지 표시

### 10-5. 반응형
- 데스크톱/모바일 반응형 레이아웃
- 키보드 내비게이션 지원

---

## 11. Out of Scope

다음 기능은 v1에서 명시적으로 제외한다:

| 기능 | 제외 이유 |
|------|----------|
| 팔로워 demographics (연령/성별/지역) | Graph API에서 타인 계정 조회 불가 |
| 팔로워 관심사 분석 | Graph API에서 타인 계정 조회 불가 |
| 봇/가짜 팔로워 비율 | 팔로워 리스트 접근 불가 |
| 이미지/영상 감성 분석 | Graph API 미지원, 별도 Vision AI 필요 |
| 팔로워 리스트 수집 | Graph API에서 제거됨 |
| 인플루언서 자동 추천/검색 | 사용자 입력 기반 분석만 제공 |
| DM 자동 발송 | v1 범위 밖 |
| 유료 광고 성과/어트리뷰션 | v1 범위 밖 |
| TikTok/유튜브 연동 | v1 범위 밖 |
| 분석 건당 과금 모델 | v1 범위 밖 (월 구독 모델 우선) |

---

## 12. Risks & Mitigations

| 위험 | 영향 | 완화 방안 |
|------|------|----------|
| Rate Limit 초과 (200콜/시간) | 분석 지연/실패 | 큐잉 + 토큰 버킷 + 캐시 + ETA 제공 |
| like_count 미제공 | 참여율 정확도 저하 | comments 기반 대체 지표 + 가중치 보정 + 사용자 안내 |
| 비프로 계정 입력 | 분석 불가 | 사전 검증 + 명확한 에러 메시지 + 대체 입력 유도 |
| Instagram 정책 변경 | 기능 중단 가능 | API 래퍼 추상화 + 피처 플래그로 빠른 비활성화 |
| 해시태그 스팸/노이즈 | 유사도 정확도 저하 | 스톱워드/스팸 태그 리스트 유지보수 + 임계치 필터 |
| Meta App Review 지연 | 프로덕션 배포 지연 | 개발 모드로 MVP 테스트 선행 + 리뷰 병행 신청 |
| 사용자 기대와 결과 불일치 | 신뢰도 저하 | 점수 산정 근거 투명 공개 + 제한사항 명시 + 피드백 루프 |
| 에이전시 영업 난이도 | B2B 세일즈 사이클 장기화 | 묶�료 체험 + 리포트 샘플 제공으로 진입장벽 완화 |
| 인플루언서 에이전시 미흡한 Pain Point | 제품 필요성 불명확 | 브랜드 매칭 역제안 시 활용 사례 교육, ROI 계산기 제공 |

---

## 13. Implementation Roadmap

### Phase 0: 인프라 셋업 (1주)
- FastAPI 프로젝트 스캐폴딩
- React + TypeScript 프론트엔드 셋업
- PostgreSQL / Redis 환경 구성
- Docker Compose 개발 환경
- Instagram 앱 생성 + 토큰 관리

### Phase 1: API 래퍼 + Rate Limit + 캐시 (1-2주)
- Business Discovery API 호출 모듈 구현
- 토큰 버킷 패턴 Rate Limit Manager
- Redis 캐시 키/TTL 전략 구현
- 에러 처리 및 재시도 로직
- 계정 유형 검증 로직

### Phase 2: 분석 파이프라인 (2주)
- 캡션/해시태그 추출 및 정규화 엔진
- 카테고리 태그 사전 구축 (패션 도메인)
- 참여율 계산 모듈
- 가중 Jaccard 유사도 알고리즘
- 점수 산정 엔진 (가중 합산 + 등급 부여)
- 과거 협업 탐지 모듈
- 고참여 게시물 Top 3 선정

### Phase 3: UI 대시보드 + 상세 페이지 (2주)
- 입력 화면 (검증 포함)
- 테이블 뷰 대시보드
- 상세 분석 페이지
- CSV 내보내기
- 진행 상태/오류 표시
- 반응형 레이아웃

### Phase 4: 품질 및 운영 (1-2주)
- 구조화 로그 + 모니터링 대시보드
- 캐시/쿼리 최적화
- 보안 점검 (토큰 관리, TLS)
- API 문서화
- Meta App Review 신청

### Phase 5: 베타 테스트 및 GTM (2주~)
- 초기 사용자 3-5팀과 테스트
- 가중치 튜닝 (사용자 피드백 기반)
- 카테고리 사전 개선
- UX 폴리싱

#### 수익 마일스톤

| 시점 | 목표 | 전략 |
|------|------|------|
| **Month 1** | MRR ₩300,000 | 묶�료 체험 → Pro 전환 10개 고객 확보 |
| **Month 3** | MRR ₩1,500,000 | Free → Pro 전환율 15% 달성, 에이전시 3개 확보 |
| **Month 6** | MRR ₩5,000,000 | Enterprise 고객 10개 이상, 월 활성 사용자 50명 |
| **Month 12** | MRR ₩20,000,000 | 에이전시 파트너십 통해 자연 유입 채널 확보 |

#### 고객 확보 마일스톤 (0→1→N)

| 단계 | 시점 | 목표 | 핵심 행동 |
|------|------|------|----------|
| **0→10** | Month 1-2 | 10개 유료 고객 | 무신사 입점사 직접 영업, 대동대 방문 |
| **10→50** | Month 3-4 | 50개 유료 고객 | 에이전시 콜드아웃바운드, 커뮤니티 포스팅 |
| **50→100** | Month 5-6 | 100개 유료 고객 | 레퍼럴 프로그램, 콘텐츠 마케팅 |
| **100→500** | Month 7-12 | 500개 유료 고객 | 파트너십 채널, PLG(제품 주도 성장) |

#### Kill Criteria (Go/No-Go 결정 기준)
- Month 2: 10개 유료 고객 확보 실패 시 BM 피봇 검토
- Month 3: Pro 전환율 10% 미만 시 가격 정책 재검토
- Month 6: MRR ₩3,000,000 미만 도달 시 타깃 세그먼트 변경 검토

---

## Appendix: 향후 확장 가능성 (v2+)

v1에서 제외한 기능 중, 추후 별도 기술로 도입 가능:
- 이미지 감성 분석: Vision AI (GPT-4V, Claude Vision) 연동
- 팔로워 품질 분석: 인플루언서가 직접 자신의 인사이트 데이터를 공유하는 기능
- 인플루언서 자동 추천: 해시태그 검색 API 기반 후보 자동 탐색
- TikTok/유튜브 확장: 멀티 플랫폼 지원
- DM 자동화: 협업 제안 자동 발송
- **Instagram Creator Marketplace API 검토**: Meta가 2025년 10월 출시한 공식 API로, 인플루언서 마케팅에 특화된 기능 제공 (키워드 검색, 오디언스 demographics, 평균 참여율 확인). Business Discovery API보다 제품 목적에 더 부합할 수 있어 v2 로드맵에 검토 추가 권장
