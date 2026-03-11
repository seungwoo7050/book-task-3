# 회고

## 이번 단계에서 명확해진 것
- quorum commit과 follower convergence는 다른 질문이라서, 테스트도 따로 보는 편이 더 정확합니다.
- retry가 있으려면 duplicate handling이 먼저 안전해야 합니다.

## 아직 단순화한 부분
- ack drop과 out-of-order delivery는 없습니다.
- disk persistence와 restart recovery도 없습니다.
- term이나 vote와 연결된 safety rule도 없습니다.

## 다음에 확장한다면
- snapshotting과 persistent log를 붙여 recovery path까지 이어 갈 수 있습니다.
- chaos script와 시각화 trace를 붙이면 학습용 observability 프로젝트로 확장할 수 있습니다.
