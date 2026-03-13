# 04 SQL And Data Modeling Structure

## 이 글이 답할 질문

- 스키마 설계와 관계 모델링을 실제 도메인 예제로 익혀야 한다.
- ORM 없이 SQL 구조를 먼저 보여 주기 위해 스키마와 쿼리 자체를 학습 표면에 올렸다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `01-backend-core/04-sql-and-data-modeling` 안에서 `10-schema-and-query-shape.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: Phase 1: 프로젝트 뼈대와 의존성 -> Phase 2: 스키마 설계 -> Phase 3: 쿼리 구현
- 세션 본문: `modernc.org/sqlite, solution/go/catalog/catalog.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/catalog/catalog.go`
- 코드 앵커 2: `solution/go/cmd/schemawalk/main.go`
- 코드 설명 초점: 이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.
- 개념 설명: `players`, `items`, `inventory` 분리는 다대다 관계를 명시적으로 드러낸다.
- 마지막 단락: 다음 글에서는 `20-transaction-and-verification-loop.md`에서 이어지는 경계를 다룬다.
