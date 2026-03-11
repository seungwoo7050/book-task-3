# 접근 정리 — BOJ 1927 (최소 힙)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `최소 힙(min-heap)으로 0 명령 시 최솟값을 추출`
- 공개 구현: `../../python/src/solution.py`
- 정식 검증: `make -C study/Core-0A-Priority-Queue/1927/problem test`

## 왜 이 전략인가

- 우선순위 큐가 필요한 상황을 식별하고 비교 기준을 일관되게 유지하는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(Q log Q)`
- 공간 복잡도: `O(Q)`
- 변수 정의: `Q=명령 수`

## 실수 포인트

- 0 입력을 데이터로 오해
- 빈 힙에서 0 출력 누락
- push/pop 분기 순서 오류
- 테스트는 통과했더라도, BOJ 1927 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- 빠른 검증: `make -C study/Core-0A-Priority-Queue/1927/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
