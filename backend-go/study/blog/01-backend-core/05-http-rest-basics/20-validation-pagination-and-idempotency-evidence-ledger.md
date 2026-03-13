# 05 HTTP REST Basics Evidence Ledger

## 20 validation-pagination-and-idempotency

- 시간 표지: Phase 4: CLI 서버 -> Phase 5: 테스트 -> Phase 6: 문서 및 최종 검증
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/cmd/server/main.go`, `solution/go/internal/api/api_test.go`
- 처음 가설: idempotency는 완성형 분산 설계가 아니라 “왜 필요한가”를 보여 주는 최소 형태로 제한했다.
- 실제 조치: main.go 작성 (`solution/go/cmd/server/main.go`) 서버 실행 및 curl 테스트 httptest 기반 테스트 (`solution/go/internal/api/api_test.go`) 테스트 실행

CLI:

```bash
# 터미널 1: 서버 시작
cd solution/go
go run ./cmd/server

# 터미널 2: curl 테스트
curl http://localhost:4020/v1/healthcheck
# {"status":"available"}

curl -X POST http://localhost:4020/v1/tasks -d '{"title":"write docs"}'
# {"task":{"id":1,"title":"write docs","created_at":"..."}}

curl -X POST http://localhost:4020/v1/tasks -d '{"title":"write docs"}' -H "Idempotency-Key: abc"
# 201 Created (첫 번째)

curl -X POST http://localhost:4020/v1/tasks -d '{"title":"write docs"}' -H "Idempotency-Key: abc"
# 200 OK (재시도)

curl http://localhost:4020/v1/tasks
# {"tasks":[...],"meta":{"page":1,"page_size":20,"total":2}}

curl http://localhost:4020/v1/tasks/1
# {"task":{"id":1,...}}

curl http://localhost:4020/v1/tasks/999
# {"error":{"message":"task not found"}} (404)

cd solution/go
go test ./...
go test -v ./internal/api/
```

- 검증 신호:
- 2026-03-07 기준 `go test ./...`가 통과했다.
- 서버 실행은 로컬에서 가능한 상태이며 기본 포트는 `:4020`이다.
- 남은 선택 검증: persistence와 인증은 이 과제 범위에 포함하지 않았다.
- 핵심 코드 앵커: `solution/go/internal/api/api_test.go`
- 새로 배운 것: 생성 성공은 `201`, 같은 idempotency key 재시도는 `200`으로 분리했다.
- 다음: persistence와 인증은 이 과제 범위에 포함하지 않았다.
