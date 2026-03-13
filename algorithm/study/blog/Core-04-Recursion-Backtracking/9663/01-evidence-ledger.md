# N-Queen Evidence Ledger

이 문서는 이 프로젝트의 chronology를 짧게 복원한 ledger다. 세션 로그가 촘촘히 남아 있지는 않아서 `Phase 1..4`로 정리했고, 각 칸에는 실제 코드, README, docs, 테스트, CLI에서 확인되는 판단만 남겼다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `Phase 1` | 문제 계약과 실행 진입점을 먼저 잡는다 | `README.md`, `problem/README.md`, `problem/code/starter.py` | 입력 계약과 fixture만 고정해도 구현 범위를 빠르게 줄일 수 있다 | starter skeleton과 `problem/Makefile`를 기준선으로 삼았다 | `make test`, `make run-py`, `make run-cpp` | fixture와 실행 경로가 이미 README와 Makefile에 정리돼 있었다 | `problem/code/starter.py`의 빈 `main/solve` | 문제 전문을 길게 다시 쓰지 않아도 실행 계약만 잡으면 구현 순서를 세울 수 있었다 | Python 쪽 핵심 상태를 먼저 본다 |
| 2 | `Phase 2` | Python 구현으로 첫 상태와 전이를 세운다 | `python/src/solution.py` | `열/대각선 점유 배열을 이용한 N-Queen backtracking`를 쓰려면 먼저 어떤 상태를 오래 들고 갈지 결정해야 한다 | 입력 파싱과 핵심 루프를 한 파일 안에서 먼저 닫았다 | `make -C study/Core-04-Recursion-Backtracking/9663/problem run-py` | `92`가 그대로 나왔다. | `python/src/solution.py`의 setup + 핵심 루프 | `좌상/우상 대각선 인덱스 변환 오류`를 피하려면 아이디어보다 상태 이름과 순서가 더 중요했다 | fixture 전체 검증으로 넘어간다 |
| 3 | `Phase 3` | fixture 전체를 돌려 실수 포인트를 묶는다 | `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md` | 한두 개 입력만 맞는 것으로는 설명이 끝나지 않는다 | 테스트 루프와 실수 체크리스트를 같은 축으로 다시 읽었다 | `make -C study/Core-04-Recursion-Backtracking/9663/problem test` | `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다. | `problem/script/test.sh`의 fixture 반복 구조 | 검증 루프가 남아 있으면 수정 후에도 어디서 흔들리는지 바로 찾을 수 있다 | 마지막 설명 축을 세운다 |
| 4 | `Phase 4` | 마지막 설명 축을 코드와 붙여 둔다 | `cpp/src/solution.cpp`의 비교 구현 루프, `docs/concepts/*.md` | 마지막 글은 결과 요약이 아니라 전환점을 남겨야 한다 | Python과 C++를 나란히 두고 같은 전이가 유지되는지 다시 확인했다 | `make -C study/Core-04-Recursion-Backtracking/9663/problem run-cpp` | `92`가 그대로 나왔다. | `cpp/src/solution.cpp`의 비교 구현 루프 | `N-Queen 개념 정리`를 구현 판단과 직접 연결해 읽게 됐다 | `00/10/20` 흐름으로 묶어 끝낸다 |
