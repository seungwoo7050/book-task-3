# Distance-Vector Routing 문제 안내

## 이 문서의 역할

이 문서는 `Distance-Vector Routing`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 문제 목표

각 노드가 이웃과 distance vector를 교환하며 자신의 라우팅 테이블을 독립적으로 계산하는 distributed distance-vector 알고리즘을 구현합니다.

## 구현해야 할 동작

### 초기화

- 토폴로지 파일에서 직접 이웃의 링크 비용을 읽습니다.
- 자기 자신까지의 비용은 0, 직접 이웃은 링크 비용, 그 외는 무한대로 초기화합니다.

### Distance Vector 교환

- 각 노드는 자신의 distance vector를 직접 이웃에게 보냅니다.
- 이웃의 vector를 받으면 `D_x(y) = min_v{c(x,v) + D_v(y)}` 식으로 갱신합니다.
- 변화가 생기면 이웃에게 다시 알립니다.

### 수렴 판정

- 더 이상 어떤 노드의 distance vector도 변하지 않으면 종료합니다.
- 최종 라우팅 테이블과 next hop을 출력합니다.

### 선택 확장

- 원하면 링크 비용 변동이나 `poisoned reverse`를 추가 실험으로 다룰 수 있습니다.

## 제공 자료와 실행 환경

- 토폴로지 파일: `data/topology.json`, `data/topology_5node.json`
- starter code: `code/dv_skeleton.py`
- 검증 스크립트: `script/test_routing.sh`

## 제약과 해석 기준

- Python 3 표준 라이브러리만 사용합니다.
- 각 노드는 자신의 링크 비용과 받은 vector만 사용해야 합니다.
- 임의의 토폴로지에서 동작해야 합니다.

## 성공 기준

| 항목 | 내용 |
| :--- | :--- |
| Bellman-Ford 적용 | DV update 식을 올바르게 구현합니다. |
| 수렴 | 최단 경로로 수렴합니다. |
| 분산성 | 각 노드가 지역 정보만으로 계산합니다. |
| 출력 | 최종 라우팅 테이블과 next hop을 명확히 보여 줍니다. |
| 확장 가능성 | 링크 변화나 `poisoned reverse`를 덧붙일 여지가 남아 있습니다. |
| 코드 품질 | 읽기 쉬운 구조와 테스트를 유지합니다. |

## 출력 예시

```text
=== Iteration 0 (Initial) ===
Node x: {x: 0, y: 2, z: 7}
...
=== Converged after 2 iterations ===
Final Routing Tables:
  Node x: to y cost 2 via y | to z cost 3 via y
```
