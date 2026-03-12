# 개발 타임라인 — 처음부터 끝까지

이 문서는 프로젝트 06을 처음부터 완성까지 만드는 전체 과정을 시간순으로 기록한다.

---

## Phase 1: 프로젝트 뼈대와 구조 결정

### 1-1. 디렉터리 구조 생성

```bash
mkdir -p 01-backend-core/06-go-api-standard/{solution/go/cmd/api,solution/go/internal/data,docs/concepts,docs/references,problem}
```

05번과 달리 `cmd/api/`에 여러 Go 파일을 두는 구조를 택했다. 같은 `main` 패키지에 속하는 파일들을 역할별로 분리한다.

### 1-2. Go 모듈 초기화

```bash
cd 01-backend-core/06-go-api-standard/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/06-go-api-standard
```

외부 의존성 없음. Go 1.22+

### 1-3. Workspace 등록

```bash
cd study
go work use 01-backend-core/06-go-api-standard/go
```

---

## Phase 2: 데이터 레이어 구현

### 2-1. Movie struct 정의 (`internal/data/models.go`)

`Movie` struct에 JSON 태그를 포함. `Version` 필드는 낙관적 잠금을 위한 것이지만 이 과제에서는 아직 사용하지 않는다. `Models` struct는 `MovieStore`를 감싸서 의존성 주입 포인트 역할.

### 2-2. MovieStore 구현 (`internal/data/movies.go`)

`sync.RWMutex`로 보호되는 인메모리 스토어. 다섯 개의 메서드:
- `Insert`: ID 자동 할당 (`atomic.Int64`), 복사본 저장
- `Get`: 복사본 반환
- `Update`: 존재 확인 후 교체
- `Delete`: 존재 확인 후 삭제
- `GetAll`: 필터링 + 페이지네이션

모든 읽기/쓰기에서 `Genres` 슬라이스를 `copy`로 복사한다. 03번 과제의 Snapshot 패턴과 같은 원리.

---

## Phase 3: 핸들러와 미들웨어 구현

### 3-1. helpers.go — JSON I/O 헬퍼

`readJSON`: `json.NewDecoder`로 request body 파싱. 크기 제한, 알 수 없는 필드 거부 등 방어 코드 포함.
`writeJSON`: `json.Marshal` → `w.Header().Set` → `w.WriteHeader` → `w.Write` 순서.

### 3-2. errors.go — 에러 응답 통일

`errorResponse`, `serverErrorResponse`, `notFoundResponse`, `badRequestResponse`, `failedValidationResponse` 다섯 함수. 모든 에러가 같은 JSON envelope 구조를 따른다.

### 3-3. handlers.go — CRUD 핸들러

| 핸들러 | 메서드 | 경로 |
|--------|--------|------|
| `healthcheckHandler` | GET | `/v1/healthcheck` |
| `createMovieHandler` | POST | `/v1/movies` |
| `showMovieHandler` | GET | `/v1/movies/{id}` |
| `listMoviesHandler` | GET | `/v1/movies` |
| `updateMovieHandler` | PATCH | `/v1/movies/{id}` |
| `deleteMovieHandler` | DELETE | `/v1/movies/{id}` |

`createMovieHandler`에서 입력 validation(title 필수, year > 1888, runtime > 0 등) 수행.
`updateMovieHandler`에서 포인터 타입 필드로 부분 업데이트 지원.

### 3-4. middleware.go — 세 가지 미들웨어

1. **`recoverPanic`**: `defer recover()`로 panic 잡기, 스택 트레이스 로깅, 500 반환
2. **`logRequest`**: 커스텀 `responseWriter`로 상태 코드 캡처, 요청 정보 + 지속시간 로깅
3. **`enableCORS`**: 허용 헤더 설정, OPTIONS preflight 처리

### 3-5. routes.go — 라우터와 미들웨어 체인

```go
return app.recoverPanic(app.logRequest(app.enableCORS(mux)))
```

---

## Phase 4: 서버 기동과 graceful shutdown

### 4-1. main.go

`slog` 로거 생성 → 환경변수에서 설정 로드(`PORT`, `ENV`) → `application` 구조체 조립 → `serve` 메서드 호출.

`http.Server`에 타임아웃 설정:
- `IdleTimeout`: 1분
- `ReadTimeout`: 5초
- `WriteTimeout`: 10초

### 4-2. serve 메서드

별도 goroutine에서 `SIGINT`/`SIGTERM` 대기 → `srv.Shutdown(ctx)` 호출 (30초 타임아웃) → 채널로 에러 전달.

### 4-3. 서버 실행 및 수동 테스트

```bash
cd solution/go
go run ./cmd/api
# time=... level=INFO msg="starting server" addr=:4000 env=development

# 다른 터미널에서:
curl http://localhost:4000/v1/healthcheck
curl -X POST http://localhost:4000/v1/movies \
  -d '{"title":"Inception","year":2010,"runtime":148,"genres":["sci-fi"]}'
curl http://localhost:4000/v1/movies/1
curl http://localhost:4000/v1/movies
curl -X PATCH http://localhost:4000/v1/movies/1 -d '{"year":2011}'
curl -X DELETE http://localhost:4000/v1/movies/1

# graceful shutdown 테스트
kill -SIGTERM <PID>
# 또는 Ctrl+C
```

---

## Phase 5: 테스트

### 5-1. MovieStore 테스트 (`internal/data/movies_test.go`)

CRUD 각 메서드와 페이지네이션, 필터링을 검증.

### 5-2. 핸들러 테스트 (`cmd/api/handlers_test.go`)

httptest 기반. 각 엔드포인트의 정상/에러 케이스를 검증.

```bash
cd solution/go
go test ./...
go test -v ./cmd/api/
go test -v ./internal/data/
```

---

## Phase 6: problem 디렉터리와 Makefile

### 6-1. problem/Makefile

```bash
make -C problem build
make -C problem test
```

### 6-2. 최종 검증

```bash
cd study
make test-migrated  # 06은 마이그레이션된 과제
make check-docs
```

`verified` 상태 확정.

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| Go 1.22+ | Go 1.22 ServeMux 라우팅, log/slog |
| `net/http` | HTTP 서버, 미들웨어 |
| `httptest` | 핸들러 테스트 |
| `log/slog` | 구조화된 로깅 |
| `os/signal` | graceful shutdown 시그널 처리 |
| `curl` | 수동 API 테스트 |
| `make` | 빌드, 테스트 자동화 |

외부 패키지 없음. Docker 불필요.
