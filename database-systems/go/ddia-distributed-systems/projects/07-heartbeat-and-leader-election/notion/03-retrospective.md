# 회고

## 이번 단계에서 명확해진 것
- failure detector는 정확한 진실 판정기가 아니라 leader 교체를 시작하게 만드는 신호입니다.
- majority rule이 있어야 isolated node가 authority를 주장하지 못합니다.

## 아직 단순화한 부분
- randomized timeout과 network partition은 없습니다.
- vote request의 log up-to-date rule도 없습니다.
- heartbeat loss가 비대칭으로 일어나는 경우도 다루지 않습니다.

## 다음에 확장한다면
- pre-vote와 randomized timeout을 넣어 split vote를 더 현실적으로 다룰 수 있습니다.
- replication retry와 commit index를 붙여 실제 write path와 연결할 수 있습니다.
