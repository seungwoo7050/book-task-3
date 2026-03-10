# 회고

## 이번 단계에서 명확해진 것
- replication의 기본은 “어떤 변경분부터 다시 보낼 것인가”를 명확히 하는 데 있습니다.
- idempotence를 먼저 잡아야 retry와 reconnect를 안전하게 이야기할 수 있습니다.
- leader-follower 모델만으로도 durability와 catch-up의 핵심 감각을 익힐 수 있습니다.

## 아직 단순화한 부분
- leader 권한 교체나 split-brain 방지는 아직 다루지 않습니다.
- quorum commit과 durability acknowledgement도 없습니다.

## 다음에 확장한다면
- batch replication과 lag metrics를 추가해 운영 감각을 더할 수 있습니다.
- leader election을 붙여 replication만으로는 해결되지 않는 문제를 보여 줄 수 있습니다.

## `03 Shard Routing`로 넘길 질문
- leader가 여러 shard를 가질 때 key는 어느 그룹으로 보내야 하는가?
- leader 자체가 죽으면 누가 새 leader가 되는가?
