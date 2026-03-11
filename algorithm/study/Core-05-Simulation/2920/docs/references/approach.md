# 접근 정리 — BOJ 2920 (음계)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `인접 음계 차이를 검사해 ascending/descending/mixed 판정`
- 공개 구현: `../../python/src/solution.py`
- 정식 검증: `make -C study/Core-05-Simulation/2920/problem test`

## 왜 이 전략인가

- 복잡한 설명을 작은 상태 전이 규칙으로 나누어 구현하는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(1)`
- 공간 복잡도: `O(1)`
- 변수 정의: `길이가 8로 고정된 음계 배열`

## 실수 포인트

- 오름/내림 동시 false일 때 mixed 처리 누락
- 입력 split 개수 검증 누락
- 고정 길이 가정이 깨질 때 방어 로직 부재
- 테스트는 통과했더라도, BOJ 2920 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- 빠른 검증: `make -C study/Core-05-Simulation/2920/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
