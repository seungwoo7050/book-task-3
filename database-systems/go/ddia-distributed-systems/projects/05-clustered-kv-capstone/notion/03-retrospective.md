# 회고

## 왜 이 프로젝트가 재현성에 특히 좋은가
- 앞선 네 프로젝트의 역할이 하나의 write path로 연결됩니다.
- topology가 정적이라 학습자가 state explosion 없이 흐름을 끝까지 따라갈 수 있습니다.
- test 3개와 demo 1개만으로 route, lag, recovery를 모두 확인할 수 있습니다.

## 이번 단계에서 명확해진 것
- 분산 시스템 학습에서 가장 중요한 것은 기능 수가 아니라 경계 연결입니다.
- routing, replication, durability는 따로 배울 때보다 마지막에 묶어 볼 때 이해가 더 깊어집니다.
- static topology는 단순화이지만, 첫 통합 단계에서는 오히려 장점입니다.

## 아직 단순화한 부분
- leader authority는 정적으로 가정합니다. consensus가 없습니다.
- membership change, rebalancing, anti-entropy는 없습니다.
- 실제 네트워크 대신 in-process 호출을 쓰므로 RPC failure는 여기서 다루지 않습니다.

## 다음에 확장한다면
- `04-raft-lite`를 실제 write path에 연결해 leader election을 붙일 수 있습니다.
- shard migration과 membership change를 넣어 static topology 제약을 깨 볼 수 있습니다.
- observability와 failure injection을 넣으면 포트폴리오 가치가 크게 올라갑니다.

## 다음 단계로 넘길 질문
- 이 구조를 공개용 포트폴리오 레포로 키운다면 어떤 메트릭과 로그를 먼저 보여 줄 것인가?
- `Cluster`와 `Store` 경계를 유지한 채 동적 topology를 넣으려면 어느 인터페이스부터 바꿔야 할까?
