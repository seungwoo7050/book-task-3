# msglab 1. 한 줄을 어떤 메시지로 볼 것인가

`msglab`에서 가장 먼저 필요한 것은 복잡한 parser가 아니다. 먼저 한 줄 입력을 어떤 모양의 데이터로 들고 있을지 정해야 한다. [`problem/README.md`](../../../shared-core/02-msglab/problem/README.md)가 prefix, command, trailing parameter를 성공 기준에 넣은 이유도 그래서다. 이 lab은 그 최소 모델부터 잡는다.

[`cpp/include/inc/Message.hpp`](../../../shared-core/02-msglab/cpp/include/inc/Message.hpp)는 parser 결과를 `prefix`, `command`, `params`, 그리고 known command enum으로 고정한다. 실제 파싱은 [`cpp/src/Message.cpp`](../../../shared-core/02-msglab/cpp/src/Message.cpp)의 생성자 하나에 모여 있는데, 여기서 optional prefix를 먼저 떼고, command를 대문자로 정규화한 뒤, trailing parameter를 마지막 하나로만 보존한다.

```cpp
if (stream.at(0) == ':')
{
    iss.get();
    if (!std::getline(iss, token, ' ').fail())
        this->prefix = token;
}
```

이후 command가 `PASS`, `NICK`, `JOIN`, `PING`처럼 알려진 값이면 enum으로도 번역된다. 하지만 번역되지 않는 command가 있다고 해서 버려지지는 않는다. `comm`은 `UNK`가 될 수 있어도 `command` 문자열 자체는 그대로 남는다. 이 점이 나중에 arena 쪽 command를 같은 모델로 흡수할 수 있게 해 준다.

여기서 framing까지 붙으면 parser의 앞문이 더 또렷해진다. [`Parser::make_messages()`](../../../shared-core/02-msglab/cpp/src/Parser.cpp)는 문자열 스트림을 참조로 받아, `\n`이 완성된 줄만 잘라 `Message`로 바꾼다. 아직 줄 끝에 도달하지 못한 partial line은 남겨 둔다.

```cpp
std::size_t line_end = stream.find('\n');
while (line_end != std::string::npos)
{
    std::string frame = stream.substr(0, line_end);
    stream.erase(0, line_end + 1);
```

이 선택은 작아 보여도 중요하다. 이제 parser는 `recv()`가 몇 번 불렸는지와 무관하게, 완성된 line만 다루는 계층이 된다. 즉 `msglab`의 첫 글은 단순한 문자열 분해가 아니라, "한 줄 메시지"와 "아직 덜 온 바이트"를 분리하는 첫 경계를 세우는 과정으로 읽는 편이 맞다.

