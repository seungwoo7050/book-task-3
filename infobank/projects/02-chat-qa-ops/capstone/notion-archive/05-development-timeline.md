> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../docs/catalog/path-migration-map.md)를 본다.

# Capstone — 개발 타임라인

## v0 — Initial Demo

### 1단계: 프로젝트 구조 생성

```bash
mkdir -p chat-qa-ops/08-capstone-submission/v0-initial-demo/{python/{src,tests},react,docs/demo/proof-artifacts,docs/presentation}
```

### 2단계: Python 백엔드 설정

```bash
cd v0-initial-demo/python
cat > pyproject.toml << 'EOF'
[project]
name = "capstone-v0"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115",
    "uvicorn>=0.34",
    "sqlalchemy>=2.0",
]
[project.optional-dependencies]
dev = ["pytest", "httpx"]
EOF

uv sync --extra dev
```

### 3단계: DB 초기화 + 데모 데이터

```bash
make init-db     # SQLite DB 생성 + 테이블 마이그레이션
make seed-demo   # 데모용 상담 데이터/golden case 삽입
make test-backend
```

### 4단계: React 대시보드 연결

```bash
cd v0-initial-demo/react
pnpm install
pnpm test --run
```

stage 07 React 코드를 복사하고, API 경로를 v0 백엔드에 맞게 조정했다.

---

## v1 — Regression Hardening

### 1단계: v0 폴더 복제

```bash
cp -r v0-initial-demo v1-regression-hardening
```

### 2단계: provider chain 추가

```bash
cd v1-regression-hardening/python
# provider chain 모듈 추가
# 의존성 추가
uv add openai anthropic httpx
```

Solar, OpenAI, Ollama 각각의 adapter 파일 생성 후,
chain을 실행하는 `run_judge_chain()` 함수를 구현했다.

### 3단계: PostgreSQL smoke test

```bash
# PostgreSQL이 로컬에 있어야 함
UV_PYTHON=python3.12 make smoke-postgres
```

Makefile에 `smoke-postgres` 타겟 추가:

```makefile
smoke-postgres:
	DATABASE_URL=postgresql://... pytest tests/ -x -v -k postgres
```

### 4단계: Langfuse 준비

```bash
uv add langfuse
```

trace envelope 구조만 정의하고, 실제 Langfuse 서버 연동은 v3에서 진행.

---

## v2 — Submission Polish

### 1단계: v1 복제 + retrieval-v2

```bash
cp -r v1-regression-hardening v2-submission-polish
cd v2-submission-polish/python
```

retrieval-v2 모듈 추가:
- alias 매핑 dict 정의
- category 태그 + 필터 로직
- risk keyword 기반 rerank

### 2단계: compare artifact 생성

```bash
# golden set을 baseline(v1 코드)과 candidate(v2 코드)로 각각 실행
make run-golden-baseline
make run-golden-candidate
make generate-compare
```

결과 파일: `docs/demo/proof-artifacts/compare.json`

### 3단계: improvement report

compare.json 기반으로 마크다운 리포트 자동 생성:

```bash
make generate-report
# docs/demo/proof-artifacts/improvement-report.md
```

---

## v3 — Self-Hosted OSS

### 1단계: v2 복제 + auth 추가

```bash
cp -r v2-submission-polish v3-self-hosted-oss
cd v3-self-hosted-oss/python
uv add passlib[bcrypt] python-jose[cryptography]
```

관리자 인증: JWT 토큰 기반, 단일 관리자 계정.

### 2단계: 비동기 worker

evaluation job을 큐에 넣고 별도 프로세스에서 처리하는 worker 구현.
Redis/Celery 대신 DB 기반 간단한 job queue를 구현했다 (scope 제한).

### 3단계: Docker Compose 작성

```bash
cat > docker-compose.yml << 'EOF'
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: postgres
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 2s
      timeout: 5s
      retries: 5
  api:
    build: ./python
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8000:8000"
  web:
    build: ./react
    ports:
      - "5173:80"
  worker:
    build: ./python
    command: python -m worker
    depends_on:
      db:
        condition: service_healthy
EOF
```

### 4단계: 검증

```bash
docker compose up --build
# 브라우저에서 http://localhost:5173 접속
# admin@example.com / password123 으로 로그인
```

## 비고

- 각 버전 폴더는 이전 버전의 완전한 복제본이다. git diff가 아닌 폴더 비교로 delta를 추적한다.
- v0~v2는 archive/demo 전용, v3이 실제 배포 대상이다.
- v3의 AI profile은 optional이므로 외부 API key 없이도 동작한다.
