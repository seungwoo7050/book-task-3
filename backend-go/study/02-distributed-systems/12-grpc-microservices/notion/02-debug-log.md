# 디버그 기록 — gRPC에서 만나는 문제들

## protoc 코드 생성 없이 작업

이 프로젝트에서는 `protoc`으로 코드를 생성하지 않고 hand-written shim을 사용했다. 실무에서는 `protoc --go_out=. --go-grpc_out=.`으로 서비스 인터페이스와 메시지 타입을 생성한다. proto 정의와 Go 코드가 분리되어 있으면 "proto를 수정했는데 코드에 반영이 안 된다"는 문제가 생긴다.

**교훈**: proto 변경 시 반드시 코드 재생성. CI에서 `protoc`을 돌리고 diff가 있으면 빌드를 실패시키는 게 좋다.

## metadata와 HTTP 헤더의 차이

gRPC metadata는 HTTP/2 헤더로 전송되지만, 키 규칙이 다르다:
- gRPC metadata 키는 소문자만 사용
- `grpc-` 접두사는 예약됨
- 바이너리 데이터는 `-bin` 접미사 키를 사용

`authorization`이 아닌 `Authorization`으로 보내면 gRPC 클라이언트가 자동으로 소문자로 변환하지만, 직접 metadata를 다룰 때는 주의해야 한다.

## Unary vs Stream Interceptor 혼동

Auth interceptor를 unary용으로만 만들면 streaming RPC(ListProducts, PriceWatch)에 인증이 적용되지 않는다. Stream interceptor에도 동일한 인증 로직을 넣어야 한다. 이 프로젝트에서는 stream에 인증 interceptor를 넣지 않았는데, 실무에서는 반드시 추가해야 한다.

## Exponential Backoff에서 context 확인

```go
select {
case <-ctx.Done():
    return ctx.Err()
case <-time.After(backoff):
}
```

`time.Sleep(backoff)` 대신 `select`를 쓰는 이유: context가 취소되면 sleep 중에도 즉시 반환해야 한다. `time.Sleep`은 취소 불가.

## grpc.Dial deprecated 경고

gRPC Go v1.63부터 `grpc.Dial`이 deprecated되고 `grpc.NewClient`로 대체된다. 이 프로젝트는 v1.62를 사용하므로 `grpc.Dial`을 그대로 쓰지만, `//nolint:staticcheck` 주석으로 경고를 명시했다.

## gRPC 상태 코드와 HTTP 상태 코드 매핑

| gRPC | HTTP | 의미 |
|------|------|------|
| OK | 200 | 성공 |
| NOT_FOUND | 404 | 자원 없음 |
| INVALID_ARGUMENT | 400 | 잘못된 입력 |
| ALREADY_EXISTS | 409 | 중복 |
| UNAUTHENTICATED | 401 | 인증 실패 |
| UNAVAILABLE | 503 | 서비스 불가 (재시도 대상) |

## 포트 50051

gRPC 기본 포트는 관례적으로 50051이다. HTTP의 80, 8080과 구분하기 위함. 이전 프로젝트들이 4010-4050 범위를 쓰는 것과 다른 네트워크 계층이라는 걸 시각적으로 보여준다.
