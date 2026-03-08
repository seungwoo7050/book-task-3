# Problem Framing

ring 위에 virtual node를 배치해서 key를 물리 node로 라우팅하고, node membership이 바뀔 때 전체 key 중 일부만 움직이도록 만든다.

## Success Criteria

- deterministic consistent hash ring
- batch routing
- add/remove 이후 reassignment count 계산
- empty ring / single node / multi-node 분산 검증

## Source Provenance

- 원본 문제: `legacy/distributed-cluster/sharding/problem/README.md`
- 원본 테스트 의미: `legacy/distributed-cluster/sharding/solve/test/sharding.test.js`
- 원본 구현 참고: `legacy/distributed-cluster/sharding/solve/solution/sharding.js`
