# Python 구현 안내

## 이 폴더의 역할

이 폴더는 현재 프로젝트의 canonical 공개 답안을 담는다. README와 `problem/`에서 문제 계약을 확인한 뒤 `src/solution.py`를 읽는다.

## 먼저 볼 파일

- `src/solution.py`

## 기준 명령

- 실행: `make -C study/Advanced-CLRS/0x12-red-black-tree/problem run-py`
- 검증: `make -C study/Advanced-CLRS/0x12-red-black-tree/problem test`

## 현재 범위

- 한 줄 답: `python/src/solution.py`에서 `레드-블랙 트리 삽입과 검증` 핵심 절차를 실행 가능한 실험으로 재현

## 남은 약점

- 장문 reasoning과 디버깅 이력은 이 폴더가 아니라 `../docs/`와 `../notion/`에 둔다.
- fixture 중심 검증 기준은 `../problem/Makefile`을 따른다.
