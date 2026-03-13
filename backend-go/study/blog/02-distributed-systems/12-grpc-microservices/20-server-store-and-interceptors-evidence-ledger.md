# 12 gRPC Microservices Evidence Ledger

## 20 server-store-and-interceptors

- 시간 표지: 5단계: ProductStore 구현 (server/store/store.go) -> 6단계: Interceptor 구현 (server/interceptors/interceptors.go) -> 7단계: 서버 구현 (server/cmd/main.go)
- 당시 목표: server-side streaming과 bidirectional streaming 흐름을 hand-written shim 기준으로 재현했다.
- 변경 단위: `solution/go/server/interceptors/interceptors.go`, `solution/go/server/cmd/main.go`
- 처음 가설: client와 server를 분리해 retry, auth, logging interceptor를 서로 다른 관점에서 읽게 했다.
- 실제 조치: 08의 Repository 패턴을 gRPC에 맞춰 적용: `sync.RWMutex` + `map[string]*Product` `atomic.Int64`로 ID 생성 (`prod-1`, `prod-2`, ...) `copyProduct`로 방어적 복사 CRUD + List(카테고리 필터) 세 가지 interceptor: `LoggingUnaryInterceptor` — method, duration, status code 로깅 (slog) `LoggingStreamInterceptor` — stream RPC 로깅 `AuthUnaryInterceptor` — metadata에서 authorization 토큰 검증 포트 50051, Seed 데이터 2개, graceful shutdown (SIGINT/SIGTERM).

CLI:

```bash
cd 02-distributed-systems/12-grpc-microservices
make -C problem build-server
make -C problem build-client
make -C problem test
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/server/interceptors/interceptors.go`
- 새로 배운 것: interceptor는 HTTP middleware와 비슷하지만 RPC 레벨의 횡단 관심사를 다룬다.
- 다음: 다음 글에서는 `30-client-flow-and-proof.md`에서 이어지는 경계를 다룬다.
