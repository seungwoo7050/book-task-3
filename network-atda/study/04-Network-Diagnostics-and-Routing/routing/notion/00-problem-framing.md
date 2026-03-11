# 00 문제 프레이밍

## 프로젝트 정의
- 프로젝트: `Distance-Vector Routing`
- 상태: `verified`
- 기준 검증: `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test`
- 문제 배경: Bellman-Ford 식을 코드로 옮겨, 각 노드가 이웃 정보만으로 라우팅 테이블에 수렴하는 과정을 시뮬레이션하는 프로젝트다.

## 이번 범위
- JSON 토폴로지를 읽어 노드와 링크 비용을 초기화한다.
- 각 노드는 자신의 DV와 이웃에게 받은 DV만으로 경로 비용을 갱신한다.
- 수렴 후 목적지별 비용과 next-hop을 출력한다.

## 제약과 전제
- 시뮬레이션은 이해와 디버깅을 위해 2-phase synchronous 방식으로 돌린다.
- 노드는 전체 토폴로지를 직접 보지 않고 이웃 DV만 사용해야 한다.
- 무한 반복을 피하려고 최대 iteration 제한을 둔다.

## 성공 기준
- 3노드, 5노드 토폴로지 모두에서 최단 경로 비용과 next-hop이 맞게 나온다.
- 변화가 없으면 수렴으로 판단하고 루프를 종료한다.
- `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test`가 통과한다.

## 공개 문서
- [`../README.md`](../README.md)
- [`../problem/README.md`](../problem/README.md)
- [`../python/README.md`](../python/README.md)
- [`../docs/README.md`](../docs/README.md)
- [`../docs/references/README.md`](../docs/references/README.md)

## 이번에 일부러 제외한 것
- split horizon, poison reverse, 비동기 메시지 모델은 구현하지 않는다.
- 실제 라우터 데몬이 아니라 교육용 시뮬레이터다.
