# 접근 과정 — JSON API를 세우기까지

## Go 1.22의 라우팅

Go 1.22부터 `http.ServeMux`에 메서드 기반 라우팅이 추가됐다. `"GET /v1/tasks/{id}"`처럼 메서드와 패턴을 함께 쓸 수 있다. 이전에는 gorilla/mux나 chi 같은 외부 라우터를 써야 했는데, 이제 표준 라이브러리만으로 충분하다.

```go
mux.HandleFunc("GET /v1/healthcheck", s.healthcheck)
mux.HandleFunc("POST /v1/tasks", s.createTask)
mux.HandleFunc("GET /v1/tasks", s.listTasks)
mux.HandleFunc("GET /v1/tasks/{id}", s.showTask)
```

path parameter는 `r.PathValue("id")`로 꺼낸다. 이것도 Go 1.22에서 추가된 기능이다.

## Server struct 설계

`Server` struct가 모든 상태를 가진다. 슬라이스(`tasks`), 자동 증가 ID(`nextID`), idempotency 맵(`idempotentCreate`). 모든 필드를 `sync.Mutex`로 보호했다.

```go
type Server struct {
    mu               sync.Mutex
    nextID           int64
    tasks            []Task
    idempotentCreate map[string]Task
}
```

`NewServer()` 생성자에서 맵을 초기화한다. 프로젝트 02에서 배운 "nil map 방지" 패턴과 같다.

## JSON 응답 헬퍼

모든 핸들러가 `writeJSON`과 `writeError`를 공유한다. 응답을 보낼 때 `Content-Type: application/json`을 세팅하고, `WriteHeader`로 상태 코드를 보내고, `json.NewEncoder`로 본문을 쓴다.

이 순서가 중요하다. `WriteHeader`를 본문 쓰기 후에 호출하면 Go가 자동으로 200을 보내버린다.

## 상태 코드 설계

| 상황 | 코드 | 이유 |
|------|------|------|
| 생성 성공 | 201 Created | 새 자원이 만들어졌으므로 |
| idempotency 재시도 | 200 OK | 자원이 이미 있으므로 |
| validation 실패 | 422 Unprocessable Entity | JSON은 유효하지만 의미가 잘못됨 |
| 잘못된 JSON | 400 Bad Request | 파싱 자체가 실패 |
| 리소스 없음 | 404 Not Found | 해당 ID의 task가 없음 |

400과 422를 구분한 건 의도적이다. JSON이 깨졌는지(400) vs JSON은 멀쩡한데 값이 잘못된 건지(422)를 분리하면, 클라이언트가 디버깅하기 쉬워진다.

## Pagination

`parsePositiveInt` 헬퍼로 `page`와 `page_size`를 파싱한다. 빈 문자열, 음수, 0은 전부 기본값으로 떨어진다. 슬라이스의 `start`와 `end` 인덱스가 범위를 벗어나지 않도록 bounds check를 넣었다.

응답에 `meta` 필드로 `page`, `page_size`, `total`을 포함시켜서 클라이언트가 "다음 페이지가 있는지"를 판단할 수 있게 했다.
