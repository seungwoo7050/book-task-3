# Data Lab C 구현

## 이 디렉터리가 가르치는 것

이 디렉터리는 연산자 제약을 지키면서 C로 bit-level 문제를 푸는 방법을 보여 줍니다.
공식 `btest` 흐름과 별도로 edge case 테스트를 덧붙여, 왜 이 구현이 맞는지 확인하는 역할도 맡습니다.

## 누구를 위한 문서인가

- C로 `bits.c`를 직접 구현하려는 학습자
- 공식 handout 검증과 자체 테스트를 함께 돌리고 싶은 사람
- 제한 조건 아래에서 코드를 정리하는 예시가 필요한 사람

## 먼저 읽을 곳

1. [`../problem/README.md`](../problem/README.md)
2. [`../README.md`](../README.md)
3. [`tests/test_bits.c`](tests/test_bits.c)

## 디렉터리 구조

```text
c/
  README.md
  src/
    bits.c
  tests/
    test_bits.c
```

## 검증 방법

```bash
cp c/src/bits.c problem/code/bits.c
cd problem
make clean && make
make test
bash script/grade.sh

cd ../c/tests
gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits
```

## 스포일러 경계

- README는 검증 경로와 학습 포인트만 설명합니다.
- 함수별 최종 구현 해설은 `docs/`와 `notion/`에 분리합니다.

## 포트폴리오로 확장하는 힌트

- 공식 검증과 자체 테스트를 함께 둔 이유를 적어 두면 저장소 신뢰도가 올라갑니다.
