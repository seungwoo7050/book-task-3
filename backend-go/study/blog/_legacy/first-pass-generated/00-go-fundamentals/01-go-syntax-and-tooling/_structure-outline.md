# 01 Go Syntax And Tooling Structure Outline

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

### 1. Phase 1 - NormalizeWords와 CountWords로 문자열 정규화 규칙을 먼저 고정한다

- 목표: NormalizeWords와 CountWords로 문자열 정규화 규칙을 먼저 고정한다
- 변경 단위: `solution/go/lesson/lesson.go`의 `NormalizeWords`
- 핵심 가설: `NormalizeWords`를 먼저 고정하면 I/O보다 데이터 규칙을 더 선명하게 설명할 수 있다고 봤다.
- 반드시 넣을 코드 앵커: `NormalizeWords`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `total=11 unique=9 top=go`였다.
- 새로 배운 것 섹션 포인트: strings.FieldsFunc`는 텍스트를 직접 루프 돌며 자르지 않아도 되는 표준 라이브러리 선택지다.
- 다음 섹션 연결 문장: BuildSummary와 toolingdemo CLI로 사람이 읽는 출력 표면을 만든다
### 2. Phase 2 - BuildSummary와 toolingdemo CLI로 사람이 읽는 출력 표면을 만든다

- 목표: BuildSummary와 toolingdemo CLI로 사람이 읽는 출력 표면을 만든다
- 변경 단위: `solution/go/lesson/lesson.go`의 `BuildSummary`
- 핵심 가설: `BuildSummary`를 중심에 두면 demo entrypoint는 얇은 연결층으로 남길 수 있다고 판단했다.
- 반드시 넣을 코드 앵커: `BuildSummary`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `?   	github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling/cmd/toolingdemo	[no test files]`였다.
- 새로 배운 것 섹션 포인트: 정렬은 `topWord` 결정의 안정성을 높여 주지만, 입력이 매우 크면 비용이 추가된다.
- 다음 섹션 연결 문장: lesson_test와 `go test` 루프로 입문형 문자열 로직을 잠근다
### 3. Phase 3 - lesson_test와 `go test` 루프로 입문형 문자열 로직을 잠근다

- 목표: lesson_test와 `go test` 루프로 입문형 문자열 로직을 잠근다
- 변경 단위: `solution/go/lesson/lesson_test.go`의 `TestBuildSummary`
- 핵심 가설: 테스트 이름 `TestBuildSummary`처럼 계약을 먼저 못 박아야 구현이 흔들리지 않는다고 봤다.
- 반드시 넣을 코드 앵커: `TestBuildSummary`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `?   	github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling/cmd/toolingdemo	[no test files]`였다.
- 새로 배운 것 섹션 포인트: 구두점 제거 기준을 너무 넓게 잡으면 숫자나 영문자가 잘못 분리된다.
- 다음 섹션 연결 문장: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/study/00-go-fundamentals/01-go-syntax-and-tooling && cd solution/go && go run ./cmd/toolingdemo)
```

```text
total=11 unique=9 top=go
```

```bash
(cd /Users/woopinbell/work/book-task-3/study/00-go-fundamentals/01-go-syntax-and-tooling && cd solution/go && go test ./...)
```

```text
?   	github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling/cmd/toolingdemo	[no test files]
ok  	github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling/lesson	(cached)
```
