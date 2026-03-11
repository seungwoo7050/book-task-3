# 접근 정리 — BOJ 9372 (상근이의 여행)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `연결 그래프에서 최소 비행기 수는 항상 N-1임을 이용한 단순 출력`
- 공개 구현: `../../python/src/solution.py`
- 정식 검증: `make -C study/Core-0D-MST-Topo/9372/problem test`

## 왜 이 전략인가

- 그래프 전체 구조를 만들거나 순서를 고정하는 규칙을 설명하는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(M)`
- 공간 복잡도: `O(1)`
- 변수 정의: `N=국가 수, M=비행기 노선 수`

## 실수 포인트

- 테스트 케이스 반복 처리 누락
- 간선 입력을 읽지 않고 넘어가 버퍼가 꼬이는 문제
- N-1 공식을 케이스별로 출력하지 않는 실수
- 테스트는 통과했더라도, BOJ 9372 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- 빠른 검증: `make -C study/Core-0D-MST-Topo/9372/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
