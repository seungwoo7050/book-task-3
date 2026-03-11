# 문제 프레이밍

## 왜 이 프로젝트를 하는가
quorum consistency만으로는 누가 write authority를 가져야 하는지 설명할 수 없습니다. 이 단계는 failure detector와 election만 떼어 내서 authority 교체를 먼저 고정합니다.

## 커리큘럼 안에서의 위치
- 트랙: DDIA Distributed Systems / Go
- 이전 단계: 06 Quorum and Consistency
- 다음 단계: 08 Failure-Injected Log Replication
- 지금 답하려는 질문: leader가 죽었을 수 있을 때, 어떤 규칙으로 단 하나의 새 leader를 고를 것인가?

## 이번 구현에서 성공으로 보는 것
- healthy leader 아래에서 follower suspicion이 계속 쌓이지 않아야 합니다.
- leader failure 후 majority vote로 새 leader가 나와야 합니다.
- isolated node는 leader가 되면 안 됩니다.
- recovered old leader는 higher term을 보고 follower로 돌아가야 합니다.
