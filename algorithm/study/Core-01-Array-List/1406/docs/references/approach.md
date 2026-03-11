# 접근 정리 — BOJ 1406 (에디터)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `커서를 기준으로 좌/우 스택(또는 리스트) 두 개를 유지하는 editor simulation`
- 공개 구현: `../../python/src/solution.py`
- 정식 검증: `make -C study/Core-01-Array-List/1406/problem test`

## 왜 이 전략인가

- 순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(N+M)`
- 공간 복잡도: `O(N+M)`
- 변수 정의: `N=초기 문자열 길이, M=명령 수`

## 실수 포인트

- 빈 좌측 버퍼에서 B/L 명령 처리 누락
- D 명령에서 우측 버퍼 pop 조건을 빠뜨리는 실수
- 최종 출력 시 우측 버퍼 역순 결합을 잊는 문제
- 테스트는 통과했더라도, BOJ 1406 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- 빠른 검증: `make -C study/Core-01-Array-List/1406/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
