# arenaserv 개념 노트

## 먼저 잡아야 할 질문

- authoritative game server에서 transport보다 session continuity가 더 중요한 순간은 언제인가
- reconnect는 왜 token 발급으로 끝나지 않고 snapshot regeneration까지 포함해야 하는가
- room queue와 match loop를 분리하지 않으면 어떤 종류의 버그가 섞이는가

## 코드 읽기 포인트

- [../cpp/src/Server.cpp](../cpp/src/Server.cpp): 네트워크와 세션 흐름
- [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp): simulation과 판정
- [../cpp/tests/test_arenaserv.py](../cpp/tests/test_arenaserv.py): multi-client 검증

## 흔한 오해

- authoritative game server는 physics가 복잡해야만 학습 가치가 있는 것이 아니다.
- reconnect는 부가 기능이 아니라 상태 연속성 설계의 핵심이다.
- 데모 영상만 있으면 충분한 것이 아니라, 어떤 테스트로 무엇을 검증했는지 같이 남겨야 포트폴리오가 강해진다.

## 다음 단계로 이어지는 지점

이 저장소 안에서는 `arenaserv`가 게임 서버 축의 마지막 capstone이다. 이후 확장은 prediction, rollback, shard, metrics 같은 운영 주제로 나누어 가는 편이 좋다.
