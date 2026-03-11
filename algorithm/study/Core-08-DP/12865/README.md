# BOJ 12865 학습 프로젝트

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `BOJ 12865 평범한 배낭` 문제를 현재 학습 구조에서 설명 가능한 풀이 프로젝트로 다시 정리한 항목 |
| 정식 검증 | `make -C study/Core-08-DP/12865/problem test` |

## 문제가 뭐였나
- 문제: `평범한 배낭`
- 트랙: `Core-08-DP`
- 학습 초점: 상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습
- CLRS 연결: `Ch 15`

## 제공된 자료
- `problem/data/`: 대표 입력과 기대 출력을 담은 fixture
- `problem/code/`: starter code 또는 문제 보조 자료
- `problem/script/`: 수동 실행과 채점 보조 스크립트
- `problem/Makefile`: `run`/`test` 진입점

## 이 레포의 답
- 한 줄 답: `무게 한도 K에서 최대 가치를 누적하는 0/1 knapsack DP`
- 공개 답안 위치: `python/src/`, `cpp/src/`
- 판단 근거: [docs/references/approach.md](docs/references/approach.md)
- 장문 학습 노트: [notion/README.md](notion/README.md)

## 어떻게 검증하나
- 정식 검증: `make -C study/Core-08-DP/12865/problem test`
- 대표 실행: `make -C study/Core-08-DP/12865/problem run-py`
- 비교 실행: `make -C study/Core-08-DP/12865/problem run-cpp`
- 최근 확인: `2026-03-11` 기준 fixture 통과

## 무엇을 배웠나
- 상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습
- 구현과 문서를 분리해 읽으면서, 코드보다 판단 기준을 먼저 설명하는 연습
- Python 기본 구현과 C++ 비교 구현의 차이를 함께 보는 연습

## 현재 한계
- canonical 공개 답안은 `python/src/`를 기준으로 읽는다.
- fixture 중심 검증이라 온라인 저지의 모든 비공개 케이스를 직접 대체하지는 않는다.
- `cpp/src/`는 비교 구현이며, 설명의 기준선은 Python 쪽에 둔다.
