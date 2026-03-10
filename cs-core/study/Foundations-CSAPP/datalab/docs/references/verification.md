# Data Lab 검증 기록

## 검증을 두 층으로 나눈 이유

`datalab`은 "과제 계약을 만족하는가"와 "내가 설명하고 싶은 경계값까지 확인했는가"를 따로 보는 편이 좋습니다.

- 공식 self-study handout 검증: `dlc`, `btest`
- 저장소 전용 검증: C/C++ edge-case 테스트

## 공식 self-study handout 검증

```bash
cd problem
make restore-official
make verify-official
```

2026-03-10 기준 기록:

- 복원한 공식 handout에서 `dlc`가 통과한다
- `btest -T 20`이 통과한다
- Apple Silicon 호스트의 amd64 에뮬레이션 환경을 고려해 기본 10초 대신 20초 제한을 사용한다

## C edge-case 테스트

```bash
cd c/tests
gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c
./test_bits
```

기록:

- `55 / 55 edge-case tests passed`

## C++ edge-case 테스트

```bash
cd cpp/tests
g++ -std=c++20 -O1 -Wall -Werror -o test_bits_cpp test_bits.cpp ../src/bits.cpp
./test_bits_cpp
```

기록:

- `55 / 55 C++ edge-case tests passed`

## 이 결과를 어떻게 읽을까

- 공식 handout 검증은 과제 계약을 충족한다는 증거다
- edge-case 테스트는 설명 가능한 경계값까지 확인했다는 증거다

둘 다 남겨 두는 편이 학습 저장소로서는 더 좋습니다.
