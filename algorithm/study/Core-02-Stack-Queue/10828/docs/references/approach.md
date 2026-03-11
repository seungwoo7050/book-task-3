# 접근 정리 — BOJ 10828 (스택)

## 문제 계약

- 입력 해석, 상태 전이, 출력 직렬화가 모두 맞아야 정답이 된다.
- canonical fixture는 `problem/data/`에 두고, 실행 경로는 `problem/Makefile`로 고정한다.
- 이 문서는 정답 코드 전문보다 어떤 판단 기준으로 구현을 읽어야 하는지 요약한다.

## 채택 답

- 전략: `명령형 스택 연산을 조건 분기와 리스트 push/pop으로 구현`
- 공개 구현: `../../python/src/solution.py`
- 정식 검증: `make -C study/Core-02-Stack-Queue/10828/problem test`

## 왜 이 전략인가

- 명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습
- 상태를 단순하게 유지해 디버깅 비용과 설명 비용을 함께 낮춘다.
- `docs/references/reproducibility.md`와 `problem/data/`를 함께 보면 재검증 루프가 단순하다.

## 복잡도

- 시간 복잡도: `O(Q)`
- 공간 복잡도: `O(Q)`
- 변수 정의: `Q=명령 수`

## 실수 포인트

- 빈 스택 pop/top 반환값(-1) 누락
- 명령 파싱 시 push 값 분리 오류
- 출력 버퍼링 없이 매번 print해 성능 저하
- 테스트는 통과했더라도, BOJ 10828 코드 변경 시에는 동일 체크리스트를 다시 실행해야 한다.

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- 빠른 검증: `make -C study/Core-02-Stack-Queue/10828/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
