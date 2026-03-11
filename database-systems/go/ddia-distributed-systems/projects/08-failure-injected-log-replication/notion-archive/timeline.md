# 08-failure-injected-log-replication 개발 타임라인

## 1. 프로젝트 골격 만들기

```bash
mkdir -p go/ddia-distributed-systems/projects/08-failure-injected-log-replication/{cmd/failure-replication,docs/concepts,docs/references,internal/replication,notion,notion-archive,problem,tests}
cd go/ddia-distributed-systems/projects/08-failure-injected-log-replication
go mod init study.local/go/ddia-distributed-systems/projects/08-failure-injected-log-replication
```

## 2. replication path 최소화

처음부터 full Raft를 넣지 않고 다음 구조로 줄였다.

- leader 1개
- follower 2개
- message type 2개: `append`, `ack`
- network harness 1개

핵심 목표는 “partial failure를 재현 가능한 장면으로 만들자”였다.

## 3. failure rule 설계

하네스는 세 규칙만 지원하게 했다.

| 규칙 | 의미 |
| --- | --- |
| `DropNext` | 특정 메시지를 한 번 버림 |
| `DuplicateNext` | 특정 메시지를 한 번 더 전달 |
| `PauseNode` / `ResumeNode` | 특정 node로 가는 메시지를 일시적으로 차단 |

이 세 규칙만으로 retry, idempotency, lagging follower를 모두 재현할 수 있다.

## 4. follower 안전 규칙 추가

duplicate delivery가 왔을 때 follower가 같은 entry를 다시 append하면 retry가 위험해진다. 그래서 다음 규칙을 넣었다.

- 같은 index에 같은 entry가 이미 있으면 무시
- gap이 있는 entry는 바로 append하지 않음
- entry가 새로 붙을 때만 state mutation과 applied count 증가

## 5. 테스트 추가

| 테스트명 | 검증 대상 |
| --- | --- |
| `TestDroppedAppendRetriesUntilFollowerConverges` | dropped append 뒤 retry로 follower catch-up |
| `TestDuplicateAppendIsIdempotent` | duplicate delivery에도 log/apply 1회 유지 |
| `TestPausedFollowerLagsButRecoversAfterResume` | quorum commit 유지 + resume 뒤 catch-up |

## 6. 데모 출력 설계

`go run ./cmd/failure-replication`은 다섯 장면을 순서대로 보여 준다.

```text
drop tick commit=0 node-2=-1 node-3=0
retry tick commit=0 node-2=0 node-3=0
duplicate tick commit=1 node-3-log=2 node-3-applied=2
pause tick commit=2 node-2=1 node-3=2
recover tick commit=2 node-2=2 node-3=2
```

- 첫 줄: 한 follower는 첫 append를 놓쳤지만 quorum commit은 이미 가능
- 둘째 줄: retry로 lagging follower가 따라옴
- 셋째 줄: duplicate append가 와도 follower state는 안전
- 넷째 줄: paused follower 때문에 lag가 남음
- 다섯째 줄: resume 뒤 convergence 완료

## 7. 검증 명령

```bash
cd go/ddia-distributed-systems/projects/08-failure-injected-log-replication
GOWORK=off go test ./...
GOWORK=off go run ./cmd/failure-replication
```

## 8. 핵심 파일

| 항목 | 위치 |
| --- | --- |
| 핵심 구현 | `internal/replication/replication.go` |
| 테스트 | `tests/replication_test.go` |
| 데모 | `cmd/failure-replication/main.go` |
| 개념 문서 | `docs/concepts/quorum-commit-and-retry.md` |

## 9. 다시 구현할 때 주의점

- leader의 `nextIndex`와 `matchIndex`를 follower별로 분리할 것
- commit index는 quorum ack로만 올릴 것
- pause를 queue 적체가 아니라 blackhole로 단순화했다는 점을 문서에 남길 것
