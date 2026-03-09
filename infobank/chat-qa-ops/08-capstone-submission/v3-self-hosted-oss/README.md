# Study 2 Capstone v3

`v3-self-hosted-oss`는 `v2-submission-polish`를 single-team self-hosted QA Ops OSS snapshot으로 승격한 버전이다.

## What You Can Do

- 관리자 로그인 후 상담 transcript JSONL을 업로드할 수 있다.
- Markdown ZIP 기반 KB bundle을 업로드할 수 있다.
- dataset + KB bundle 조합으로 비동기 evaluation job을 생성할 수 있다.
- 선택한 job/run 기준으로 overview, failures, session review를 볼 수 있다.
- baseline/candidate run label 비교로 배포 승인 판단 근거를 만들 수 있다.

## Supported Workflow

`로그인 -> dataset import -> KB import -> job 생성 -> worker 처리 -> dashboard / session review`

## Quickstart

가장 단순한 경로는 Docker Compose다.

```bash
cd study2/08-capstone-submission/v3-self-hosted-oss
docker compose up --build
```

기본 접속:

- Web: `http://localhost:5173`
- API: `http://localhost:8000`
- Admin email: `admin@example.com`
- Admin password: `password123`

Compose 기본 모드는 외부 API key 없이 동작한다.

- evaluator mode: heuristic
- retrieval backend: keyword
- database: PostgreSQL
- optional profile: `ai` (`ollama`, `chroma`)

AI profile이 필요하면:

```bash
docker compose --profile ai up --build
```

## Repository Position

- supported self-host target: `v3-self-hosted-oss`
- archive/demo only: `v0-initial-demo`
- archive/demo only: `v1-regression-hardening`
- archive/demo only: `v2-submission-polish`

## Local Validation

백엔드:

```bash
cd python
UV_PYTHON=python3.12 uv sync --extra dev
UV_PYTHON=python3.12 make gate-all
```

프론트엔드:

```bash
cd react
pnpm install
pnpm test --run
```

## Known Scope

- single admin auth만 지원한다.
- transcript는 이미 생성된 `user_message` / `assistant_response` pair 평가용이다.
- multi-tenant, RBAC, SSO, billing, Redis/Celery, Kubernetes는 범위 밖이다.
