# Majority Election

leader election의 핵심은 단순히 “가장 먼저 손든 node”가 아니라, 과반이 인정한 node만 authority를 가진다는 점입니다.

## 왜 majority가 필요한가

cluster가 3개 node라면 과반은 2표입니다. 한 node가 혼자 살아 있다고 해서 leader가 되면, 나중에 다른 node들과 다시 만났을 때 서로 다른 authority가 동시에 존재할 수 있습니다.

## 이 프로젝트에서 확인할 질문

- isolated node는 왜 leader가 되면 안 되는가?
- recovered old leader는 왜 higher term heartbeat를 받으면 물러나야 하는가?
- healthy leader 아래에서 follower가 계속 suspect 상태로 남아 있으면 왜 안 되는가?

## full Raft와의 경계

이 단계는 vote와 term만 다룹니다. log up-to-date rule, AppendEntries consistency, commit advancement는 다음이 아니라 이전 `04-raft-lite` 또는 이후 replication lab과 연결해서 읽습니다.
