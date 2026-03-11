# 접근 정리 — BOJ 1717 (집합의 표현)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `다음 트랙에서 필요한 선행 개념을 별도 실습으로 고정하는 연습`
- 공개 구현: `../../python/src/solution.py`
- 정식 검증: `make -C study/Core-Bridges/1717/problem test`

## 왜 이 전략인가

- 다음 트랙에서 필요한 선행 개념을 별도 실습으로 고정하는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 복잡도는 `python/src/solution.py` 구현 기준으로 확인한다.

## 실수 포인트

- 입력 계약을 구현에 제대로 옮기지 못하는 문제
- 경계 사례를 fixture에 고정하지 않아 재검증이 어려워지는 문제

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- 빠른 검증: `make -C study/Core-Bridges/1717/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
