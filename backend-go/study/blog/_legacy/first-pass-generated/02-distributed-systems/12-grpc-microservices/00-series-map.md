# 12 gRPC Microservices 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../02-distributed-systems/12-grpc-microservices/README.md), [`problem/README.md`](../../02-distributed-systems/12-grpc-microservices/problem/README.md)
- 구현 표면:
- `solution/go/server/store/store.go`
- `solution/go/server/interceptors/interceptors.go`
- `solution/go/server/store/store_test.go`
- 검증 표면: `cd solution/go && go test -run TestCreateAndGet -v ./server/store`, `cd solution/go && go test -v -race -count=1 ./...`
- 개념 축: `proto-first는 API 계약을 코드보다 먼저 고정하는 접근이다.`, `interceptor는 HTTP middleware와 비슷하지만 RPC 레벨의 횡단 관심사를 다룬다.`, `unary 중심 예제라도 client/server 분리와 retry 로직을 같이 보면 gRPC 특성이 더 잘 드러난다.`

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

grpc transport, interceptor, store를 분리해 가장 작은 catalog microservice를 만든다.
