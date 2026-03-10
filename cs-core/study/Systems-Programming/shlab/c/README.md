# Shell Lab C 구현

## 이 디렉터리가 가르치는 것

이 디렉터리는 tiny shell 계약을 C로 직접 구현합니다.
foreground/background job control과 signal forwarding, `SIGCHLD` reaping을 실제 코드로 다룹니다.

## 누구를 위한 문서인가

- C로 셸을 직접 구현해 보고 싶은 학습자
- 시그널 관련 race를 테스트까지 포함해 보고 싶은 사람
- self-owned 테스트 기반 셸 프로젝트 구조가 필요한 사람

## 먼저 읽을 곳

1. [`../problem/README.md`](../problem/README.md)
2. [`../docs/README.md`](../docs/README.md)
3. `tests/run_tests.sh`

## 디렉터리 구조

```text
c/
  README.md
  include/
    tsh_helper.h
  src/
    tsh.c
  tests/
    run_tests.sh
    traces/
  Makefile
```

## 검증 방법

```bash
cd c
make clean && make test
```

## 스포일러 경계

- README는 구현 범위와 검증 경로만 설명합니다.
- race 세부 분석은 `docs/`와 `notion/`에 분리합니다.

## 포트폴리오로 확장하는 힌트

- 셸 프로젝트는 signal trace를 어떻게 만들었는지를 한 줄로만 적어도 강한 인상을 줍니다.
