# Distance-Vector Routing — 분산 알고리즘으로 경로를 찾다

## 패킷이 가는 길은 누가 정하나

Traceroute로 패킷의 경로를 추적해봤다. 그런데 그 경로는 누가, 어떻게 결정하는 걸까?

인터넷의 모든 라우터는 **라우팅 테이블**을 갖고 있다. "목적지 X로 가려면 이웃 Y에게 보내라"는 규칙의 모음이다. 이 테이블을 사람이 수동으로 채울 수도 있지만, 라우터가 수백만 대이고 토폴로지가 수시로 바뀌는 인터넷에서는 **자동으로 계산**해야 한다.

Distance-Vector(DV) 알고리즘은 그 방법 중 하나다. 각 라우터가 이웃에게 "나는 어디까지 얼마에 갈 수 있다"는 정보를 공유하고, 이걸 바탕으로 각자의 라우팅 테이블을 갱신한다.

## Bellman-Ford 수식: 한 줄로 된 핵심

DV 알고리즘의 핵심은 이 한 줄이다:

$$D_x(y) = \min_v\{c(x,v) + D_v(y)\}$$

"노드 x에서 노드 y까지의 최소 비용은, x의 모든 이웃 v에 대해 (x→v 링크 비용 + v에서 y까지의 비용) 중 최솟값이다."

교과서에서 이 수식을 처음 봤을 때는 그냥 수학이었다. 이걸 코드로 바꾸고, 실제로 반복 수렴시키면서 "아, 각 노드가 이웃의 정보만으로 전역 최단 경로를 알 수 있구나"라는 걸 체감했다.

## 토폴로지를 JSON으로 정의

시뮬레이션에 사용할 네트워크 토폴로지는 JSON 파일로 제공된다:

```json
{
  "nodes": ["x", "y", "z"],
  "edges": [
    {"from": "x", "to": "y", "cost": 2},
    {"from": "x", "to": "z", "cost": 7},
    {"from": "y", "to": "z", "cost": 1}
  ]
}
```

x→z의 직접 비용은 7이지만, x→y→z 경로는 2+1=3으로 더 짧다. DV 알고리즘은 이걸 자동으로 발견해야 한다.

## DVNode: 각 노드가 아는 것

각 노드는 다음만 안다:
1. **자신의 이웃과 링크 비용**: `{y: 2, z: 7}` (x의 경우)
2. **이웃에게 받은 distance vector**: y가 "나는 z까지 1에 갈 수 있어"라고 알려줌

전체 토폴로지는 모른다. x는 y와 z가 직접 연결되어 있는지조차 모른다. 오직 이웃의 DV를 통해 간접적으로 추론할 뿐이다. 이것이 "분산 알고리즘"의 핵심이다.

노드를 초기화할 때:
- 자기 자신까지의 비용은 0
- 이웃까지의 비용은 링크 비용
- 나머지는 무한대(∞)

## 2-Phase Synchronous 시뮬레이션

실제 인터넷에서는 각 노드가 비동기적으로 DV를 교환한다. 하지만 이 과제에서는 이해와 디버깅을 위해 **동기식 시뮬레이션**을 구현했다:

1. **Phase 1**: 모든 노드가 현재 DV를 수집
2. **Phase 2**: 각 노드가 이웃의 DV를 받아 Bellman-Ford 업데이트 실행

이걸 DV가 더 이상 변하지 않을 때까지 반복한다.

```python
for iteration in range(1, max_iterations + 1):
    # Phase 1: 모든 DV 수집
    messages = {name: node.get_dv() for name, node in dv_nodes.items()}
    
    # Phase 2: 이웃 DV 수신 및 업데이트
    any_changed = False
    for name, node in dv_nodes.items():
        for neighbor in node.neighbors:
            if node.receive_dv(neighbor, messages[neighbor]):
                any_changed = True
    
    if not any_changed:
        print(f"Converged after {iteration} iterations")
        break
```

## 수렴 과정을 눈으로 보다

3노드 토폴로지(x, y, z)의 수렴 과정을 출력하면:

```
=== Iteration 0 (Initial) ===
Node x: {x: 0, y: 2, z: 7}
Node y: {x: 2, y: 0, z: 1}
Node z: {x: 7, y: 1, z: 0}

=== Iteration 1 ===
Node x: {x: 0, y: 2, z: 3}   ← z 비용이 7→3으로 바뀜 (y 경유)
Node z: {x: 3, y: 1, z: 0}   ← x 비용이 7→3으로 바뀜 (y 경유)

=== Converged after 2 iterations ===
```

x가 z까지 2+1=3으로 갈 수 있음을 y의 DV를 통해 발견한다. "이웃에게 물어보면 더 나은 경로가 있을 수 있다"는 원리가 코드로 동작하는 걸 볼 수 있었다.

## next-hop: "어디로 보내야 하나"

비용만 아는 것으로는 충분하지 않다. "z까지 비용 3"이라는 건 알겠는데, **첫 번째 패킷을 어느 이웃에게 보내야** 비용 3으로 갈 수 있는가?

그래서 라우팅 테이블은 `(destination, cost, next_hop)` 세 값을 관리한다:

```
Node x: to y cost 2 via y | to z cost 3 via y
Node y: to x cost 2 via x | to z cost 1 via z
Node z: to x cost 3 via y | to y cost 1 via y
```

x에서 z로 가려면 y에게 보내라. y는 z에게 직접 보낸다. 이게 실제 IP 라우터의 포워딩 테이블과 같은 구조다.

## deep copy의 중요성

시뮬레이션에서 한 가지 실수할 뻔한 부분이 있었다. 노드 A가 자신의 DV를 이웃 B에게 보낼 때, **참조가 아니라 복사본**을 보내야 한다. 안 그러면 B가 받은 DV를 수정했을 때 A의 원본까지 바뀌어버린다.

```python
def get_dv(self) -> dict[str, float]:
    return copy.deepcopy(self.distance_vector)
```

실제 네트워크에서 DV는 패킷으로 전송되니 별도의 복사본이 자연스럽게 만들어진다. 하지만 하나의 프로세스 안에서 시뮬레이션할 때는 이 메모리 공유 문제를 명시적으로 처리해야 했다.

## 이 과제에서 가져간 것

"분산 시스템에서 지역 정보만으로 어떻게 전역 최적해에 도달하는가"를 직접 구현한 과제였다. 각 노드는 전체 네트워크를 모르지만, 이웃과 정보를 반복적으로 교환하면 결국 올바른 라우팅 테이블에 수렴한다.

이 경험은 나중에 분산 시스템을 이해하는 제 기반이 됐다. consensus 알고리즘, 결국 일관성(eventual consistency) 같은 개념도 결국 "로컬 정보의 반복 교환으로 전역 상태에 수렴"하는 같은 원리를 공유한다.

---

> **학습 키워드**: Distance-Vector 알고리즘, Bellman-Ford 수식, 동기식 시뮬레이션, 수렴(convergence), next-hop, 라우팅 테이블, deep copy, 분산 알고리즘