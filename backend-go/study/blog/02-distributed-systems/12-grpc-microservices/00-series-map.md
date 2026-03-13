# 12 gRPC Microservices Series Map

`02-distributed-systems/12-grpc-microservices`는 Protocol Buffers, unary/streaming RPC, interceptor를 작은 Product Catalog 서비스로 묶어 contract-first 감각을 익히는 과제다.

## 이 시리즈가 복원하는 것

- 시작점: Product Catalog용 gRPC 서비스 계약을 설계해야 한다.
- 구현 축: proto-first contract, minimal server/client, interceptor 예제를 `solution/go`에 구현했다.
- 검증 축: 2026-03-07 기준 세 명령이 모두 통과했다.
- 글 수: 3편

## 읽는 순서

- [10-proto-contract-and-service-shape.md](10-proto-contract-and-service-shape.md)
- [20-server-store-and-interceptors.md](20-server-store-and-interceptors.md)
- [30-client-flow-and-proof.md](30-client-flow-and-proof.md)

## 근거 기준

- 소스코드, README, docs, 테스트, CLI만 입력 근거로 사용했다.
- 기존 blog 초안과 `_legacy` 본문은 입력 근거로 사용하지 않았다.
