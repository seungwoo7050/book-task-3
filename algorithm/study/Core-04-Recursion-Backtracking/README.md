# Core-04-Recursion-Backtracking

## 트랙 한 줄 질문

재귀 호출 구조와 상태 복원을 어디까지 명시해야 할까?

## 왜 이 순서인가

재귀는 코드 길이는 짧지만 실수 지점은 많다. 종료 조건, 선택-복구 순서를 문서와 함께 정리하는 습관이 필요하다.

## 프로젝트 카탈로그

| 순서 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [10872](10872/README.md) | `팩토리얼` | `python/src/` | `make -C study/Core-04-Recursion-Backtracking/10872/problem test` | `verified` |
| 2 | [15649](15649/README.md) | `N과 M (1)` | `python/src/` | `make -C study/Core-04-Recursion-Backtracking/15649/problem test` | `verified` |
| 3 | [9663](9663/README.md) | `N-Queen` | `python/src/`, `cpp/src/` | `make -C study/Core-04-Recursion-Backtracking/9663/problem test` | `verified` |

## 공통 읽기 순서

1. [../README.md](../README.md)에서 전체 트랙 인덱스를 확인한다.
2. [../../docs/curriculum-map.md](../../docs/curriculum-map.md)에서 이 트랙이 놓인 이유를 본다.
3. 원하는 프로젝트 README에서 6문답을 먼저 읽고 `problem/ -> 구현 -> docs/ -> notion/` 순서로 내려간다.

## 포트폴리오 관점 메모

백트래킹 문제는 '선택 -> 재귀 호출 -> 복구' 흐름을 코드 옆에서 문장으로 풀어 주면 학습 레포와 포트폴리오 모두에서 강점이 된다.
