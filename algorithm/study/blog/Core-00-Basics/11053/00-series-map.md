# 가장 긴 증가하는 부분 수열 시리즈 맵

이 문서는 `가장 긴 증가하는 부분 수열`를 읽기 시작할 때 필요한 지도다. `Core-00-Basics`의 질문이 이 문제에서 어떤 코드 선택으로 이어졌는지, 그리고 어떤 검증으로 끝을 맺는지를 앞에서 먼저 잡아 둔다. 세부 timestamp 대신 `Phase 1..4` 순서로 흐름만 복원했고, 기존 초안은 `_legacy`에 따로 보관했다.

## 프로젝트 전체에서 어디쯤인가

- 트랙 질문: `작은 입력과 조건 분기를 어떻게 안정적으로 구현하고 검증할까?`
- 이 프로젝트의 한 줄 답: `1차원 DP로 각 위치에서 끝나는 LIS 길이를 누적 계산`
- 기본 검증 명령: `make -C study/Core-00-Basics/11053/problem test`
- 시간/공간 복잡도: `O(N^2)`, `O(N)`

## 먼저 볼 파일

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [05-structure-plan.md](05-structure-plan.md)
3. [10-development-timeline.md](10-development-timeline.md)
4. [20-development-timeline.md](20-development-timeline.md)

## 이번 시리즈를 따라가는 순서

1. `problem/README.md`와 `problem/code/starter.py`에서 입출력 계약과 실행 진입점을 먼저 본다.
2. `python/src/solution.py`에서 `1차원 DP로 각 위치에서 끝나는 LIS 길이를 누적 계산`가 실제 상태 전이로 어떻게 굳는지 따라간다.
3. `make -C study/Core-00-Basics/11053/problem test`와 `problem/script/test.sh`로 fixture 전체가 어떻게 닫히는지 확인한다.
4. `docs/concepts/*.md`와 `cpp/src/solution.cpp`를 붙여 마지막 판단 기준을 다시 읽는다.

## 읽는 동안 붙잡을 질문

- `작은 입력과 조건 분기를 어떻게 안정적으로 구현하고 검증할까?`가 이 문제에서는 어떤 상태 설계로 바뀌는가?
- `엄격 증가(<) 대신 비엄격 증가(<=)를 써서 정답이 커지는 실수`를 막기 위해 가장 먼저 고정한 줄은 어디인가?
- `LIS (Longest Increasing Subsequence) — Concept & Background`를 다시 읽고 나면 어떤 코드 조각이 핵심으로 남는가?
