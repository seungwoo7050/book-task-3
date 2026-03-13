# 20 Validation And Command Normalization

## Day 1
### Session 2

- 목표: `Parser`가 무엇을 엄격하게 검증하고 무엇을 generic token으로 남기는지 구분한다.
- 진행: `toupper`, `is_channel`, `is_nickname`, `is_integer`, `is_facing`, `is_binary_flag`를 테스트 케이스와 함께 읽었다.
- 이슈: 처음엔 arena command를 위해 별도 parser가 추가된 줄 알았지만, 실제로는 기존 `Message` 구조를 그대로 두고 validator helper만 넓힌 구조였다.
- 판단: `msglab`의 두 번째 답은 "IRC용 parser와 게임용 parser를 따로 만들지 않는다"는 쪽에 가깝다.

CLI:

```bash
$ cd study/shared-core/02-msglab/cpp
$ rg -n "toupper|is_channel|is_nickname|is_integer|is_facing|is_binary_flag" src/Parser.cpp tests/test_parser.cpp
$ sed -n '1,120p' src/Parser.cpp
$ sed -n '70,140p' tests/test_parser.cpp
```

이 시점의 핵심 코드는 아래였다.

```cpp
bool Parser::is_integer(const std::string &token)
{
    if (token.empty())
        return false;

    std::size_t start = 0;
    if (token[0] == '-' || token[0] == '+')
    {
        if (token.size() == 1)
            return false;
        start = 1;
    }
```

나중에 보니 이 helper는 arena `INPUT`의 `seq`, `dx`, `dy`, `fire`를 위해 따로 새 타입 시스템을 들인 것이 아니라, 텍스트 protocol에서 숫자 token을 걸러 내는 최소 계약만 추가한 형태였다.

같은 맥락에서 arena command는 전용 enum으로 승격되지 않는다.

```cpp
Message hello("HELLO alpha");
expect(hello.comm == Message::UNK, "arena HELLO should stay generic");
expect(hello.command == "HELLO", "HELLO command should be preserved");
```

이 선택 덕분에 parser는 command set을 폐쇄적으로 정의하지 않고, executor나 server가 후단에서 책임을 나눌 여지를 남긴다.

