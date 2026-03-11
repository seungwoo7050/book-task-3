# MCP 추천 데모 v3 OSS 고도화

`v3-oss-hardening`은 `v2-submission-polish`를 self-hosted OSS 후보로 끌어올린 제품화 확장 버전이다. 목표는 새 추천 기능을 더 넣는 것이 아니라, 한 팀이 직접 설치해서 로그인된 권한 아래 catalog, experiment, release candidate, release gate를 운영할 수 있게 만드는 것이다.

`v2`는 여전히 최종 capstone 데모이고, `v3`는 그 위에 얹은 productization extension이다.

## 이 버전에서 할 수 있는 것

- 이메일/비밀번호 로그인과 `owner | operator | viewer` 권한으로 콘솔을 구분할 수 있다.
- MCP catalog를 import/export하고 CRUD로 직접 운영할 수 있다.
- baseline/candidate 추천은 즉시 실행하고, eval/compare/compatibility/release gate/artifact export는 background job으로 안전하게 실행할 수 있다.
- audit log, job activity, latest artifact preview로 운영 흔적을 추적할 수 있다.
- `docker compose up -d --build` 한 번으로 `postgres + api + worker + web`를 single-node 환경에 올릴 수 있다.

## 권장 읽기 순서

1. 상위 [`../README.md`](../README.md)
2. [`../docs/README.md`](../docs/README.md)
3. 이 문서
4. 필요하면 `node/`, `react/`, `shared/`, `docs/`를 차례로 읽는다

## 패키지 구성

- `shared/`: Zod contracts, seed catalog, offline eval fixtures
- `node/`: Fastify API, auth/session, RBAC, pg-boss worker, Drizzle/PostgreSQL
- `react/`: Next.js 운영 콘솔
- `problem/`: v3 범위와 acceptance criteria
- `docs/`: install, security, operations, API, backup/restore, proof, 발표 문서
- `notion/`: 레포에 함께 보관하는 공개 백업 문서

## 빠른 시작

### 로컬

```bash
pnpm install
cp .env.example .env
pnpm db:up
pnpm migrate
pnpm seed
pnpm bootstrap:owner
pnpm dev
```

- Web: `http://127.0.0.1:3003`
- API: `http://127.0.0.1:3103`

### 컨테이너 실행

```bash
docker compose up -d --build
```

Compose는 `postgres + api + worker + web`를 함께 올리고, API 컨테이너에서 migration을 적용한 뒤 서버를 시작한다.

## 검증 명령

```bash
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

## 포트폴리오 관점 메모

- `v0~v2`는 학습 흐름과 제출 증빙을 보여 주고, `v3`는 설치 가능한 운영 버전까지의 확장을 보여 준다.
- 학생 입장에서는 "최종 제출 버전"과 "제품화 확장 버전"을 분리하는 README 구조를 참고하면 좋다.
- 세부 판단 과정은 stage별 `notion/`과 capstone `notion/`에 백업해 둔다.

## 범위 밖

- multi-workspace SaaS
- SSO/OAuth
- live GitHub or package registry sync
- webhook ingest
