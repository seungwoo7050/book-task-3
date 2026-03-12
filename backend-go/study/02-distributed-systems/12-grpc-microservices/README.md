# 12 gRPC Microservices

## 한 줄 요약

Protocol Buffers, unary/streaming RPC, interceptor를 작은 Product Catalog 서비스로 묶어 contract-first 감각을 익히는 과제다.

## 이 프로젝트가 푸는 문제

- Product Catalog용 gRPC 서비스 계약을 설계해야 한다.
- unary RPC와 streaming RPC를 모두 다뤄야 한다.
- logging/auth interceptor와 client retry interceptor를 함께 구현해야 한다.

## 내가 만든 답

- proto-first contract, minimal server/client, interceptor 예제를 `solution/go`에 구현했다.
- server-side streaming과 bidirectional streaming 흐름을 hand-written shim 기준으로 재현했다.
- generated `.pb.go` 자동화는 뒤로 미루고 contract 구조와 interceptor 역할에 집중했다.

## 핵심 설계 선택

- generated code 자동화보다 계약과 호출 흐름을 먼저 이해시키기 위해 hand-written shim 예제를 택했다.
- client와 server를 분리해 retry, auth, logging interceptor를 서로 다른 관점에서 읽게 했다.

## 검증

- `make -C problem build-server`
- `make -C problem build-client`
- `make -C problem test`

## 제외 범위

- 실제 `.pb.go` 코드 생성 자동화
- production service discovery

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: legacy/02-distributed-system/04-grpc-microservices (`legacy/02-distributed-system/04-grpc-microservices/README.md`, public repo에는 미포함)
