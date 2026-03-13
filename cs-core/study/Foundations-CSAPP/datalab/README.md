# Data Lab

`datalab`은 bit-level 제약을 지키면서 정수 표현과 부동소수점 경계를 직접 구현하는 프로젝트다.

## 한눈에 보기

| 문제 | 중요 제약 | 이 레포의 답 | 검증 시작점 | 배우는 개념 | 상태 |
| --- | --- | --- | --- | --- | --- |
| `bits.c`의 13개 함수를 원문 허용 연산자, 상수, max ops 제약 안에서 구현한다. | 정수 퍼즐은 bit-level contract를 유지하고, float 퍼즐은 unsigned bit pattern만 다룬다. 공식 handout verifier는 로컬에서 복원한다. | C 답은 [`c/src/bits.c`](c/src/bits.c), C++ 답은 [`cpp/src/bits.cpp`](cpp/src/bits.cpp)이며, 풀이 근거는 `docs/`, `notion/`으로 분리한다. | [`problem/README.md`](problem/README.md), [`c/README.md`](c/README.md), [`cpp/README.md`](cpp/README.md) | two's complement, mask 구성, 부호 비트 해석, IEEE754 경계 | `verified (local-only asset)` |

실제 소스코드·테스트·검증 엔트리 기준의 blog 시리즈: [`../../blog/Foundations-CSAPP/datalab/00-series-map.md`](../../blog/Foundations-CSAPP/datalab/00-series-map.md)

## 디렉터리 역할

- `problem/`: 원문 과제 계약과 공식 verifier 경계
- `c/`: `bits.c`에 대한 C 답과 edge-case test
- `cpp/`: 같은 계약을 C++로 다시 구현한 답
- `docs/`: integer pattern, float boundary 같은 durable concept note
- `notion/`: 접근 로그, 디버그 근거, 재검증 timeline

## 검증 빠른 시작

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

## 공개 경계

- 공개 문서는 연산 패턴, 경계값 사고법, 검증 흐름을 설명한다.
- 함수별 최종 구현 전체를 README에 붙여 넣지 않고, 코드와 개념 문서를 분리한다.
- 공식 handout은 `problem/official/` 아래 로컬에서만 복원한다.
