# Python 구현 안내

## 이 폴더의 역할

이 폴더는 현재 프로젝트의 canonical 공개 답안을 담는다. README와 `problem/`에서 문제 계약을 확인한 뒤 `src/solution.py`를 읽는다.

## 먼저 볼 파일

- `src/solution.py`

## 기준 명령

- 실행: `make -C study/Core-07-Binary-Search-Hash/1920/problem run-py`
- 검증: `make -C study/Core-07-Binary-Search-Hash/1920/problem test`

## 현재 범위

- 한 줄 답: `정렬된 배열에서 각 질의를 이분 탐색(binary search)으로 판정`

## 남은 약점

- 장문 reasoning과 디버깅 이력은 이 폴더가 아니라 `../docs/`와 `../notion/`에 둔다.
- fixture 중심 검증 기준은 `../problem/Makefile`을 따른다.
