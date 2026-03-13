# msglab evidence ledger

이 ledger는 parser lab의 구현 흐름을 `Phase 1`부터 `Phase 4`까지 다시 세운 것이다. 처음에는 raw line을 `Message` 모델로 바꾸고, 이어서 validation helper를 더하고, 그다음 incomplete frame을 남기는 framing 책임을 굳히고, 마지막으로 transcript 테스트로 공개 표면을 닫는 흐름으로 읽으면 자연스럽다.

## Phase 1

가장 먼저 필요한 것은 방대한 parser가 아니라, 한 줄을 어떤 필드로 나눠 들고 있을지 정하는 일이다. 이 phase에서 `Message` 모델이 그 최소 형태를 만든다.

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: raw line을 구조화된 `Message` 객체로 바꾼다.
- 변경 단위: `cpp/include/inc/Message.hpp`, `cpp/src/Message.cpp`
- 처음 가설: prefix, command, params를 한 번에 파싱하는 작은 모델이 있어야 이후 validator와 executor가 얇아진다.
- 실제 조치: `Message::Message()`가 optional prefix, command uppercasing, known command translation, trailing parameter 보존을 담당한다.
- CLI: `make clean && make test`
- 검증 신호: `test_prefix_and_trailing()`가 prefix와 trailing text를 직접 확인한다.
- 핵심 코드 앵커: `Message::Message()`
- 새로 배운 것: trailing parameter는 마지막 하나만 공백을 보존한다는 IRC 규칙이 모델 단계에서 이미 드러난다.
- 다음: message model 위에 normalization과 validation helper를 붙인다.

## Phase 2

모델만으로는 아직 충분하지 않다. 다음 단계에서 parser는 어떤 토큰을 정상으로 볼지, 그리고 그 판단을 어디서 끝낼지 정한다.

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: parser가 직접 책임질 token validation을 분리한다.
- 변경 단위: `cpp/include/inc/Parser.hpp`, `cpp/src/Parser.cpp`
- 처음 가설: nickname/channel 규칙과 arena input helper를 executor나 server에 두면 나중에 같은 버그를 여러 번 고친다.
- 실제 조치: `tolower()`, `toupper()`, `is_channel()`, `is_nickname()`, `is_integer()`, `is_facing()`, `is_binary_flag()`를 분리한다.
- CLI: `make clean && make test`
- 검증 신호: `test_validators()`와 `test_arena_commands()`가 유효/무효 입력을 함께 확인한다.
- 핵심 코드 앵커: `Parser::is_channel()`, `Parser::is_nickname()`, `Parser::is_integer()`
- 새로 배운 것: 같은 parser surface가 IRC token과 arena input token을 동시에 받으려면 command semantic이 아니라 token contract에 집중해야 한다.
- 다음: framing과 partial line 보존을 다룬다.

## Phase 3

이 phase부터 parser는 단순한 token helper가 아니라, 스트림과 완성된 메시지 사이의 경계 역할도 맡게 된다. incomplete frame을 남기는 선택이 여기서 중요해진다.

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: 스트림에서 완성된 메시지만 batch로 꺼내고 덜 온 줄은 남긴다.
- 변경 단위: `cpp/src/Parser.cpp`
- 처음 가설: 네트워크 레이어가 여러 번 `recv()`하더라도 parser는 경계가 완성된 line만 다뤄야 한다.
- 실제 조치: `Parser::make_messages()`가 `\n` 경계만 소비하고, 마지막 partial line은 원본 `stream`에 남긴다.
- CLI: `make clean && make test`
- 검증 신호: `test_make_messages_keeps_partial_line()`에서 `PART #cpp`가 남아 있는지 직접 본다.
- 핵심 코드 앵커: `Parser::make_messages()`
- 새로 배운 것: framing은 parser의 앞문이지 executor의 일이 아니다.
- 다음: transcript 테스트로 공개 표면을 고정한다.

## Phase 4

마지막 phase는 parser가 실제로 얼마나 넓은 표면을 커버하는지 확인하는 단계다. IRC만 볼 것이냐, 뒤의 arena 명령까지 미리 볼 것이냐가 여기서 갈린다.

- 순서: 4
- 시간 표지: Phase 4
- 당시 목표: parser가 뒤쪽 lab 두 축을 모두 받쳐 줄 만큼 넓은 transcript 표면을 확인한다.
- 변경 단위: `cpp/tests/test_parser.cpp`
- 처음 가설: IRC 명령만 검증하면 뒤에서 game server 명령이 parser 표면을 다시 흔들 수 있다.
- 실제 조치: PASS/NICK/USER/JOIN/PRIVMSG/TOPIC/MODE/KICK/INVITE와 HELLO/INPUT/REJOIN을 한 테스트 파일에서 모두 확인한다.
- CLI: `make clean && make test`
- 검증 신호: `msglab parser tests passed.`
- 핵심 코드 앵커: `test_golden_transcripts()`, `test_arena_commands()`
- 새로 배운 것: 알려진 command enum으로 번역하지 않는 명령도 `command` 문자열 자체는 보존해야 한다.
- 다음: parser 결과를 실제 TCP 상태 전이와 붙이는 [`../../irc-track/01-roomlab/README.md`](../../irc-track/01-roomlab/README.md)로 넘어간다.

