# 선 긋기 시리즈 맵

`선 긋기` 시리즈는 `Core-06-Sorting`의 `Gold` 프로젝트를 다시 읽기 좋게 묶은 입구다. 코드만 보는 대신, 이 풀이가 어떤 근거와 검증 위에서 정리됐는지 한 번에 따라가도록 구성했다. 세부 timestamp 대신 `Phase 1..4` 순서로 흐름만 복원했고, 기존 초안은 `_legacy`에 따로 보관했다.

## 프로젝트 전체에서 어디쯤인가

- 트랙 질문: `정렬 기준과 정렬 후 후처리를 어떻게 분리할까?`
- 이 프로젝트의 한 줄 답: `구간을 시작점 기준 정렬 후 병합해 총 길이 계산`
- 기본 검증 명령: `make -C study/Core-06-Sorting/2170/problem test`
- 시간/공간 복잡도: `O(N log N)`, `O(N)`

## 먼저 볼 파일

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [05-structure-plan.md](05-structure-plan.md)
3. [10-development-timeline.md](10-development-timeline.md)
4. [20-development-timeline.md](20-development-timeline.md)

## 이번 시리즈를 따라가는 순서

1. `problem/README.md`와 `problem/code/starter.py`에서 입출력 계약과 실행 진입점을 먼저 본다.
2. `python/src/solution.py`에서 `구간을 시작점 기준 정렬 후 병합해 총 길이 계산`가 실제 상태 전이로 어떻게 굳는지 따라간다.
3. `make -C study/Core-06-Sorting/2170/problem test`와 `problem/script/test.sh`로 fixture 전체가 어떻게 닫히는지 확인한다.
4. `docs/concepts/*.md`와 `cpp/src/solution.cpp`를 붙여 마지막 판단 기준을 다시 읽는다.

## 읽는 동안 붙잡을 질문

- `정렬 기준과 정렬 후 후처리를 어떻게 분리할까?`가 이 문제에서는 어떤 상태 설계로 바뀌는가?
- `끝점 포함/배타 해석 혼동`를 막기 위해 가장 먼저 고정한 줄은 어디인가?
- `구간 병합(Interval Merge) 개념 정리 — 선 긋기`를 다시 읽고 나면 어떤 코드 조각이 핵심으로 남는가?
