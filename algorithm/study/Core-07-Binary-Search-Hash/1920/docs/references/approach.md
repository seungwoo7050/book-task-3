# 접근 정리 — BOJ 1920 (수 찾기)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `정렬된 배열에서 각 질의를 이분 탐색(binary search)으로 판정`
- 공개 구현: `../../python/src/solution.py`
- 정식 검증: `make -C study/Core-07-Binary-Search-Hash/1920/problem test`

## 왜 이 전략인가

- 탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(N log N + M log N)`
- 공간 복잡도: `O(N)`
- 변수 정의: `N=기준 배열 크기, M=질의 수`

## 실수 포인트

- mid 업데이트에서 무한 루프
- 정렬 누락
- 출력 순서를 질의 순서와 다르게 내보내는 문제
- 테스트는 통과했더라도, BOJ 1920 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- 빠른 검증: `make -C study/Core-07-Binary-Search-Hash/1920/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
