# 접근 정리 — BOJ 5397 (키로거)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `키 입력 문자열을 좌/우 버퍼로 시뮬레이션하는 keylogger 처리`
- 공개 구현: `../../python/src/solution.py`
- 비교 구현: `../../cpp/src/solution.cpp`
- 정식 검증: `make -C study/Core-01-Array-List/5397/problem test`

## 왜 이 전략인가

- 순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(L)`
- 공간 복잡도: `O(L)`
- 변수 정의: `L=테스트 케이스별 입력 길이`

## 실수 포인트

- <, >, - 처리 우선순위 혼동
- 케이스 간 상태 초기화 누락
- 빈 버퍼에서 삭제 시 예외 처리 누락
- 테스트는 통과했더라도, BOJ 5397 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- C++ 비교 구현: `../../cpp/src/solution.cpp`
- 빠른 검증: `make -C study/Core-01-Array-List/5397/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
