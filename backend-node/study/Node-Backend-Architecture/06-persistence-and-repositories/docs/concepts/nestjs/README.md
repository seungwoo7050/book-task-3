# Documentation — NestJS Database

- 상위 리포트: [../../lab-report.md](../../lab-report.md)
- 챕터 개요: [../../README.md](../../README.md)

## 목적

TypeORM 기반 Entity/Repository로 데이터 접근을 표준화하고 NestJS DI와 결합한다.
근거: [문서] ../../README.md

## 읽기 순서

1. [typeorm-basics.md](typeorm-basics.md)
2. [nestjs-typeorm.md](nestjs-typeorm.md)
3. [testing-patterns.md](testing-patterns.md)
4. [reproducibility.md](reproducibility.md)

근거: [문서] 위 문서군

## 예상 소요시간

- 총 85~105분
근거: [추론] 문서 분량 기반 추정

## 선수지식

- ORM 기본 개념
- NestJS 모듈/프로바이더
- Promise 기반 비동기 흐름
근거: [문서] typeorm-basics.md, [문서] nestjs-typeorm.md

## 핵심 질문

- Entity가 타입/스키마/매핑을 동시에 맡을 때의 장단점은?
- `synchronize`를 어떤 환경에서 허용할 것인가?
- 테스트에서 mock repository vs 실제 in-memory DB 중 무엇을 선택할 것인가?
근거: [문서] testing-patterns.md
