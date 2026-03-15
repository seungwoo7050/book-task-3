# 12-grpc-microservices-go 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 Product CRUD와 리스트/가격 감시용 RPC를 정의한다, logging interceptor와 auth interceptor를 구현한다, client retry interceptor와 round-robin 예제를 제공한다를 한 흐름으로 설명하고 검증한다. 핵심은 `main`와 `NewConnection`, `retryInterceptor` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- Product CRUD와 리스트/가격 감시용 RPC를 정의한다.
- logging interceptor와 auth interceptor를 구현한다.
- client retry interceptor와 round-robin 예제를 제공한다.
- 첫 진입점은 `../study/02-distributed-systems/12-grpc-microservices/solution/go/client/cmd/main.go`이고, 여기서 `main`와 `NewConnection` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/02-distributed-systems/12-grpc-microservices/solution/go/client/cmd/main.go`: `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/server/cmd/main.go`: `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/client/client.go`: `NewConnection`, `retryInterceptor`, `loggingClientInterceptor`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/server/interceptors/interceptors.go`: `LoggingUnaryInterceptor`, `LoggingStreamInterceptor`, `AuthUnaryInterceptor`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/server/store/store.go`: `NewProductStore`, `Create`, `Get`, `Update`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/server/store/store_test.go`: `TestCreateAndGet`, `TestGetNotFound`, `TestUpdate`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/02-distributed-systems/12-grpc-microservices/problem/Makefile`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/go.mod`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.

## 정답을 재구성하는 절차

1. `../study/02-distributed-systems/12-grpc-microservices/solution/go/client/cmd/main.go`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `TestCreateAndGet` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make -C /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/12-grpc-microservices/problem test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/12-grpc-microservices/problem test
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `TestCreateAndGet`와 `TestGetNotFound`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/12-grpc-microservices/problem test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/02-distributed-systems/12-grpc-microservices/solution/go/client/cmd/main.go`
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/server/cmd/main.go`
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/client/client.go`
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/server/interceptors/interceptors.go`
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/server/store/store.go`
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/server/store/store_test.go`
- `../study/02-distributed-systems/12-grpc-microservices/problem/Makefile`
- `../study/02-distributed-systems/12-grpc-microservices/solution/go/go.mod`
