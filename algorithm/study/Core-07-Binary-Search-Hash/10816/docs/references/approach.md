# 접근 정리 — BOJ 10816 (숫자 카드 2)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `빈도 해시맵(counter)으로 카드 개수를 누적하고 질의별 출력`
- 공개 구현: `../../python/src/solution.py`
- 정식 검증: `make -C study/Core-07-Binary-Search-Hash/10816/problem test`

## 왜 이 전략인가

- 탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(N+M)`
- 공간 복잡도: `O(N)`
- 변수 정의: `N=카드 수, M=질의 수`

## 실수 포인트

- 기본값 0 처리 누락(KeyError)
- 입출력 버퍼링 누락
- 질의 순서대로 출력하지 않는 문제
- 테스트는 통과했더라도, BOJ 10816 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- 빠른 검증: `make -C study/Core-07-Binary-Search-Hash/10816/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
