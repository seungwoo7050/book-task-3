# 회고

## 이번 단계에서 명확해진 것
- “최신 값 하나” 모델에서 transaction isolation으로 넘어갈 때 가장 중요한 변화는 visibility rule이라는 점이 분명해졌습니다.
- write conflict는 write 시점이 아니라 commit 시점에 드러낼 수도 있습니다.
- GC는 storage 최적화이기 전에 visibility를 깨지 않도록 경계 조건을 정확히 잡는 작업입니다.

## 아직 단순화한 부분
- secondary index나 range query가 없어 phantom 문제는 설명하지 못합니다.
- disk persistence가 없어 version chain은 메모리 모델에 머뭅니다.

## 다음에 확장한다면
- timestamp oracle이나 lock table을 추가해 다른 isolation level과 비교할 수 있습니다.
- range scan과 index를 붙여 MVCC가 query layer까지 어떻게 번지는지 확장할 수 있습니다.

## 다음 단계로 넘길 질문
- 네트워크를 넘어가면 이 visibility rule은 RPC나 replication과 어떻게 만나는가?
- 분산 환경에서 leader와 follower가 각자 어떤 snapshot을 보여야 일관성이 맞을까?
