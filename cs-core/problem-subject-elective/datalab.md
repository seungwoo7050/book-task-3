# datalab 문제지

## 왜 중요한가

이 디렉터리는 datalab의 공식 문제 계약과 검증 경계를 보존합니다. 핵심은 code/bits.c의 13개 함수를 제약된 연산자 집합 안에서 구현하는 것입니다.

## 목표

시작 위치의 구현을 완성해 정수 퍼즐은 int만 사용하고, 문제별 허용 연산자만 사용할 수 있습니다, 상수는 0x00부터 0xFF까지만 사용할 수 있습니다, 정수 퍼즐에서는 if, while, for, switch, ?:, &&, ||를 사용할 수 없습니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Foundations-CSAPP/datalab/problem/code/bits.c`
- `../study/Foundations-CSAPP/datalab/problem/code/btest.c`
- `../study/Foundations-CSAPP/datalab/c/src/bits.c`
- `../study/Foundations-CSAPP/datalab/cpp/src/bits.cpp`
- `../study/Foundations-CSAPP/datalab/c/tests/test_bits.c`
- `../study/Foundations-CSAPP/datalab/cpp/tests/test_bits.cpp`
- `../study/Foundations-CSAPP/datalab/problem/script/grade.sh`
- `../study/Foundations-CSAPP/datalab/problem/Makefile`

## starter code / 입력 계약

- ../study/Foundations-CSAPP/datalab/problem/code/bits.c에서 starter 코드와 입력 경계를 잡는다.
- ../study/Foundations-CSAPP/datalab/problem/code/btest.c에서 starter 코드와 입력 경계를 잡는다.
- ../study/Foundations-CSAPP/datalab/problem/code/decl.c에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- 정수 퍼즐은 int만 사용하고, 문제별 허용 연산자만 사용할 수 있습니다.
- 상수는 0x00부터 0xFF까지만 사용할 수 있습니다.
- 정수 퍼즐에서는 if, while, for, switch, ?:, &&, ||를 사용할 수 없습니다.
- 부동소수점 퍼즐은 unsigned 비트 표현을 다루며, 조건문과 반복문을 사용할 수 있습니다.

## 제외 범위

- `../study/Foundations-CSAPP/datalab/problem/code/bits.c` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/Foundations-CSAPP/datalab/problem/script/grade.sh` fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- `../study/Foundations-CSAPP/datalab/problem/code/bits.c`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `bitXor`와 `tmin`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `bitXor`와 `tmin`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/Foundations-CSAPP/datalab/problem/script/grade.sh` fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/datalab/c/tests && ./test_bits
```

```bash
cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/datalab/cpp/tests && ./test_bits_cpp
```

- 검증 명령을 실행하기 전에 필요한 toolchain이 현재 셸에 준비돼 있는지 먼저 확인한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`datalab_answer.md`](datalab_answer.md)에서 확인한다.
