# Distance-Vector Routing 개발 타임라인

현재 구현을 다시 읽으면 이 lab의 흐름은 Bellman-Ford 식을 코드로 번역하는 한 번의 점프가 아니다. 먼저 topology를 node-local view로 바꾸고, 그 위에 distance vector state를 올리고, 마지막에 synchronous round로 수렴을 관찰하는 순서다. 전환점은 네 번이다.

## 1. topology loader가 centralized graph를 각 node의 local neighborhood로 자른다

`load_topology()`는 JSON edge list를 읽어 양방향 adjacency dict로 바꾼다. 여기서 이미 viewpoint가 바뀐다. 전체 graph는 여전히 파일 안에 있지만, 이후 각 node는 자기 neighbor와 link cost만 직접 들고 시작한다.

즉 이 첫 단계는 graph problem을 distributed routing problem으로 번역하는 준비 단계다.

## 2. 초기 DV는 self, direct neighbor, unknown을 세 단계로 나눈다

`DVNode.__init__()`는 self cost `0`, direct neighbor cost `link cost`, 나머지 `INF`로 초기화한다. 이 구조 덕분에 simulation iteration 0 출력만 봐도 "직접 아는 것"과 "아직 모르는 것"이 분명히 갈린다.

이 초기 상태가 있어야 이후 neighbor advertisement가 가져온 정보가 얼마나 가치 있었는지 눈에 보인다.

## 3. `receive_dv()`가 Bellman-Ford 식을 neighbor advertisement update로 바꾼다

핵심 전환은 `c(x,v) + D_v(y)`를 모든 neighbor `v`에 대해 비교하는 루프다. `receive_dv()`는 sender 하나의 DV를 받았더라도 전체 destination set을 다시 훑는다. 그리고 더 좋은 path가 보이면 cost와 next hop을 함께 갱신한다.

3-node rerun에서 სწორედ 이 update가 `x -> z` cost를 `7`에서 `3 via y`로 바꿨다. formula가 routing table row로 변하는 장면이 여기에 있다.

## 4. 마지막으로 synchronous 2-phase loop가 convergence를 teaching-simulator 형태로 고정한다

`simulate()`는 먼저 모든 node의 현재 DV snapshot을 `messages`로 저장하고, 그 snapshot만으로 next phase update를 돌린다. 이 2-phase 구조 덕분에 같은 iteration 안에서 방금 바뀐 DV가 곧바로 다시 전파되는 self-feedback을 막는다. rerun output에서도 3-node topology는 2 iterations 후 convergence를 선언하고 final routing table을 출력한다.

결국 이 lab의 마지막 전환점은 shortest path 계산을 static answer로 끝내지 않고, "여러 node가 round를 거치며 점차 같은 진실에 수렴하는 과정"으로 보여 주는 데 있다.

## 지금 남는 한계

현재 model은 intentionally 단순하다. async delay, poison reverse, count-to-infinity mitigation, link failure recovery는 없다. 그래도 neighbor DV exchange와 convergence concept를 코드 수준으로 옮기는 목적만큼은 분명히 달성한다.
