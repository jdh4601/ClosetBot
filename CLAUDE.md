# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Status

**Phase**: Validation (Phase 1, Week 1–3) — no production code exists yet.

This is an **influencer marketing SaaS** for Korean fashion/beauty brands. The core product lets a brand input their Instagram username + up to 5 influencer usernames and receive a 0–100 fit score for each influencer within 5 minutes, powered entirely by the Instagram Graph API (Business Discovery).

Key documents:
- `PRD.md` — full product requirements, data model, scoring algorithm, API integration details
- `인플루언서마케팅_SaaS_전략.md` — 3-phase execution strategy (validation → build → growth) with kill criteria
- `docs/plans/` — implementation plans for specific sub-systems

---

## Architecture (Planned)

```
React + TypeScript (TanStack Table, TanStack Query, Tailwind)
        │
FastAPI (Python 3.11+)  ←→  Instagram Graph API (Business Discovery)
        │                    Rate limit: 200 req/hr
        ├── Celery + Redis   (async job queue, API response cache)
        └── PostgreSQL       (profiles, media snapshots, analysis results)
```

**Critical path**: API validation (Phase 1.3) → data pipeline → quality scoring → matching → dashboard UI

**API budget per analysis job**: ~156 calls (1 brand + 5 influencers × ~26 calls each), just within the 200/hr limit. Caching is essential — profile TTL 6h, media TTL 1h.

---

## Scoring Algorithm (PRD §FR-05)

Final fit score (0–100) = weighted sum of three components:

| Component | Weight | Method |
|-----------|--------|--------|
| Brand similarity | 40% | Weighted Jaccard (hashtags + caption keywords) |
| Engagement quality | 35% | Percentile within follower tier (Nano/Micro/Mid/Macro) |
| Category fit | 25% | Category taxonomy match score |

Grades: A (80–100), B (60–79), C (40–59), D (0–39). Score breakdown must be shown to users.

---

## Development Commands

**These commands apply once scaffolding is complete.** The directories do not yet exist.

### Backend
```bash
cd backend/
source venv/bin/activate
uvicorn main:app --reload --port 8000

# Migrations
alembic revision --autogenerate -m "description"
alembic upgrade head

# Tests
pytest tests/ -v
pytest tests/unit/test_scoring.py -v   # single test file
```

### Frontend
```bash
cd frontend/
npm install
npm run dev        # http://localhost:3000
npm run build && npm run start   # production check
```

### Infrastructure
```bash
docker-compose up -d postgres redis
docker-compose up worker   # Celery worker
celery -A tasks beat       # Celery scheduler (refresh jobs)
```

---

## Available Agents

Agents are in `.claude/agents/`. Use the `Task` tool to invoke them.

### Phase 1 — Validation (use now)
| Agent | Purpose |
|-------|---------|
| `competitor-analyst` | Deep analysis of HypeAuditor, CreatorIQ, Upfluence, Grin, AspireIQ, Influe, Trashtag → feature matrix + Go/No-Go |
| `customer-researcher` | Interview script design + WTP/pain point analysis + Kill Criteria evaluation (6/10 paid intent) |
| `api-researcher` | Instagram Graph API + TikTok API PoC, rate limit analysis, scraping alternative research |

### Phase 2 — Build (use during MVP development)
| Agent | Purpose |
|-------|---------|
| `influencer-data-engineer` | Celery+Redis pipeline, PostgreSQL schema (influencer_profiles, engagement_snapshots, audience_demographics) |
| `quality-score-engineer` | Bot detection algorithm, audience match scoring, brand↔influencer matching |
| `roi-tracker` | UTM link generation, click→purchase funnel, ROI dashboard APIs, Stripe integration |

### General Development
| Agent | Purpose |
|-------|---------|
| `backend-dev` | FastAPI routes, SQLAlchemy models, Alembic migrations |
| `frontend-dev` | Next.js pages, components (GiGi design system) |
| `db-architect` | Schema design, indexing strategy |
| `code-validator` | Code quality review |
| `integration-tester` | API endpoint + E2E tests |
| `ux-analyst` | UI/UX review |

---

## Go/No-Go Kill Criteria (Week 3)

Proceed if ≥2 of 3 conditions are met:

| Condition | Go ✅ | Stop ❌ |
|-----------|-------|---------|
| Customer signal | 6/10 interviews express willingness to pay | <3 WTP confirmations |
| Technical feasibility | Core data (followers, engagement, profile) accessible via API | API limitations block core features |
| Differentiation | 2+ clear advantages vs HypeAuditor | "Basically the same product" |

---

## Design System (GiGi-Inspired)

Applied to all frontend work:
- **Colors**: Cream `#f5f5eb` (BG), Lime green `#c4ff0e` (accent), Black `#000000` (text)
- **Buttons**: Pill-shaped (`border-radius: 9999px`), `16px 32px` padding
- **Cards**: White BG, `1px solid #e0e0d8` border, `16px` radius, `48px` padding

---

## Environment Variables

**Backend `.env`**:
```
DATABASE_URL=postgresql://user:pass@localhost:5432/fasion
REDIS_URL=redis://localhost:6379/0
INSTAGRAM_ACCESS_TOKEN=...
INSTAGRAM_BUSINESS_ACCOUNT_ID=...
JWT_SECRET=...
```

**Frontend `.env.local`**:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Key Constraints

- **Instagram API**: Business Discovery endpoint only. No follower-list access, no private account data, no demographics for third-party accounts. Only business/creator accounts can be analyzed.
- **like_count**: May not be returned by Business Discovery — fall back to comment-based engagement estimate and show a "estimated" badge in the UI.
- **Rate limit**: 200 calls/hr shared across all workers. The rate limiter state must live in Redis (shared across Celery workers), not in-process.
- **Out of scope (v1)**: Follower demographics, bot detection via follower lists, image sentiment analysis, TikTok, DM automation, automatic influencer discovery.
