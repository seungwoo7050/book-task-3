# 30 Transcript Coverage And Boundaries

## 2026-03-11
### Session 1

- 목표: 현재 `msglab` 검증이 어떤 transcript를 고정하는지 확인한다.
- 진행: `Makefile`, `cpp/README.md`, `tests/test_parser.cpp`를 함께 읽었다.
- 판단: 이 lab의 검증은 parser 내부 함수를 촘촘히 unit-test하기보다, representative line 몇 개로 prefix, trailing parameter, partial frame, IRC command table, arena command token preservation을 묶는 방식에 가깝다.
- 검증: README 표면은 `verified`, 테스트 최종 신호는 `msglab parser tests passed.`다.
- 다음: 이 결과를 실제 connection state와 합치는 쪽은 `roomlab`이 맡는다.

CLI:

```bash
$ cd study/shared-core/02-msglab/cpp
$ sed -n '1,200p' Makefile
$ sed -n '1,220p' tests/test_parser.cpp
$ make clean && make test
```

출력:

```text
msglab parser tests passed.
```

이 시점의 핵심 코드는 테스트 케이스 배열이었다.

```cpp
const Case cases[] = {
    {"PASS hunter2", Message::PASS, 1},
    {"NICK alice", Message::NICK, 1},
    {"USER alice 0 * :Alice", Message::USER, 4},
    {"JOIN #cpp", Message::JOIN, 1},
    {"PRIVMSG #cpp :hello", Message::PRIVMSG, 2},
};
```

처음엔 이 정도면 IRC만 위한 golden transcript라고 생각했는데, 뒤쪽에 `HELLO`, `INPUT`, `REJOIN` 케이스가 더 붙어 있는 걸 보고 나서야 이 lab의 범위가 특정 도메인 parser가 아니라 "텍스트 command boundary 전체"라는 점이 선명해졌다.

현재 경계:

- 포함: line framing, prefix extraction, command normalization, token validation
- 제외: socket read/write, registration state, channel mutation, room simulation

