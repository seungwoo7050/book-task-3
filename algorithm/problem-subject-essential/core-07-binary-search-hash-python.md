# core-07-binary-search-hash-python 문제지

## 왜 중요한가

문제 자료와 fixture, starter code, 실행 스크립트를 한곳에 모아 두는 입구다. 구현을 읽기 전에 이 폴더에서 입력 계약과 검증 명령을 먼저 확인한다.

## 목표

시작 위치의 구현을 완성해 주제: 수 찾기, 학습 초점: 탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Core-07-Binary-Search-Hash/1920/problem/code/starter.py`
- `../study/Core-07-Binary-Search-Hash/1920/python/src/solution.py`
- `../study/Core-07-Binary-Search-Hash/1920/problem/data/input1.txt`
- `../study/Core-07-Binary-Search-Hash/1920/problem/data/output1.txt`
- `../study/Core-07-Binary-Search-Hash/1920/problem/script/test.sh`
- `../study/Core-07-Binary-Search-Hash/1920/problem/Makefile`

## starter code / 입력 계약

- ../study/Core-07-Binary-Search-Hash/1920/problem/code/starter.py에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- 주제: 수 찾기
- 학습 초점: 탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습
- canonical fixture는 data/input*.txt, data/output*.txt에 둔다.

## 제외 범위

- `../study/Core-07-Binary-Search-Hash/1920/problem/code/starter.py` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/Core-07-Binary-Search-Hash/1920/problem/data/input1.txt` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- `../study/Core-07-Binary-Search-Hash/1920/problem/code/starter.py`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `main`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- `../study/Core-07-Binary-Search-Hash/1920/problem/data/input1.txt` 등 fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-07-Binary-Search-Hash/1920/problem test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-07-Binary-Search-Hash/1920/problem test
```

- `1920`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`core-07-binary-search-hash-python_answer.md`](core-07-binary-search-hash-python_answer.md)에서 확인한다.
