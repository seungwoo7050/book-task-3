# 지식 인덱스 — 빠른 참조용

## net/http 패턴

```go
// 라우터 구성 (Go 1.22+)
mux := http.NewServeMux()
mux.HandleFunc("GET /v1/resource", handler)
mux.HandleFunc("POST /v1/resource", createHandler)
mux.HandleFunc("GET /v1/resource/{id}", showHandler)

// path parameter
id := r.PathValue("id")

// query parameter
page := r.URL.Query().Get("page")
```

## JSON 응답 작성 순서

```go
// 반드시 이 순서: Header → WriteHeader → Write
w.Header().Set("Content-Type", "application/json")
w.WriteHeader(http.StatusCreated)
json.NewEncoder(w).Encode(payload)
```

## httptest 패턴

```go
req := httptest.NewRequest(http.MethodPost, "/v1/tasks", bytes.NewBufferString(`{"title":"test"}`))
req.Header.Set("Idempotency-Key", "abc")
rr := httptest.NewRecorder()

server.Routes().ServeHTTP(rr, req)  // 라우터 통째로 호출

if rr.Code != http.StatusCreated { ... }
```

## 상태 코드 가이드

| 코드 | 의미 | 사용 상황 |
|------|------|-----------|
| 200 | OK | 성공적 조회, idempotent 재시도 |
| 201 | Created | 새 리소스 생성 성공 |
| 400 | Bad Request | 잘못된 JSON, 잘못된 path parameter |
| 404 | Not Found | 리소스 없음 |
| 422 | Unprocessable Entity | 유효한 JSON이지만 값이 잘못됨 |
| 500 | Internal Server Error | 예기치 않은 서버 오류 |

## CLI 명령 정리

```bash
# 모듈 초기화
go mod init github.com/woopinbell/go-backend/study/01-backend-core/05-http-rest-basics

# 서버 실행
cd go
go run ./cmd/server  # :4020에서 수신 대기

# 테스트
go test ./...

# curl로 수동 테스트
curl http://localhost:4020/v1/healthcheck
curl -X POST http://localhost:4020/v1/tasks -d '{"title":"write docs"}'
curl -X POST http://localhost:4020/v1/tasks -d '{"title":"write docs"}' -H "Idempotency-Key: abc"
curl http://localhost:4020/v1/tasks?page=1&page_size=2
curl http://localhost:4020/v1/tasks/1
```
