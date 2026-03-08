# Verification

## Commands

```bash
cd 05-portfolio-projects/18-workspace-saas-api/go
go test ./...
make e2e
make smoke

cd ../../..
make test-portfolio-unit test-portfolio-repro
make test-all
```

## Result

- `go test ./...` 통과
- `make e2e` 통과
  - owner 가입
  - project 생성
  - invitation 생성 및 수락
  - issue 생성과 idempotent replay
  - optimistic locking conflict
  - comment 생성
  - worker outbox 소비와 notification 생성
  - dashboard summary 조회
  - refresh rotation / logout revoke
- `make smoke` 통과
  - 실제 API/worker 바이너리를 띄운 뒤 curl 시나리오가 `smoke scenario completed successfully`로 끝났다.
- [presentation-assets/demo-2026-03-07](presentation-assets/demo-2026-03-07)는
  `./scripts/demo_capture.sh`를 실제로 실행해 생성했다.
  이번 라운드에서는 Docker Desktop이 비정상 응답이라, 로컬 Postgres/Redis 임시 프로세스를 띄운 뒤 같은 앱 바이너리로 캡처를 만들었다.
- `make test-portfolio-unit test-portfolio-repro` 통과
- `make test-all` 통과

## OpenAPI Alignment

- `openapi.yaml`에 적어 둔 핵심 응답 필드 `access_token`, `refresh_token`,
  `memberships[].organization_id`, `project.id`, `issue.id`, `issue.version`,
  `notifications[]`, `summary.projects_total`은 `e2e`와 `smoke`에서 실제로 파싱했다.
- 문서와 구현을 동시에 바꾸는 대신, smoke/e2e가 기대하는 필드를 OpenAPI와 같게 두는 방식으로 drift를 줄였다.

## Out Of Scope

- Helm/GitOps 배포 자산
- 외부 프런트엔드 연동
