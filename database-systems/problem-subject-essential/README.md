# Database Systems 서버 개발 필수 문제지

`database-systems`에서 서버 공통 필수로 남긴 문제지만 모아 둡니다.
단일 노드 durable write path와 분산 복제의 가장 직접적인 경계만 남깁니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [leader-follower-replication](leader-follower-replication.md) | 시작 위치의 구현을 완성해 순차 offset을 갖는 mutation log를 유지해야 합니다, put과 delete가 복제돼야 합니다, follower watermark 기반 incremental sync가 필요합니다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication && GOWORK=off go test ./...` |
| [mvcc](mvcc.md) | 시작 위치의 구현을 완성해 snapshot isolation 하에서 읽기 스냅샷과 write-write conflict를 관리해야 합니다, read-your-own-write를 보장해야 합니다, first-committer-wins conflict detection이 필요합니다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc && GOWORK=off go test ./...` |
| [wal-recovery](wal-recovery.md) | 시작 위치의 구현을 완성해 PUT/DELETE는 memtable 반영 전에 WAL에 먼저 기록돼야 합니다, 레코드는 checksum, type, key/value 길이, payload를 포함해야 합니다, replay는 첫 손상 레코드에서 멈추고 그 뒤는 버려야 합니다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery && GOWORK=off go test ./...` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
