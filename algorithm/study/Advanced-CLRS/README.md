# Advanced-CLRS

## 트랙 한 줄 질문

proof-heavy 주제를 실행 가능한 실험으로 어떻게 바꿀까?

## 왜 이 순서인가

고급 알고리즘은 읽기만 하면 남지 않는다. 이 트랙은 proof-heavy 챕터를 실행 가능한 과제로 바꿔 학습 장벽을 낮춘다.

## 프로젝트 카탈로그

| 순서 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [0x10-strassen-matrix](0x10-strassen-matrix/README.md) | `Strassen 행렬 곱셈` | `python/src/` | `make -C study/Advanced-CLRS/0x10-strassen-matrix/problem test` | `verified` |
| 2 | [0x11-amortized-analysis-lab](0x11-amortized-analysis-lab/README.md) | `상각 분석 실습` | `python/src/` | `make -C study/Advanced-CLRS/0x11-amortized-analysis-lab/problem test` | `verified` |
| 3 | [0x12-red-black-tree](0x12-red-black-tree/README.md) | `레드-블랙 트리 삽입과 검증` | `python/src/` | `make -C study/Advanced-CLRS/0x12-red-black-tree/problem test` | `verified` |
| 4 | [0x13-meldable-heap](0x13-meldable-heap/README.md) | `합칠 수 있는 힙 브리지` | `python/src/` | `make -C study/Advanced-CLRS/0x13-meldable-heap/problem test` | `verified` |
| 5 | [0x14-network-flow](0x14-network-flow/README.md) | `네트워크 플로우` | `python/src/` | `make -C study/Advanced-CLRS/0x14-network-flow/problem test` | `verified` |
| 6 | [0x15-string-matching](0x15-string-matching/README.md) | `고급 문자열 매칭` | `python/src/` | `make -C study/Advanced-CLRS/0x15-string-matching/problem test` | `verified` |
| 7 | [0x16-computational-geometry](0x16-computational-geometry/README.md) | `계산 기하 실습` | `python/src/` | `make -C study/Advanced-CLRS/0x16-computational-geometry/problem test` | `verified` |
| 8 | [0x17-number-theory-lab](0x17-number-theory-lab/README.md) | `정수론 실습` | `python/src/` | `make -C study/Advanced-CLRS/0x17-number-theory-lab/problem test` | `verified` |
| 9 | [0x18-np-completeness-lab](0x18-np-completeness-lab/README.md) | `NP-완전성 실습` | `python/src/` | `make -C study/Advanced-CLRS/0x18-np-completeness-lab/problem test` | `verified` |
| 10 | [0x19-approximation-lab](0x19-approximation-lab/README.md) | `근사 알고리즘 실습` | `python/src/` | `make -C study/Advanced-CLRS/0x19-approximation-lab/problem test` | `verified` |

## 공통 읽기 순서

1. [../README.md](../README.md)에서 전체 트랙 인덱스를 확인한다.
2. [../../docs/curriculum-map.md](../../docs/curriculum-map.md)에서 이 트랙이 놓인 이유를 본다.
3. 원하는 프로젝트 README에서 6문답을 먼저 읽고 `problem/ -> 구현 -> docs/ -> notion/` 순서로 내려간다.

## 포트폴리오 관점 메모

심화 트랙은 '책 내용을 그대로 베꼈다'가 아니라 '핵심 개념을 실행 가능한 형태로 재구성했다'는 점이 드러나야 한다.
