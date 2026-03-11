# 접근 정리 — BOJ 2110 (공유기 설치)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `거리 D에 대한 가능성 판정을 이분 탐색하는 parametric search`
- 공개 구현: `../../python/src/solution.py`
- 비교 구현: `../../cpp/src/solution.cpp`
- 정식 검증: `make -C study/Core-07-Binary-Search-Hash/2110/problem test`

## 왜 이 전략인가

- 탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(N log N + N log D)`
- 공간 복잡도: `O(N)`
- 변수 정의: `N=집 개수, C=공유기 수, D=가능 거리 범위`

## 실수 포인트

- mid 갱신 시 lo/hi 경계 처리 오류
- 판정 함수에서 첫 집 설치 누락
- 정렬 전제 누락
- 테스트는 통과했더라도, BOJ 2110 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- C++ 비교 구현: `../../cpp/src/solution.cpp`
- 빠른 검증: `make -C study/Core-07-Binary-Search-Hash/2110/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
