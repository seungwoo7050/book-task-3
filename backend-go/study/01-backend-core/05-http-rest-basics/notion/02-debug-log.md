# 디버그 기록 — 어디서 막혔고 어떻게 풀었나

## WriteHeader 호출 순서

Go의 `http.ResponseWriter`에서 `WriteHeader`를 호출하기 전에 `Write`를 호출하면, Go가 자동으로 200 상태 코드를 보낸다. 처음에 `writeJSON` 헬퍼에서 `json.NewEncoder(w).Encode(payload)` 를 `w.WriteHeader(status)` 전에 호출했다가, 모든 응답이 200으로 나가는 현상이 생겼다.

```go
// 잘못된 순서
json.NewEncoder(w).Encode(payload)  // 여기서 Write가 호출됨 → 200이 암묵적으로 설정됨
w.WriteHeader(status)               // 이미 늦음: "superfluous response.WriteHeader call" 경고
```

수정은 `WriteHeader`를 먼저 호출하도록 바꾸는 것이었다. 이건 Go HTTP 핸들러의 기본적인 함정이다.

## idempotency key가 없는 요청

처음 구현에서 `Idempotency-Key` 헤더가 반드시 있어야 하는 것처럼 만들었다가, 헤더 없이 POST하면 에러가 나는 문제가 생겼다. 실제로는 idempotency key가 없는 POST도 유효하다—단지 중복 방지 기능이 없을 뿐이다. key가 있을 때만 맵을 확인하도록 조건문을 넣었다.

## pagination 경계 조건

`page=100`인데 task가 3개밖에 없으면 `start`가 슬라이스 길이를 초과한다. `s.tasks[start:end]`에서 panic이 날 수 있다.

```go
start := (page - 1) * pageSize
if start > len(s.tasks) {
    start = len(s.tasks)
}
```

이 bounds check를 처음에 넣지 않았다. 빈 페이지를 요청했을 때 panic이 나서야 추가했다. pagination이 있는 API에서는 항상 "마지막 페이지 너머"를 처리해야 한다.

## httptest로 테스트할 때 라우터 통째로 호출

처음에 핸들러 함수를 직접 호출해서 테스트했는데, path parameter가 파싱되지 않는 문제가 있었다. `r.PathValue("id")`는 `ServeMux`를 통해야 설정되기 때문이다. `server.Routes().ServeHTTP(rr, req)` 로 라우터 전체를 통과시키는 게 정확한 테스트 방법이었다.
