# 00 — 문제 정의: MCP 추천 시스템 전체 통합

## 배경

stage 00부터 07까지는 각 단계의 문제를 정의하고 설계 방향을 잡았을 뿐이다.  
실제 동작하는 코드는 이 capstone stage에서 v0 → v1 → v2 → v3로 반복적으로 구현한다.

## 문제 정의

> MCP(Model Context Protocol) 도구 추천 시스템을 baseline selector부터 시작해서,  
> reranking, feedback loop, release gate, 인증/인가까지 점진적으로 확장하라.  
> 각 버전은 독립적으로 실행 가능해야 하고, 이전 버전 대비 개선 증거를 포함해야 한다.

## 4개 버전의 범위

### v0 — Initial Demo

- Registry seed: 10+ MCP 도구를 한국어 메타데이터와 함께 등록
- Manifest validation: Zod 기반 스키마 검증
- Baseline selector: capability matching + freshness + 한국어 설명 생성
- Offline eval: golden set 기반 top-3 recall, explanation completeness 측정

**핵심 질문**: "query + 원하는 capability가 주어졌을 때, 가장 적합한 MCP 도구 3개를 한국어로 설명할 수 있는가?"

### v1 — Ranking Hardening

- Signal reranker: usage + feedback 신호를 점수에 반영
- Usage logs: impression / click / accept / dismiss 추적
- Feedback loop: 운영자가 남긴 score delta를 candidate 정렬에 반영
- Baseline/Candidate compare: nDCG@3 + uplift 기반 A/B 비교
- Catalog CRUD + Experiment CRUD: 대시보드에서 운영

**핵심 질문**: "실사용 신호를 넣으면 baseline 대비 추천 품질이 올라가는가?"

### v2 — Submission Polish

- Compatibility gate: manifest semver + clientVersion 호환성 분석
- Release gate: eval + compare + compatibility 결과를 종합해서 PASS/FAIL 판정
- Submission artifact export: gate 결과를 JSON 증빙으로 추출
- Release Candidate CRUD: RC별 lifecycle 관리
- Dry-run pipeline: 배포 전 시뮬레이션

**핵심 질문**: "이 MCP 도구를 릴리즈해도 되는지, 증거 기반으로 판단할 수 있는가?"

### v3 — OSS Hardening

- Auth/RBAC: 이메일·비밀번호 로그인, owner / operator / viewer 3레벨 권한
- pg-boss worker: eval, compare, compatibility, release gate, artifact export를 백그라운드 job으로 실행
- Audit log: 누가 언제 무엇을 했는지 추적
- Docker Compose: postgres + api + worker + web을 한 번에 올리는 self-hosted 배포
- Catalog import/export: JSON 번들로 catalog 이동

**핵심 질문**: "한 팀이 이 시스템을 직접 설치해서 권한 관리 아래 운영할 수 있는가?"

## 이 stage가 커버하지 않는 것

- Multi-workspace SaaS
- SSO / OAuth 연동
- Live GitHub 또는 패키지 레지스트리 동기화
- Webhook ingest
- 실시간 알림 (이메일, Slack)

## 기술 스택 결정 배경

| 선택 | 이유 |
|------|------|
| Fastify (not Express) | 타입스크립트 first-class, 스키마 기반 라우트, 성능 |
| Drizzle ORM (not Prisma) | SQL에 가까운 API, zero-codegen, 가벼운 migration |
| Next.js App Router | React Server Components, 파일 기반 라우팅 |
| pnpm workspace | 모노레포에서 shared/node/react 패키지 분리 |
| PostgreSQL 17 | JSON 컬럼, pg-boss 호환, 프로덕션 준비도 |
| Zod | 런타임 + 타입 동시 검증, shared 패키지의 단일 진실 소스 |
