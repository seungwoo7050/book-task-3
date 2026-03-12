# 개발 타임라인 — 처음부터 끝까지

이 문서는 프로젝트 05를 처음부터 완성까지 만드는 전체 과정을 시간순으로 기록한다.

---

## Phase 1: 프로젝트 뼈대

### 1-1. 디렉터리 구조 생성

```bash
mkdir -p 01-backend-core/05-http-rest-basics/{solution/go/cmd/server,solution/go/internal/api,docs/concepts,docs/references,problem}
```

`internal/` 디렉터리를 처음 사용했다. Go에서 `internal/` 패키지는 같은 모듈 내에서만 import할 수 있다. API 핸들러를 외부에 노출하지 않겠다는 의도다.

### 1-2. Go 모듈 초기화

```bash
cd 01-backend-core/05-http-rest-basics/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/05-http-rest-basics
```

Go 1.22, 외부 의존성 없음. 표준 라이브러리만 사용.

### 1-3. Workspace 등록

```bash
cd study
go work use 01-backend-core/05-http-rest-basics/go
```

---

## Phase 2: 핵심 타입과 서버 구조

### 2-1. Task struct 정의 (`solution/go/internal/api/api.go`)

`Task` struct에 JSON 태그를 붙임. `ID`, `Title`, `CreatedAt` 세 필드.

### 2-2. Server struct

`sync.Mutex`로 보호되는 인메모리 스토어. `tasks` 슬라이스, `nextID` 카운터, `idempotentCreate` 맵.

### 2-3. 라우터 구성 (`Routes` 메서드)

Go 1.22의 새 라우팅 문법 사용. `"GET /v1/healthcheck"`, `"POST /v1/tasks"`, `"GET /v1/tasks"`, `"GET /v1/tasks/{id}"` 네 개의 라우트 등록.

---

## Phase 3: 핸들러 구현

### 3-1. healthcheck

가장 먼저 만든 핸들러. `{"status": "available"}` JSON 반환. 서버가 동작하는지 확인하는 최소 기능.

### 3-2. createTask

1. JSON 디코딩 — 실패 시 400
2. title 빈 문자열 검증 — 실패 시 422
3. Idempotency-Key 확인 — 기존 키면 200으로 기존 Task 반환
4. 새 Task 생성, 슬라이스에 추가, idempotency 맵에 저장 — 201 반환

### 3-3. listTasks

1. page, page_size 쿼리 파라미터 파싱 (기본값: page=1, page_size=20)
2. bounds check으로 슬라이스 범위 초과 방지
3. tasks와 meta 정보 함께 반환

### 3-4. showTask

1. path parameter `{id}` 파싱 (`r.PathValue("id")`)
2. `strconv.ParseInt`로 변환, 실패 시 400
3. 슬라이스에서 선형 탐색, 없으면 404

### 3-5. 헬퍼 함수

`writeJSON`, `writeError`, `parsePositiveInt` 세 개의 헬퍼 작성.

---

## Phase 4: CLI 서버

### 4-1. main.go 작성 (`solution/go/cmd/server/main.go`)

```go
log.Fatal(http.ListenAndServe(":4020", server.Routes()))
```

### 4-2. 서버 실행 및 curl 테스트

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
```

---

## Phase 5: 테스트

### 5-1. httptest 기반 테스트 (`solution/go/internal/api/api_test.go`)

| 테스트 | 검증 대상 |
|--------|-----------|
| `TestHealthcheck` | 200 응답 |
| `TestCreateTaskValidation` | 빈 제목 시 422 |
| `TestCreateTaskIdempotency` | 같은 키로 두 번 → 201 + 200 |
| `TestListTasksPagination` | 3개 생성 후 page=2&page_size=2 →  200 |
| `TestShowTaskNotFound` | 없는 ID → 404 |

### 5-2. 테스트 실행

```bash
cd solution/go
go test ./...
go test -v ./internal/api/
```

---

## Phase 6: 문서 및 최종 검증

```bash
cd study
make test-new
make check-docs
```

`verified` 상태 확정.

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| Go 1.22+ | 컴파일, 실행, 테스트, Go 1.22 라우팅 |
| `net/http` | HTTP 서버, 라우터 |
| `httptest` | 서버 없이 핸들러 테스트 |
| `encoding/json` | JSON 인코딩/디코딩 |
| `curl` | 수동 API 테스트 |
| `make` | 전체 검증 |

외부 패키지 없음. Docker 불필요.
