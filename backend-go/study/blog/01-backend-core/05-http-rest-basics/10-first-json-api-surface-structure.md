# 05 HTTP REST Basics Structure

## 이 글이 답할 질문

- HTTP method와 상태 코드를 단순 암기가 아니라 직접 선택해야 한다.
- 저장소 복잡도를 제거해 상태 코드와 요청 검증에 집중하도록 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `01-backend-core/05-http-rest-basics` 안에서 `10-first-json-api-surface.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: Phase 1: 프로젝트 뼈대 -> Phase 2: 핵심 타입과 서버 구조 -> Phase 3: 핸들러 구현
- 세션 본문: `internal/, solution/go/internal/api/api.go, "GET /v1/healthcheck", "POST /v1/tasks"` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/internal/api/api.go`
- 코드 앵커 2: `solution/go/cmd/server/main.go`
- 코드 설명 초점: 이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.
- 개념 설명: `GET /v1/healthcheck`는 서비스 생존 여부를 확인하는 최소 endpoint다.
- 마지막 단락: 다음 글에서는 `20-validation-pagination-and-idempotency.md`에서 이어지는 경계를 다룬다.
