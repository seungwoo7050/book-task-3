# 02 Distributed Systems blog

`02-distributed-systems`는 - contract-first gRPC 서비스와 파일 기반 commit log 구현을 각각 독립 실행 가능한 프로젝트로 만들었다.

## 프로젝트 인덱스

| 프로젝트 | 시리즈 맵 | evidence ledger | structure | final blog | 대표 검증 |
| --- | --- | --- | --- | --- | --- |
| 12 gRPC Microservices | [00-series-map](12-grpc-microservices/00-series-map.md) | [01-evidence-ledger](12-grpc-microservices/01-evidence-ledger.md) | [_structure-outline](12-grpc-microservices/_structure-outline.md) | [10-reconstructed](12-grpc-microservices/10-2026-03-13-reconstructed-development-log.md) | `cd solution/go && go test -run TestCreateAndGet -v ./server/store` |
| 13 Distributed Log Core | [00-series-map](13-distributed-log-core/00-series-map.md) | [01-evidence-ledger](13-distributed-log-core/01-evidence-ledger.md) | [_structure-outline](13-distributed-log-core/_structure-outline.md) | [10-reconstructed](13-distributed-log-core/10-2026-03-13-reconstructed-development-log.md) | `cd solution/go && go test -run TestLogRestore -v ./log` |
