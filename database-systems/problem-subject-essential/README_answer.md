# Database Systems 서버 개발 필수 답안지

이 문서는 `database-systems` 필수 문제의 해답을 실제 Python 소스와 테스트만으로 읽히게 정리한 답안지다. 핵심은 durable write path, 다중 버전 가시성, 기본 복제를 각각 추상 설명이 아니라 재현 가능한 코드 경로로 이해하는 데 있다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [leader-follower-replication](leader-follower-replication_answer.md) | 시작 위치의 구현을 완성해 순차 offset을 갖는 mutation log를 유지해야 합니다, put과 delete가 복제돼야 합니다, follower watermark 기반 incremental sync가 필요합니다를 한 흐름으로 설명하고 검증한다. 핵심은 main와 Append, From 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication && GOWORK=off go test ./...` |
| [mvcc](mvcc_answer.md) | 시작 위치의 구현을 완성해 snapshot isolation 하에서 읽기 스냅샷과 write-write conflict를 관리해야 합니다, read-your-own-write를 보장해야 합니다, first-committer-wins conflict detection이 필요합니다를 한 흐름으로 설명하고 검증한다. 핵심은 main와 must, NewVersionStore 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc && GOWORK=off go test ./...` |
| [wal-recovery](wal-recovery_answer.md) | 시작 위치의 구현을 완성해 PUT/DELETE는 memtable 반영 전에 WAL에 먼저 기록돼야 합니다, 레코드는 checksum, type, key/value 길이, payload를 포함해야 합니다, replay는 첫 손상 레코드에서 멈추고 그 뒤는 버려야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 main와 must, New 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery && GOWORK=off go test ./...` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
