# 02 Distributed Systems

## 이 트랙이 푸는 문제

- gRPC, append-only log 같은 분산 시스템 주제를 추상 설명으로만 배우면 코드 감각이 붙지 않는다.

## 이 트랙의 답

- contract-first gRPC 서비스와 파일 기반 commit log 구현을 각각 독립 실행 가능한 프로젝트로 만들었다.

## 프로젝트 순서

1. [12-grpc-microservices](12-grpc-microservices/README.md) : Protocol Buffers, unary/streaming RPC, interceptor를 작은 Product Catalog 서비스로 묶어 contract-first 감각을 익히는 과제다.
2. [13-distributed-log-core](13-distributed-log-core/README.md) : append-only store, mmap index, segment rotation, log abstraction을 직접 구현해 commit log 핵심을 익히는 대표 과제다.

## 졸업 기준

- gRPC contract-first 설계와 interceptor 역할을 코드 기준으로 설명할 수 있어야 한다.
- segment, index, append-only log가 왜 필요한지 파일 포맷과 테스트 기준으로 설명할 수 있어야 한다.

## 대표 프로젝트

- [13-distributed-log-core](13-distributed-log-core/README.md) : 분산 시스템 개념을 자료구조와 파일 포맷으로 번역한 대표 과제다.
