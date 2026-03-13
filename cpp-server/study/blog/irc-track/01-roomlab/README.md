# roomlab Source-First Blog

`roomlab`은 이 저장소에서 처음으로 "실제 상태 전이"가 전면에 올라오는 서버다. 여기서 풀고 싶은 문제는 완전한 IRCd를 만드는 것이 아니라, registration과 room lifecycle을 실제 TCP 서버 위에서 어디까지 core subset으로 보여 줄 수 있는가다. 뒤의 capstone과 비교해도 흐려지지 않도록 일부러 범위를 좁혀 둔 첫 완성형이라고 보면 된다.

이 시리즈는 그 흐름을 소스와 테스트만으로 다시 따라간다. 근거는 [`problem/README.md`](../../../irc-track/01-roomlab/problem/README.md), [`cpp/README.md`](../../../irc-track/01-roomlab/cpp/README.md), [`docs/README.md`](../../../irc-track/01-roomlab/docs/README.md), 실제 소스, 그리고 직접 실행한 CLI뿐이다. chronology는 정확한 시각 대신 `Phase`로 복원했지만, `Connection`, `Server`, `Executor`, `Channel`이 어느 순서로 무거워지는지는 코드 의존 관계 그대로 드러난다.

## 검증 명령

```sh
cd /Users/woopinbell/work/book-task-3/cpp-server/study/irc-track/01-roomlab/cpp
make clean && make test
```

최근 확인 결과:

- `python3 tests/test_roomlab.py`
- `roomlab smoke passed.`

## 읽기 순서

- [00-series-map.md](00-series-map.md)
- [evidence-ledger.md](evidence-ledger.md)
- [structure-plan.md](structure-plan.md)
- [10-registration-and-server-surface.md](10-registration-and-server-surface.md)
- [20-channel-lifecycle-and-cleanup.md](20-channel-lifecycle-and-cleanup.md)
- [30-delivery-cleanup-and-verification.md](30-delivery-cleanup-and-verification.md)

## 핵심 근거 파일

- [`cpp/src/Connection.cpp`](../../../irc-track/01-roomlab/cpp/src/Connection.cpp)
- [`cpp/src/Server.cpp`](../../../irc-track/01-roomlab/cpp/src/Server.cpp)
- [`cpp/src/Executor.cpp`](../../../irc-track/01-roomlab/cpp/src/Executor.cpp)
- [`cpp/src/execute_join.cpp`](../../../irc-track/01-roomlab/cpp/src/execute_join.cpp)
- [`cpp/tests/test_roomlab.py`](../../../irc-track/01-roomlab/cpp/tests/test_roomlab.py)

