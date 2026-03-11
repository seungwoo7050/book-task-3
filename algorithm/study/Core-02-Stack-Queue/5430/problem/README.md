# BOJ 5430 문제 자료

## 이 폴더의 역할

문제 자료와 fixture, starter code, 실행 스크립트를 한곳에 모아 두는 입구다. 구현을 읽기 전에 이 폴더에서 입력 계약과 검증 명령을 먼저 확인한다.

## 제공된 자료

- `data/`: 대표 입력과 기대 출력
- `code/`: starter code 또는 문제 보조 자료
- `script/`: 수동 실행과 채점 보조 스크립트
- `Makefile`: `run`/`test` 진입점

## 기준 명령

- `make test`
- `make run-py`
- `make run-cpp`

## 문제 계약

- 주제: `AC`
- 학습 초점: 명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습
- canonical fixture는 `data/input*.txt`, `data/output*.txt`에 둔다.

## 남은 약점

- 이 README는 문제 전문을 복제하지 않고, 문제 계약과 실행 경로만 보여 준다.
- 세부 판단 근거와 실패 기록은 `../docs/`와 `../notion/`으로 분리한다.
