# 13 Distributed Log Core Structure Outline

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

### 1. Phase 1 - store와 index로 바이트, offset primitive를 먼저 고정한다

- 목표: store와 index로 바이트, offset primitive를 먼저 고정한다
- 변경 단위: `solution/go/log/store.go`의 `store.Append`
- 핵심 가설: `store.Append` 같은 바이트 단위 primitive가 먼저 안정돼야 segment와 log 조합을 설명할 수 있다고 봤다.
- 반드시 넣을 코드 앵커: `store.Append`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestLogRestore`였다.
- 새로 배운 것 섹션 포인트: store는 레코드 바이트를 순차 append하는 역할이다.
- 다음 섹션 연결 문장: segment와 Log로 append-only composition을 완성한다
### 2. Phase 2 - segment와 Log로 append-only composition을 완성한다

- 목표: segment와 Log로 append-only composition을 완성한다
- 변경 단위: `solution/go/log/log.go`의 `Log.Append`
- 핵심 가설: `Log.Append`에 append path를 모으면 segment split과 reopen 규칙을 한 흐름으로 읽을 수 있다고 판단했다.
- 반드시 넣을 코드 앵커: `Log.Append`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `goos: darwin`였다.
- 새로 배운 것 섹션 포인트: replication을 빼면 범위는 줄지만 “분산”이라는 이름이 다소 강하게 들릴 수 있다.
- 다음 섹션 연결 문장: restore, truncate tests와 benchmark로 durability 계약을 잠근다
### 3. Phase 3 - restore, truncate tests와 benchmark로 durability 계약을 잠근다

- 목표: restore, truncate tests와 benchmark로 durability 계약을 잠근다
- 변경 단위: `solution/go/log/log_test.go`의 `TestLogRestore`
- 핵심 가설: `TestLogRestore` 같은 회복 테스트가 있어야 durability를 진짜로 설명할 수 있다고 봤다.
- 반드시 넣을 코드 앵커: `TestLogRestore`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `goos: darwin`였다.
- 새로 배운 것 섹션 포인트: truncate/reset 시 store와 index를 같이 정리하지 않으면 논리적 오염이 남는다.
- 다음 섹션 연결 문장: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## Fixed CLI Anchor

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/02-distributed-systems/13-distributed-log-core && cd solution/go && go test -run TestLogRestore -v ./log)
```

```text
=== RUN   TestLogRestore
--- PASS: TestLogRestore (0.02s)
PASS
ok  	github.com/woopinbell/go-backend/study/02-distributed-systems/13-distributed-log-core/log	(cached)
```

```bash
(cd /Users/woopinbell/work/book-task-3/study/02-distributed-systems/13-distributed-log-core && cd solution/go && go test ./log/... -bench=.)
```

```text
goos: darwin
goarch: arm64
pkg: github.com/woopinbell/go-backend/study/02-distributed-systems/13-distributed-log-core/log
cpu: Apple M1
BenchmarkLogAppend-8     	 2452268	       445.6 ns/op
BenchmarkStoreAppend-8   	 3288534	       363.9 ns/op
PASS
ok  	github.com/woopinbell/go-backend/study/02-distributed-systems/13-distributed-log-core/log	3.433s
```
