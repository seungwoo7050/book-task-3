# 최소 스패닝 트리 시리즈 맵

이 시리즈는 `Core-0D-MST-Topo`의 `최소 스패닝 트리` 문제를 어떤 순서로 다듬어 갔는지 따라가기 위한 안내서다. 정답 요약보다, 문제 계약과 구현 판단이 어디서 맞물렸는지를 보여 주는 데 초점을 둔다. 세부 timestamp 대신 `Phase 1..4` 순서로 흐름만 복원했고, 기존 초안은 `_legacy`에 따로 보관했다.

## 프로젝트 전체에서 어디쯤인가

- 트랙 질문: `그래프 전체 구조나 순서를 만드는 규칙을 어떻게 설명할까?`
- 이 프로젝트의 한 줄 답: `간선 가중치 정렬 + 유니온파인드로 MST를 구성하는 Kruskal`
- 기본 검증 명령: `make -C study/Core-0D-MST-Topo/1197/problem test`
- 시간/공간 복잡도: `O(E log E)`, `O(E)`

## 먼저 볼 파일

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [05-structure-plan.md](05-structure-plan.md)
3. [10-development-timeline.md](10-development-timeline.md)
4. [20-development-timeline.md](20-development-timeline.md)

## 이번 시리즈를 따라가는 순서

1. `problem/README.md`와 `problem/code/starter.py`에서 입출력 계약과 실행 진입점을 먼저 본다.
2. `python/src/solution.py`에서 `간선 가중치 정렬 + 유니온파인드로 MST를 구성하는 Kruskal`가 실제 상태 전이로 어떻게 굳는지 따라간다.
3. `make -C study/Core-0D-MST-Topo/1197/problem test`와 `problem/script/test.sh`로 fixture 전체가 어떻게 닫히는지 확인한다.
4. `docs/concepts/*.md`와 `cpp/src/solution.cpp`를 붙여 마지막 판단 기준을 다시 읽는다.

## 읽는 동안 붙잡을 질문

- `그래프 전체 구조나 순서를 만드는 규칙을 어떻게 설명할까?`가 이 문제에서는 어떤 상태 설계로 바뀌는가?
- `find 경로압축 누락으로 성능 저하`를 막기 위해 가장 먼저 고정한 줄은 어디인가?
- `최소 스패닝 트리 (Kruskal) 개념 정리`를 다시 읽고 나면 어떤 코드 조각이 핵심으로 남는가?
