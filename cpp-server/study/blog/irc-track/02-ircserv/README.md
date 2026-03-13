# ircserv Source-First Blog

`ircserv`은 roomlab 위에 기능을 조금 더 얹은 버전이라기보다, subset에서 미리 분리해 둔 책임을 다시 한 서버로 모으는 capstone에 가깝다. 여기서 핵심은 코드가 얼마나 길어졌는가가 아니라, 어떤 command가 실제로 dispatcher에 열리고, 그 추가가 channel privilege와 cleanup까지 어떻게 이어지는가다.

이 시리즈는 그 차이를 source-first로 다시 읽는다. 근거는 [`problem/README.md`](../../../irc-track/02-ircserv/problem/README.md), [`cpp/README.md`](../../../irc-track/02-ircserv/cpp/README.md), [`docs/README.md`](../../../irc-track/02-ircserv/docs/README.md), 실제 소스, 그리고 직접 실행한 CLI뿐이다. roomlab와 비슷한 뼈대는 유지하지만, command surface와 state model이 어디서 넓어지는지가 문서의 중심이 된다.

## 검증 명령

```sh
cd /Users/woopinbell/work/book-task-3/cpp-server/study/irc-track/02-ircserv/cpp
make clean && make test
```

최근 확인 결과:

- `python3 tests/test_irc_join.py`
- `ircserv capstone smoke passed.`

## 읽기 순서

- [00-series-map.md](00-series-map.md)
- [evidence-ledger.md](evidence-ledger.md)
- [structure-plan.md](structure-plan.md)
- [10-baseline-capability-and-registration.md](10-baseline-capability-and-registration.md)
- [20-channel-privilege-and-mode-state.md](20-channel-privilege-and-mode-state.md)
- [30-advanced-command-flows-and-verification.md](30-advanced-command-flows-and-verification.md)

## 핵심 근거 파일

- [`cpp/src/Executor.cpp`](../../../irc-track/02-ircserv/cpp/src/Executor.cpp)
- [`cpp/src/Channel.cpp`](../../../irc-track/02-ircserv/cpp/src/Channel.cpp)
- [`cpp/src/execute_join.cpp`](../../../irc-track/02-ircserv/cpp/src/execute_join.cpp)
- [`cpp/src/Server.cpp`](../../../irc-track/02-ircserv/cpp/src/Server.cpp)
- [`cpp/tests/test_irc_join.py`](../../../irc-track/02-ircserv/cpp/tests/test_irc_join.py)

