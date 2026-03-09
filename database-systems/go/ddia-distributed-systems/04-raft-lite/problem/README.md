# Problem Framing

노드 집합이 tick 기반으로 움직이는 동기 시뮬레이터 안에서 Raft 선거와 로그 복제를 재현한다. 목표는 안전성과 직관을 보는 것이지 production-grade persistence나 snapshotting을 구현하는 것은 아니다.

## Success Criteria

- leader election과 단일 leader 보장
- vote rule: up-to-date log를 가진 candidate만 승리
- AppendEntries consistency check
- majority replicated entry에 대한 commit advancement
- higher term 발견 시 leader step-down

## Source Provenance

- 원본 문제: `legacy/distributed-cluster/consensus/problem/README.md`
- 원본 테스트 의미: `legacy/distributed-cluster/consensus/solve/test/raft.test.js`
- 원본 구현 참고: `legacy/distributed-cluster/consensus/solve/solution/raft.js`
