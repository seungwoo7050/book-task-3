# algorithm 종합 과제 문제지

현재 `algorithm`에는 별도의 종합 capstone 트랙을 두지 않습니다.

## 왜 capstone이 없는가

- 이 저장소의 핵심은 16개 트랙과 53개 개별 문제를 단계적으로 쌓아 가는 구조입니다.
- 그래서 여러 주제를 한 프로젝트로 다시 묶는 종합 과제보다, 트랙 자체를 문제군 단위로 읽는 편이 더 자연스럽습니다.

## 대신 어디서 시작할까

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [elective-path-python](elective-path-python.md) | 시작 위치의 구현을 완성해 주제: 타임머신, 학습 초점: 가중치 조건과 그래프 특성에 맞는 최단 경로 알고리즘을 선택하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-0C-Shortest-Path/11657/problem test` |
| [essential-path-python](essential-path-python.md) | 시작 위치의 구현을 완성해 주제: 타임머신, 학습 초점: 가중치 조건과 그래프 특성에 맞는 최단 경로 알고리즘을 선택하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-0C-Shortest-Path/11657/problem test` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
