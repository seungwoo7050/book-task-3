# Core-0A-Priority-Queue

## 트랙 한 줄 질문

힙이 필요한 문제 구조를 어떻게 구분할까?

## 왜 이 순서인가

우선순위 큐는 알고리즘 곳곳에서 재사용된다. 여기서 최소/최대 힙과 힙 기반 그리디를 묶어 두면 이후 그래프 문제에서 다시 쓰기 쉽다.

## 프로젝트 카탈로그

| 순서 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [11279](11279/README.md) | `최대 힙` | `python/src/` | `make -C study/Core-0A-Priority-Queue/11279/problem test` | `verified` |
| 2 | [1927](1927/README.md) | `최소 힙` | `python/src/` | `make -C study/Core-0A-Priority-Queue/1927/problem test` | `verified` |
| 3 | [1715](1715/README.md) | `카드 정렬하기` | `python/src/`, `cpp/src/` | `make -C study/Core-0A-Priority-Queue/1715/problem test` | `verified` |

## 공통 읽기 순서

1. [../README.md](../README.md)에서 전체 트랙 인덱스를 확인한다.
2. [../../docs/curriculum-map.md](../../docs/curriculum-map.md)에서 이 트랙이 놓인 이유를 본다.
3. 원하는 프로젝트 README에서 6문답을 먼저 읽고 `problem/ -> 구현 -> docs/ -> notion/` 순서로 내려간다.

## 포트폴리오 관점 메모

힙 문제는 자료구조 API를 정확히 쓰는 능력이 드러난다. push/pop 시점과 비교 기준을 문서에 분리해서 적어 두면 좋다.
