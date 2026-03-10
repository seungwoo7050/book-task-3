# BOJ 1991 학습 프로젝트

## 문제 한눈에 보기

| 항목 | 내용 |
| :--- | :--- |
| 트랙 | `Core-0B-Graph-Tree` |
| 문제명/주제 | 트리 순회 |
| CLRS | Ch 22-24 |

BOJ 1991 `트리 순회`를 학습용 구조에 맞게 분리한 프로젝트다. 문제 자료는 `problem/`, 공개 해설은 `docs/`, 기본 구현은 `python/`, 긴 호흡의 학습 노트는 `notion/`에서 읽는다.

## 이 프로젝트에서 배우는 것

- 트리 구조의 성질을 이용해 탐색과 누적 계산을 재구성하는 연습
- 구현과 문서를 분리해 읽으면서, 코드보다 판단 기준을 먼저 설명하는 연습
- Python 하나로도 재현 가능한 최소 완성본을 만드는 연습

## 추천 읽기 순서

1. [problem/README.md](problem/README.md)에서 문제 자료와 실행 파일 구성을 확인한다.
2. [docs/references/overview.md](docs/references/overview.md)에서 공개 문서 읽기 순서를 본다.
3. [python/README.md](python/README.md)로 내려가 기본 구현을 읽는다.
4. [notion/05-development-timeline.md](notion/05-development-timeline.md)에서 전체 재현 흐름을 따라간다.
5. [notion/README.md](notion/README.md)에서 장문 학습 노트 전체를 훑는다.

## 디렉터리 구성

- `problem/`: 문제 자료, fixture, 실행 스크립트
- `python/`: 기본 구현과 실행 메모
- `docs/`: 공개용 해설과 검증 메모
- `notion/`: 길게 정리한 공개 학습 노트와 `05-development-timeline.md` 중심의 재현 기록
- `notion-archive/`: 이전 버전 메모와 보관본

## 검증 방법

- `make -C problem test`: 가장 먼저 실행할 자동 검증 명령이다. fixture 기준으로 현재 구현이 깨지지 않았는지 빠르게 확인한다.
- `make -C problem run-py`: 대표 입력을 눈으로 따라가며 Python 구현을 읽고 싶을 때 사용한다.
- `notion/05-development-timeline.md`: 위 명령을 어떤 순서로 다시 실행하고 무엇을 확인하면 되는지까지 정리한 장문 재현 기록이다.

## 현재 상태

- Python: 2026-03-10 기준 `make -C problem test` 통과
- C++: 이 프로젝트 범위에서는 유지하지 않음
- provenance: 이 프로젝트는 현재 `study/` 구조를 기준으로 읽으면 된다.

## 다음 확장 아이디어

- 대표 경계 사례를 하나 더 만들어 `problem/data/`에 추가하고, 왜 그 사례가 중요한지 `docs/`에 적어 보자.
- 트리 문제는 입력을 어떤 그래프 구조로 저장했는지와, 왜 그 저장 방식이 적절한지를 밝혀 두면 설명력이 좋아진다.
