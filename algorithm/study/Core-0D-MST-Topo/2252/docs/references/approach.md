# 접근 정리 — BOJ 2252 (줄 세우기)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `진입차수(indegree) 기반 Kahn 알고리즘으로 위상정렬 수행`
- 공개 구현: `../../python/src/solution.py`
- 비교 구현: `../../cpp/src/solution.cpp`
- 정식 검증: `make -C study/Core-0D-MST-Topo/2252/problem test`

## 왜 이 전략인가

- 그래프 전체 구조를 만들거나 순서를 고정하는 규칙을 설명하는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(N+M)`
- 공간 복잡도: `O(N+M)`
- 변수 정의: `N=학생 수, M=비교 관계 수`

## 실수 포인트

- indegree 감소 누락
- 초기 0차수 노드 큐 삽입 누락
- 출력 노드 수 검증 누락
- 테스트는 통과했더라도, BOJ 2252 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- C++ 비교 구현: `../../cpp/src/solution.cpp`
- 빠른 검증: `make -C study/Core-0D-MST-Topo/2252/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
