# Capstone — 디버그 기록

## PostgreSQL 전환 시 SQLite 호환 문제

### 상황

v0에서 SQLite로 동작하던 ORM 모델을 v1에서 PostgreSQL로 전환했다.
SQLAlchemy는 두 DB 모두 지원하지만, 몇몇 차이가 있었다:

1. `AUTOINCREMENT` 키워드가 PostgreSQL에서는 불필요 (SERIAL 사용)
2. `datetime` 기본값이 SQLite에서는 문자열로 저장되지만 PostgreSQL에서는 타입 체크
3. `JSON` 컬럼이 SQLite에서는 TEXT로 저장되지만 PostgreSQL에서는 JSONB 지원

### 해결

SQLAlchemy의 `dialect-agnostic` 타입을 사용했다:
- `Integer` + `primary_key=True` (AUTOINCREMENT/SERIAL 자동 처리)
- `DateTime(timezone=True)` (양쪽 모두 동작)
- `JSON` (SQLAlchemy가 dialect에 맞게 변환)

추가로 `make smoke-postgres` 명령을 만들어서 PostgreSQL 전용 테스트를 분리했다.

## provider chain에서 timeout 처리

### 상황

provider chain에서 1차 provider(Solar)가 응답을 안 할 때,
얼마나 기다려야 2차(OpenAI)로 넘어갈지 결정해야 했다.

너무 짧으면 정상 응답을 놓치고, 너무 길면 전체 파이프라인이 느려진다.

### 해결

provider별 timeout을 다르게 설정했다:
- Solar: 10초 (한국어 모델이라 속도 예측 가능)
- OpenAI: 15초
- Ollama(local): 30초 (로컬 모델이라 느릴 수 있음)

전체 chain timeout은 설정하지 않았다. 각 provider의 개별 timeout으로 충분하다.

## Docker Compose에서 서비스 시작 순서

### 상황

`docker compose up --build`로 전체를 시작하면,
API 서버가 PostgreSQL보다 먼저 시작되어 DB 연결 오류가 발생했다.

### 해결

`depends_on` + `healthcheck` 조합을 사용했다:

```yaml
services:
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 2s
      timeout: 5s
      retries: 5
  api:
    depends_on:
      db:
        condition: service_healthy
```

단순 `depends_on`만으로는 부족하다.
`condition: service_healthy`를 써야 PostgreSQL이 실제로 쿼리 수락 가능한 상태인지 확인한다.

## React 빌드 후 static 파일 서빙

### 상황

개발 환경에서는 Vite dev server가 React를 서빙하지만,
Docker 환경에서는 빌드된 static 파일을 서빙해야 한다.

### 해결

multi-stage Docker build를 사용했다:

```dockerfile
# Build stage
FROM node:20-alpine AS build
WORKDIR /app
COPY . .
RUN pnpm install && pnpm build

# Serve stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

nginx에서 SPA routing을 위해 `try_files $uri /index.html;` 설정을 추가했다.
