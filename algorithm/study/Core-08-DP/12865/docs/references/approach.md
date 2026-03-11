# 접근 정리 — BOJ 12865 (평범한 배낭)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `무게 한도 K에서 최대 가치를 누적하는 0/1 knapsack DP`
- 공개 구현: `../../python/src/solution.py`
- 비교 구현: `../../cpp/src/solution.cpp`
- 정식 검증: `make -C study/Core-08-DP/12865/problem test`

## 왜 이 전략인가

- 상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(N*K)`
- 공간 복잡도: `O(N*K)`
- 변수 정의: `N=물건 수, K=최대 허용 무게`

## 실수 포인트

- 같은 물건을 중복 선택하는 전이 실수
- 인덱스 기준(1-based/0-based) 혼동
- 무게 초과 조건 검사 누락
- 테스트는 통과했더라도, BOJ 12865 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- C++ 비교 구현: `../../cpp/src/solution.cpp`
- 빠른 검증: `make -C study/Core-08-DP/12865/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
