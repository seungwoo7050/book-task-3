# 접근 정리 — BOJ 1916 (최소비용 구하기)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `우선순위 큐 기반 Dijkstra로 시작-도착 최소 비용 계산`
- 공개 구현: `../../python/src/solution.py`
- 정식 검증: `make -C study/Core-0C-Shortest-Path/1916/problem test`

## 왜 이 전략인가

- 가중치 조건과 그래프 특성에 맞는 최단 경로 알고리즘을 선택하는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O((N+M) log N)`
- 공간 복잡도: `O(N+M)`
- 변수 정의: `N=도시 수, M=버스 수`

## 실수 포인트

- dist 초기값 INF 설정 누락
- 힙에서 꺼낸 값이 구버전인지 검사 누락
- 인접 리스트 방향성 처리 오류
- 테스트는 통과했더라도, BOJ 1916 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- 빠른 검증: `make -C study/Core-0C-Shortest-Path/1916/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
