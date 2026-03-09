# 05 — 개발 타임라인: 전체 빌드·실행·테스트·배포 명령어

## Phase 1: v0 — Initial Demo

### 1-1. 프로젝트 초기화

```bash
mkdir -p 08-capstone-submission/v0-initial-demo
cd 08-capstone-submission/v0-initial-demo

# pnpm workspace 설정
cat > pnpm-workspace.yaml << 'EOF'
packages:
  - shared
  - node
  - react
EOF

pnpm init
```

### 1-2. shared 패키지 생성

```bash
mkdir -p shared/src
cd shared && pnpm init

# Zod 설치
pnpm add zod

# contracts.ts — mcpManifestSchema, catalogEntrySchema 등
# catalog.ts — 10+ seed MCP 도구 (한국어 메타데이터 포함)
# eval.ts — golden set eval cases
```

### 1-3. API 서버 구축

```bash
mkdir -p node/src/db node/src/repositories node/src/services
cd node && pnpm init

# 의존성 설치
pnpm add fastify @fastify/cors drizzle-orm postgres
pnpm add -D drizzle-kit typescript @types/node vitest

# Drizzle 설정
cat > drizzle.config.ts  # PostgreSQL 연결 설정

# DB schema 정의
# node/src/db/schema.ts

# migration 생성 및 적용
pnpm exec drizzle-kit generate
pnpm exec drizzle-kit migrate
```

### 1-4. PostgreSQL 준비

```bash
# Docker로 PostgreSQL 실행
docker run -d --name study1-postgres \
  -e POSTGRES_DB=study1_v0 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5540:5432 \
  postgres:17-alpine

# DB 준비 확인
pg_isready -h 127.0.0.1 -p 5540 -U postgres
```

### 1-5. Seed 실행 및 서버 기동

```bash
# seed 실행 (catalog 도구 등록)
pnpm seed

# 개발 서버 시작
pnpm dev
# API: http://127.0.0.1:3100

# 추천 테스트
curl -X POST http://127.0.0.1:3100/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"query":"manifest 호환성 체크","desiredCapabilities":["release-management"],"preferredCategories":["ops"],"environment":{"locale":"ko-KR","clientVersion":"1.2.0","transport":"stdio","platform":"node"},"maxResults":3}'
```

### 1-6. Offline eval 실행

```bash
pnpm eval
# top3Recall: 0.xxx
# explanationCompleteness: 1.0
# forbiddenHitRate: 0.0
```

## Phase 2: v1 — Ranking Hardening

### 2-1. v0 복사 및 확장

```bash
cp -r v0-initial-demo v1-ranking-hardening
cd v1-ranking-hardening

# 포트 변경: 3100 → 3101, 3000 → 3001
# shared/src/contracts.ts에 experimentConfigSchema, feedbackRecordSchema, usageEventSchema 추가
```

### 2-2. Reranker 구현

```bash
# node/src/services/rerank-service.ts 생성
# signal-rerank: usage + feedback → score boost

# candidate 라우트 추가
# POST /api/recommendations/candidate
```

### 2-3. Usage & Feedback API 추가

```bash
# usage event 기록
curl -X POST http://127.0.0.1:3101/api/usage-events \
  -H "Content-Type: application/json" \
  -d '{"id":"evt-1","recommendationRunId":"run-1","catalogId":"release-check-bot","action":"accept","actor":"operator","createdAt":"2024-01-01T00:00:00Z","metadata":{}}'

# feedback 기록
curl -X POST http://127.0.0.1:3101/api/feedback \
  -H "Content-Type: application/json" \
  -d '{"id":"fb-1","recommendationRunId":"run-1","catalogId":"release-check-bot","scoreDelta":2,"noteKo":"정렬이 적절했습니다","reviewer":"cli","createdAt":"2024-01-01T00:00:00Z"}'
```

### 2-4. Compare 실행

```bash
pnpm compare
# baselineNdcg3: 0.xxx
# candidateNdcg3: 0.xxx
# uplift: +0.xxx
```

### 2-5. 대시보드 구현

```bash
cd react
pnpm dev
# http://localhost:3001 — MPC Dashboard
# Baseline 실행, Candidate 실행, Compare 갱신 확인
```

### 2-6. 테스트 실행

```bash
pnpm test
# selector, reranker unit test
pnpm test:integration
# DB 연동 라우트 test (PostgreSQL 필요)
```

## Phase 3: v2 — Submission Polish

### 3-1. v1 복사 및 확장

```bash
cp -r v1-ranking-hardening v2-submission-polish
cd v2-submission-polish

# 포트 변경: 3101 → 3102, 3001 → 3002
# shared에 releaseCandidateSchema, compatibilityReportSchema 등 추가
```

### 3-2. Release Candidate + Gate 구현

```bash
# RC 생성
curl -X POST http://127.0.0.1:3102/api/release-candidates \
  -H "Content-Type: application/json" \
  -d '{"id":"rc-release-check-bot-1-5-0","name":"release-check-bot RC","manifestId":"release-check-bot","previousVersion":"1.0.0","releaseVersion":"1.5.0","targetClientVersion":"1.2.0",...}'

# compatibility gate 실행
pnpm compatibility rc-release-check-bot-1-5-0

# release gate 실행
pnpm release:gate rc-release-check-bot-1-5-0

# artifact export
pnpm artifact:export rc-release-check-bot-1-5-0
```

### 3-3. e2e 테스트

```bash
# Playwright 설치
pnpm add -D @playwright/test
npx playwright install --with-deps chromium

# 테스트 실행 (API + Web 서버 기동 상태에서)
pnpm e2e
```

## Phase 4: v3 — OSS Hardening

### 4-1. v2 복사 및 확장

```bash
cp -r v2-submission-polish v3-oss-hardening
cd v3-oss-hardening

# 포트 변경: 3102 → 3103, 3002 → 3003
# shared에 auth, job, audit 관련 스키마 추가
```

### 4-2. Auth / RBAC 구현

```bash
# auth-service.ts, audit-service.ts 생성
# resolveAuth() 미들웨어 추가

# owner 계정 부트스트랩
cp .env.example .env
# BOOTSTRAP_OWNER_EMAIL=owner@study1.local
# BOOTSTRAP_OWNER_PASSWORD=ChangeMe123!
pnpm bootstrap:owner

# 로그인 테스트
curl -X POST http://127.0.0.1:3103/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"owner@study1.local","password":"ChangeMe123!"}' \
  -c cookies.txt

# 인증된 요청
curl http://127.0.0.1:3103/api/auth/me -b cookies.txt
```

### 4-3. pg-boss Worker 구현

```bash
# worker.ts 생성 — pg-boss consumer
# job-service.ts — enqueue 로직

# worker 단독 실행
pnpm worker

# job enqueue (API 경유)
curl -X POST http://127.0.0.1:3103/api/jobs/enqueue \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"jobName":"eval"}'
```

### 4-4. Docker Compose

```bash
# Dockerfile.api, Dockerfile.web, Dockerfile.worker 작성
# docker-compose.yml 작성

# 빌드 및 실행
docker compose up -d --build

# 상태 확인
docker compose ps
docker compose logs -f api

# 종료
docker compose down
docker compose down -v  # 볼륨까지 삭제
```

### 4-5. 전체 검증

```bash
# 로컬 모드
pnpm install
cp .env.example .env
pnpm db:up
pnpm migrate
pnpm seed
pnpm bootstrap:owner
pnpm dev

# 검증 명령 (순서대로)
pnpm build
pnpm test
pnpm test:integration
pnpm eval
pnpm compare
pnpm compatibility rc-release-check-bot-1-5-0
pnpm release:gate rc-release-check-bot-1-5-0
pnpm artifact:export rc-release-check-bot-1-5-0
pnpm e2e
pnpm capture:presentation
```

### 4-6. Docker 모드 검증

```bash
docker compose up -d --build
# Web: http://127.0.0.1:3003
# API: http://127.0.0.1:3103
# owner@study1.local / ChangeMe123! 로 로그인
```
