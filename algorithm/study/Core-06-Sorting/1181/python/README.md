# Python 구현 안내

## 이 폴더의 역할

이 폴더는 현재 프로젝트의 canonical 공개 답안을 담는다. README와 `problem/`에서 문제 계약을 확인한 뒤 `src/solution.py`를 읽는다.

## 먼저 볼 파일

- `src/solution.py`

## 기준 명령

- 실행: `make -C study/Core-06-Sorting/1181/problem run-py`
- 검증: `make -C study/Core-06-Sorting/1181/problem test`

## 현재 범위

- 한 줄 답: `중복 제거 후 (길이, 사전순) 복합 키로 정렬`

## 남은 약점

- 장문 reasoning과 디버깅 이력은 이 폴더가 아니라 `../docs/`와 `../notion/`에 둔다.
- fixture 중심 검증 기준은 `../problem/Makefile`을 따른다.
