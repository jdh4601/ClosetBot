# API Documentation

## Fashion Influencer Matcher API

Base URL: `http://localhost:8000/api/v1`

---

## Authentication

### POST /auth/login

Login with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials
- `422 Validation Error`: Invalid email format

---

### POST /auth/register

Register a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "created_at": "2026-02-19T10:00:00Z"
}
```

**Error Responses:**
- `409 Conflict`: Email already exists
- `422 Validation Error`: Invalid input

---

## Analysis

### POST /analysis/jobs

Create a new influencer analysis job.

**Request:**
```json
{
  "brand_username": "myfashionbrand",
  "influencer_usernames": ["influencer1", "influencer2", "influencer3"]
}
```

**Validation:**
- `brand_username`: Required, 1-30 characters
- `influencer_usernames`: Required, 1-5 items

**Response (202 Accepted):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "message": "Analysis job created successfully",
  "estimated_completion_minutes": 5,
  "created_at": "2026-02-19T10:00:00Z"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid usernames
- `429 Too Many Requests`: Rate limit exceeded
- `422 Validation Error`: Invalid input format

---

### GET /analysis/jobs/{job_id}

Get the status of an analysis job.

**Response (200):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "progress_percent": 60,
  "estimated_completion_minutes": 2,
  "created_at": "2026-02-19T10:00:00Z",
  "started_at": "2026-02-19T10:00:05Z",
  "finished_at": null,
  "error_message": null
}
```

**Status Values:**
- `queued`: Job is waiting in queue
- `running`: Analysis is in progress
- `done`: Analysis completed successfully
- `failed`: Analysis failed (see error_message)

**Error Responses:**
- `404 Not Found`: Job not found

---

### GET /analysis/jobs/{job_id}/results

Get the results of a completed analysis job.

**Response (200):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "brand_username": "myfashionbrand",
  "status": "done",
  "results": [
    {
      "username": "influencer1",
      "profile_picture_url": "https://...",
      "followers_count": 45000,
      "media_count": 1230,
      "biography": "Fashion influencer based in Seoul",
      "scores": {
        "similarity_score": 92.0,
        "engagement_score": 85.0,
        "category_score": 78.0,
        "final_score": 87.0,
        "grade": "A"
      },
      "top_posts": [
        {
          "permalink": "https://instagram.com/p/...",
          "caption_preview": "Love this outfit!...",
          "engagement_rate": 9.2,
          "likes_count": 1560,
          "comments_count": 156,
          "posted_at": "2025-12-03T10:00:00Z"
        }
      ],
      "collaboration_signals": [
        {
          "brand_username": "luxury_brand",
          "collaboration_type": "paid",
          "post_permalink": "https://instagram.com/p/...",
          "posted_at": "2025-12-01T10:00:00Z"
        }
      ],
      "hashtag_distribution": {
        "fashion": 45,
        "minimal": 22,
        "ootd": 18
      },
      "common_hashtags_with_brand": ["fashion", "minimal"]
    }
  ],
  "total_api_calls": 156,
  "created_at": "2026-02-19T10:00:00Z",
  "completed_at": "2026-02-19T10:04:30Z"
}
```

**Error Responses:**
- `404 Not Found`: Job not found or not yet complete

---

## Brands

### POST /brands/analyze

Analyze a brand's Instagram profile.

**Request:**
```json
{
  "username": "myfashionbrand"
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "ig_username": "myfashionbrand",
  "followers_count": 12500,
  "media_count": 450,
  "biography": "Sustainable fashion brand from Seoul",
  "categories": ["minimal", "sustainable"],
  "top_hashtags": [
    {"hashtag": "sustainablefashion", "count": 45},
    {"hashtag": "minimal", "count": 32}
  ],
  "keywords": ["sustainable", "eco", "minimal", "korean"],
  "last_fetched_at": "2026-02-19T10:00:00Z"
}
```

**Error Responses:**
- `400 Bad Request`: Not a business/creator account
- `404 Not Found`: Account not found
- `404 Not Found`: Account not accessible (private)

---

### GET /brands/{username}

Get cached brand profile.

**Response (200):** Same as POST /brands/analyze

**Error Responses:**
- `404 Not Found`: Profile not found in cache

---

## Influencers

### GET /influencers/search?username={username}

Search for influencers (cached data only).

**Response (200):**
```json
[
  {
    "id": "uuid",
    "ig_username": "influencer1",
    "followers_count": 45000,
    "media_count": 1230,
    "biography": "Fashion influencer",
    "is_verified": false,
    "categories": ["fashion", "minimal"],
    "last_fetched_at": "2026-02-19T10:00:00Z"
  }
]
```

---

### GET /influencers/{username}

Get detailed influencer information.

**Response (200):**
```json
{
  "id": "uuid",
  "ig_username": "influencer1",
  "followers_count": 45000,
  "media_count": 1230,
  "biography": "Fashion influencer based in Seoul",
  "is_verified": false,
  "categories": ["fashion", "minimal"],
  "recent_media": [
    {
      "id": "media_id",
      "caption": "Love this outfit! #fashion #minimal",
      "comments_count": 156,
      "like_count": 1560,
      "media_type": "IMAGE",
      "permalink": "https://instagram.com/p/...",
      "posted_at": "2025-12-03T10:00:00Z"
    }
  ],
  "hashtag_distribution": {
    "fashion": 45,
    "minimal": 22
  },
  "avg_engagement_rate": 5.2,
  "last_fetched_at": "2026-02-19T10:00:00Z"
}
```

**Error Responses:**
- `404 Not Found`: Influencer not found

---

## Health

### GET /health

Health check endpoint.

**Response (200):**
```json
{
  "status": "healthy",
  "service": "fasion-api"
}
```

---

### GET /health/ready

Readiness probe (includes database and Redis checks).

**Response (200):**
```json
{
  "status": "ready",
  "checks": {
    "database": "ok",
    "redis": "ok"
  }
}
```

**Response (503):**
```json
{
  "status": "not_ready",
  "checks": {
    "database": "error",
    "redis": "ok"
  }
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| `RATE_LIMIT_EXCEEDED` | Instagram API rate limit (200/hour) exceeded |
| `ACCOUNT_NOT_FOUND` | Instagram account not found or not accessible |
| `PRIVATE_ACCOUNT` | Account is private or not a business/creator account |
| `ANALYSIS_FAILED` | Analysis job failed |
| `INVALID_USERNAME` | Invalid Instagram username format |
| `CACHE_MISS` | Data not found in cache |

---

## Rate Limiting

API endpoints are rate limited per IP address:

- General endpoints: 100 requests/minute
- Analysis endpoints: 10 requests/minute
- Instagram API: 200 calls/hour (enforced by Instagram)

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1645272000
```

---

## Data Retention

- Analysis results: 90 days
- Cached profiles: 6 hours
- Cached media: 1 hour
- Job history: 90 days

After retention period, data is automatically deleted per Meta Developer Policy.
