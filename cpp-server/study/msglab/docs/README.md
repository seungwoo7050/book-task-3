# msglab 개념 노트

## 먼저 잡아야 할 질문

- trailing parameter는 왜 마지막 하나만 공백을 보존하는가
- partial line을 버리지 않으면 어떤 종류의 버그를 피할 수 있는가
- validation을 parser 근처에 두면 executor는 얼마나 단순해지는가

## 코드 읽기 포인트

- [../cpp/src/Message.cpp](../cpp/src/Message.cpp): 메시지 모델 생성
- [../cpp/src/Parser.cpp](../cpp/src/Parser.cpp): frame split과 parse 흐름
- [../cpp/tests/test_parser.cpp](../cpp/tests/test_parser.cpp): 고정 fixture 기반 검증

## 흔한 오해

- parser는 문자열만 자르면 끝나는 계층이 아니다.
- validator를 나중으로 미루면 에러 메시지가 좋아지는 것이 아니라, 책임 경계가 흐려질 때가 많다.
- parser lab은 작아 보여도 이후 서버 lab의 디버깅 시간을 크게 줄여 준다.

## 다음 단계로 이어지는 지점

이제 parser 책임을 분리했으니, 실제 연결과 상태 전이를 붙여 보고 싶다면 [../roomlab/README.md](../roomlab/README.md)로 넘어가면 된다.
