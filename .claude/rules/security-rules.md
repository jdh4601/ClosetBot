# Security Rules (OWASP Top 10)

## CRITICAL: Never Commit Secrets

**YOU MUST check before EVERY commit:**

```bash
# Red flags in staged files
git diff --cached | grep -E "(API_KEY|SECRET|PASSWORD|TOKEN)"
```

**If found**: STOP. Remove from code, use environment variables.

**IMPORTANT**: Files that should NEVER be committed:
- `.env`
- `*.pem`, `*.key`
- `credentials.json`
- Any file with API keys/tokens

**Already committed secret?**: Rotate immediately, don't just delete from code.

## Input Validation (MANDATORY)

**YOU MUST validate ALL external input:**

**Backend (Pydantic)**:
```python
from pydantic import BaseModel, Field, validator

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: str
    price: float = Field(gt=0, le=1000000)

    @validator('category')
    def validate_category(cls, v):
        allowed = ['jacket', 'pants', 'bag', 'shoes']
        if v not in allowed:
            raise ValueError(f'Category must be one of {allowed}')
        return v
```

**Frontend (Zod)**:
```typescript
import { z } from 'zod';

const productSchema = z.object({
  name: z.string().min(1).max(100),
  category: z.enum(['jacket', 'pants', 'bag', 'shoes']),
  price: z.number().positive().max(1000000),
});
```

**NEVER**: Trust user input. Always validate type, length, range, format.

## SQL Injection Prevention

**✅ ALWAYS use ORM**:
```python
# SQLAlchemy (safe)
product = db.query(Product).filter(Product.id == product_id).first()
```

**❌ NEVER use raw SQL with user input**:
```python
# DANGEROUS - SQL injection vulnerability
db.execute(f"SELECT * FROM products WHERE id = {product_id}")
```

## XSS Prevention

**Frontend**: React auto-escapes by default.

**CRITICAL**: NEVER render unsanitized HTML from user content.

**If HTML absolutely required**: Use DOMPurify sanitization library first.

## Authentication & Authorization

**Instagram OAuth tokens**:
- Store in database (encrypted in production)
- Never expose in API responses
- Validate on EVERY protected endpoint

**IMPORTANT**: Check authorization on ALL routes:
```python
@router.get("/posts/{post_id}")
async def get_post(
    post_id: int,
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post.user_id != current_user.id:
        raise HTTPException(403, "Not authorized")
    return post
```

## Rate Limiting

**Instagram API**: 200 requests/hour limit

**YOU MUST**:
- Log 429 errors (rate limit exceeded)
- Skip processing, don't retry
- Inform user via response logs

## CORS Configuration

**IMPORTANT**: Never use wildcard in production.

**Development**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
)
```

**Production**:
```python
allow_origins=[os.getenv("FRONTEND_URL")]
```

## Error Handling

**❌ NEVER expose internal errors**:
```python
except Exception as e:
    raise HTTPException(500, detail=str(e))  # Leaks info
```

**✅ Generic errors, log details**:
```python
except Exception as e:
    logger.error(f"Product creation failed: {e}")
    raise HTTPException(500, detail="Internal server error")
```

## Security Headers

**YOU MUST set these** (FastAPI middleware):

```python
response.headers["X-Content-Type-Options"] = "nosniff"
response.headers["X-Frame-Options"] = "DENY"
response.headers["Strict-Transport-Security"] = "max-age=31536000"
```

## Security Checklist

- [ ] No secrets in code
- [ ] All inputs validated
- [ ] SQL injection protected (ORM only)
- [ ] XSS protected
- [ ] Auth on all protected routes
- [ ] CORS configured
- [ ] Error messages generic
- [ ] Security headers set
