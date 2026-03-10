# Bomb Lab 문제 경계

## 이 디렉터리가 가르치는 것

이 디렉터리는 Bomb Lab의 공식 과제 계약과 공개 가능한 분석 경계를 보존합니다.
핵심은 주어진 x86-64 bomb를 무작정 brute force하지 않고 단계적으로 해석하는 것입니다.

## 누구를 위한 문서인가

- 공식 self-study bomb를 로컬에서 복원해 보고 싶은 학습자
- 어떤 파일은 공개하고 어떤 자산은 제외해야 하는지 알고 싶은 사람
- companion 구현과 공식 문제 경계를 분리해서 관리하고 싶은 사람

## 먼저 읽을 곳

1. [`../README.md`](../README.md)
2. [`../docs/README.md`](../docs/README.md)
3. [`script/run_bomb.sh`](script/run_bomb.sh)

## 디렉터리 구조

```text
problem/
  README.md
  Makefile
  code/
    bomb.c
  data/
    solutions.txt
  script/
    run_bomb.sh
```

## 검증 방법

```bash
cd problem
make restore-official
make verify-official
make status
make disas
make strings
make symbols
bash script/run_bomb.sh --gdb
```

## 스포일러 경계

- 공개 문서는 워크플로와 분석 도구 사용법을 설명합니다.
- 공식 bomb 바이너리와 course-instance 전용 답안은 공개하지 않습니다.
- 로컬에 복원된 bomb는 `problem/official/` 아래에서만 사용합니다.

## 포트폴리오로 확장하는 힌트

- "어떤 도구로 어떤 가설을 세웠는가"를 단계별로 적으면 역공학 프로젝트 설명력이 좋아집니다.
