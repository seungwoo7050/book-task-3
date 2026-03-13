# 06 Go API Standard Structure Outline

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

### 1. Phase 1 - MovieStore와 data model로 API 핵심 상태를 먼저 고정한다

- 목표: MovieStore와 data model로 API 핵심 상태를 먼저 고정한다
- 변경 단위: `solution/go/internal/data/movies.go`의 `NewMovieStore`
- 핵심 가설: `NewMovieStore` 같은 저장소 경계가 먼저 있어야 handler와 middleware가 표준 라이브러리 수준에서 정리된다고 봤다.
- 반드시 넣을 코드 앵커: `NewMovieStore`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestHealthcheckHandler`였다.
- 새로 배운 것 섹션 포인트: application` struct에 의존성을 모으면 handler와 middleware를 같은 문맥에서 다루기 쉽다.
- 다음 섹션 연결 문장: handlers, routes, middleware로 표준 라이브러리 HTTP surface를 조립한다
### 2. Phase 2 - handlers, routes, middleware로 표준 라이브러리 HTTP surface를 조립한다

- 목표: handlers, routes, middleware로 표준 라이브러리 HTTP surface를 조립한다
- 변경 단위: `solution/go/cmd/api/handlers.go`의 `createMovieHandler`
- 핵심 가설: `createMovieHandler` 쪽에 공개 API 규칙을 모으면 framework 없이도 응답 shape를 안정적으로 유지할 수 있다고 판단했다.
- 반드시 넣을 코드 앵커: `createMovieHandler`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `ok  	github.com/woopinbell/go-backend/study/01-backend-core/06-go-api-standard/cmd/api	(cached)`였다.
- 새로 배운 것 섹션 포인트: 표준 라이브러리만 쓰면 학습엔 좋지만 반복 코드가 늘어난다.
- 다음 섹션 연결 문장: handler/store tests와 race 검증으로 공개 계약을 잠근다
### 3. Phase 3 - handler/store tests와 race 검증으로 공개 계약을 잠근다

- 목표: handler/store tests와 race 검증으로 공개 계약을 잠근다
- 변경 단위: `solution/go/cmd/api/handlers_test.go`의 `TestCreateMovieHandler`
- 핵심 가설: `TestCreateMovieHandler`와 race 검증이 같이 있어야 middleware 순서와 store 동시성까지 닫힌다고 봤다.
- 반드시 넣을 코드 앵커: `TestCreateMovieHandler`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `ok  	github.com/woopinbell/go-backend/study/01-backend-core/06-go-api-standard/cmd/api	(cached)`였다.
- 새로 배운 것 섹션 포인트: middleware 체인 순서를 잘못 두면 panic recovery나 로깅이 기대와 다르게 동작할 수 있다.
- 다음 섹션 연결 문장: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## Fixed CLI Anchor

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/06-go-api-standard && cd solution/go && go test -v ./cmd/api)
```

```text
=== RUN   TestHealthcheckHandler
=== RUN   TestHealthcheckHandler/valid_healthcheck
--- PASS: TestHealthcheckHandler (0.00s)
    --- PASS: TestHealthcheckHandler/valid_healthcheck (0.00s)
=== RUN   TestCreateMovieHandler
=== RUN   TestCreateMovieHandler/valid_movie
=== RUN   TestCreateMovieHandler/missing_title
=== RUN   TestCreateMovieHandler/year_too_low
=== RUN   TestCreateMovieHandler/negative_runtime
=== RUN   TestCreateMovieHandler/no_genres
=== RUN   TestCreateMovieHandler/empty_body
--- PASS: TestCreateMovieHandler (0.00s)
    --- PASS: TestCreateMovieHandler/valid_movie (0.00s)
    --- PASS: TestCreateMovieHandler/missing_title (0.00s)
    --- PASS: TestCreateMovieHandler/year_too_low (0.00s)
    --- PASS: TestCreateMovieHandler/negative_runtime (0.00s)
    --- PASS: TestCreateMovieHandler/no_genres (0.00s)
    --- PASS: TestCreateMovieHandler/empty_body (0.00s)
=== RUN   TestShowMovieHandler
=== RUN   TestShowMovieHandler/existing_movie
=== RUN   TestShowMovieHandler/non-existing_movie
=== RUN   TestShowMovieHandler/invalid_id
... (12 more lines)
```

```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/06-go-api-standard && cd solution/go && go test -race ./...)
```

```text
ok  	github.com/woopinbell/go-backend/study/01-backend-core/06-go-api-standard/cmd/api	(cached)
ok  	github.com/woopinbell/go-backend/study/01-backend-core/06-go-api-standard/internal/data	(cached)
```
