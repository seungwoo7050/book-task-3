# 02 Leader-Follower Replication

## 이 랩의 실제 초점

이 프로젝트는 replication을 "두 store 상태를 맞춘다"는 수준보다 더 정확하게, ordered mutation log와 follower watermark를 이용해 incremental sync를 만든다. leader는 local state와 append-only log를 함께 유지하고, follower는 자신이 마지막으로 적용한 offset 이후 entry만 받아 적용한다. 같은 batch를 다시 받아도 `offset <= watermark`면 건너뛰므로 replay가 idempotent하다. delete 역시 ordinary mutation으로 복제된다.

즉 이 랩의 핵심은 consensus나 failover가 아니라, replication을 가능하게 만드는 가장 작은 ordered log contract를 source-first로 드러내는 데 있다.

이번 시리즈는 기존 blog를 입력 근거로 쓰지 않고 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/problem/README.md), [`replication.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/internal/replication/replication.go), [`replication_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/tests/replication_test.go), [`main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/cmd/replication/main.go), 그리고 2026-03-14 재실행 결과만으로 다시 썼다.

## 이번에 붙드는 질문

- leader는 local state와 replication log를 어떤 순서로 함께 갱신하는가
- follower watermark는 incremental sync 경계를 어디서 자르는가
- duplicate replay는 왜 결과를 바꾸지 않는가
- delete는 ordered mutation stream 안에서 어떻게 보존되는가

## 문서 지도

- [10-chronology-scope-and-surface.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/02-leader-follower-replication/10-chronology-scope-and-surface.md): 문제 범위, leader/follower 표면, demo 결과를 시간순으로 정리한다.
- [20-chronology-core-invariants.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/02-leader-follower-replication/20-chronology-core-invariants.md): sequential offset, watermark-based fetch, idempotent apply, delete propagation을 소스 기준으로 해부한다.
- [30-chronology-verification-and-boundaries.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/02-leader-follower-replication/30-chronology-verification-and-boundaries.md): go test와 demo, 추가 재실행을 묶어 현재 검증 범위와 한계를 정리한다.
- [_evidence-ledger.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/02-leader-follower-replication/_evidence-ledger.md): 근거 파일과 재실행 명령, 관찰값을 남긴다.
- [_structure-outline.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/02-leader-follower-replication/_structure-outline.md): 문서 구조 선택 이유와 버린 접근을 적는다.

## 지금 기준의 결론

이 랩은 Go 분산 시스템 트랙의 두 번째 단계에서 "state replication보다 mutation stream replication이 핵심"이라는 사실을 보여 준다. election, quorum, multi-leader는 아직 없다. 대신 ordered offset log, watermark fetch, idempotent replay, delete propagation은 분명하게 드러난다.
