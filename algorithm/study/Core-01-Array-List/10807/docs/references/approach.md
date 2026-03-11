# 접근 정리 — BOJ 10807 (개수 세기)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `단일 선형 스캔으로 목표 값 v의 출현 횟수를 집계`
- 공개 구현: `../../python/src/solution.py`
- 정식 검증: `make -C study/Core-01-Array-List/10807/problem test`

## 왜 이 전략인가

- 순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(N)`
- 공간 복잡도: `O(1)`
- 변수 정의: `N=배열 길이`

## 실수 포인트

- 입력 분리 과정에서 음수 기호를 잘못 처리하는 오류
- 카운터 변수 초기화 누락
- 정수 변환 전에 비교해 문자열 기준 오동작
- 테스트는 통과했더라도, BOJ 10807 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- 빠른 검증: `make -C study/Core-01-Array-List/10807/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
