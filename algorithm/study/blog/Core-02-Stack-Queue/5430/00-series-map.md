# AC 시리즈 맵

`AC` 시리즈는 `Core-02-Stack-Queue`의 `Gold` 프로젝트를 다시 읽기 좋게 묶은 입구다. 코드만 보는 대신, 이 풀이가 어떤 근거와 검증 위에서 정리됐는지 한 번에 따라가도록 구성했다. 세부 timestamp 대신 `Phase 1..4` 순서로 흐름만 복원했고, 기존 초안은 `_legacy`에 따로 보관했다.

## 프로젝트 전체에서 어디쯤인가

- 트랙 질문: `명령 규칙을 LIFO/FIFO/덱 모델로 어떻게 옮길까?`
- 이 프로젝트의 한 줄 답: `함수 문자열을 reverse flag + deque 양끝 제거로 lazy evaluation`
- 기본 검증 명령: `make -C study/Core-02-Stack-Queue/5430/problem test`
- 시간/공간 복잡도: `O(|P|+N)`, `O(N)`

## 먼저 볼 파일

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [05-structure-plan.md](05-structure-plan.md)
3. [10-development-timeline.md](10-development-timeline.md)
4. [20-development-timeline.md](20-development-timeline.md)

## 이번 시리즈를 따라가는 순서

1. `problem/README.md`와 `problem/code/starter.py`에서 입출력 계약과 실행 진입점을 먼저 본다.
2. `python/src/solution.py`에서 `함수 문자열을 reverse flag + deque 양끝 제거로 lazy evaluation`가 실제 상태 전이로 어떻게 굳는지 따라간다.
3. `make -C study/Core-02-Stack-Queue/5430/problem test`와 `problem/script/test.sh`로 fixture 전체가 어떻게 닫히는지 확인한다.
4. `docs/concepts/*.md`와 `cpp/src/solution.cpp`를 붙여 마지막 판단 기준을 다시 읽는다.

## 읽는 동안 붙잡을 질문

- `명령 규칙을 LIFO/FIFO/덱 모델로 어떻게 옮길까?`가 이 문제에서는 어떤 상태 설계로 바뀌는가?
- `빈 배열에서 D 실행 시 error 처리 누락`를 막기 위해 가장 먼저 고정한 줄은 어디인가?
- `덱(Deque)과 Lazy Reversal 개념 정리`를 다시 읽고 나면 어떤 코드 조각이 핵심으로 남는가?
