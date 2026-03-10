# Data Lab 문제 경계

## 이 디렉터리가 가르치는 것

이 디렉터리는 `datalab`의 공식 문제 계약과 검증 경계를 보존합니다.
핵심은 `code/bits.c`의 13개 함수를 제약된 연산자 집합 안에서 구현하는 것입니다.

## 누구를 위한 문서인가

- 구현에 들어가기 전에 과제 계약을 먼저 확인하고 싶은 학습자
- 공식 self-study handout 복원 경로가 필요한 사람
- 구현 디렉터리와 starter boundary를 분리해서 보고 싶은 사람

## 먼저 읽을 곳

1. [`../README.md`](../README.md)
2. [`code/bits.c`](code/bits.c)
3. [`../c/README.md`](../c/README.md)
4. [`../cpp/README.md`](../cpp/README.md)

## 디렉터리 구조

```text
problem/
  README.md
  code/
    bits.c
    btest.c
    decl.c
    tests.c
  script/
    grade.sh
  Makefile
```

## 검증 방법

```bash
make restore-official
make verify-official
```

`verify-official`은 로컬에 복원한 self-study handout 안에서 `dlc`와 `btest -T 20`을 실행합니다.

## 스포일러 경계

- 이 문서는 문제 계약과 검증 방법만 설명합니다.
- 함수별 완성 코드는 구현 디렉터리와 tests를 통해 확인합니다.
- 공식 handout은 `official/` 아래 로컬에서만 복원합니다.

## 포트폴리오로 확장하는 힌트

- 문제 README에는 전체 퍼즐 목록보다 "어떤 제약이 핵심인가"를 먼저 적는 편이 읽기 쉽습니다.

## 핵심 제약

- 정수 퍼즐은 `int`만 사용하고, 문제별 허용 연산자만 사용할 수 있습니다.
- 상수는 `0x00`부터 `0xFF`까지만 사용할 수 있습니다.
- 정수 퍼즐에서는 `if`, `while`, `for`, `switch`, `?:`, `&&`, `||`를 사용할 수 없습니다.
- 부동소수점 퍼즐은 `unsigned` 비트 표현을 다루며, 조건문과 반복문을 사용할 수 있습니다.
