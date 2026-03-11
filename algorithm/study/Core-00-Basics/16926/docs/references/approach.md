# 접근 정리 — BOJ 16926 (배열 돌리기 1)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `레이어 분해(layer decomposition) 후 각 테두리를 독립적으로 회전`
- 공개 구현: `../../python/src/solution.py`
- 정식 검증: `make -C study/Core-00-Basics/16926/problem test`

## 왜 이 전략인가

- 작은 입력을 안정적으로 읽고, 조건 분기를 코드와 문서로 함께 정리하는 감각
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(N*M)`
- 공간 복잡도: `O(N*M)`
- 변수 정의: `N=행 수, M=열 수, R=회전 횟수`

## 실수 포인트

- 레이어 길이 계산에서 코너를 중복 포함하는 오류
- R을 레이어 길이로 모듈러하지 않아 시간 초과
- 행/열 경계를 혼동해 인덱스 에러 발생
- 테스트는 통과했더라도, BOJ 16926 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- 빠른 검증: `make -C study/Core-00-Basics/16926/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
