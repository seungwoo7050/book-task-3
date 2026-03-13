# 18 Workspace SaaS API — Repro Demo And Portfolio Proof

`05-portfolio-projects/18-workspace-saas-api`는 JWT auth, 조직 단위 RBAC, async notification, Redis cache를 한 제품형 API로 묶은 대표 포트폴리오 과제다. 이 글에서는 Phase 12 — 전체 재현성 검증 -> Phase 13 — Demo Capture 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- Phase 12 — 전체 재현성 검증
- Phase 13 — Demo Capture

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `scripts/demo_capture.sh`
- 처음 가설: worker와 API를 바이너리 수준에서 분리해 async notification과 web request 경계를 명확히 했다.
- 실제 진행: 한 명령으로 전체 검증: `scripts/demo_capture.sh` — 프레젠테이션용 아티팩트 생성. 실제 API 호출의 요청/응답을 캡처하여 문서화에 활용.

CLI:

```bash
make repro

make up → make migrate → make seed → make test → make test-race → make e2e → make smoke
```

검증 신호:

- make up → make migrate → make seed → make test → make test-race → make e2e → make smoke
- `go test ./...` 통과
- `make e2e` 통과
- `make smoke` 통과
- [presentation-assets/demo-2026-03-07](presentation-assets/demo-2026-03-07)는

핵심 코드: `solution/go/scripts/smoke.sh`

```text
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${PORT:-4080}"
DATABASE_URL="${DATABASE_URL:-postgres://postgres:postgres@localhost:54339/workspace_saas?sslmode=disable}"
REDIS_ADDR="${REDIS_ADDR:-localhost:6381}"
JWT_SECRET="${JWT_SECRET:-workspace-saas-secret}"
WORKER_POLL_INTERVAL="${WORKER_POLL_INTERVAL:-250ms}"
BASE_URL="http://127.0.0.1:${PORT}"
API_LOG="$(mktemp)"
WORKER_LOG="$(mktemp)"

cleanup() {
  if [[ -n "${API_PID:-}" ]]; then kill "${API_PID}" >/dev/null 2>&1 || true; fi
  if [[ -n "${WORKER_PID:-}" ]]; then kill "${WORKER_PID}" >/dev/null 2>&1 || true; fi
  rm -f "${API_LOG}" "${WORKER_LOG}"
}
```

왜 이 코드가 중요했는가:

이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.

새로 배운 것:

- 대표작의 검증 가치는 API 문서, e2e, smoke가 같이 돌아갈 때 생긴다.

보조 코드: `solution/go/e2e/workspace_flow_test.go`

```go
func TestWorkspaceSaaSFlow(t *testing.T) {
	t.Parallel()

	ctx := context.Background()
	cfg := platform.LoadConfig()
	store, err := repository.Open(ctx, cfg.DatabaseURL)
	if err != nil {
		t.Fatalf("open store: %v", err)
	}
	defer store.Close()

	if err := resetDatabase(ctx, store.DB()); err != nil {
		t.Fatalf("reset database: %v", err)
	}
	if err := flushRedis(ctx, cfg); err != nil {
		t.Fatalf("flush redis: %v", err)
	}
```

왜 이 코드도 같이 봐야 하는가:

이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.

CLI:

```bash
cd 05-portfolio-projects/18-workspace-saas-api/go
go test ./...
make e2e
make smoke

cd ../../..
make test-portfolio-unit test-portfolio-repro
make test-all
```

검증 신호:

- `go test ./...` 통과
- `make e2e` 통과
- `make smoke` 통과
- [presentation-assets/demo-2026-03-07](presentation-assets/demo-2026-03-07)는
- `make test-portfolio-unit test-portfolio-repro` 통과

다음:

- 선택 검증이나 운영 환경에서만 가능한 경계를 짧게 남긴다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/scripts/smoke.sh` 같은 결정적인 코드와 `cd 05-portfolio-projects/18-workspace-saas-api/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
