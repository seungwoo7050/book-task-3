# msglab 문제 재구성

이 문서는 현재 저장소의 구현, 테스트, 보존된 기록을 바탕으로 다시 정리한 학습용 문제 설명이다. 원본 과제지 대신, 지금 레포 안에서 검증 가능한 parser 범위만 문제로 고정한다.

## 학습 목표

- 줄 단위 메시지를 안전하게 분리한다.
- parser가 어떤 정보를 구조화하고 어떤 검증을 맡는지 정한다.
- 작은 텍스트 fixture로 parser 동작을 빠르게 검증한다.

## 구현해야 할 것

- `\r\n` 또는 `\n` 경계를 찾아 메시지 frame 분리하기
- optional prefix 인식하기
- command token을 대문자로 정규화하기
- trailing parameter를 `:<text>` 규칙 그대로 보존하기
- nickname과 channel 이름의 유효성 검사하기

## 산출물

- `Message` 데이터 모델
- `Parser` 유틸리티
- transcript 기반 unit test

## 범위에서 제외하는 것

- socket read/write
- IRC command 실행기
- room state와 connection lifetime

## 현재 저장소에서 확인할 수 있는 근거

- [../cpp/include/inc/Message.hpp](../cpp/include/inc/Message.hpp): parser 결과 모델
- [../cpp/src/Parser.cpp](../cpp/src/Parser.cpp): line split과 parse 구현
- [../cpp/tests/test_parser.cpp](../cpp/tests/test_parser.cpp): 현재 검증 fixture
- [../notion-archive/00-problem-framing.md](../notion-archive/00-problem-framing.md): 이전 문제 정의 메모 백업
