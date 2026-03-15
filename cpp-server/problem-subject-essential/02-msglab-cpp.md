# 02-msglab-cpp 문제지

## 왜 중요한가

줄 단위 메시지를 안전하게 frame으로 자르고, parser가 구조화해야 할 정보와 validation이 맡아야 할 책임을 분리해야 한다.

## 목표

시작 위치의 구현을 완성해 \r\n 또는 \n 경계를 기준으로 메시지를 분리한다, optional prefix를 인식한다, command token을 대문자로 정규화한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/shared-core/02-msglab/cpp/src/Message.cpp`
- `../study/shared-core/02-msglab/cpp/src/Parser.cpp`
- `../study/shared-core/02-msglab/cpp/include/inc/macros.hpp`
- `../study/shared-core/02-msglab/cpp/include/inc/Message.hpp`
- `../study/shared-core/02-msglab/cpp/tests/test_parser.cpp`
- `../study/shared-core/02-msglab/cpp/Makefile`

## starter code / 입력 계약

- `../study/shared-core/02-msglab/cpp/src/Message.cpp`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- \r\n 또는 \n 경계를 기준으로 메시지를 분리한다.
- optional prefix를 인식한다.
- command token을 대문자로 정규화한다.
- trailing parameter를 :<text> 규칙 그대로 보존한다.
- nickname과 channel 이름의 유효성을 검사한다.

## 제외 범위

- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 검증 기준은 `main`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/shared-core/02-msglab/cpp test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/cpp-server/study/shared-core/02-msglab/cpp test
```

- `02-msglab`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`02-msglab-cpp_answer.md`](02-msglab-cpp_answer.md)에서 확인한다.
