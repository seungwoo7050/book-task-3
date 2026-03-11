# msglab 지식 색인

## 핵심 개념

- framing: 연속된 문자열 스트림에서 메시지 경계를 찾는 일
- trailing parameter: 마지막 하나만 공백을 그대로 보존하는 IRC 규칙
- validation: 실행 전 단계에서 입력이 최소 규칙을 만족하는지 확인하는 일

## 먼저 볼 파일

- [../cpp/include/inc/Message.hpp](../cpp/include/inc/Message.hpp)
- [../cpp/src/Parser.cpp](../cpp/src/Parser.cpp)
- [../cpp/tests/test_parser.cpp](../cpp/tests/test_parser.cpp)

## 다음 프로젝트와의 연결

- `roomlab`: parser 결과를 실제 connection state와 합친다.
- `ircserv`: parser 경계가 capstone에서 어떻게 유지되는지 본다.

## 백업 자료

- 예전 버전 노트와 타임라인은 [../notion-archive/](../notion-archive/)에 있다.
