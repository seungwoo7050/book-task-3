# routing 문제지

## 왜 중요한가

이 문서는 Distance-Vector Routing를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 목표

시작 위치의 구현을 완성해 Bellman-Ford 적용: DV update 식을 올바르게 구현합니다, 수렴: 최단 경로로 수렴합니다, 분산성: 각 노드가 지역 정보만으로 계산합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/04-Network-Diagnostics-and-Routing/routing/problem/code/dv_skeleton.py`
- `../study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py`
- `../study/04-Network-Diagnostics-and-Routing/routing/problem/script/test_routing.sh`
- `../study/04-Network-Diagnostics-and-Routing/routing/python/tests/test_dv_routing.py`
- `../study/04-Network-Diagnostics-and-Routing/routing/problem/data/topology.json`
- `../study/04-Network-Diagnostics-and-Routing/routing/problem/data/topology_5node.json`
- `../study/04-Network-Diagnostics-and-Routing/routing/problem/Makefile`

## starter code / 입력 계약

- ../study/04-Network-Diagnostics-and-Routing/routing/problem/code/dv_skeleton.py에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- Bellman-Ford 적용: DV update 식을 올바르게 구현합니다.
- 수렴: 최단 경로로 수렴합니다.
- 분산성: 각 노드가 지역 정보만으로 계산합니다.
- 출력: 최종 라우팅 테이블과 next hop을 명확히 보여 줍니다.
- 확장 가능성: 링크 변화나 poisoned reverse를 덧붙일 여지가 남아 있습니다.
- 코드 품질: 읽기 쉬운 구조와 테스트를 유지합니다.

## 제외 범위

- `../study/04-Network-Diagnostics-and-Routing/routing/problem/code/dv_skeleton.py` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/04-Network-Diagnostics-and-Routing/routing/problem/script/test_routing.sh` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- `../study/04-Network-Diagnostics-and-Routing/routing/problem/code/dv_skeleton.py`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `load_topology`와 `DVNode`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `_make_topo_file`와 `TestLoadTopology`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/04-Network-Diagnostics-and-Routing/routing/problem/script/test_routing.sh` 등 fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/network-atda/study/04-Network-Diagnostics-and-Routing/routing/problem test
```

- `routing`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`routing_answer.md`](routing_answer.md)에서 확인한다.
