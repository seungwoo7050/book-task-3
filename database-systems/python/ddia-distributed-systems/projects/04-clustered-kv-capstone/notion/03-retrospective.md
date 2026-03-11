# 회고

## 이번 단계에서 명확해진 것
- 분산 저장소를 설명할 때는 routing, replication, durability를 분리해서 만들고 마지막에 합치는 편이 훨씬 이해하기 쉽습니다.
- 정적 topology만으로도 end-to-end write/read/restart 흐름은 충분히 설득력 있게 보여 줄 수 있습니다.
- 캡스톤의 가치는 기능 수보다 “여러 학습 조각이 한 파이프라인으로 연결되는가”에 있다는 점이 분명해졌습니다.

## 아직 단순화한 부분
- 자동 failover와 consensus가 없어 leader authority는 정적으로 가정합니다.
- cross-shard transaction, rebalancing migration, anti-entropy는 빠져 있습니다.

## 다음에 확장한다면
- Raft 기반 leader election을 붙여 authority를 동적으로 만들 수 있습니다.
- rebalancing과 membership change를 넣어 static topology 제약을 넘어갈 수 있습니다.

## 다음 단계로 넘길 질문
- 이 캡스톤을 포트폴리오 공개용으로 바꾼다면 어떤 observability와 failure injection을 추가할 것인가?
- 정적 topology를 깨고도 같은 코드 구조를 유지하려면 어떤 인터페이스를 먼저 바꿔야 하는가?
