# Bomb Lab C companion

## 이 디렉터리가 가르치는 것

이 디렉터리는 공식 bomb를 재배포하지 않고도 phase별 개념군을 C 코드와 테스트로 다시 실행하게 만듭니다.
역공학 결과를 직접 검증 가능한 companion 구현으로 바꾸는 예시입니다.

## 누구를 위한 문서인가

- 공식 bomb 없이도 phase 패턴을 코드로 확인하고 싶은 학습자
- 역공학 산출물을 companion program으로 재구성하는 예시가 필요한 사람
- C 테스트 기반으로 phase별 동작을 검증하고 싶은 사람

## 먼저 읽을 곳

1. [`../problem/README.md`](../problem/README.md)
2. [`../docs/README.md`](../docs/README.md)
3. [`tests/test_mini_bomb.c`](tests/test_mini_bomb.c)

## 디렉터리 구조

```text
c/
  README.md
  include/
    mini_bomb.h
  src/
    mini_bomb.c
    main.c
  tests/
    test_mini_bomb.c
  Makefile
```

## 검증 방법

```bash
cd c
make clean && make test

printf 'Assembly reveals intent.\n1 2 4 8 16 32\n1 311\n6 6\n01234.\n4 6 2 3 5 1\n35\n' > /tmp/bomblab_c_answers.txt
./build/mini_bomb /tmp/bomblab_c_answers.txt
rm /tmp/bomblab_c_answers.txt
```

## 스포일러 경계

- companion 구현은 학습용 재구성입니다.
- 공식 bomb 정답이나 외부 course binary 정보를 README에 추가하지 않습니다.

## 포트폴리오로 확장하는 힌트

- "공식 자산을 재배포하지 않고도 학습 결과를 검증 가능하게 만들었다"는 점을 강조하기 좋습니다.
