# 08 SQL Store API Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- optimistic update와 rollback을 같은 과제에 묶어 이후 정합성 과제의 발판으로 삼았다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `01-backend-core/08-sql-store-api` 안에서 `20-http-surface-optimistic-update-and-rollback.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 7단계: 에러 정의 -> 8단계: App 구조체와 라우트 -> 9단계: 핸들러 구현 -> 10단계: main.go 작성 -> 11단계: 테스트 작성 (store_test.go) -> 12단계: 실행 및 API 검증
- 세션 본문: `solution/go/internal/store/store_test.go, solution/go/internal/store/store.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/internal/store/store_test.go`
- 코드 앵커 2: `solution/go/internal/store/store.go`
- 코드 설명 초점: 이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.
- 개념 설명: repository는 handler가 SQL 세부 사항을 직접 알지 않게 분리해 준다.
- 마지막 단락: 외부 DB 연결과 connection pool 조정은 다루지 않았다.
