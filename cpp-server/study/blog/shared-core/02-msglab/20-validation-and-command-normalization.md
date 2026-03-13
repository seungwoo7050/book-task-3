# msglab 2. validation과 command normalization을 parser 근처에 두기

한 줄을 `Message`로 바꾸는 것만으로는 아직 부족하다. 그다음엔 어떤 토큰을 유효한 입력으로 받아들일지 정해야 한다. `msglab`이 좋은 이유는 이 판단을 executor나 server가 아니라 [`cpp/src/Parser.cpp`](../../../shared-core/02-msglab/cpp/src/Parser.cpp) 근처에서 끝낸다는 점이다.

가장 먼저 눈에 띄는 것은 `toupper()`와 `tolower()`다. command는 대문자로 정규화되고, channel이나 nickname 비교는 소문자로 맞춰진다. 입력은 제멋대로 들어와도 내부 비교는 정규화된 값으로 한다는 계약이 여기서 이미 만들어진다.

그 위에 validator들이 붙는다. `is_channel()`은 `#` 또는 `&`로 시작하는지, 공백과 comma가 없는지, 길이가 맞는지 본다. `is_nickname()`은 첫 글자 규칙과 허용 문자 집합을 확인한다. 여기에 `is_integer()`, `is_facing()`, `is_binary_flag()`까지 추가되면서 parser는 IRC command뿐 아니라 arena command에 필요한 token 규칙도 함께 제공한다.

```cpp
expect(Parser::is_integer(input.params[0]), "INPUT seq should be numeric");
expect(Parser::is_facing(input.params[3]), "INPUT facing should be validated");
expect(Parser::is_binary_flag(input.params[4]), "INPUT fire flag should be binary");
```

이 구조가 중요한 이유는 parser가 이미 두 축을 동시에 바라보고 있기 때문이다. [`tests/test_parser.cpp`](../../../shared-core/02-msglab/cpp/tests/test_parser.cpp)는 IRC 쪽에선 `PASS`, `NICK`, `JOIN`, `MODE`, `KICK`, `INVITE`를 확인하고, game 쪽에선 `INPUT 42 1 0 E 1`, `REJOIN token-7` 같은 명령을 검사한다. 알려진 enum으로 번역되지 않는 command라도, `command` 문자열과 params는 여전히 살아 있어야 다음 레이어가 의미를 붙일 수 있다.

그래서 이 글의 초점은 helper 목록을 나열하는 데 있지 않다. 문자열을 어떻게 정규화하고, 어디까지를 parser가 책임지고, 어떤 규칙을 뒤의 server가 다시 검사하지 않아도 되게 만들었는가가 더 중요하다. `eventlab`이 소켓 표면을 분리했다면, `msglab`은 그 위에 올라갈 입력 표면을 분리해 둔 셈이다.

