# 접근 정리 — BOJ 1167 (트리의 지름)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `임의 정점에서 최원점 탐색 후 한 번 더 탐색하는 트리 지름(two-pass)`
- 공개 구현: `../../python/src/solution.py`
- 비교 구현: `../../cpp/src/solution.cpp`
- 정식 검증: `make -C study/Core-0B-Graph-Tree/1167/problem test`

## 왜 이 전략인가

- 트리 구조의 성질을 이용해 탐색과 누적 계산을 재구성하는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(V)`
- 공간 복잡도: `O(V)`
- 변수 정의: `V=정점 수`

## 실수 포인트

- 입력 라인의 -1 종결 처리 누락
- 가중치 누적 대신 간선 수만 세는 실수
- 재방문 체크 누락
- 테스트는 통과했더라도, BOJ 1167 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- C++ 비교 구현: `../../cpp/src/solution.cpp`
- 빠른 검증: `make -C study/Core-0B-Graph-Tree/1167/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
