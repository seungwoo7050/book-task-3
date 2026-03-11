# Core-08-DP

## 트랙 한 줄 질문

상태와 전이를 표의 의미로 끝까지 유지하려면 무엇을 고정해야 할까?

## 왜 이 순서인가

DP는 풀이를 외우면 금방 무너지고, 상태 정의를 스스로 세워야 오래 간다. 그래서 작은 1차원 DP부터 배낭 문제까지 묶는다.

## 프로젝트 카탈로그

| 순서 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [2748](2748/README.md) | `피보나치 수 2` | `python/src/` | `make -C study/Core-08-DP/2748/problem test` | `verified` |
| 2 | [1149](1149/README.md) | `RGB거리` | `python/src/` | `make -C study/Core-08-DP/1149/problem test` | `verified` |
| 3 | [12865](12865/README.md) | `평범한 배낭` | `python/src/`, `cpp/src/` | `make -C study/Core-08-DP/12865/problem test` | `verified` |

## 공통 읽기 순서

1. [../README.md](../README.md)에서 전체 트랙 인덱스를 확인한다.
2. [../../docs/curriculum-map.md](../../docs/curriculum-map.md)에서 이 트랙이 놓인 이유를 본다.
3. 원하는 프로젝트 README에서 6문답을 먼저 읽고 `problem/ -> 구현 -> docs/ -> notion/` 순서로 내려간다.

## 포트폴리오 관점 메모

DP 문서는 점화식을 먼저 쓰고, 각 항이 무엇을 의미하는지 바로 아래에 풀어 써야 읽는 사람이 따라오기 쉽다.
