# Virtual Nodes

물리 node마다 ring에 하나의 점만 두면 hash 편차 때문에 분산이 쉽게 치우친다. virtual node는 물리 node 하나를 ring 위의 여러 점으로 쪼개서 더 고르게 분산되도록 만든다.

이 프로젝트는 `nodeID#v<index>`를 해시해서 ring entry를 만들고, lookup은 key 해시보다 크거나 같은 첫 entry를 찾는다. 끝을 넘으면 0번 entry로 wrap 한다.
