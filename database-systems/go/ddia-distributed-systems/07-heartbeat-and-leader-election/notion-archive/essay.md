# Heartbeat and Leader Election 에세이

분산 시스템에서 replication을 설명한 뒤에도 아직 풀리지 않는 질문이 하나 남는다. “그래서 누가 write authority를 가지는가?”다.  
quorum은 최신값을 읽는 조건을 설명하지만, 권한 교체를 설명해 주지는 않는다. heartbeat와 leader election은 바로 그 빈칸을 메운다.

## failure detector는 진실 판정기가 아니다

많은 입문자가 failure detector를 “죽었는지 아닌지 정확히 알려 주는 장치”처럼 이해한다. 실제로는 그렇지 않다.  
failure detector는 보통 “지금까지 본 신호로는 죽었을 가능성이 높다”는 suspicion을 만든다.

이 프로젝트가 `Suspected` 플래그를 따로 두는 이유도 여기 있다.

- 먼저 silence가 쌓인다.
- 그다음 suspicion이 생긴다.
- 마지막으로 election이 시작된다.

이 순서를 분리하면 authority 교체가 한 번에 튀어나오지 않고, 장애 신호가 먼저 보인다.

## 왜 majority 없는 self-promotion을 막아야 하는가

node 하나가 고립됐다고 해서 leader가 되어 버리면 split-brain이 생긴다.  
예를 들어 3-node cluster에서 `node-1`만 살아 있다고 착각해 leader가 되면, 나중에 `node-2`, `node-3`와 다시 만났을 때 서로 다른 authority가 동시에 존재할 수 있다.

그래서 election의 핵심은 “누가 먼저 손들었는가”가 아니라 “누가 과반의 인정을 받았는가”다.

## term은 왜 필요한가

term은 authority의 세대를 구분하는 숫자다.  
leader가 바뀌면 term이 올라가고, 더 낮은 term을 가진 old leader는 더 이상 권한을 주장할 수 없다.

이 규칙이 없으면 복구된 old leader가 heartbeat를 다시 뿌리며 stale authority를 주장할 수 있다.  
그래서 higher term heartbeat를 받은 node는 즉시 step-down해야 한다.

## 왜 full Raft보다 작게 쪼갰는가

Raft-lite 하나만 두면 vote rule, log up-to-date rule, AppendEntries consistency, commit advancement가 한 파일에 섞여 보인다. 그건 전체 흐름을 이해하는 데는 좋지만, leader authority 문제만 따로 보고 싶을 때는 오히려 부담이다.

이 프로젝트는 일부러 아래만 남겼다.

- heartbeat
- suspicion
- majority vote
- higher term step-down

로그 복제는 뺐다. commit rule도 뺐다. 그 덕분에 “누가 leader인가”만 선명하게 남는다.

## 트랙 안에서의 역할

이 프로젝트는 `06-quorum-and-consistency`와 `08-failure-injected-log-replication` 사이에 놓여 있다.

- 06은 “무엇을 최신이라고 읽는가”를 묻는다.
- 07은 “누가 authority를 가지는가”를 묻는다.
- 08은 “authority가 있다고 가정할 때 partial failure 뒤에 어떻게 수렴하는가”를 묻는다.

같은 분산 시스템이라도 질문이 다르면 프로젝트를 쪼개는 편이 더 잘 보인다.

## 다시 구현할 때 기억할 것

- suspicion과 election을 같은 tick으로 합치지 말 것
- isolated node가 leader가 되지 못하게 majority 계산을 먼저 테스트로 고정할 것
- recovered old leader는 반드시 higher term에 밀려 follower가 되게 할 것

이 세 규칙만 지켜도 작은 코드로 split-brain 방지의 핵심을 보여 줄 수 있다.
