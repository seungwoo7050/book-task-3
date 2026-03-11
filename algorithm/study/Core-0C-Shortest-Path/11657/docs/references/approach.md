# 접근 정리 — BOJ 11657 (타임머신)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `N-1회 완화 + 추가 1회 검사로 음수 사이클을 판정하는 Bellman-Ford`
- 공개 구현: `../../python/src/solution.py`
- 비교 구현: `../../cpp/src/solution.cpp`
- 정식 검증: `make -C study/Core-0C-Shortest-Path/11657/problem test`

## 왜 이 전략인가

- 가중치 조건과 그래프 특성에 맞는 최단 경로 알고리즘을 선택하는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(V*E)`
- 공간 복잡도: `O(V)`
- 변수 정의: `V=도시 수, E=버스 수`

## 실수 포인트

- 시작점 도달 불가 정점 완화 조건 누락
- 음수 사이클 검사 라운드 누락
- 출력에서 시작점 제외 범위 처리 오류
- 테스트는 통과했더라도, BOJ 11657 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- C++ 비교 구현: `../../cpp/src/solution.cpp`
- 빠른 검증: `make -C study/Core-0C-Shortest-Path/11657/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
