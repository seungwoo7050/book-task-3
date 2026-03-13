# 최대 힙 시리즈 맵

`최대 힙` 시리즈는 `Core-0A-Priority-Queue`의 `Bronze` 프로젝트를 다시 읽기 좋게 묶은 입구다. 코드만 보는 대신, 이 풀이가 어떤 근거와 검증 위에서 정리됐는지 한 번에 따라가도록 구성했다. 세부 timestamp 대신 `Phase 1..4` 순서로 흐름만 복원했고, 기존 초안은 `_legacy`에 따로 보관했다.

## 프로젝트 전체에서 어디쯤인가

- 트랙 질문: `힙이 필요한 문제 구조를 어떻게 구분할까?`
- 이 프로젝트의 한 줄 답: `최대 힙(max-heap)에 삽입/삭제 연산을 매 명령마다 처리`
- 기본 검증 명령: `make -C study/Core-0A-Priority-Queue/11279/problem test`
- 시간/공간 복잡도: `O(Q log Q)`, `O(Q)`

## 먼저 볼 파일

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [05-structure-plan.md](05-structure-plan.md)
3. [10-development-timeline.md](10-development-timeline.md)
4. [20-development-timeline.md](20-development-timeline.md)

## 이번 시리즈를 따라가는 순서

1. `problem/README.md`와 `problem/code/starter.py`에서 입출력 계약과 실행 진입점을 먼저 본다.
2. `python/src/solution.py`에서 `최대 힙(max-heap)에 삽입/삭제 연산을 매 명령마다 처리`가 실제 상태 전이로 어떻게 굳는지 따라간다.
3. `make -C study/Core-0A-Priority-Queue/11279/problem test`와 `problem/script/test.sh`로 fixture 전체가 어떻게 닫히는지 확인한다.
4. `docs/concepts/*.md`를 붙여 마지막 판단 기준을 다시 읽는다.

## 읽는 동안 붙잡을 질문

- `힙이 필요한 문제 구조를 어떻게 구분할까?`가 이 문제에서는 어떤 상태 설계로 바뀌는가?
- `파이썬 min-heap을 max-heap으로 변환할 때 부호 처리 실수`를 막기 위해 가장 먼저 고정한 줄은 어디인가?
- `우선순위 큐 / 힙 개념 정리 — 최대 힙`를 다시 읽고 나면 어떤 코드 조각이 핵심으로 남는가?
