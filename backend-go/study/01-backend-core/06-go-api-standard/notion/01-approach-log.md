# 접근 과정 — API 구조를 세우기까지

## application struct — 의존성을 한 곳에 모으기

05번에서는 `Server` struct에 데이터와 핸들러가 섞여 있었다. 이 과제에서는 `application` struct로 의존성을 명확히 분리했다:

```go
type application struct {
    config config
    logger *slog.Logger
    models data.Models
}
```

모든 핸들러와 미들웨어가 `application`의 메서드로 정의된다. 이 패턴의 장점은 의존성 주입이 암묵적이라는 것이다—구조체 필드로 logger와 models에 접근할 수 있으니 함수 인자로 넘길 필요가 없다.

## 파일 분리

`cmd/api/` 아래에 파일을 역할별로 분리했다:
- `main.go`: 설정 로드, 의존성 조립, 서버 시작
- `routes.go`: 라우트 등록과 미들웨어 체인
- `handlers.go`: CRUD 핸들러
- `helpers.go`: JSON 읽기/쓰기 헬퍼
- `errors.go`: 에러 응답 헬퍼
- `middleware.go`: 로깅, panic recovery, CORS

이 분리는 단순히 파일 크기를 줄이려는 게 아니다. 각 파일이 하나의 관심사를 담아서, "에러 응답을 바꾸고 싶으면 errors.go만 보면 된다"는 식의 탐색이 가능해진다.

## JSON envelope

모든 응답을 `envelope` 타입으로 감싼다. 성공 시:
```json
{"data": {"movie": {...}}, "meta": {"page": 1}}
```
실패 시:
```json
{"error": {"message": "title must not be empty"}}
```

응답 구조가 고정되면 클라이언트가 파싱 로직을 하나만 만들면 된다.

## Middleware 체인

```go
return app.recoverPanic(app.logRequest(app.enableCORS(mux)))
```

순서가 중요하다. 가장 바깥이 `recoverPanic`인 이유는, 어떤 미들웨어나 핸들러에서 panic이 나더라도 잡을 수 있어야 하기 때문이다. `logRequest`는 그 안에 있어서 요청 정보를 로깅한 뒤 다음으로 넘기고, `enableCORS`는 가장 안쪽에서 CORS 헤더를 추가한다.

## Graceful shutdown

`SIGINT`나 `SIGTERM`을 받으면 새 요청을 막고, 기존 요청을 최대 30초까지 기다린 뒤 종료한다. `http.Server.Shutdown(ctx)`가 이걸 처리한다. `ListenAndServe`가 `ErrServerClosed`를 반환하면 정상 종료 흐름이다.

이 패턴은 프로덕션에서 무중단 배포를 할 때 필수다. 로드밸런서가 새 인스턴스로 트래픽을 옮기는 동안 기존 요청이 정상 완료되어야 한다.

## 환경변수 기반 설정

포트와 환경(development/staging/production)을 환경변수로 받는다. 코드에 하드코딩하지 않고 `PORT=8080 go run ./cmd/api`처럼 실행 시점에 주입한다. 12-Factor App의 기본 원칙을 따른 것이다.

## 인메모리 MovieStore의 thread-safety

`sync.RWMutex`로 읽기와 쓰기를 분리했다. 읽기(`Get`, `GetAll`)는 `RLock`, 쓰기(`Insert`, `Update`, `Delete`)는 `Lock`을 사용한다. 또한 내부 데이터의 복사본을 반환해서 외부 코드가 내부 상태를 직접 수정하는 걸 방지했다. 프로젝트 03에서 배운 Snapshot 복사 패턴과 같은 원리다.
