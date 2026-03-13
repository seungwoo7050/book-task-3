# 10 Message Model And Framing

## Day 1
### Session 1

- 목표: `msglab`이 단순 validator 묶음이 아니라, line framing과 message model을 먼저 고정하는 lab인지 확인한다.
- 진행: `README`, `problem/README.md`, `Message.hpp`, `Parser.hpp`, `Parser::make_messages`를 함께 읽었다.
- 이슈: 처음엔 command enum이 더 중요해 보였지만, 실제로 뒤쪽 lab을 단순하게 만드는 출발점은 partial line을 버리지 않는 framing이었다.
- 판단: 이 lab의 첫 번째 답은 "무슨 command를 지원할까"가 아니라 "언제 message 하나가 끝났다고 볼까"였다.

CLI:

```bash
$ cd study/shared-core/02-msglab
$ sed -n '1,160p' README.md
$ sed -n '1,160p' problem/README.md
$ sed -n '1,200p' cpp/include/inc/Message.hpp
$ sed -n '1,200p' cpp/include/inc/Parser.hpp
$ sed -n '60,140p' cpp/src/Parser.cpp
```

이 시점의 핵심 코드는 아래였다.

```cpp
while (line_end != std::string::npos)
{
    std::string frame = stream.substr(0, line_end);
    stream.erase(0, line_end + 1);
    if (!frame.empty() && frame[frame.size() - 1] == '\r')
        frame.erase(frame.size() - 1);
    if (!frame.empty() && !isspace(frame))
        batch.push_back(Message(frame));
    line_end = stream.find('\n');
}
```

처음엔 parser라면 토큰 분해가 중심이라고 생각했는데, 실제로는 `stream`에서 완성된 line만 떼고 남은 조각은 그대로 보존하는 이 루프가 뒤쪽 socket server 전체의 입력 경계를 대신 고정한다.

이 선택은 테스트에서 더 직접적으로 확인된다.

```cpp
std::string stream = "PING one\r\nJOIN #cpp\r\nPART #cpp";
Parser::make_messages(stream, batch);
expect(stream == "PART #cpp", "partial line was not preserved");
```

처음엔 마지막 `PART #cpp`도 그냥 버려도 된다고 생각했는데, 이 assertion 덕분에 parser가 "완성된 frame만 소비한다"는 계약이 명시적으로 남는다.

다음 질문:

- command token은 어디서 대문자로 정규화하는가
- nickname, channel, arena input 제약은 어느 helper에서 막는가
