# 05 HTTP REST Basics Evidence Ledger

## 10 first-json-api-surface

- 시간 표지: Phase 1: 프로젝트 뼈대 -> Phase 2: 핵심 타입과 서버 구조 -> Phase 3: 핸들러 구현
- 당시 목표: HTTP method와 상태 코드를 단순 암기가 아니라 직접 선택해야 한다.
- 변경 단위: `internal/`, `solution/go/internal/api/api.go`, `"GET /v1/healthcheck"`, `"POST /v1/tasks"`, `"GET /v1/tasks"`, `"GET /v1/tasks/{id}"`
- 처음 가설: 저장소 복잡도를 제거해 상태 코드와 요청 검증에 집중하도록 했다.
- 실제 조치: 디렉터리 구조 생성 `internal/` 디렉터리를 처음 사용했다. Go에서 `internal/` 패키지는 같은 모듈 내에서만 import할 수 있다. API 핸들러를 외부에 노출하지 않겠다는 의도다. Task struct 정의 (`solution/go/internal/api/api.go`) `Task` struct에 JSON 태그를 붙임. `ID`, `Title`, `CreatedAt` 세 필드.

CLI:

```bash
mkdir -p 01-backend-core/05-http-rest-basics/{solution/go/cmd/server,solution/go/internal/api,docs/concepts,docs/references,problem}

cd 01-backend-core/05-http-rest-basics/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/05-http-rest-basics
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/internal/api/api.go`
- 새로 배운 것: `GET /v1/healthcheck`는 서비스 생존 여부를 확인하는 최소 endpoint다.
- 다음: 다음 글에서는 `20-validation-pagination-and-idempotency.md`에서 이어지는 경계를 다룬다.
