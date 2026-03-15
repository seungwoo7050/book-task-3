# datalab 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 정수 퍼즐은 int만 사용하고, 문제별 허용 연산자만 사용할 수 있습니다, 상수는 0x00부터 0xFF까지만 사용할 수 있습니다, 정수 퍼즐에서는 if, while, for, switch, ?:, &&, ||를 사용할 수 없습니다를 한 흐름으로 설명하고 검증한다. 핵심은 `bitXor`와 `tmin`, `isTmax` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 정수 퍼즐은 int만 사용하고, 문제별 허용 연산자만 사용할 수 있습니다.
- 상수는 0x00부터 0xFF까지만 사용할 수 있습니다.
- 정수 퍼즐에서는 if, while, for, switch, ?:, &&, ||를 사용할 수 없습니다.
- 첫 진입점은 `../study/Foundations-CSAPP/datalab/c/src/bits.c`이고, 여기서 `bitXor`와 `tmin` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Foundations-CSAPP/datalab/c/src/bits.c`: `bitXor`, `tmin`, `isTmax`, `allOddBits`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/datalab/cpp/src/bits.cpp`: `bitXor`, `tmin`, `isTmax`, `allOddBits`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/datalab/problem/code/bits.c`: `bitXor`, `tmin`, `isTmax`, `allOddBits`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/datalab/problem/code/btest.c`: `bitXor`, `tmin`, `isTmax`, `allOddBits`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/datalab/problem/code/decl.c`: starter skeleton으로 입력 계약과 확장 포인트를 보여 준다.
- `../study/Foundations-CSAPP/datalab/c/tests/test_bits.c`: `bitXor`, `tmin`, `isTmax`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Foundations-CSAPP/datalab/cpp/tests/test_bits.cpp`: `bitXor`, `tmin`, `isTmax`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Foundations-CSAPP/datalab/problem/script/grade.sh`: 검증 절차나 보조 자동화를 담아 결과를 재현하는 스크립트다.

## 정답을 재구성하는 절차

1. `../study/Foundations-CSAPP/datalab/problem/code/bits.c`와 `../study/Foundations-CSAPP/datalab/c/src/bits.c`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `bitXor` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/datalab/c/tests && ./test_bits`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/datalab/c/tests && ./test_bits
```

```bash
cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/datalab/cpp/tests && ./test_bits_cpp
```

- `../study/Foundations-CSAPP/datalab/problem/code/bits.c` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `bitXor`와 `tmin`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/datalab/c/tests && ./test_bits`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Foundations-CSAPP/datalab/c/src/bits.c`
- `../study/Foundations-CSAPP/datalab/cpp/src/bits.cpp`
- `../study/Foundations-CSAPP/datalab/problem/code/bits.c`
- `../study/Foundations-CSAPP/datalab/problem/code/btest.c`
- `../study/Foundations-CSAPP/datalab/problem/code/decl.c`
- `../study/Foundations-CSAPP/datalab/c/tests/test_bits.c`
- `../study/Foundations-CSAPP/datalab/cpp/tests/test_bits.cpp`
- `../study/Foundations-CSAPP/datalab/problem/script/grade.sh`
- `../study/Foundations-CSAPP/datalab/problem/Makefile`
- `../study/Foundations-CSAPP/datalab/problem/official/datalab-handout/Makefile`
