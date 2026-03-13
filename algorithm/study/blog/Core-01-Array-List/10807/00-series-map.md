# 개수 세기 시리즈 맵

이 문서는 `개수 세기`를 읽기 시작할 때 필요한 지도다. `Core-01-Array-List`의 질문이 이 문제에서 어떤 코드 선택으로 이어졌는지, 그리고 어떤 검증으로 끝을 맺는지를 앞에서 먼저 잡아 둔다. 세부 timestamp 대신 `Phase 1..4` 순서로 흐름만 복원했고, 기존 초안은 `_legacy`에 따로 보관했다.

## 프로젝트 전체에서 어디쯤인가

- 트랙 질문: `순차 자료구조 선택이 편집과 이동 비용을 어떻게 바꾸는가?`
- 이 프로젝트의 한 줄 답: `단일 선형 스캔으로 목표 값 v의 출현 횟수를 집계`
- 기본 검증 명령: `make -C study/Core-01-Array-List/10807/problem test`
- 시간/공간 복잡도: `O(N)`, `O(1)`

## 먼저 볼 파일

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [05-structure-plan.md](05-structure-plan.md)
3. [10-development-timeline.md](10-development-timeline.md)
4. [20-development-timeline.md](20-development-timeline.md)

## 이번 시리즈를 따라가는 순서

1. `problem/README.md`와 `problem/code/starter.py`에서 입출력 계약과 실행 진입점을 먼저 본다.
2. `python/src/solution.py`에서 `단일 선형 스캔으로 목표 값 v의 출현 횟수를 집계`가 실제 상태 전이로 어떻게 굳는지 따라간다.
3. `make -C study/Core-01-Array-List/10807/problem test`와 `problem/script/test.sh`로 fixture 전체가 어떻게 닫히는지 확인한다.
4. `docs/concepts/*.md`를 붙여 마지막 판단 기준을 다시 읽는다.

## 읽는 동안 붙잡을 질문

- `순차 자료구조 선택이 편집과 이동 비용을 어떻게 바꾸는가?`가 이 문제에서는 어떤 상태 설계로 바뀌는가?
- `입력 분리 과정에서 음수 기호를 잘못 처리하는 오류`를 막기 위해 가장 먼저 고정한 줄은 어디인가?
- `Array & Linear Search — Concept & Background`를 다시 읽고 나면 어떤 코드 조각이 핵심으로 남는가?
