# 04 SQL And Data Modeling Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 실제 migration tool은 뒤로 미루고 데이터 모델과 transaction 경계를 먼저 학습하게 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `01-backend-core/04-sql-and-data-modeling` 안에서 `20-transaction-and-verification-loop.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: Phase 4: CLI 바이너리 작성 -> Phase 5: 테스트 작성 -> Phase 6: 문서 작성 및 최종 검증
- 세션 본문: `solution/go/cmd/schemawalk/main.go, problem/README.md, docs/README.md, docs/concepts/core-concepts.md` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/catalog/catalog_test.go`
- 코드 앵커 2: `solution/go/cmd/schemawalk/main.go`
- 코드 설명 초점: 이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.
- 개념 설명: `PRIMARY KEY (player_id, item_id)`는 같은 아이템의 중복 행 생성을 막는다.
- 마지막 단락: 실제 migration binary와 외부 RDBMS 연결은 다음 과제에서 다룬다.
