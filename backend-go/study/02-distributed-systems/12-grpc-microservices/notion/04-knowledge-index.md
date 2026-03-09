# 지식 색인 — gRPC 핵심 개념

## gRPC

Google이 만든 고성능 RPC 프레임워크. HTTP/2 위에서 동작하며, Protocol Buffers로 직렬화한다. 양방향 스트리밍, 코드 생성, 강타입 인터페이스를 제공한다.

## Protocol Buffers (protobuf)

언어 중립적 직렬화 포맷. `.proto` 파일에서 메시지와 서비스를 정의하고, `protoc`으로 Go/Java/Python 등의 코드를 생성한다.

```protobuf
message Product {
  string id = 1;       // 필드 번호
  string name = 2;
  double price = 4;
}
```

필드 번호는 바이너리 인코딩에서 식별자 역할. 한 번 할당하면 변경하지 않는다.

## RPC 패턴

| 패턴 | 요청 | 응답 | 용도 |
|------|------|------|------|
| Unary | 1 | 1 | CRUD |
| Server streaming | 1 | N | 목록 조회, 구독 |
| Client streaming | N | 1 | 파일 업로드, 배치 |
| Bidirectional | N | N | 채팅, 실시간 감시 |

## Interceptor

gRPC의 미들웨어. Unary와 Stream 각각 별도 시그니처:

```go
type UnaryServerInterceptor func(ctx, req, info, handler) (any, error)
type StreamServerInterceptor func(srv, ss, info, handler) error
```

`ChainUnaryInterceptor`로 여러 interceptor를 체이닝한다.

## gRPC Status & Codes

gRPC는 자체 에러 코드 체계를 사용한다:

```go
status.Errorf(codes.NotFound, "product %s not found", id)
```

`status.Code(err)`로 에러에서 코드를 추출한다.

## Metadata

gRPC에서 HTTP 헤더에 대응하는 키-값 쌍. 인증 토큰, trace ID 등을 전달한다.

```go
md, ok := metadata.FromIncomingContext(ctx)
tokens := md.Get("authorization")
```

## Exponential Backoff

재시도 간격을 지수적으로 증가시키는 전략: 100ms → 200ms → 400ms. 서버가 일시적으로 과부하일 때, 클라이언트들이 동시에 재시도하는 "thundering herd"를 방지한다.

## Round-Robin Load Balancing

여러 서버 인스턴스에 요청을 순환 분배. gRPC 클라이언트가 내장 지원:

```go
grpc.WithDefaultServiceConfig(`{"loadBalancingConfig": [{"round_robin":{}}]}`)
```

## grpc.GracefulStop

진행 중인 RPC를 마무리한 후 서버를 중지한다. 새 연결은 거부하지만 기존 스트림은 완료된다. HTTP의 `http.Server.Shutdown`에 대응.

## HTTP/2

gRPC의 전송 계층. HTTP/1.1과 달리 하나의 TCP 연결에서 여러 스트림을 다중화(multiplexing)한다. 헤더 압축(HPACK)으로 오버헤드를 줄인다.

## well-known types

Google이 제공하는 표준 protobuf 메시지. `google.protobuf.Timestamp`, `google.protobuf.Duration`, `google.protobuf.Any` 등. 직접 시간 타입을 정의하지 않고 `import "google/protobuf/timestamp.proto"`로 사용한다.
