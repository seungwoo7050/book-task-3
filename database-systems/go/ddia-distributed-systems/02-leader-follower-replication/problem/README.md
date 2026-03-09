# Problem Framing

leader는 write를 local store에 적용하면서 append-only log에 기록하고, follower는 자신이 마지막으로 적용한 offset 이후의 log entry만 받아 local state를 따라간다.

## Success Criteria

- 순차 offset을 갖는 mutation log
- `put` / `delete` 복제
- follower watermark 기반 incremental sync
- replay된 entry를 다시 받아도 결과가 깨지지 않는 idempotent apply

## Source Provenance

- 원본 문제: `legacy/distributed-cluster/replication/problem/README.md`
- 원본 테스트 의미: `legacy/distributed-cluster/replication/solve/test/replication.test.js`
- 원본 구현 참고: `legacy/distributed-cluster/replication/solve/solution/replication.js`
