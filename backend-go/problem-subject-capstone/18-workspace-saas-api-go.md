# 18-workspace-saas-api-go 문제지

## 왜 중요한가

웹 백엔드 공고에 제출할 수 있는 대표 포트폴리오용 B2B SaaS API를 만든다.

## 목표

시작 위치의 구현을 완성해 owner/admin/member RBAC가 있는 조직 단위 SaaS 도메인을 구현한다, POST /v1/auth/register-owner, 로그인/refresh/logout, invitation, project/issue/comment, notification, dashboard API를 제공한다, API와 worker가 별도 바이너리로 동작한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/05-portfolio-projects/18-workspace-saas-api/solution/go/cmd/api/main.go`
- `../study/05-portfolio-projects/18-workspace-saas-api/solution/go/cmd/migrate/main.go`
- `../study/05-portfolio-projects/18-workspace-saas-api/solution/go/cmd/worker/main.go`
- `../study/05-portfolio-projects/18-workspace-saas-api/solution/go/internal/auth/tokens.go`
- `../study/05-portfolio-projects/18-workspace-saas-api/solution/go/internal/auth/tokens_test.go`
- `../study/05-portfolio-projects/18-workspace-saas-api/solution/go/internal/worker/worker_test.go`
- `../study/05-portfolio-projects/18-workspace-saas-api/problem/data/create-issue.example.json`
- `../study/05-portfolio-projects/18-workspace-saas-api/problem/data/register-owner.example.json`

## starter code / 입력 계약

- `../study/05-portfolio-projects/18-workspace-saas-api/solution/go/cmd/api/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- owner/admin/member RBAC가 있는 조직 단위 SaaS 도메인을 구현한다.
- POST /v1/auth/register-owner, 로그인/refresh/logout, invitation, project/issue/comment, notification, dashboard API를 제공한다.
- API와 worker가 별도 바이너리로 동작한다.
- Postgres + Redis 기반으로 e2e와 smoke 검증이 가능해야 한다.
- 기존 학습 프로젝트를 runtime dependency로 import하지 않는다.

## 제외 범위

- Helm/GitOps 배포 자산
- MSA 분리
- `../study/05-portfolio-projects/18-workspace-saas-api/problem/data/create-issue.example.json` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `applyFiles`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestAccessTokenRoundTrip`와 `TestRefreshTokenRoundTrip`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/05-portfolio-projects/18-workspace-saas-api/problem/data/create-issue.example.json` 등 fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/backend-go/study/05-portfolio-projects/18-workspace-saas-api/solution/go test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/05-portfolio-projects/18-workspace-saas-api/solution/go test
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`18-workspace-saas-api-go_answer.md`](18-workspace-saas-api-go_answer.md)에서 확인한다.
