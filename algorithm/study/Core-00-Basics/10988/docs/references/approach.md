# 접근 정리 — BOJ 10988 (팰린드롬인지 확인하기)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `양끝 포인터(two pointers)로 좌우 문자를 동시에 비교`
- 공개 구현: `../../python/src/solution.py`
- 정식 검증: `make -C study/Core-00-Basics/10988/problem test`

## 왜 이 전략인가

- 작은 입력을 안정적으로 읽고, 조건 분기를 코드와 문서로 함께 정리하는 감각
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(L)`
- 공간 복잡도: `O(1)`
- 변수 정의: `L=입력 문자열 길이`

## 실수 포인트

- 인덱스 이동 순서를 잘못 두어 중앙 비교를 건너뛰는 실수
- 개행 문자를 제거하지 않아 회문 판정이 틀어지는 경우
- 첫 불일치 이후에도 루프를 지속해 불필요한 비교를 수행하는 문제
- 테스트는 통과했더라도, BOJ 10988 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- 빠른 검증: `make -C study/Core-00-Basics/10988/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
