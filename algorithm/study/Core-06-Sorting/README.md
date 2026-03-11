# Core-06-Sorting

## 트랙 한 줄 질문

정렬 기준과 정렬 후 후처리를 어떻게 분리할까?

## 왜 이 순서인가

정렬은 단독 기술이 아니라 이후의 탐색, 그리디, 구간 문제를 풀기 위한 공통 도구다. 그래서 순수 정렬과 활용형을 함께 둔다.

## 프로젝트 카탈로그

| 순서 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [2750](2750/README.md) | `수 정렬하기` | `python/src/` | `make -C study/Core-06-Sorting/2750/problem test` | `verified` |
| 2 | [1181](1181/README.md) | `단어 정렬` | `python/src/` | `make -C study/Core-06-Sorting/1181/problem test` | `verified` |
| 3 | [2170](2170/README.md) | `선 긋기` | `python/src/`, `cpp/src/` | `make -C study/Core-06-Sorting/2170/problem test` | `verified` |

## 공통 읽기 순서

1. [../README.md](../README.md)에서 전체 트랙 인덱스를 확인한다.
2. [../../docs/curriculum-map.md](../../docs/curriculum-map.md)에서 이 트랙이 놓인 이유를 본다.
3. 원하는 프로젝트 README에서 6문답을 먼저 읽고 `problem/ -> 구현 -> docs/ -> notion/` 순서로 내려간다.

## 포트폴리오 관점 메모

정렬 문제는 '무엇을 어떤 기준으로 정렬했는지'를 문장으로 못 쓰면 코드만 봐서는 의도가 잘 안 보인다. 기준식을 분리해서 적어 두는 편이 좋다.
