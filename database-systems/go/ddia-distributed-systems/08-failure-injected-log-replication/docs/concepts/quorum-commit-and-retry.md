# Quorum Commit and Retry

leader는 모든 follower가 다 따라올 때까지 기다리지 않고, quorum ack가 모이면 commit index를 올립니다. 하지만 뒤처진 follower는 retry를 통해 결국 따라잡아야 합니다.

## 이 프로젝트의 규칙

- cluster는 leader 1개와 follower 2개로 고정됩니다.
- leader 자신은 항상 1표로 계산됩니다.
- follower별 `nextIndex`를 유지해 아직 못 받은 entry만 다시 보냅니다.
- commit index는 majority replicated entry까지만 전진합니다.

## 왜 commit과 convergence를 분리해서 봐야 하는가

quorum commit은 “이 write를 성공으로 인정할 수 있는가”를 묻습니다. convergence는 “뒤처진 follower가 결국 동일한 상태에 도달하는가”를 묻습니다. 이 둘을 섞으면 follower lag와 retry 의미가 흐려집니다.

## duplicate delivery에서 꼭 확인할 것

같은 entry가 두 번 와도 log length와 state mutation은 한 번만 증가해야 합니다. 그렇지 않으면 retry 자체가 시스템을 망가뜨립니다.
