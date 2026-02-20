# Fashion Influencer Matcher API

## 개발 환경 설정

### 1. 가상환경 생성 및 활성화

```bash
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일 편집하여 필요한 값 설정
```

### 4. 데이터베이스 마이그레이션

```bash
alembic upgrade head
```

### 5. 개발 서버 실행

```bash
uvicorn main:app --reload --port 8000
```

## API 문서

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 테스트 실행

```bash
pytest tests/ -v
```
