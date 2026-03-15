# 04 Raft Lite

## 이 랩의 실제 초점

이 프로젝트는 Raft 전체를 구현하지 않는다. 대신 leader election, vote rule, AppendEntries consistency, current-term majority commit, higher-term step-down이라는 핵심 규칙만 남긴 작은 동기 시뮬레이터다. randomized timeout 대신 노드별 고정 election TTL을 써서 테스트를 결정적으로 만들고, persistent log나 snapshotting은 일부러 비워 둔다.

즉 이 랩의 핵심은 consensus 시스템을 완성했다는 데 있지 않고, term과 log 규칙이 leader 교체와 commit safety를 어떻게 만들고 있는지 source-first로 드러내는 데 있다.

이번 시리즈는 기존 blog를 입력 근거로 쓰지 않고 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite/problem/README.md), [`raft.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite/internal/raft/raft.go), [`raft_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite/tests/raft_test.go), [`main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite/cmd/raft-lite/main.go), 그리고 2026-03-14 재실행 결과만으로 다시 썼다.

## 이번에 붙드는 질문

- follower가 candidate로 바뀌고 leader가 되기까지 term과 vote는 어떻게 움직이는가
- AppendEntries consistency check는 log mismatch를 어떻게 다루는가
- majority commit은 왜 current term entry에만 적용되는가
- higher term을 본 leader는 언제 어떻게 step-down하는가

## 문서 지도

- [10-chronology-scope-and-surface.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/04-raft-lite/10-chronology-scope-and-surface.md): 문제 범위, node/cluster 표면, demo 결과를 시간순으로 정리한다.
- [20-chronology-core-invariants.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/04-raft-lite/20-chronology-core-invariants.md): election cycle, vote up-to-date rule, AppendEntries consistency, majority commit, higher-term step-down을 소스 기준으로 해부한다.
- [30-chronology-verification-and-boundaries.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/04-raft-lite/30-chronology-verification-and-boundaries.md): go test와 demo, 추가 재실행을 묶어 현재 검증 범위와 한계를 정리한다.
- [_evidence-ledger.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/04-raft-lite/_evidence-ledger.md): 근거 파일과 재실행 명령, 관찰값을 남긴다.
- [_structure-outline.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/04-raft-lite/_structure-outline.md): 문서 구조 선택 이유와 버린 접근을 적는다.

## 지금 기준의 결론

이 랩은 Go 분산 시스템 트랙에서 처음으로 consensus 규칙을 드러낸다. persistent log, membership change, snapshotting, real transport는 아직 없다. 대신 election, vote up-to-date, append consistency, majority commit, step-down 규칙은 분명하게 드러난다.
