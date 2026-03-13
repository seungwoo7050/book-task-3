# 10 Concurrency Patterns Structure Outline

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

### 1. Phase 1 - Pool과 worker goroutine으로 bounded concurrency를 먼저 고정한다

- 목표: Pool과 worker goroutine으로 bounded concurrency를 먼저 고정한다
- 변경 단위: `solution/go/workerpool/pool.go`의 `NewPool`
- 핵심 가설: `NewPool`처럼 worker lifecycle을 먼저 고정해야 goroutine 누수 여부를 나중에 설명할 수 있다고 봤다.
- 반드시 넣을 코드 앵커: `NewPool`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `Running worker pool example...`였다.
- 새로 배운 것 섹션 포인트: worker pool은 제한된 수의 goroutine으로 작업을 소비하는 패턴이다.
- 다음 섹션 연결 문장: Generate, Filter, FanOut으로 channel pipeline을 조립한다
### 2. Phase 2 - Generate, Filter, FanOut으로 channel pipeline을 조립한다

- 목표: Generate, Filter, FanOut으로 channel pipeline을 조립한다
- 변경 단위: `solution/go/pipeline/pipeline.go`의 `FanOut`
- 핵심 가설: `FanOut`를 통해 channel 흐름을 분리하면 backpressure와 cancellation을 코드 수준에서 읽기 쉬워진다고 판단했다.
- 반드시 넣을 코드 앵커: `FanOut`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `Running pipeline example...`였다.
- 새로 배운 것 섹션 포인트: pipeline은 읽기 쉽지만 stage가 많아질수록 디버깅이 어려워질 수 있다.
- 다음 섹션 연결 문장: demo CLI와 benchmark로 concurrency 패턴 차이를 닫는다
### 3. Phase 3 - demo CLI와 benchmark로 concurrency 패턴 차이를 닫는다

- 목표: demo CLI와 benchmark로 concurrency 패턴 차이를 닫는다
- 변경 단위: `solution/go/workerpool/pool_test.go`의 `TestPoolNoGoroutineLeaks`
- 핵심 가설: demo와 테스트가 같이 있어야 concurrency 패턴 차이가 수치와 출력 둘 다에서 보인다고 봤다.
- 반드시 넣을 코드 앵커: `TestPoolNoGoroutineLeaks`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `Running tests...`였다.
- 새로 배운 것 섹션 포인트: benchmark 숫자만 보고 실서비스 concurrency 정책으로 바로 옮기면 과적합될 수 있다.
- 다음 섹션 연결 문장: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/10-concurrency-patterns && make -C problem run-workerpool)
```

```text
Running worker pool example...
cd ../solution/go && go run ./cmd/workerpool
Job 1: result = 1
Job 2: result = 4
Job 3: result = 9
Job 4: result = 16
Job 7: result = 49
Job 6: result = 36
Job 5: result = 25
Job 8: result = 64
Job 10: result = 100
Job 9: result = 81
Job 12: result = 144
Job 11: result = 121
Job 16: result = 256
Job 14: result = 196
Job 13: result = 169
Job 15: result = 225
Job 18: result = 324
Job 20: result = 400
Job 17: result = 289
Job 19: result = 361
... (1 more lines)
```

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/10-concurrency-patterns && make -C problem run-pipeline)
```

```text
Running pipeline example...
cd ../solution/go && go run ./cmd/pipeline
Primes from 1 to 50: [2 3 5 7 11 13 17 19 23 29 31 37 41 43 47]
Count: 15
```
