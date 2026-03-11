# 접근 정리 — BOJ 11053 (가장 긴 증가하는 부분 수열)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `1차원 DP로 각 위치에서 끝나는 LIS 길이를 누적 계산`
- 공개 구현: `../../python/src/solution.py`
- 비교 구현: `../../cpp/src/solution.cpp`
- 정식 검증: `make -C study/Core-00-Basics/11053/problem test`

## 왜 이 전략인가

- 작은 입력을 안정적으로 읽고, 조건 분기를 코드와 문서로 함께 정리하는 감각
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(N^2)`
- 공간 복잡도: `O(N)`
- 변수 정의: `N=수열 길이`

## 실수 포인트

- 엄격 증가(<) 대신 비엄격 증가(<=)를 써서 정답이 커지는 실수
- dp 초기값을 0으로 두어 길이 1 케이스를 놓치는 문제
- 최종 정답을 max(dp)로 집계하지 않는 누락
- 테스트는 통과했더라도, BOJ 11053 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- C++ 비교 구현: `../../cpp/src/solution.cpp`
- 빠른 검증: `make -C study/Core-00-Basics/11053/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
