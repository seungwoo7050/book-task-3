# BOJ 16926 학습 프로젝트

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `BOJ 16926 배열 돌리기 1` 문제를 현재 학습 구조에서 설명 가능한 풀이 프로젝트로 다시 정리한 항목 |
| 정식 검증 | `make -C study/Core-00-Basics/16926/problem test` |

## 문제가 뭐였나
- 문제: `배열 돌리기 1`
- 트랙: `Core-00-Basics`
- 학습 초점: 작은 입력을 안정적으로 읽고, 조건 분기를 코드와 문서로 함께 정리하는 감각
- CLRS 연결: `Ch 1-3`

## 제공된 자료
- `problem/data/`: 대표 입력과 기대 출력을 담은 fixture
- `problem/code/`: starter code 또는 문제 보조 자료
- `problem/script/`: 수동 실행과 채점 보조 스크립트
- `problem/Makefile`: `run`/`test` 진입점

## 이 레포의 답
- 한 줄 답: `레이어 분해(layer decomposition) 후 각 테두리를 독립적으로 회전`
- 공개 답안 위치: `python/src/`
- 판단 근거: [docs/references/approach.md](docs/references/approach.md)
- 장문 학습 노트: [notion/README.md](notion/README.md)

## 어떻게 검증하나
- 정식 검증: `make -C study/Core-00-Basics/16926/problem test`
- 대표 실행: `make -C study/Core-00-Basics/16926/problem run-py`
- 최근 확인: `2026-03-11` 기준 fixture 통과

## 무엇을 배웠나
- 작은 입력을 안정적으로 읽고, 조건 분기를 코드와 문서로 함께 정리하는 감각
- 구현과 문서를 분리해 읽으면서, 코드보다 판단 기준을 먼저 설명하는 연습
- Python 하나로도 재현 가능한 최소 완성본을 만드는 연습

## 현재 한계
- canonical 공개 답안은 `python/src/`를 기준으로 읽는다.
- fixture 중심 검증이라 온라인 저지의 모든 비공개 케이스를 직접 대체하지는 않는다.
- 현재 공개 표면은 Python 단일 구현에 집중한다.
