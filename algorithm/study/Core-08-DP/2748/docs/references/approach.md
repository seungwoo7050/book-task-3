# 접근 정리 — BOJ 2748 (피보나치 수 2)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `반복 DP로 피보나치 수를 하향식 없이 누적 계산`
- 공개 구현: `../../python/src/solution.py`
- 정식 검증: `make -C study/Core-08-DP/2748/problem test`

## 왜 이 전략인가

- 상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(N)`
- 공간 복잡도: `O(1)`
- 변수 정의: `N=피보나치 인덱스`

## 실수 포인트

- F(0)/F(1) 기저값 혼동
- 정수 범위 가정 오류
- 반복문 시작 인덱스 오프바이원
- 테스트는 통과했더라도, BOJ 2748 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- 빠른 검증: `make -C study/Core-08-DP/2748/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
