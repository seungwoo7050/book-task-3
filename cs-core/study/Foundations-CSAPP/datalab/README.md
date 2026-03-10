# Data Lab

## 이 프로젝트가 가르치는 것

`datalab`은 비트 연산 제약 아래에서 정수 표현과 부동소수점 경계를 직접 다루게 만드는 프로젝트입니다.
연산자 제한, 상수 제한, 함수별 최대 연산 수를 지키면서도 정답과 설명을 동시에 설계하는 감각을 익히게 합니다.

## 누구를 위한 문서인가

- CS:APP 프로젝트를 처음 시작하는 학습자
- 비트 트릭을 "암기"가 아니라 "이유가 있는 규칙"으로 이해하고 싶은 사람
- 제한 조건이 강한 과제를 공개 저장소 형태로 정리하고 싶은 사람

## 먼저 읽을 곳

1. [`problem/README.md`](problem/README.md)
2. [`c/README.md`](c/README.md)
3. [`cpp/README.md`](cpp/README.md)
4. [`docs/README.md`](docs/README.md)
5. [`notion/README.md`](notion/README.md)

## 디렉터리 구조

```text
datalab/
  README.md
  problem/
  c/
  cpp/
  docs/
  notion/
  notion-archive/
```

## 검증 방법

2026-03-10 문서 정비 기준으로 유지하는 검증 경로는 다음과 같습니다.

공식 self-study handout 검증:

```bash
cd problem
make restore-official
make verify-official
```

C 구현 검증:

```bash
cp c/src/bits.c problem/code/bits.c
cd problem
make clean && make
make test
bash script/grade.sh
cd ../c/tests
gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits
```

C++ 구현 검증:

```bash
cd cpp/tests
g++ -std=c++20 -O1 -Wall -Werror -o test_bits_cpp test_bits.cpp ../src/bits.cpp
./test_bits_cpp
```

## 스포일러 경계

- 공개 문서는 연산 패턴, 경계값 사고법, 검증 흐름을 설명합니다.
- 함수별 최종 구현을 README에 그대로 붙여 넣지는 않습니다.
- 공식 handout은 `problem/official/` 아래 로컬에서만 복원합니다.

## 포트폴리오로 확장하는 힌트

- 연산자 제한이 있는 문제를 어떻게 분해했는지 짧게 요약하면 문제 해결력 전달이 좋습니다.
- 개인 저장소에서는 "가장 설명하기 어려웠던 함수 1개"를 골라 테스트 전략과 함께 정리하면 차별화가 됩니다.
