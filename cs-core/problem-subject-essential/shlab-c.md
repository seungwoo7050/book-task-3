# shlab-c 문제지

## 왜 중요한가

이 디렉터리는 Shell Lab의 문제 계약을 self-written 형태로 보존합니다. 공식 starter shell, traces, driver는 공개 트리에서 제거하고, 계약과 공개 경계만 남깁니다.

## 목표

시작 위치의 구현을 완성해 공식 starter 없이도 과제 목적을 먼저 파악하고 싶은 학습자, 어떤 자산을 제거했고 무엇으로 대체했는지 알고 싶은 사람, 공개 가능한 문제 경계 문서를 설계하고 싶은 사람을 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Systems-Programming/shlab/c/src/tsh.c`
- `../study/Systems-Programming/shlab/c/include/tsh_helper.h`
- `../study/Systems-Programming/shlab/c/tests/run_tests.sh`
- `../study/Systems-Programming/shlab/c/Makefile`
- `../study/Systems-Programming/shlab/problem/Makefile`

## starter code / 입력 계약

- `../study/Systems-Programming/shlab/c/src/tsh.c`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 공식 starter 없이도 과제 목적을 먼저 파악하고 싶은 학습자
- 어떤 자산을 제거했고 무엇으로 대체했는지 알고 싶은 사람
- 공개 가능한 문제 경계 문서를 설계하고 싶은 사람
- 공개 트리에는 문제 계약만 남기고, 공식 starter 자산은 싣지 않습니다.

## 제외 범위

- `../study/Systems-Programming/shlab/c/tests/run_tests.sh` fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `handler_t`와 `eval`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- `../study/Systems-Programming/shlab/c/tests/run_tests.sh` fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/shlab/c test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/shlab/c test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/shlab/problem
```

- `shlab`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`shlab-c_answer.md`](shlab-c_answer.md)에서 확인한다.
