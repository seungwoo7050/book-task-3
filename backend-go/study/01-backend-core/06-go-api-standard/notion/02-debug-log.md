# 디버그 기록 — 어디서 막혔고 어떻게 풀었나

## middleware 순서에 따른 로깅 누락

처음에 `logRequest`를 `recoverPanic` 바깥에 놓았다. 그러니 panic이 발생하면 로깅이 중간에 끊어졌다. HTTP 응답 상태 코드도 기록되지 않았다. `recoverPanic`을 가장 바깥으로 옮기니 panic 후에도 로그가 정상적으로 남았다.

middleware 체인은 "양파 껍질"과 같다. 가장 바깥 껍질이 먼저 실행되고, 가장 안쪽 핸들러까지 도달한 뒤 다시 밖으로 나온다. 이 흐름을 한번 그려 보면 순서 결정이 훨씬 분명해진다.

## responseWriter 래핑의 필요성

`logRequest` 미들웨어에서 응답 상태 코드를 기록하려면 `WriteHeader` 호출을 가로채야 한다. Go의 `http.ResponseWriter`는 상태 코드를 외부에서 읽을 수 있는 API를 제공하지 않기 때문이다.

커스텀 `responseWriter`를 만들어서 `WriteHeader`를 오버라이드했다. `headerWritten` 플래그로 중복 호출을 방지한 것은, 일부 핸들러가 `WriteHeader`를 두 번 호출하는 경우가 있기 때문이다.

## PATCH 핸들러에서 nil 체크

PATCH는 부분 업데이트이므로 요청 JSON에 없는 필드는 기존 값을 유지해야 한다. 이를 위해 입력 struct의 필드를 포인터 타입으로 만들었다:

```go
var input struct {
    Title   *string  `json:"title"`
    Year    *int32   `json:"year"`
    Runtime *int32   `json:"runtime"`
    Genres  []string `json:"genres"`
}
```

포인터가 nil이면 해당 필드는 클라이언트가 보내지 않은 것이므로 기존 값을 유지한다. 처음에 이걸 고려하지 않아서 PATCH 요청이 빈 필드를 zero value로 덮어쓰는 문제가 있었다.

## graceful shutdown에서 이미 닫힌 서버

`Shutdown`을 호출한 뒤 `ListenAndServe`가 `ErrServerClosed`를 반환한다. 이걸 일반 에러처럼 처리하면 "서버가 에러로 종료됨"이라는 잘못된 로그가 남는다. `errors.Is(err, http.ErrServerClosed)`로 분리해야 정상 종료와 비정상 종료를 구별할 수 있다.

## sync.RWMutex vs sync.Mutex

처음에 `MovieStore`를 `sync.Mutex`로만 보호했다. 읽기 요청도 쓰기 잠금을 필요로 해서 동시 읽기 성능이 떨어졌다. `sync.RWMutex`로 바꾸면 여러 goroutine이 동시에 읽을 수 있다. 이 과제의 규모에서 성능 차이는 미미하지만, 올바른 패턴을 익히는 데 의미가 있었다.
