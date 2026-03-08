# Documentation — Express Database

- 상위 리포트: [../../lab-report.md](../../lab-report.md)
- 챕터 개요: [../../README.md](../../README.md)

## 목적

Express에서 SQLite 영속 계층을 도입하고 repository 패턴으로 상위 계층 계약을 보존한다.
근거: [문서] ../../README.md

## 읽기 순서

1. [sqlite-basics.md](sqlite-basics.md)
2. [repository-pattern.md](repository-pattern.md)
3. [testing-patterns.md](testing-patterns.md)
4. [reproducibility.md](reproducibility.md)

근거: [문서] 위 문서군

## 예상 소요시간

- 총 80~100분
근거: [추론] 문서 분량 기반 추정

## 선수지식

- SQL CRUD/DDL
- TypeScript 타입 매핑
- 테스트 격리 기법
근거: [문서] sqlite-basics.md, [문서] testing-patterns.md

## 핵심 질문

- `BookRow -> Book` 매핑을 어디서 책임질 것인가?
- 동기 DB 드라이버 사용 시 어떤 트레이드오프가 있는가?
- E2E에서 DB 직접 검증을 어디까지 허용할 것인가?
근거: [문서] repository-pattern.md, [문서] testing-patterns.md
