# Election Cycle

follower는 heartbeat를 받지 못하면 candidate가 되고 term을 올린 뒤 RequestVote를 보낸다. 과반을 얻으면 leader가 되고, 그렇지 못하면 다시 follower/candidate 사이를 오간다.

이 프로젝트는 flake를 줄이기 위해 랜덤 대신 노드별 고정 election timeout을 사용한다. 덕분에 테스트는 결정적이지만, 의미는 그대로 유지된다.
