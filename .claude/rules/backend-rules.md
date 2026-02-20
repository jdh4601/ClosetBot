# Backend Development Rules (FastAPI)

## Path: backend/**/*.py

## CRITICAL: Security Requirements

**YOU MUST validate ALL user input:**

- Type validation (Pydantic models required)
- Length/range checks
- SQL injection prevention (use SQLAlchemy ORM, NEVER raw SQL)
- XSS prevention (sanitize before rendering)

**NEVER**:
- Store secrets in code (use environment variables)
- Log sensitive data (passwords, tokens, API keys)
- Expose internal errors to clients (generic error messages only)

## API Design Standards

**IMPORTANT**: Every endpoint must include:

- Request validation (Pydantic schema)
- Response schema (return type hint)
- Error handling (try/except with HTTPException)
- Status codes (200, 201, 400, 401, 404, 500)

**Example**:
```python
@router.post("/posts/{post_id}/products", status_code=201)
async def create_product(
    post_id: int,
    product: ProductCreate,  # Pydantic validation
    db: Session = Depends(get_db)
) -> ProductResponse:  # Response schema
    try:
        # Implementation
        return ProductResponse.from_orm(db_product)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## Async/Await Requirements

**YOU MUST use async for ALL I/O operations:**

- Database queries: `await db.execute()`
- HTTP requests: `async with httpx.AsyncClient()`
- File operations: `async with aiofiles.open()`
- Instagram API calls: `await instagram_client.get()`

**NEVER**: Use synchronous blocking calls in async routes.

## Error Handling Pattern

**IMPORTANT**: Use this exact pattern:

```python
try:
    # Business logic
except ValueError as e:
    # User error (400)
    raise HTTPException(status_code=400, detail=str(e))
except UnauthorizedError:
    # Auth error (401)
    raise HTTPException(status_code=401, detail="Unauthorized")
except NotFoundError:
    # Not found (404)
    raise HTTPException(status_code=404, detail="Resource not found")
except Exception as e:
    # Server error (500) - log but don't expose
    logger.error(f"Internal error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

## Instagram API Integration

**Rate Limits**: 200 requests/hour

**YOU MUST**:
- Log 429 errors (rate limit exceeded)
- Skip processing, don't retry in MVP
- Store rate limit status in response logs

**NEVER**: Retry failed requests automatically (avoid hitting rate limits faster).

## Database Operations

**YOU MUST**:
- Use SQLAlchemy ORM (no raw SQL)
- Run migrations with Alembic
- Add database indexes for foreign keys
- Use transactions for multi-table operations

**Example**:
```python
async with db.begin():
    post = await db.get(Post, post_id)
    product = Product(**product_data)
    post.products.append(product)
    await db.commit()
```

## Environment Variables

**REQUIRED in .env**:
- `DATABASE_URL`
- `OPENAI_API_KEY`
- `INSTAGRAM_APP_ID`
- `INSTAGRAM_APP_SECRET`
- `WEBHOOK_VERIFY_TOKEN`

**NEVER commit .env file to git.**
