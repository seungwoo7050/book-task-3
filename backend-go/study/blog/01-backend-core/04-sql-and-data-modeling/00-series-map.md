# 04 SQL And Data Modeling Series Map

`01-backend-core/04-sql-and-data-modeling`는 스키마 설계, join, transaction을 게임 상점 예제로 묶어 SQL 기초를 백엔드 문맥에서 익히는 브리지 과제다.

## 이 시리즈가 복원하는 것

- 시작점: 스키마 설계와 관계 모델링을 실제 도메인 예제로 익혀야 한다.
- 구현 축: `players`, `items`, `inventory`를 중심으로 한 게임 상점 스키마와 조회/구매 예제를 `solution/go`에 구현했다.
- 검증 축: 2026-03-07 기준 `go run ./cmd/schemawalk`가 정상 실행됐다.
- 글 수: 2편

## 읽는 순서

- [10-schema-and-query-shape.md](10-schema-and-query-shape.md)
- [20-transaction-and-verification-loop.md](20-transaction-and-verification-loop.md)

## 근거 기준

- 소스코드, README, docs, 테스트, CLI만 입력 근거로 사용했다.
- 기존 blog 초안과 `_legacy` 본문은 입력 근거로 사용하지 않았다.
