# 접근 정리 — BOJ 1753 (최단경로)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `단일 시작점에서 모든 정점까지 Dijkstra 최단거리 계산`
- 공개 구현: `../../python/src/solution.py`
- 비교 구현: `../../cpp/src/solution.cpp`
- 정식 검증: `make -C study/Core-0C-Shortest-Path/1753/problem test`

## 왜 이 전략인가

- 가중치 조건과 그래프 특성에 맞는 최단 경로 알고리즘을 선택하는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O((V+E) log V)`
- 공간 복잡도: `O(V+E)`
- 변수 정의: `V=정점 수, E=간선 수, K=시작 정점`

## 실수 포인트

- INF 출력 문자열 처리 누락
- 1-based 정점 인덱스 오류
- 힙 push 조건 누락
- 테스트는 통과했더라도, BOJ 1753 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- C++ 비교 구현: `../../cpp/src/solution.cpp`
- 빠른 검증: `make -C study/Core-0C-Shortest-Path/1753/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
