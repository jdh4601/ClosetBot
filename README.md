# Fashion Influencer Matcher SaaS

Korean fashion/beauty 브랜드를 위한 인플루언서 매칭 플랫폼입니다. Instagram Graph API를 활용하여 브랜드와 인플루언서 간의 적합도를 0-100점 스케일로 분석합니다.

## 🚀 주요 기능

- **빠른 분석**: 브랜드 1개 + 인플루언서 최대 5명을 5분 내 분석
- **정확한 매칭 스코어**: 브랜드 유사도(40%) + 참여도 품질(35%) + 카테고리 적합도(25%)
- **등급 시스템**: A (80-100), B (60-79), C (40-59), D (0-39)
- **상세 분석**: 스코어 구성 요소별 세부 분석 제공

## 📋 기술 스택

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15
- **Cache/Queue**: Redis 7 + Celery
- **ORM**: SQLAlchemy (async)
- **API**: Instagram Graph API (Business Discovery)

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS (GiGi-inspired design system)
- **State Management**: TanStack Query
- **Tables**: TanStack Table

## 🐳 Docker 개발 환경 설정

### 사전 요구사항

- Docker Desktop 설치
- Docker Compose V2 설치
- Instagram Business Account + Access Token

### 1. 환경 변수 설정

```bash
# .env.example을 복사하여 .env 생성
cp .env.example .env

# .env 파일을 열어 필수 값 입력
# - INSTAGRAM_ACCESS_TOKEN: Instagram Graph API 액세스 토큰
# - INSTAGRAM_BUSINESS_ACCOUNT_ID: Instagram 비즈니스 계정 ID
# - JWT_SECRET: 프로덕션 환경에서는 안전한 랜덤 문자열로 변경
```

### 2. Instagram API 설정

1. [Facebook Developer Portal](https://developers.facebook.com/) 접속
2. 앱 생성 후 Instagram Basic Display 또는 Instagram Graph API 제품 추가
3. Graph API Explorer에서 Long-lived Access Token 생성
4. Instagram Business Account ID 확인 (Graph API Explorer 사용)
5. `.env` 파일에 값 입력

### 3. Docker Compose로 전체 스택 실행

```bash
# 모든 서비스 시작 (PostgreSQL, Redis, Backend, Frontend, Worker)
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 특정 서비스 로그만 확인
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f worker
```

### 4. 서비스 접속

| 서비스 | URL | 비고 |
|--------|-----|------|
| Frontend | http://localhost:3000 | Vite dev server (HMR 지원) |
| Backend API | http://localhost:8000 | FastAPI (auto-reload) |
| API Docs (Swagger) | http://localhost:8000/docs | 대화형 API 문서 |
| PostgreSQL | localhost:5432 | DB 접속 (postgres/postgres) |
| Redis | localhost:6379 | 캐시/큐 |

### 5. 데이터베이스 마이그레이션

```bash
# Backend 컨테이너에서 Alembic 마이그레이션 실행
docker-compose exec backend alembic upgrade head

# 새 마이그레이션 생성
docker-compose exec backend alembic revision --autogenerate -m "description"
```

### 6. 개발 중 유용한 명령어

```bash
# 서비스 중지
docker-compose stop

# 서비스 재시작
docker-compose restart backend

# 컨테이너 및 볼륨 완전 제거 (DB 데이터 삭제됨!)
docker-compose down -v

# Backend 컨테이너에 shell 접속
docker-compose exec backend /bin/bash

# Frontend 컨테이너에 shell 접속
docker-compose exec frontend /bin/sh

# Python 의존성 재설치 (requirements.txt 변경 시)
docker-compose build backend
docker-compose up -d backend

# Node 의존성 재설치 (package.json 변경 시)
docker-compose build frontend
docker-compose up -d frontend
```

## 🧪 테스트 실행

```bash
# Backend 단위 테스트
docker-compose exec backend pytest tests/ -v

# Frontend 테스트
docker-compose exec frontend npm test

# 특정 테스트 파일만 실행
docker-compose exec backend pytest tests/unit/test_scoring.py -v
```

## 📁 프로젝트 구조

```
fasion/
├── backend/
│   ├── app/
│   │   ├── api/          # API 라우터 및 엔드포인트
│   │   ├── core/         # 설정, 보안, Celery
│   │   ├── db/           # 데이터베이스 연결
│   │   ├── models/       # SQLAlchemy 모델
│   │   ├── schemas/      # Pydantic 스키마
│   │   ├── services/     # 비즈니스 로직
│   │   └── utils/        # 유틸리티 함수
│   ├── alembic/          # DB 마이그레이션
│   ├── tests/            # 테스트
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/   # React 컴포넌트
│   │   ├── pages/        # 페이지 컴포넌트
│   │   ├── hooks/        # Custom hooks
│   │   ├── lib/          # 유틸리티 & API 클라이언트
│   │   └── styles/       # 전역 스타일
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🎨 디자인 시스템 (GiGi-Inspired)

- **배경색**: Cream `#f5f5eb`
- **강조색**: Lime green `#c4ff0e`
- **텍스트**: Black `#000000`
- **버튼**: Pill-shaped (`border-radius: 9999px`), `16px 32px` padding
- **카드**: White BG, `1px solid #e0e0d8` border, `16px` radius, `48px` padding

## 🔒 보안 주의사항

- `.env` 파일을 절대 Git에 커밋하지 마세요
- `INSTAGRAM_ACCESS_TOKEN`은 안전하게 보관하세요
- 프로덕션 환경에서는 `JWT_SECRET`을 강력한 랜덤 문자열로 변경하세요
- Instagram API Rate Limit: 200 calls/hour (공유됨)

## 📊 API Rate Limit 관리

- **분석 1회당 API 호출**: ~156회 (브랜드 1개 + 인플루언서 5명 × 26 호출)
- **Rate Limit**: 200 calls/hour
- **캐싱 전략**:
  - 프로필 데이터: TTL 6시간
  - 미디어 데이터: TTL 1시간
  - Redis 기반 중앙화된 Rate Limiter (Celery Worker 간 공유)

## 🚦 Phase 1 - Validation (현재)

현재는 검증 단계입니다. Week 3 종료 시 Go/No-Go 결정:

| 조건 | Go ✅ | Stop ❌ |
|------|-------|---------|
| 고객 신호 | 10명 중 6명 이상 유료 의향 | 3명 미만 |
| 기술 가능성 | API로 핵심 데이터 접근 가능 | API 제한으로 핵심 기능 불가 |
| 차별화 | 경쟁사 대비 2개 이상 명확한 장점 | "거의 같은 제품" |

## 📚 관련 문서

- [PRD.md](./PRD.md) - 전체 제품 요구사항
- [CLAUDE.md](./CLAUDE.md) - Claude Code 작업 가이드
- [API_주의사항.md](./API_주의사항.md) - Instagram API 제약사항
- [backend/API.md](./backend/API.md) - API 엔드포인트 문서

## 🤝 기여 가이드

1. Feature branch 생성: `git checkout -b feat/feature-name`
2. 변경사항 커밋: `git commit -m "feat(scope): description"`
3. 테스트 실행 및 통과 확인
4. Pull Request 생성

## 📝 라이선스

Proprietary - All rights reserved

---

**개발 시작하기**: `docker-compose up -d` 실행 후 http://localhost:3000 접속
