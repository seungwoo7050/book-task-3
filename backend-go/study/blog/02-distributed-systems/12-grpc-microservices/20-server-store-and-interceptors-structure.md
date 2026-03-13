# 12 gRPC Microservices Structure

## 이 글이 답할 질문

- server-side streaming과 bidirectional streaming 흐름을 hand-written shim 기준으로 재현했다.
- client와 server를 분리해 retry, auth, logging interceptor를 서로 다른 관점에서 읽게 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `02-distributed-systems/12-grpc-microservices` 안에서 `20-server-store-and-interceptors.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 5단계: ProductStore 구현 (server/store/store.go) -> 6단계: Interceptor 구현 (server/interceptors/interceptors.go) -> 7단계: 서버 구현 (server/cmd/main.go)
- 세션 본문: `solution/go/server/interceptors/interceptors.go, solution/go/server/cmd/main.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/server/interceptors/interceptors.go`
- 코드 앵커 2: `solution/go/server/cmd/main.go`
- 코드 설명 초점: 이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.
- 개념 설명: interceptor는 HTTP middleware와 비슷하지만 RPC 레벨의 횡단 관심사를 다룬다.
- 마지막 단락: 다음 글에서는 `30-client-flow-and-proof.md`에서 이어지는 경계를 다룬다.
