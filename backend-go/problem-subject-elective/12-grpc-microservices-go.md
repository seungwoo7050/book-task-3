# 12-grpc-microservices-go 문제지

## 왜 중요한가

Product Catalog 마이크로서비스를 gRPC와 Protocol Buffers로 설계하고 unary/streaming RPC를 구현한다.

## 목표

시작 위치의 구현을 완성해 Product CRUD와 리스트/가격 감시용 RPC를 정의한다, logging interceptor와 auth interceptor를 구현한다, client retry interceptor와 round-robin 예제를 제공한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/02-distributed-systems/12-grpc-microservices/solution/go/client/cmd/main.go`
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/server/cmd/main.go`
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/client/client.go`
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/server/interceptors/interceptors.go`
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/server/store/store_test.go`
- `../study/02-distributed-systems/12-grpc-microservices/problem/Makefile`
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/go.mod`

## starter code / 입력 계약

- `../study/02-distributed-systems/12-grpc-microservices/solution/go/client/cmd/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- Product CRUD와 리스트/가격 감시용 RPC를 정의한다.
- logging interceptor와 auth interceptor를 구현한다.
- client retry interceptor와 round-robin 예제를 제공한다.
- server-side streaming과 bidirectional streaming을 둘 다 보여 준다.

## 제외 범위

- 자동 generated code workflow
- production service mesh
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `NewConnection`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestCreateAndGet`와 `TestGetNotFound`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `make -C /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/12-grpc-microservices/problem test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/12-grpc-microservices/problem test
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`12-grpc-microservices-go_answer.md`](12-grpc-microservices-go_answer.md)에서 확인한다.
