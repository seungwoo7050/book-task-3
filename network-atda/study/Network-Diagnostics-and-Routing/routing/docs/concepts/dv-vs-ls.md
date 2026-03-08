# Distance-Vector vs Link-State 라우팅 비교

## 개요

인터넷 라우팅 프로토콜은 크게 두 가지 접근 방식으로 나뉜다:
- **Distance-Vector (DV)**: 이웃에게 자신의 거리 벡터를 전파 (Bellman-Ford 기반)
- **Link-State (LS)**: 전체 네트워크에 자신의 링크 상태를 전파 (Dijkstra 기반)

과제에서 구현한 DV 알고리즘의 특성과 LS와의 차이를 분석한다.

## 비교 표

| 특성 | Distance-Vector (DV) | Link-State (LS) |
| :--- | :--- | :--- |
| 알고리즘 | Bellman-Ford | Dijkstra |
| 정보 교환 대상 | 이웃만 (neighbor) | 전체 네트워크 (flooding) |
| 교환하는 정보 | 거리 벡터 (모든 목적지까지 비용) | 링크 상태 (직접 연결된 링크 비용) |
| 네트워크 지식 | 부분적 (이웃의 DV만 앎) | 전체 토폴로지 |
| 테이블 계산 | 분산적 (각 노드 독립) | 집중적 (전체 토폴로지로 계산) |
| 수렴 속도 | 느림 (최대 $|V|-1$ 반복) | 빠름 (1회 flooding 후 계산) |
| 루프 문제 | Count-to-infinity 가능 | 없음 |
| 메시지 복잡도 | $O(|V| \times |E|)$ per round | $O(|V| \times |E|)$ flooding |
| 실제 프로토콜 | RIP, BGP (path-vector) | OSPF, IS-IS |

## DV 알고리즘 (과제 구현)

### 동작 원리

$$D_x(y) = \min_v \{ c(x,v) + D_v(y) \}$$

각 노드는:
1. 자신의 거리 벡터를 이웃에게 전송
2. 이웃의 거리 벡터를 수신하면 Bellman-Ford 방정식으로 업데이트
3. 변경이 있으면 다시 이웃에게 전파
4. 수렴할 때까지 반복

### 장점

- **단순한 구현**: 각 노드가 이웃 정보만 관리
- **낮은 메모리**: 전체 토폴로지를 저장할 필요 없음
- **분산 처리**: 중앙 집중식 계산 불필요

### 단점

- **느린 수렴**: 정보가 hop-by-hop으로 전파
- **Count-to-infinity**: 링크 비용 증가 시 수렴이 매우 느릴 수 있음
- **라우팅 루프**: 수렴 전에 패킷이 루프를 돌 수 있음

## LS 알고리즘 (참조)

### 동작 원리

1. 각 노드가 자신의 링크 상태(직접 연결된 링크와 비용)를 파악
2. **Flooding**으로 전체 네트워크에 링크 상태를 전파
3. 모든 노드가 동일한 토폴로지 데이터베이스를 구축
4. Dijkstra 알고리즘으로 최단 경로 트리를 계산

### Dijkstra 알고리즘

```python
def dijkstra(graph, source):
    dist = {v: INF for v in graph}
    dist[source] = 0
    visited = set()
    
    while len(visited) < len(graph):
        u = min((v for v in graph if v not in visited), key=lambda v: dist[v])
        visited.add(u)
        for v, cost in graph[u].items():
            if dist[u] + cost < dist[v]:
                dist[v] = dist[u] + cost
```

시간 복잡도: $O(|V|^2)$ (힙 사용 시 $O((|V|+|E|) \log |V|)$)

## 요약: 핵심 차이

### 정보의 범위

```
DV: 이웃에게만 공유 → "나는 목적지까지 비용이 얼마다"
                        (경로의 세부 사항은 공유하지 않음)

LS: 전체 네트워크에 flooding → "나는 이런 링크들이 연결되어 있다"
                                 (각 노드가 전체 그래프를 구성)
```

### 실제 프로토콜에서의 사용

| 프로토콜 | 유형 | 사용 범위 |
| :--- | :--- | :--- |
| **RIP** | DV | 소규모 네트워크 (최대 15 hop) |
| **OSPF** | LS | 대규모 기업 네트워크 (area 기반 계층화) |
| **IS-IS** | LS | ISP 백본 네트워크 |
| **BGP** | Path-Vector (DV 변형) | 인터넷 AS 간 라우팅 |

### BGP: DV의 진화

BGP(Border Gateway Protocol)는 DV의 변형인 **Path-Vector** 방식을 사용한다:
- 거리(비용) 대신 **경로(AS 리스트)**를 전파
- 경로에 자신의 AS가 포함되어 있으면 폐기 → 루프 방지
- 정책 기반 라우팅 지원 (비용 최소화가 아닌 정책 우선)

## 과제에서의 교훈

DV 알고리즘을 직접 구현하면서:
1. **Bellman-Ford의 분산적 특성**: 각 노드가 로컬 정보만으로 전역 최적해에 도달
2. **수렴 과정의 시각화**: 매 반복마다 거리 벡터가 어떻게 변하는지 관찰
3. **Count-to-infinity의 실체**: 왜 poisoned reverse가 필요한지 직접 체험
4. **동기 vs 비동기**: 동기식 시뮬레이션이 디버깅에 용이하지만, 실제는 비동기적
