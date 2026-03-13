# msglab structure plan

`msglab`은 구현량보다 경계 설명이 중요한 문서다. 독자는 "parser가 어떤 helper를 갖고 있는가"보다 "어디까지를 parser에서 끝내고, 어디서부터 server나 executor로 넘기는가"를 알고 싶어 한다. 그래서 글도 그 질문에 맞춰 설계한다.

## 10-message-model-and-framing.md

첫 글은 `Message` 모델과 `Parser::make_messages()`가 만나는 지점을 중심에 둔다. optional prefix, command normalization, trailing parameter 보존, partial line 보존이 하나의 입력 표면으로 묶이는 장면을 보여 주는 것이 목적이다. 코드는 `Message.hpp`, `Message::Message()`, `Parser::make_messages()`를 중심 앵커로 잡는다.

## 20-validation-and-command-normalization.md

둘째 글은 validation helper를 parser 근처에 두는 이유를 설명한다. `toupper()`, `tolower()`, `is_channel()`, `is_nickname()`, `is_integer()`, `is_facing()`, `is_binary_flag()`가 뒤의 IRC와 game track 모두를 받쳐 준다는 점을 자연스럽게 드러내야 한다. 여기서는 코드 목록보다 "왜 이 책임이 여기 있어야 하는가"가 더 중요하다.

## 30-transcript-coverage-and-boundaries.md

마지막 글은 `tests/test_parser.cpp`를 proof 문서로 읽게 만든다. `make clean && make test`와 `msglab parser tests passed.`를 닫는 신호로 두고, parser가 이미 넓은 입력 표면을 보호하지만 상태 전이와 socket I/O는 아직 일부러 맡지 않았다는 점까지 함께 정리한다.

