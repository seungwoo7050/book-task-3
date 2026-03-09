# Static Topology

이 capstone은 membership change 자체를 다루지 않는다. shard 집합과 각 shard의 leader/follower 배치는 초기화 시점에 고정된다.

정적 토폴로지를 택한 이유는 저장 엔진, 라우팅, 복제를 한 번에 연결하는 첫 통합 단계에서 reconfiguration 복잡도를 배제하기 위해서다. 이후 동적 membership은 별도 프로젝트로 확장할 수 있다.
