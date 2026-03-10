# 회고

## 이번 단계에서 명확해진 것
- RPC의 핵심은 fancy framework가 아니라 frame boundary와 request-response matching이라는 점이 분명해졌습니다.
- 상위 분산 알고리즘 전에 transport 실패를 명확히 모델링해야 나중에 디버깅이 쉬워집니다.
- 동시성 문제는 protocol 설계에서 correlation id 하나로도 상당 부분 정리됩니다.

## 아직 단순화한 부분
- 실제 네트워크 retry, backoff, TLS는 없습니다.
- single connection 중심 구현이라 connection pool이나 streaming은 다루지 않습니다.

## 다음에 확장한다면
- streaming RPC를 추가해 frame decoder 재사용 범위를 넓힐 수 있습니다.
- connection pool과 retry budget을 넣어 운영에 가까운 failure handling을 실험할 수 있습니다.

## `02 Leader-Follower Replication`로 넘길 질문
- transport가 마련되었을 때 leader는 follower에게 어떤 단위의 log를 보내야 하는가?
- 동시 요청이 많아진 상태에서 replication lag를 어떻게 드러낼 것인가?
