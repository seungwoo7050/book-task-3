# 03 Testing And Debugging Structure Outline

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

### 1. Phase 1 - ParseLine과 Recorder로 로그 파싱 경계를 먼저 나눈다

- 목표: ParseLine과 Recorder로 로그 파싱 경계를 먼저 나눈다
- 변경 단위: `solution/go/analyzer/analyzer.go`의 `ParseLine`
- 핵심 가설: `ParseLine`를 먼저 고정하면 I/O보다 데이터 규칙을 더 선명하게 설명할 수 있다고 봤다.
- 반드시 넣을 코드 앵커: `ParseLine`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `search count=2 avg_ms=100`였다.
- 새로 배운 것 섹션 포인트: table-driven test는 입력과 기대값을 나란히 놓아 케이스 확장을 쉽게 만든다.
- 다음 섹션 연결 문장: Summarize와 debugdemo CLI로 요약 표면을 만든다
### 2. Phase 2 - Summarize와 debugdemo CLI로 요약 표면을 만든다

- 목표: Summarize와 debugdemo CLI로 요약 표면을 만든다
- 변경 단위: `solution/go/analyzer/analyzer.go`의 `Summarize`
- 핵심 가설: `Summarize`를 중심에 두면 demo entrypoint는 얇은 연결층으로 남길 수 있다고 판단했다.
- 반드시 넣을 코드 앵커: `Summarize`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `goos: darwin`였다.
- 새로 배운 것 섹션 포인트: benchmark 수치만 보고 설계를 바꾸면 실제 서비스 병목과 어긋날 수 있다.
- 다음 섹션 연결 문장: table-driven test와 benchmark로 디버깅 루프를 고정한다
### 3. Phase 3 - table-driven test와 benchmark로 디버깅 루프를 고정한다

- 목표: table-driven test와 benchmark로 디버깅 루프를 고정한다
- 변경 단위: `solution/go/analyzer/analyzer_test.go`의 `BenchmarkSummarize`
- 핵심 가설: 테스트 이름 `BenchmarkSummarize`처럼 계약을 먼저 못 박아야 구현이 흔들리지 않는다고 봤다.
- 반드시 넣을 코드 앵커: `BenchmarkSummarize`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `goos: darwin`였다.
- 새로 배운 것 섹션 포인트: 파싱 에러를 너무 넓게 뭉개면 디버깅 신호가 약해진다.
- 다음 섹션 연결 문장: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## Fixed CLI Anchor

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/00-go-fundamentals/03-testing-and-debugging && cd solution/go && go run ./cmd/debugdemo)
```

```text
search count=2 avg_ms=100
checkout count=1 avg_ms=150
```

```bash
(cd /Users/woopinbell/work/book-task-3/study/00-go-fundamentals/03-testing-and-debugging && cd solution/go && go test ./... -bench=.)
```

```text
goos: darwin
goarch: arm64
pkg: github.com/woopinbell/go-backend/study/00-go-fundamentals/03-testing-and-debugging/analyzer
cpu: Apple M1
BenchmarkSummarize-8   	   21090	     54910 ns/op
PASS
ok  	github.com/woopinbell/go-backend/study/00-go-fundamentals/03-testing-and-debugging/analyzer	1.965s
?   	github.com/woopinbell/go-backend/study/00-go-fundamentals/03-testing-and-debugging/cmd/debugdemo	[no test files]
```
