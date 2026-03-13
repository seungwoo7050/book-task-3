# Distance-Vector Routing structure guide

## 이 글의 중심 질문

- distance-vector가 topology 입력에서 최종 routing table로 수렴하는 과정을 어떻게 보여 줬는가?
- 한 줄 답: Bellman-Ford 식을 분산 라우팅 테이블 갱신으로 옮기는 시뮬레이션 과제입니다.

## 권장 흐름

1. 실행 표면과 entrypoint를 먼저 고정하기
2. Bellman-Ford 갱신을 node 단위 상태 변화로 읽기
3. 테스트와 남은 범위를 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test`
- `study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py`의 `def receive_dv`
- `study/04-Network-Diagnostics-and-Routing/routing/python/tests/test_dv_routing.py`의 `def test_convergence`

## 리라이트 주의점

- `Distance-Vector Routing`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 poisoned reverse는 구현하지 않았습니다. 같은 남은 경계를 사람 말로 다시 정리한다.
