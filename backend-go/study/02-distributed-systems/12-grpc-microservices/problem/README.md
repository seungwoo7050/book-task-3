# 문제 정의

Product Catalog 마이크로서비스를 gRPC와 Protocol Buffers로 설계하고 unary/streaming RPC를 구현한다.

## 성공 기준

- Product CRUD와 리스트/가격 감시용 RPC를 정의한다.
- logging interceptor와 auth interceptor를 구현한다.
- client retry interceptor와 round-robin 예제를 제공한다.
- server-side streaming과 bidirectional streaming을 둘 다 보여 준다.

## 제공 자료와 출처

- legacy `02-distributed-system/04-grpc-microservices` 문제를 한국어 canonical 형태로 정리한 문서다.
- 원문 요구사항은 provenance로만 유지한다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `make -C problem build-server`
- `make -C problem build-client`
- `make -C problem test`

## 제외 범위

- 자동 generated code workflow
- production service mesh
