# Core-05-Simulation

## 트랙 한 줄 질문

긴 문제 설명을 작은 상태 전이 규칙으로 어떻게 쪼갤까?

## 왜 이 순서인가

시뮬레이션은 실수하기 쉬운 대신, 문서화가 잘되면 실력을 보여 주기 좋은 분야다. 상태 표와 규칙 분리를 익히기 좋다.

## 프로젝트 카탈로그

| 순서 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [2920](2920/README.md) | `음계` | `python/src/` | `make -C study/Core-05-Simulation/2920/problem test` | `verified` |
| 2 | [14503](14503/README.md) | `로봇 청소기` | `python/src/`, `cpp/src/` | `make -C study/Core-05-Simulation/14503/problem test` | `verified` |
| 3 | [14891](14891/README.md) | `톱니바퀴` | `python/src/` | `make -C study/Core-05-Simulation/14891/problem test` | `verified` |

## 공통 읽기 순서

1. [../README.md](../README.md)에서 전체 트랙 인덱스를 확인한다.
2. [../../docs/curriculum-map.md](../../docs/curriculum-map.md)에서 이 트랙이 놓인 이유를 본다.
3. 원하는 프로젝트 README에서 6문답을 먼저 읽고 `problem/ -> 구현 -> docs/ -> notion/` 순서로 내려간다.

## 포트폴리오 관점 메모

포트폴리오에서는 상태 전이 표, 방향 정의, 반복 종료 조건 세 가지만 깔끔하게 보여 줘도 문제 이해도가 확 올라간다.
