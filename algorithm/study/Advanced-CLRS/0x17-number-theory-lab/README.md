# 0x17 정수론 실습 학습 프로젝트

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `정수론 실습` 개념을 `CLRS Ch 31` 맥락에서 실행 가능한 입출력 실험으로 다시 정리한 심화 프로젝트 |
| 정식 검증 | `make -C study/Advanced-CLRS/0x17-number-theory-lab/problem test` |

## 문제가 뭐였나
- 문제: `정수론 실습`
- 트랙: `Advanced-CLRS`
- 학습 초점: 이론 중심 알고리즘을 작은 실험과 검증 가능한 입출력 문제로 재구성하는 연습
- CLRS 연결: `Ch 31`

## 제공된 자료
- `problem/data/`: 대표 입력과 기대 출력을 담은 fixture
- `problem/code/`: starter code 또는 문제 보조 자료
- `problem/script/`: 수동 실행과 채점 보조 스크립트
- `problem/Makefile`: `run`/`test` 진입점

## 이 레포의 답
- 한 줄 답: `python/src/solution.py`에서 `정수론 실습` 핵심 절차를 실행 가능한 실험으로 재현
- 공개 답안 위치: `python/src/`
- 판단 근거: [docs/references/approach.md](docs/references/approach.md)
- 장문 학습 노트: [notion/README.md](notion/README.md)

## 어떻게 검증하나
- 정식 검증: `make -C study/Advanced-CLRS/0x17-number-theory-lab/problem test`
- 대표 실행: `make -C study/Advanced-CLRS/0x17-number-theory-lab/problem run-py`
- 최근 확인: `2026-03-11` 기준 fixture 통과

## 무엇을 배웠나
- 이론 중심 알고리즘을 작은 실험과 검증 가능한 입출력 문제로 재구성하는 연습
- 구현과 문서를 분리해 읽으면서, 코드보다 판단 기준을 먼저 설명하는 연습
- Python 하나로도 재현 가능한 최소 완성본을 만드는 연습

## 현재 한계
- canonical 공개 답안은 `python/src/`를 기준으로 읽는다.
- fixture 중심 검증이라 온라인 저지의 모든 비공개 케이스를 직접 대체하지는 않는다.
- 현재 공개 표면은 Python 단일 구현에 집중한다.
