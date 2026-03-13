# 18 Workspace SaaS API Series Map

`05-portfolio-projects/18-workspace-saas-api`는 JWT auth, 조직 단위 RBAC, async notification, Redis cache를 한 제품형 API로 묶은 대표 포트폴리오 과제다.

## 이 시리즈가 복원하는 것

- 시작점: 채용 제출용 B2B SaaS API를 로컬에서 완결형으로 재현할 수 있어야 한다.
- 구현 축: API server, worker, Postgres repository, Redis cache/session store, OpenAPI, e2e, smoke를 `solution/go`에 구현했다.
- 검증 축: `go test ./...` 통과
- 글 수: 5편

## 읽는 순서

- [10-bootstrap-schema-and-platform.md](10-bootstrap-schema-and-platform.md)
- [20-auth-and-session-rotation.md](20-auth-and-session-rotation.md)
- [30-repository-service-cache-boundaries.md](30-repository-service-cache-boundaries.md)
- [40-http-worker-seed-and-smoke-surface.md](40-http-worker-seed-and-smoke-surface.md)
- [50-repro-demo-and-portfolio-proof.md](50-repro-demo-and-portfolio-proof.md)

## 근거 기준

- 소스코드, README, docs, 테스트, CLI만 입력 근거로 사용했다.
- 기존 blog 초안과 `_legacy` 본문은 입력 근거로 사용하지 않았다.
