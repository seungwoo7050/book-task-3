# 05 HTTP REST Basics Structure Outline

이 문서는 chronology ledger를 바탕으로 최종 blog를 어떤 순서로 전개할지 먼저 고정한 설계 메모다. 기존 `blog/` 초안은 입력에서 제외했고, 실제 코드, README, docs, 테스트, CLI만을 근거로 삼는다.

## Planned Files

- `00-series-map.md`: 프로젝트 범위, source-of-truth, 읽는 순서를 잡는 진입 문서
- `01-evidence-ledger.md`: 파일, 함수, CLI 단위 chronology를 거칠게 복원한 근거 문서
- `10-2026-03-13-reconstructed-development-log.md`: 구현 순서와 판단 전환점을 세션 흐름으로 다시 쓴 최종 blog

## Final Blog Flow

- 도입: README 한 줄 요약과 이번 재검증 범위를 붙여 글의 위치를 먼저 밝힌다.
- 구현 순서 요약: Phase 1 -> Phase 2 -> Phase 3 순서를 미리 보여 준다.
- 세션형 chronology: 각 phase에서 당시 목표, 가설, 조치, 코드 앵커, 검증 신호를 순서대로 다시 적는다.
- CLI로 닫는 구간: 현재 저장소에서 다시 실행한 명령과 excerpt를 붙여 README 계약이 아직 살아 있는지 확인한다.
- 남은 질문: 개념 축과 다음 실험 지점을 남긴다.

## Section Plan

### 1. Phase 1 - Task와 in-memory Server로 리소스 경계를 먼저 고정한다

- 목표: Task와 in-memory Server로 리소스 경계를 먼저 고정한다
- 변경 단위: `solution/go/internal/api/api.go`의 `NewServer`
- 핵심 가설: `NewServer` 쪽에서 상태 경계를 먼저 세우면 HTTP layer는 훨씬 단순해질 것이라고 봤다.
- 반드시 넣을 코드 앵커: `NewServer`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestHealthcheck`였다.
- 새로 배운 것 섹션 포인트: `GET /v1/healthcheck`는 서비스 생존 여부를 확인하는 최소 endpoint다.
- 다음 섹션 연결 문장: Routes와 createTask, listTasks handler로 HTTP 표면을 세운다
### 2. Phase 2 - Routes와 createTask, listTasks handler로 HTTP 표면을 세운다

- 목표: Routes와 createTask, listTasks handler로 HTTP 표면을 세운다
- 변경 단위: `solution/go/internal/api/api.go`의 `createTask`
- 핵심 가설: `createTask`에 transport 규칙을 모아 두면 validation과 응답 shape를 한곳에서 설명할 수 있다고 판단했다.
- 반드시 넣을 코드 앵커: `createTask`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestListTasksPagination`였다.
- 새로 배운 것 섹션 포인트: idempotency key 저장을 메모리에 두면 동작은 보이지만 프로세스 재시작에는 약하다.
- 다음 섹션 연결 문장: api_test로 validation, idempotency, pagination 계약을 잠근다
### 3. Phase 3 - api_test로 validation, idempotency, pagination 계약을 잠근다

- 목표: api_test로 validation, idempotency, pagination 계약을 잠근다
- 변경 단위: `solution/go/internal/api/api_test.go`의 `TestCreateTaskIdempotency`
- 핵심 가설: `TestCreateTaskIdempotency` 같은 테스트가 있어야 handler, auth, cache 계약이 서로 섞이지 않는다고 봤다.
- 반드시 넣을 코드 앵커: `TestCreateTaskIdempotency`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestListTasksPagination`였다.
- 새로 배운 것 섹션 포인트: page/page_size를 음수나 0으로 넣었을 때 fallback 규칙을 빼먹기 쉽다.
- 다음 섹션 연결 문장: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/05-http-rest-basics && cd solution/go && go test -v ./internal/api)
```

```text
=== RUN   TestHealthcheck
=== PAUSE TestHealthcheck
=== RUN   TestCreateTaskValidation
=== PAUSE TestCreateTaskValidation
=== RUN   TestCreateTaskIdempotency
=== PAUSE TestCreateTaskIdempotency
=== RUN   TestListTasksPagination
=== PAUSE TestListTasksPagination
=== RUN   TestShowTaskNotFound
=== PAUSE TestShowTaskNotFound
=== CONT  TestHealthcheck
=== CONT  TestShowTaskNotFound
=== CONT  TestCreateTaskIdempotency
=== CONT  TestListTasksPagination
=== CONT  TestCreateTaskValidation
--- PASS: TestHealthcheck (0.00s)
--- PASS: TestCreateTaskIdempotency (0.00s)
--- PASS: TestShowTaskNotFound (0.00s)
--- PASS: TestCreateTaskValidation (0.00s)
--- PASS: TestListTasksPagination (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/01-backend-core/05-http-rest-basics/internal/api	(cached)
```

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/05-http-rest-basics && cd solution/go && go test -run TestListTasksPagination -v ./internal/api)
```

```text
=== RUN   TestListTasksPagination
=== PAUSE TestListTasksPagination
=== CONT  TestListTasksPagination
--- PASS: TestListTasksPagination (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/01-backend-core/05-http-rest-basics/internal/api	(cached)
```
