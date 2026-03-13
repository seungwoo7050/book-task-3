# msglab 3. transcript 테스트가 보호하는 범위

`msglab`은 실행 서버가 없는 대신 [`cpp/tests/test_parser.cpp`](../../../shared-core/02-msglab/cpp/tests/test_parser.cpp)가 곧 공개 표면이다. 이 테스트가 하는 일은 단순한 유닛 테스트 몇 개를 넘어서, parser가 어떤 종류의 입력을 안정적으로 받아들일 수 있는지 보여 주는 proof에 가깝다.

테스트는 크게 네 장면으로 나뉜다. prefix와 trailing parameter가 정확히 분리되는지 확인하고, nickname/channel validator가 제대로 작동하는지 본다. 이어서 `make_messages()`가 incomplete line을 남기는지 확인하고, 마지막으로 IRC transcript와 arena command transcript를 한 파일 안에서 함께 검증한다.

그중에서도 partial line 테스트는 이 lab의 경계를 가장 잘 보여 준다.

```cpp
std::string stream = "PING one\r\nJOIN #cpp\r\nPART #cpp";
Parser::make_messages(stream, batch);
expect(stream == "PART #cpp", "partial line was not preserved");
```

이 장면 하나로 parser와 socket I/O의 역할이 분리된다. 네트워크가 메시지를 두 번에 나눠 줘도 parser는 완성된 frame만 소비하고, 남은 조각은 그대로 보존한다. 뒤의 server 문서들이 `recvbuf`를 다루면서도 parser 자체를 단순하게 유지할 수 있는 이유가 바로 여기 있다.

직접 실행한 CLI도 이 표면을 간결하게 확인해 준다.

```sh
cd /Users/woopinbell/work/book-task-3/cpp-server/study/shared-core/02-msglab/cpp
make clean && make test
```

```text
./msglab_tests
msglab parser tests passed.
```

이 결과가 의미하는 바는 분명하다. parser는 이미 IRC와 arena 양쪽 입력을 받을 만큼 넓고, incomplete frame도 보존하며, token validation도 갖추고 있다. 반대로 아직 일부러 맡지 않은 일도 분명하다. socket read/write는 전혀 다루지 않고, PASS 뒤에만 NICK을 허용한다든지 하는 상태 전이도 알지 못한다. 그 빈자리는 다음 문서들, 특히 [`../../irc-track/01-roomlab/README.md`](../../irc-track/01-roomlab/README.md)과 `game-track`의 서버 문서들이 채운다.

