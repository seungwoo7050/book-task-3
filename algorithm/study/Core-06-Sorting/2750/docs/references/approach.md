# 접근 정리 — BOJ 2750 (수 정렬하기)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `입력 수열을 정렬해 오름차순으로 출력하는 기본 sorting`
- 공개 구현: `../../python/src/solution.py`
- 정식 검증: `make -C study/Core-06-Sorting/2750/problem test`

## 왜 이 전략인가

- 정렬 기준을 설계하고, 정렬 이후의 후처리 로직을 분리해 설명하는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(N log N)`
- 공간 복잡도: `O(N)`
- 변수 정의: `N=원소 개수`

## 실수 포인트

- 정수 입력을 문자열로 정렬하는 실수
- 출력 개행 누락
- N줄 입력 대신 한 줄 입력 가정 오류
- 테스트는 통과했더라도, BOJ 2750 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- 빠른 검증: `make -C study/Core-06-Sorting/2750/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
