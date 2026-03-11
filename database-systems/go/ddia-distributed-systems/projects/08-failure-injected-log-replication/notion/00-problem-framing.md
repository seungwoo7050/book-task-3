# 문제 프레이밍

## 왜 이 프로젝트를 하는가
leader election만 끝나면 authority는 정해졌지만, 실제 write path가 failure를 어떻게 견디는지는 아직 비어 있습니다. 이 단계는 retry, duplicate handling, quorum commit을 작은 replication harness로 고정합니다.

## 커리큘럼 안에서의 위치
- 트랙: DDIA Distributed Systems / Go
- 이전 단계: 07 Heartbeat and Leader Election
- 다음 단계: 현재 트랙의 마지막 심화 슬롯
- 지금 답하려는 질문: follower 일부가 실패하거나 느려져도 write를 어떻게 commit하고, 나중에 어떻게 따라잡게 할 것인가?

## 이번 구현에서 성공으로 보는 것
- dropped append는 retry로 수렴해야 합니다.
- duplicate append는 idempotent하게 무시돼야 합니다.
- paused follower가 있어도 quorum commit은 가능해야 합니다.
- resumed follower는 catch-up 뒤 leader와 같은 상태에 도달해야 합니다.
